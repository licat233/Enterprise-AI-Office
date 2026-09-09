---
name: video-to-text-agent
description: Run the Enterprise media-transcription CLI to extract spoken narration from a local video, then use the video filename stem as its cover text.
version: 1.2.0
author: local
license: MIT
metadata:
  hermes:
    tags: [media, video, narration, transcription, social-video, local-tool]
---

# Video To Text Agent

Use this skill when a user provides a local video and asks to understand its
narration, cover text, selling points, script, or other short-video content.

The production tool is the Enterprise repository's non-interactive CLI:

```bash
"${ENTERPRISE_AI_OFFICE_ROOT}/scripts/transcribe"
```

The legacy personal wrapper and interactive command were not migrated. Do not
invoke, source, or depend on them during Agent execution.

This skill does not use OCR. Spoken narration is the authoritative content
source, and the source video filename stem is the cover text.

## Path Rules

For a source video:

```text
<media-file>/pre-coated with 3M tape,Mass potting line.mp4
```

the derived values are:

```text
cover_text: pre-coated with 3M tape,Mass potting line
result_dir: the Enterprise runtime transcript output for the source basename
transcript: the Enterprise runtime transcript output for the source basename
```

The result directory must be beside the video and have exactly the same name
as the video filename without its final extension. Do not add `_文案` or any
other suffix.

The cover text is the exact filename stem. Do not translate, rewrite, or
otherwise alter it when reporting the extracted source information.

## Agent Commands

For Chinese or Chinese-heavy narration, use SenseVoice:

```bash
"${ENTERPRISE_AI_OFFICE_ROOT}/scripts/transcribe" "/absolute/path/video.mp4" \
  --engine sensevoice --language zh
```

For English or mixed-language narration, use Whisper:

```bash
"${ENTERPRISE_AI_OFFICE_ROOT}/scripts/transcribe" "/absolute/path/video.mp4" \
  --engine whisper --language auto --model base --cpu-threads 8
```

For a path-only check before a potentially long transcription:

```bash
"${ENTERPRISE_AI_OFFICE_ROOT}/scripts/transcribe" "/absolute/path/video.mp4" \
  --engine whisper --dry-run
```

The CLI is non-interactive and suitable for Hermes running commands in a bash
environment. Always quote video paths because filenames may contain spaces,
commas, or non-ASCII characters.

## Workflow

1. Confirm the local video path exists.
2. Derive `cover_text` from the exact filename stem.
3. Derive the same-directory, same-stem result folder.
4. If a non-empty `.txt` transcript already exists in that folder, read it;
   do not transcribe the video again unnecessarily.
5. Otherwise run `${ENTERPRISE_AI_OFFICE_ROOT}/scripts/transcribe` with the
   appropriate engine and wait for it to finish.
6. Read `speech.txt` by default. If legacy output contains another clear
   transcript `.txt` file, it may be used as a fallback.
7. Use the transcript to summarize or repurpose the video as requested.

## Content Rules

Keep the source fields separate:

```text
cover_text: exact filename stem
narration: contents of speech.txt
```

Use narration to derive summaries, selling points, hooks, product facts,
subtitles, scripts, or social copy. Do not claim that a visual detail appears
in the video unless it is stated in the narration or established by the
filename.

If the transcript is missing, empty, or ambiguous, report that clearly. Do not
invent missing narration.

## Prohibited Workflow

- Do not run any legacy personal wrapper or interactive command.
- Do not use RapidOCR or extract video frames for text recognition.
- Do not use a web transcription service unless the user explicitly asks.
- Do not install models or dependencies without the user's approval.

## Example Result

```text
封面文字：pre-coated with 3M tape,Mass potting line

口播内容：
（读取同名文件夹中的 speech.txt）

根据口播整理：
（按用户要求输出摘要、卖点、脚本或社媒文案）
```
