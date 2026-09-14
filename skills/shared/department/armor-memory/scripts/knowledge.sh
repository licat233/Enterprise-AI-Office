#!/usr/bin/env bash
set -euo pipefail

resolve_script_path() {
  local source_path="${BASH_SOURCE[0]}"

  while [[ -L "$source_path" ]]; do
    local source_dir
    source_dir="$(cd -P "$(dirname "$source_path")" >/dev/null 2>&1 && pwd)"
    source_path="$(readlink "$source_path")"

    if [[ "$source_path" != /* ]]; then
      source_path="$source_dir/$source_path"
    fi
  done

  local final_dir
  final_dir="$(cd -P "$(dirname "$source_path")" >/dev/null 2>&1 && pwd)"
  printf '%s/%s\n' "$final_dir" "$(basename "$source_path")"
}

real_script="$(resolve_script_path)"
script_dir="$(dirname "$real_script")"
knowledge_tool="$script_dir/armor-knowledge.py"

if [[ ! -f "$knowledge_tool" ]]; then
  echo "ERROR: ARMOR knowledge tool not found: $knowledge_tool" >&2
  echo "The armor-memory Skill must contain its local armor-knowledge.py implementation." >&2
  exit 1
fi

exec python3 "$knowledge_tool" "$@"
