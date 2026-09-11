"""Deterministic, supplemental screening for untrusted email content.

This module returns only fixed indicator codes. It never returns matched
content, decoded secrets, or an instruction block for an agent to follow.
Pattern screening is defense in depth; authorization and envelope validation
remain the primary controls.
"""

from __future__ import annotations

import html
import re
import unicodedata
from typing import Iterable


UNTRUSTED_EMAIL_CONTENT = "UNTRUSTED_EMAIL_CONTENT"
NO_INSTRUCTION_AUTHORITY = "NONE"

_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "ignore_previous_instructions",
        re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior|former)\s+instructions\b"),
    ),
    (
        "ignore_system_instructions",
        re.compile(r"\bignore\s+(?:the\s+)?system\s+instructions?\b"),
    ),
    (
        "reveal_system_prompt",
        re.compile(r"\b(?:reveal|show|print|tell\s+me)\b.{0,40}\b(?:system\s+prompt|hidden\s+prompt)\b"),
    ),
    (
        "developer_mode",
        re.compile(r"\bdeveloper\s+mode\b"),
    ),
    (
        "jailbreak",
        re.compile(r"\bjailbreak\b"),
    ),
    (
        "tool_execution_request",
        re.compile(r"\b(?:call|invoke|use|open)\b.{0,40}\b(?:this\s+)?(?:tool|browser|url|link)\b"),
    ),
    (
        "command_execution_request",
        re.compile(r"\b(?:execute|run)\b.{0,40}\b(?:this\s+)?(?:command|code|script)\b"),
    ),
    (
        "credential_exfiltration_request",
        re.compile(r"\b(?:send|reveal|show|include|expose)\b.{0,40}\b(?:credentials?|passwords?|tokens?)\b"),
    ),
    (
        "api_key_or_env_request",
        re.compile(r"\b(?:show|read|reveal|include|print)\b.{0,40}\b(?:api\s*key|\.env|environment\s+variables?)\b"),
    ),
    (
        "internal_file_exfiltration_request",
        re.compile(r"\b(?:read|upload|attach|send|expose)\b.{0,50}\b(?:internal\s+files?|private\s+files?|vault|config(?:uration)?)\b"),
    ),
    (
        "internal_sensitive_data_request",
        re.compile(r"\b(?:include|send|reveal|show|provide)\b.{0,50}\b(?:internal\s+(?:pricing|information|instructions|policy)|private\s+(?:data|information))\b"),
    ),
    (
        "private_employee_data_request",
        re.compile(r"\b(?:send|reveal|show|provide|include)\b.{0,50}\b(?:private\s+employee\s+data|employee\s+(?:passwords?|personal\s+data|private\s+information))\b"),
    ),
    (
        "internal_only_instruction_request",
        re.compile(r"\b(?:send|reveal|show|provide|include|read)\b.{0,50}\b(?:internal[- ]only\s+(?:instructions?|operating\s+instructions?)|private\s+authentication)\b"),
    ),
    (
        "act_as_system",
        re.compile(r"\b(?:act|behave|pretend)\s+as\s+(?:the\s+)?system\b"),
    ),
    (
        "system_role_claim",
        re.compile(r"\b(?:you\s+are\s+now|you\s+are)\b.{0,30}\b(?:system\s+administrator|administrator|system)\b"),
    ),
    (
        "policy_override",
        re.compile(r"\b(?:override|bypass|disable)\b.{0,40}\b(?:policy|safety|security|authorization)\b"),
    ),
    (
        "role_tag",
        re.compile(r"<\s*(?:system|developer|assistant|tool|instructions?)\s*>"),
    ),
    (
        "encoded_instruction_request",
        re.compile(r"\b(?:base64|encoded|decode|解码|编码)\b.{0,50}\b(?:instruction|指令|prompt|提示)\b"),
    ),
    (
        "ignore_previous_instructions_zh",
        re.compile(r"(?:忽略|无视).{0,12}(?:之前|以前|先前|所有).{0,12}(?:指令|提示|规则)"),
    ),
    (
        "reveal_system_prompt_zh",
        re.compile(r"(?:显示|透露|告诉我|输出).{0,20}(?:系统提示|系统指令|隐藏提示)"),
    ),
    (
        "developer_mode_zh",
        re.compile(r"(?:开发者模式|越狱模式)"),
    ),
    (
        "tool_execution_request_zh",
        re.compile(r"(?:调用|打开|使用).{0,20}(?:工具|浏览器|链接|网址)"),
    ),
    (
        "command_execution_request_zh",
        re.compile(r"(?:执行|运行).{0,20}(?:命令|代码|脚本)"),
    ),
    (
        "credential_exfiltration_request_zh",
        re.compile(r"(?:发送|显示|提供|泄露).{0,20}(?:凭证|密码|密钥|令牌)"),
    ),
    (
        "internal_file_exfiltration_request_zh",
        re.compile(r"(?:读取|上传|发送).{0,20}(?:内部文件|私有文件|配置|知识库)"),
    ),
    (
        "internal_sensitive_data_request_zh",
        re.compile(r"(?:提供|发送|显示|包含).{0,20}(?:内部报价|内部信息|内部政策|私有数据)"),
    ),
    (
        "private_employee_data_request_zh",
        re.compile(r"(?:提供|发送|显示|包含).{0,20}(?:员工私密数据|员工密码|员工个人信息)"),
    ),
    (
        "internal_only_instruction_request_zh",
        re.compile(r"(?:提供|发送|显示|读取).{0,20}(?:内部操作指令|内部专用说明|私有认证信息)"),
    ),
    (
        "act_as_system_zh",
        re.compile(r"(?:扮演|充当).{0,10}(?:系统|管理员)"),
    ),
    (
        "system_role_claim_zh",
        re.compile(r"(?:你现在是|你是).{0,12}(?:系统管理员|管理员|系统)"),
    ),
    (
        "policy_override_zh",
        re.compile(r"(?:覆盖|绕过|禁用).{0,12}(?:策略|安全|授权|规则)"),
    ),
)

_BASE64_CANDIDATE = re.compile(
    r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{48,}={0,2}(?![A-Za-z0-9+/])"
)
_URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")


def normalize_for_security(value: str) -> str:
    """Normalize a private inspection copy; the normalized text is never emitted."""
    normalized = unicodedata.normalize("NFKC", value or "")
    normalized = "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Cf"
    )
    return re.sub(r"\s+", " ", html.unescape(normalized)).strip().casefold()


def extract_links(value: str | None) -> list[str]:
    """Extract visible URL-shaped strings without fetching or validating them."""
    return _URL_PATTERN.findall(value or "")


def screen_untrusted_email(*parts: str | Iterable[str] | None) -> dict[str, object]:
    values: list[str] = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, str):
            values.append(part)
        else:
            values.extend(str(item) for item in part)
    normalized = normalize_for_security("\n".join(values))
    indicators = {
        code for code, pattern in _PATTERNS if pattern.search(normalized)
    }
    if _BASE64_CANDIDATE.search(normalized):
        indicators.add("encoded_payload_candidate")
    return {
        "trust_class": UNTRUSTED_EMAIL_CONTENT,
        "instruction_authority": NO_INSTRUCTION_AUTHORITY,
        "suspected_prompt_injection": bool(indicators),
        "indicators": sorted(indicators),
    }
