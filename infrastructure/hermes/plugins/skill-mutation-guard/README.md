# EAO Hermes Skill Mutation Guard

This repository artifact implements the approved Operations Skill mutation
boundary without modifying Hermes Agent.

It registers one Hermes pre_tool_call hook. The hook is policy code, not prompt
wording, and returns Hermes' blocking directive before skill_manage executes.

## Authorization contract

A skill_manage mutation is allowed only when all conditions hold:

1. The operation is one of Hermes 0.21.2's mutation actions:
   create, edit, patch, delete, write_file, or remove_file.
2. The Skill name starts with the configured namespace, learned- by default.
3. The resolved target remains inside the configured learning_root.
4. The target and any supporting file path resolve safely.

All malformed, unknown, external, third-party, company, traversal, absolute-path,
symlink-escape, missing-configuration, and resolution-error cases block.

The current Operations configuration should use:

    profile: operations
    learning_root: ~/.hermes/profiles/operations/skills
    allowed_namespace: learned-

The plugin does not classify a target by string prefix alone. Existing Skill
names are located under the configured learning root and then checked with
Path.resolve(). A profile-local symlink to a Company Skill therefore resolves
outside the root and is blocked. A Skill that exists only in an external
directory is not found in the learning root and is blocked.

Batch calls are checked completely before Hermes receives them. The plugin
rejects unsupported batch actions and mixed safe/protected batches, so a
Company mutation cannot be hidden beside an allowed learned mutation.

## Hermes extension contract

Hermes 0.21.2 requires a directory plugin containing:

- plugin.yaml with provides_hooks: pre_tool_call;
- __init__.py exposing register(ctx);
- register(ctx) calling ctx.register_hook("pre_tool_call", callback).

The callback receives tool_name and args. Returning:

    {"action": "block", "message": "..."}

makes Hermes return a blocked tool result and prevents execution. Returning
None proceeds.

Hermes invokes this policy hook before tool execution through both
agent/tool_executor.py and agent/agent_runtime_helpers.py, which covers normal
foreground and Background Review tool calls.

The plugin is Operations-scoped. It is intentionally not registered for other
Profiles. Future department reuse supplies a different profile, root, and
namespace through the same settings.

## Registration example

This is an example only and was not applied to production:

    plugins:
      enabled:
        - eao-skill-mutation-guard
      entries:
        eao-skill-mutation-guard:
          settings:
            profile: operations
            learning_root: ~/.hermes/profiles/operations/skills
            allowed_namespace: learned-

The plugin directory must also be placed in a supported Hermes plugin source,
for example:

    <HERMES_HOME>/plugins/eao-skill-mutation-guard/

A deployment may symlink that directory to this repository artifact. This
implementation task does not perform that placement or enablement.

## Rolling compatibility contract

Every future Hermes candidate must verify all of the following before this
plugin is enabled:

- pre_tool_call still exists and accepts a callback;
- the callback still receives tool_name and args;
- the block directive still prevents execution;
- foreground skill_manage passes through the hook;
- Background Review skill_manage passes through the hook;
- the plugin is discovered and registered for Operations;
- negative Company, third-party, traversal, absolute-path, and symlink tests pass;
- positive learned-* fixture tests pass.

The plugin declares requires_hermes >=0.21.2. If an upstream release changes
the hook or skill_manage payload, adapt this small plugin during rolling
validation rather than forking Hermes.

## Testing

From the repository root:

    python3 -m unittest discover -s infrastructure/hermes/plugins/skill-mutation-guard/tests -p 'test_*.py'

The tests use only temporary directories and never touch a real Hermes Profile,
Company Skill, or production configuration.
