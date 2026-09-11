#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

if ! command -v ruby >/dev/null 2>&1; then
  printf '%s\n' "FAIL YAML syntax check requires Ruby/Psych on the validation host." >&2
  exit 2
fi

ruby - "$ROOT" <<'RUBY'
require "psych"

root = ARGV.fetch(0)
trees = %w[config infrastructure reference state validation .github profiles skills]
files = trees.flat_map do |tree|
  base = File.join(root, tree)
  next [] unless Dir.exist?(base)
  Dir.glob(File.join(base, "**", "*")).select do |path|
    File.file?(path) && [".yaml", ".yml"].include?(File.extname(path).downcase)
  end
end.uniq.sort

failures = []

puts "Enterprise AI Office YAML Syntax"
puts "--------------------------------"
puts "YAML files discovered: #{files.length}"

files.each do |path|
  relative = path.delete_prefix(root + File::SEPARATOR)
  begin
    Psych.parse_stream(File.read(path))
    puts "PASS #{relative}"
  rescue Psych::SyntaxError => e
    failures << "#{relative}: #{e.message.lines.first.to_s.strip}"
    puts "FAIL #{relative}"
  end
end

if failures.any?
  puts "YAML syntax failures: #{failures.length}"
  failures.each { |failure| puts "FAIL #{failure}" }
  exit 2
end

puts "YAML syntax failures: 0"
puts "YAML SYNTAX: PASS"
RUBY
