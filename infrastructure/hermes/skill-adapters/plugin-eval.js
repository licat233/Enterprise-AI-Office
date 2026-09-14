#!/usr/bin/env node

import { access } from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

const [command, skillName, ...extraArgs] = process.argv.slice(2);
const allowedCommands = new Set(["analyze", "explain-budget", "measurement-plan"]);

function fail(message) {
  console.error(`plugin-eval adapter: ${message}`);
  process.exit(2);
}

function isSafeSkillName(value) {
  return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value || "");
}

function isInside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === "" || (!relative.startsWith(".." + path.sep) && relative !== "..");
}

if (command === "benchmark") {
  fail("BLOCKED: live Codex benchmark is unsupported in this adapter context");
} else if (!allowedCommands.has(command)) {
  fail("BLOCKED: only analyze, explain-budget, and measurement-plan are supported");
} else if (!isSafeSkillName(skillName)) {
  fail("BLOCKED: Skill name must be a simple lowercase hyphen-case name, not a path");
} else if (extraArgs.length > 0 && !(extraArgs.length === 2 && extraArgs[0] === "--format" && ["json", "markdown"].includes(extraArgs[1]))) {
  fail("BLOCKED: only --format json|markdown is accepted");
} else {
  const rawRoots = String(process.env.PLUGIN_EVAL_APPROVED_SKILL_ROOTS || "")
    .split(path.delimiter)
    .filter(Boolean);
  if (rawRoots.some((root) => !path.isAbsolute(root))) {
    fail("BLOCKED: every approved Skill root must be absolute");
  }
  const roots = rawRoots
    .map((root) => path.resolve(root))
    .filter((root, index, all) => all.indexOf(root) === index);
  const upstreamRoot = process.env.PLUGIN_EVAL_UPSTREAM_ROOT;
  if (roots.length === 0 || !upstreamRoot || !path.isAbsolute(upstreamRoot)) {
    fail("BLOCKED: approved Skill roots and an absolute upstream checkout are required");
  } else {
    const cliPath = path.resolve(upstreamRoot, "scripts/plugin-eval.js");
    let target = null;
    for (const root of roots) {
      const candidate = path.resolve(root, skillName);
      if (isInside(root, candidate) && await access(path.join(candidate, "SKILL.md")).then(() => true, () => false)) {
        target = candidate;
        break;
      }
    }
    if (!target) {
      fail(`NOT FOUND: approved Skill ${JSON.stringify(skillName)}`);
    } else if (!await access(cliPath).then(() => true, () => false)) {
      fail("BLOCKED: pinned upstream plugin-eval CLI is unavailable");
    } else {
      console.error(`plugin-eval adapter: resolved ${skillName} -> ${target}`);
      console.error(`plugin-eval adapter: invoking ${cliPath} ${command}`);
      const child = spawn(process.execPath, [cliPath, command, target, ...extraArgs], {
        env: { PATH: process.env.PATH || "", HOME: process.env.HOME || "" },
        stdio: "inherit",
      });
      child.on("error", (error) => fail(`upstream CLI failed to start: ${error.message}`));
      child.on("exit", (code, signal) => {
        if (signal) {
          fail(`upstream CLI terminated by ${signal}`);
        } else {
          process.exitCode = code ?? 1;
        }
      });
    }
  }
}
