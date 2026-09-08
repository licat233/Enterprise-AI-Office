#!/usr/bin/env python3
"""Local, explicit media-to-Markdown transcription for Enterprise AI Office.

The command intentionally stops at a reviewable local transcript. It does not
write to WeKnora, Open WebUI, Hermes, or any other enterprise system.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional


VIDEO_EXTENSIONS = {
    ".3gp", ".avi", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg",
    ".webm", ".wmv",
}

LANGUAGE_ALIASES = {
    "en": "en", "english": "en", "zh": "zh", "zh-cn": "zh",
    "zh-hans": "zh", "chinese": "zh", "mandarin": "zh",
    "yue": "yue", "cantonese": "yue",
}


class TranscriptionError(RuntimeError):
    """A safe, user-facing transcription failure without subprocess details."""


@dataclass
class Segment:
    start: float
    end: float
    text: str


@dataclass
class EngineResult:
    engine: str
    engine_version: str
    model: str
    language: str
    segments: list[Segment]


def _safe_model_label(value: str, fallback: str) -> str:
    """Keep model metadata useful without ever recording a private path."""

    value = str(value or "").strip()
    if not value:
        return fallback
    if "/" in value or "\\" in value:
        value = Path(value).name
    return re.sub(r"[^A-Za-z0-9._@:-]+", "-", value) or fallback


def _yaml_runtime_root(config_path: Path) -> Optional[str]:
    """Read only deployment.runtime_root without requiring a YAML dependency."""

    try:
        lines = config_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise TranscriptionError("company configuration cannot be read") from exc

    in_deployment = False
    for line in lines:
        stripped = line.strip()
        if stripped == "deployment:" and not line[:1].isspace():
            in_deployment = True
            continue
        if in_deployment and line and not line[:1].isspace():
            in_deployment = False
        if not in_deployment:
            continue
        match = re.match(r"^\s+runtime_root:\s*(.*?)\s*(?:#.*)?$", line)
        if match:
            value = match.group(1).strip().strip("\"'")
            return value or None
    return None


def resolve_runtime_root(explicit: Optional[str], config_path: Optional[str]) -> Path:
    """Resolve the runtime root from CLI, environment, or active config."""

    value = explicit or os.environ.get("EAIO_RUNTIME_ROOT")
    if not value and config_path:
        value = _yaml_runtime_root(Path(config_path).expanduser())
    if not value:
        raise TranscriptionError(
            "runtime root is required; set EAIO_RUNTIME_ROOT or EAIO_COMPANY_CONFIG"
        )
    return Path(value).expanduser().resolve()


def _ensure_private_dir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(path, 0o700)
    except OSError as exc:
        raise TranscriptionError("transcript runtime directories are unavailable") from exc


def _run(args: list[str], label: str) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, check=False,
        )
    except (OSError, ValueError) as exc:
        raise TranscriptionError(f"{label} is unavailable") from exc
    if result.returncode != 0:
        raise TranscriptionError(f"{label} failed")
    return result


def _require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise TranscriptionError(f"required command not found: {name}")
    return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise TranscriptionError("source media cannot be read") from exc
    return digest.hexdigest()


def _duration_seconds(path: Path) -> float:
    ffprobe = _require_command("ffprobe")
    result = _run([
        ffprobe, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(path),
    ], "ffprobe duration inspection")
    try:
        return max(0.0, float(result.stdout.strip()))
    except ValueError as exc:
        raise TranscriptionError("media duration is invalid") from exc


def _is_video(path: Path) -> bool:
    ffprobe = _require_command("ffprobe")
    result = subprocess.run([
        ffprobe, "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=codec_type", "-of", "default=nw=1:nk=1",
        str(path),
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if result.returncode == 0 and "video" in result.stdout.split():
        return True
    return path.suffix.lower() in VIDEO_EXTENSIONS


def _prepare_audio(source: Path, work_dir: Path) -> Path:
    if not _is_video(source):
        return source

    ffmpeg = _require_command("ffmpeg")
    audio = work_dir / "extracted-audio.wav"
    _run([
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le", str(audio),
    ], "video audio extraction")
    if not audio.is_file() or audio.stat().st_size == 0:
        raise TranscriptionError("video has no usable audio stream")
    return audio


def _normalize_language(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    key = value.strip().lower().replace("_", "-")
    if not key:
        return None
    if key in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[key]

    try:
        from whisper.tokenizer import LANGUAGES
        reverse = {name.lower(): code for code, name in LANGUAGES.items()}
        if key in reverse:
            return reverse[key]
    except ImportError:
        pass

    if re.fullmatch(r"[a-z]{2,3}", key):
        return key
    raise TranscriptionError(f"unsupported language hint: {value}")


def _torch_device(env_name: str, *, prefer_mps: bool) -> str:
    requested = os.environ.get(env_name, "auto").strip().lower()
    if requested and requested != "auto":
        return requested
    try:
        import torch
        if prefer_mps and torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except (ImportError, AttributeError):
        pass
    return "cpu"


def _load_whisper(model_name: str, device: str) -> Any:
    try:
        import whisper
        kwargs: dict[str, Any] = {}
        cache = os.environ.get("EAIO_WHISPER_MODEL_CACHE")
        if cache:
            kwargs["download_root"] = cache
        return whisper.load_model(model_name, device=device, **kwargs)
    except Exception as exc:
        raise TranscriptionError("Whisper model could not be loaded") from exc


def _whisper_language_probe(audio: Path) -> str:
    try:
        import whisper
        model_name = os.environ.get("EAIO_WHISPER_DETECTION_MODEL", "base")
        device = _torch_device("EAIO_WHISPER_DEVICE", prefer_mps=False)
        model = _load_whisper(model_name, device)
        audio_array = whisper.load_audio(str(audio))
        audio_array = whisper.pad_or_trim(audio_array)
        mel = whisper.log_mel_spectrogram(audio_array).to(model.device)
        _, probabilities = model.detect_language(mel)
        return max(probabilities, key=probabilities.get)
    except TranscriptionError:
        raise
    except Exception as exc:
        raise TranscriptionError("Whisper language detection failed") from exc


def _transcribe_whisper(audio: Path, language: Optional[str]) -> EngineResult:
    try:
        import whisper
        model_name = os.environ.get("EAIO_WHISPER_MODEL", "small")
        device = _torch_device("EAIO_WHISPER_DEVICE", prefer_mps=False)
        model = _load_whisper(model_name, device)
        kwargs: dict[str, Any] = {
            "task": "transcribe", "fp16": False, "verbose": False,
        }
        if language:
            kwargs["language"] = language
        result = model.transcribe(str(audio), **kwargs)
    except TranscriptionError:
        raise
    except Exception as exc:
        raise TranscriptionError("Whisper transcription failed") from exc

    segments = [
        Segment(
            float(item.get("start", 0.0)),
            float(item.get("end", 0.0)),
            str(item.get("text", "")).strip(),
        )
        for item in result.get("segments", [])
        if str(item.get("text", "")).strip()
    ]
    if not segments:
        raise TranscriptionError("Whisper returned an empty transcript")
    return EngineResult(
        engine="whisper",
        engine_version=str(getattr(whisper, "__version__", "unknown")),
        model=_safe_model_label(model_name, "whisper"),
        language=_normalize_language(result.get("language")) or language or "unknown",
        segments=segments,
    )


def _sensevoice_language(text: str, requested: Optional[str]) -> str:
    match = re.search(r"<\|(zh|en|yue|ja|ko|nospeech)\|>", text or "")
    return _normalize_language(match.group(1) if match else None) or requested or "unknown"


def _sensevoice_segments(
    words: Iterable[Any], timestamps: Iterable[Any], duration: float, text: str,
) -> list[Segment]:
    clean_words = [str(word) for word in words]
    clean_timestamps = list(timestamps)
    segments: list[Segment] = []
    current_words: list[str] = []
    current_times: list[tuple[float, float]] = []
    punctuation = set("。！？!?；;，,、：:")

    def flush() -> None:
        if not current_words:
            return
        content = "".join(current_words).strip()
        if not content:
            current_words.clear()
            current_times.clear()
            return
        start = current_times[0][0] if current_times else 0.0
        end = current_times[-1][1] if current_times else duration
        segments.append(Segment(start, max(start, end), content))
        current_words.clear()
        current_times.clear()

    for index, word in enumerate(clean_words):
        stamp = clean_timestamps[index] if index < len(clean_timestamps) else None
        try:
            start_ms, end_ms = float(stamp[0]), float(stamp[1])
            timing = (start_ms / 1000.0, end_ms / 1000.0)
        except (TypeError, ValueError, IndexError):
            timing = (current_times[-1][1] if current_times else 0.0, duration)
        current_words.append(word)
        current_times.append(timing)
        if word in punctuation or len(current_words) >= 80:
            flush()
    flush()

    if not segments and text.strip():
        segments.append(Segment(0.0, duration, text.strip()))
    return segments


def _transcribe_sensevoice(
    audio: Path, language: Optional[str], duration: float,
) -> EngineResult:
    try:
        import funasr
        from funasr import AutoModel
        from funasr.utils.postprocess_utils import rich_transcription_postprocess

        model_spec = os.environ.get("EAIO_SENSEVOICE_MODEL", "iic/SenseVoiceSmall")
        requested_device = _torch_device("EAIO_SENSEVOICE_DEVICE", prefer_mps=True)
        vad_model = os.environ.get("EAIO_SENSEVOICE_VAD_MODEL", "fsmn-vad")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            model = AutoModel(
                model=model_spec, vad_model=vad_model, device=requested_device,
                disable_update=True,
            )
            result = model.generate(
                input=str(audio), language=language or "auto", use_itn=True,
                batch_size_s=float(os.environ.get("EAIO_SENSEVOICE_BATCH_SECONDS", "60")),
                output_timestamp=True, return_raw_text=True, disable_pbar=True,
            )
    except Exception as exc:
        raise TranscriptionError("SenseVoice transcription failed") from exc

    item = result[0] if result else {}
    raw_text = str(item.get("text", ""))
    text = rich_transcription_postprocess(raw_text).strip()
    if not text:
        raise TranscriptionError("SenseVoice returned an empty transcript")
    segments = _sensevoice_segments(
        item.get("words", []), item.get("timestamp", []), duration, text,
    )
    if not segments:
        raise TranscriptionError("SenseVoice returned no timestamped transcript")
    return EngineResult(
        engine="sensevoice",
        engine_version=f"FunASR {getattr(funasr, '__version__', 'unknown')}",
        model=_safe_model_label(model_spec, "SenseVoiceSmall"),
        language=_sensevoice_language(raw_text, language),
        segments=segments,
    )


def _select_engine(
    engine: str, language: Optional[str], audio: Path,
) -> tuple[str, Optional[str]]:
    if engine != "auto":
        return engine, language
    if language:
        return ("sensevoice" if language in {"zh", "yue"} else "whisper"), language
    detected = _normalize_language(_whisper_language_probe(audio))
    if not detected:
        raise TranscriptionError("automatic language detection returned no language")
    return ("sensevoice" if detected in {"zh", "yue"} else "whisper"), detected


def _format_timestamp(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remaining:06.3f}"


def _yaml_string(value: str) -> str:
    import json
    return json.dumps(str(value), ensure_ascii=False)


def _write_markdown(
    output: Path, source_name: str, source_hash: str, duration: float,
    result: EngineResult,
) -> None:
    lines = [
        "---",
        f"source_file: {_yaml_string(source_name)}",
        f"source_sha256: {_yaml_string(source_hash)}",
        f"duration_seconds: {duration:.3f}",
        f"detected_language: {_yaml_string(result.language)}",
        f"engine: {_yaml_string(result.engine)}",
        f"engine_version: {_yaml_string(result.engine_version)}",
        f"model: {_yaml_string(result.model)}",
        f"generated_at: {_yaml_string(datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'))}",
        "---", "", "# Transcript", "",
    ]
    for segment in result.segments:
        text = segment.text.replace("\r", " ").replace("\n", " ").strip()
        if text:
            lines.append(
                f"[{_format_timestamp(segment.start)} - {_format_timestamp(segment.end)}] {text}"
            )
    try:
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.chmod(output, 0o600)
    except OSError as exc:
        raise TranscriptionError("transcript cannot be written") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transcribe local media to reviewable Markdown"
    )
    parser.add_argument("media_file", type=Path)
    parser.add_argument(
        "--language", default=None,
        help="en, zh/zh-CN/Chinese, yue/Cantonese, or another Whisper language",
    )
    parser.add_argument(
        "--engine", choices=("auto", "whisper", "sensevoice"), default="auto",
    )
    parser.add_argument("--runtime-root", default=None, help="override deployment.runtime_root")
    parser.add_argument(
        "--company-config", default=os.environ.get("EAIO_COMPANY_CONFIG"),
        help="active company YAML used to derive runtime_root",
    )
    parser.add_argument("--output", type=Path, default=None, help="explicit Markdown output path")
    parser.add_argument("--force", action="store_true", help="replace an existing transcript")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        source = args.media_file.expanduser().resolve()
        if not source.is_file():
            raise TranscriptionError("source media file does not exist")
        runtime_root = resolve_runtime_root(args.runtime_root, args.company_config)
        media_root = runtime_root / "media-transcription"
        _ensure_private_dir(media_root)
        work_root = media_root / "work"
        transcript_root = media_root / "transcripts"
        _ensure_private_dir(work_root)
        _ensure_private_dir(transcript_root)

        _require_command("ffmpeg")
        source_hash = _sha256(source)
        duration = _duration_seconds(source)
        requested_language = _normalize_language(args.language)
        stem = re.sub(r"[^A-Za-z0-9._-]+", "-", source.stem).strip("-") or "media"
        default_output = transcript_root / f"{stem}.{source_hash[:12]}.md"
        output = args.output.expanduser().resolve() if args.output else default_output
        if output.exists() and not args.force:
            raise TranscriptionError("transcript already exists; use --force to replace it")
        _ensure_private_dir(output.parent)

        with tempfile.TemporaryDirectory(prefix="job-", dir=work_root) as temp_name:
            with_audio = _prepare_audio(source, Path(temp_name))
            selected_engine, selected_language = _select_engine(
                args.engine, requested_language, with_audio,
            )
            try:
                if selected_engine == "whisper":
                    result = _transcribe_whisper(with_audio, selected_language)
                else:
                    result = _transcribe_sensevoice(
                        with_audio, selected_language, duration,
                    )
            except TranscriptionError:
                if args.engine != "auto":
                    raise
                fallback = "sensevoice" if selected_engine == "whisper" else "whisper"
                if fallback == "whisper":
                    result = _transcribe_whisper(with_audio, selected_language)
                else:
                    result = _transcribe_sensevoice(
                        with_audio, selected_language, duration,
                    )

        if _sha256(source) != source_hash:
            raise TranscriptionError("source media changed during transcription")
        _write_markdown(output, source.name, source_hash, duration, result)
        print(f"transcript={output}")
        print(f"engine={result.engine} language={result.language} model={result.model}")
        return 0
    except TranscriptionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
