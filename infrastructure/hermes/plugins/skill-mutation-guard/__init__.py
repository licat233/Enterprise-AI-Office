"""Hermes registration entry point for the EAO Skill Mutation Guard."""

from .policy import SkillMutationGuard


def _get_config(ctx, key, default=None):
    try:
        return ctx.get_config(key, default)
    except Exception:
        return default


def register(ctx):
    """Register only for the configured target Profile.

    A missing root or namespace still registers a fail-closed callback for the
    Operations Profile. Other Profiles are left untouched.
    """
    try:
        active_profile = ctx.profile_name
    except Exception:
        return

    configured_profile = _get_config(ctx, "profile")
    if not isinstance(configured_profile, str) or not configured_profile.strip():
        if active_profile != "operations":
            return
        guard = SkillMutationGuard(
            profile_name=str(active_profile),
            learning_root=None,
            allowed_namespace=None,
            configuration_error="target Profile setting is missing or invalid",
        )
        ctx.register_hook("pre_tool_call", guard.pre_tool_call)
        return

    if active_profile != configured_profile:
        if active_profile != "operations":
            return
        guard = SkillMutationGuard(
            profile_name=str(active_profile),
            learning_root=None,
            allowed_namespace=None,
            configuration_error="target Profile setting is missing or does not select Operations",
        )
    else:
        guard = SkillMutationGuard.from_config(
            profile_name=str(active_profile),
            learning_root=_get_config(ctx, "learning_root"),
            allowed_namespace=_get_config(ctx, "allowed_namespace"),
        )

    ctx.register_hook("pre_tool_call", guard.pre_tool_call)
