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

if [[ -n "${ARMOR_ARCH_ROOT:-}" ]]; then
  repo_root="$ARMOR_ARCH_ROOT"
else
  real_script="$(resolve_script_path)"
  script_dir="$(dirname "$real_script")"
  repo_root="$(cd "$script_dir/../../../.." >/dev/null 2>&1 && pwd)"
fi

knowledge_tool="$repo_root/minimal-stable/scripts/armor-knowledge.py"

if [[ ! -f "$knowledge_tool" ]]; then
  echo "ERROR: ARMOR knowledge tool not found: $knowledge_tool" >&2
  echo "Set ARMOR_ARCH_ROOT to the armor-memory repository root." >&2
  exit 1
fi

exec python3 "$knowledge_tool" "$@"
