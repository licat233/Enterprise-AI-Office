# Local media transcription

This is the conditional media_transcription capability. It is an explicit,
host-native command that converts an audio or video file into a UTF-8,
timestamped Markdown transcript for human review.

It does not add a daemon, watcher, queue, employee-facing media UI, WeKnora ASR
integration, or automatic knowledge publication. The publication boundary is:

~~~
media → local transcript → human review/approval → optional WeKnora ingestion
~~~

## Runtime contract

The capability reuses already installed local tools:

- OpenAI Whisper for English and other explicitly selected non-Chinese languages;
- FunASR SenseVoiceSmall for Chinese and Cantonese;
- ffmpeg/ffprobe for media inspection and video audio extraction.

SenseVoice provenance is split deliberately:

- source/reference upstream: `QwenAudio/SenseVoice`;
- runtime model identifier: `iic/SenseVoiceSmall`;
- source code and model weights are separate licensing surfaces.

Do not infer model-weight redistribution rights from the source-code license.
Consult `THIRD_PARTY_NOTICES.md` and the exact selected model card/artifact
before redistribution or commercial packaging.

The deployment must provide a Python interpreter with the selected local ASR
packages. The repository does not install models or dependencies. Use
EAIO_MEDIA_TRANSCRIPTION_PYTHON with scripts/transcribe when the packages are
in a dedicated virtual environment.

The runtime root is derived in this order:

1. --runtime-root;
2. EAIO_RUNTIME_ROOT;
3. deployment.runtime_root from EAIO_COMPANY_CONFIG/--company-config.

Outputs are stored under:

~~~
<runtime_root>/media-transcription/work/
<runtime_root>/media-transcription/transcripts/
~~~

Both directories are created with mode 0700; transcript files use 0600.
Temporary extracted audio is scoped to one job and removed on success or
failure. The original media is never changed and is checksummed before and
after the job.

## CLI

From the repository root, with the existing ASR environment selected:

~~~
EAIO_MEDIA_TRANSCRIPTION_PYTHON=/path/to/video-transcription-venv/bin/python \
  scripts/transcribe media.mp4

scripts/transcribe media.mp3 --language en
scripts/transcribe meeting.mov --language zh
scripts/transcribe call.m4a --language yue
scripts/transcribe lecture.wav --engine whisper
scripts/transcribe interview.wav --engine sensevoice
~~~

For an active private company configuration:

~~~
EAIO_COMPANY_CONFIG=/protected/company.yaml \
EAIO_MEDIA_TRANSCRIPTION_PYTHON=/path/to/asr/python \
  scripts/transcribe media.mp4
~~~

The default output name includes the source basename and a source checksum.
An existing output is not replaced unless --force is supplied.

## Routing

Explicit hints are deterministic:

| Input | Engine |
| --- | --- |
| en, English | Whisper |
| zh, zh-CN, Chinese, Mandarin | SenseVoice |
| yue, Cantonese | SenseVoice |
| another supported Whisper language | Whisper |

With no hint, the command uses the existing Whisper base model only for a
short language-identification probe, then performs one final transcription:
Chinese/Cantonese goes to SenseVoice and English/other languages go to
Whisper. This is not a dual transcription or an ensemble. If the selected
engine has an explicit process/empty-output failure, automatic mode makes one
fallback attempt with the other installed engine and records the engine that
actually produced the transcript. A subjective quality concern does not trigger
fallback.

The current OpenAI Whisper package may not support the MPS backend on every
Apple Silicon/PyTorch combination. The adapter therefore defaults Whisper to
the verified local device path and allows an operator override through
EAIO_WHISPER_DEVICE; SenseVoice uses MPS when the installed runtime reports
it as available.

## Markdown contract

Each transcript contains YAML front matter with:

~~~
source_file: "meeting.mp4"
source_sha256: "..."
duration_seconds: 42.100
detected_language: "en"
engine: "whisper"
engine_version: "..."
model: "small"
generated_at: "..."
~~~

The body is # Transcript followed by timestamped lines. It records only the
source basename, never a private absolute path. Secrets, tokens, passwords,
credentials, and provider/API material are not read or written by the command.

## Acceptance and knowledge compatibility

The enabled capability acceptance is in docs/ACCEPTANCE-TESTS.md under Media
transcription. Use non-sensitive English and Chinese fixtures, test both direct
audio and video extraction, and verify temporary-audio cleanup.

If WeKnora compatibility is tested, ingest a reviewed copy into a temporary
test Knowledge Base only. Delete that document and Knowledge Base afterward.
The command itself never calls WeKnora and never writes the formal Company
Knowledge Knowledge Base.
