#!/usr/bin/env bash
set -euo pipefail

absolute_output=false
json_output=false
router_args=()

for arg in "$@"; do
  case "$arg" in
    --absolute)
      absolute_output=true
      ;;
    --json)
      json_output=true
      router_args+=("$arg")
      ;;
    *)
      router_args+=("$arg")
      ;;
  esac
done

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

if [[ "$absolute_output" == true && "$json_output" == true ]]; then
  echo "ERROR: --absolute cannot currently be combined with --json." >&2
  exit 1
fi

if [[ -n "${ARMOR_ARCH_ROOT:-}" ]]; then
  repo_root="$ARMOR_ARCH_ROOT"
else
  real_script="$(resolve_script_path)"
  script_dir="$(dirname "$real_script")"
  repo_root="$(cd "$script_dir/../../../.." >/dev/null 2>&1 && pwd)"
fi

router="$repo_root/minimal-stable/scripts/armor-route.py"

if [[ ! -f "$router" ]]; then
  echo "ERROR: ARMOR Router not found: $router" >&2
  echo "Set ARMOR_ARCH_ROOT to the AI-Agent-Memory-Architecture repository root." >&2
  exit 1
fi

route_output="$(
  python3 "$router" "${router_args[@]}"
)"

if [[ "$absolute_output" == false ]]; then
  printf '%s\n' "$route_output"
  exit 0
fi

if [[ -z "${ARMOR_VAULT_ROOT:-}" ]]; then
  echo "ERROR: ARMOR_VAULT_ROOT is required with --absolute." >&2
  exit 1
fi

relative_path="$(printf '%s\n' "$route_output" | sed -n '1p')"
category="$(printf '%s\n' "$route_output" | sed -n '2p')"
reason="$(printf '%s\n' "$route_output" | sed -n '3p')"

absolute_path="${ARMOR_VAULT_ROOT%/}/${relative_path#/}"

printf '%s\n' "$absolute_path"
printf '%s\n' "$category"
printf '%s\n' "$reason"
