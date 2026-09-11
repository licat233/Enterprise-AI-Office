#!/usr/bin/env python3
"""Deterministic article draft gate for ARMOR website articles.

The checker owns draft-format, Frontmatter, heading hierarchy, and deterministic
SEO checks. Blueprint section intentions are expert-owned: heading suggestions
are deliberately not compared by exact text, count, or order. It does not claim
to validate rendered JSON-LD, live URLs, Google indexing, or AI citation
probability. Use ``--json`` for the machine-readable gate contract.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import yaml
except ImportError:  # pragma: no cover - the bundled environment has PyYAML
    yaml = None


REQUIRED_FIELDS = (
    "date",
    "site",
    "author",
    "title",
    "summary",
    "seo_title",
    "seo_description",
    "seo_keywords",
    "categories",
    "labels",
    "tags",
    "permalink",
    "thumbnail_prompt",
    "images_prompt",
)
RETIRED_FIELDS = {
    "memory_layer",
    "memory_class",
    "write_policy",
    "author_agent",
    "confidence",
    "expires",
    "ssot_checked",
}
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*")
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")
CLAIM_RE = re.compile(
    r"(?:\b\d+(?:\.\d+)?%?|\b20\d{2}\b|\b(?:twice|three times|\d+x)\b|"
    r"\b(?:according to|research|study|survey|market|industry-leading|best|largest|"
    r"fastest|more effective|faster than)\b)",
    re.IGNORECASE,
)
CITATION_RE = re.compile(
    r"https?://|\[[^\]]+\]\([^)]*https?://|\[\d+\]|"
    r"\b(?:according to|per|reported by|data from|source:|study from)\b",
    re.IGNORECASE,
)
AUDIENCE_BEHAVIOR_RE = re.compile(
    r"\b(?:"
    r"(?:the|a|every|any) (?:shopper|buyer|customer)'?s? (?:decision|choice|attention|instinct|hand|eye) (?:happens|takes place|is (?:made|decided))"
    r"|(?:buyers|shoppers|customers) (?:most commonly|almost always|usually|typically|always|never|tend to|care (?:most about|about)|look for|reach for|scan|judge|prefer|expect|notice|forget|overlook)"
    r"|most (?:buyers|shoppers|customers)"
    r"|(?:the|every|any) (?:shopper|buyer|customer) (?:looks|reaches|scans|expects|decides|notices|judges|prefers|forgets)"
    r")\b",
    re.IGNORECASE,
)
AUDIENCE_ATTRIBUTION_RE = re.compile(
    r"\b(?:according to|research|survey|stud(?:y|ies)|data|reported by|source|"
    r"customers? (?:told|reported|said)|user research|behavioral research|field research)\b",
    re.IGNORECASE,
)
ROADMAP_RE = re.compile(
    r"\b(?:"
    r"this (?:article|guide|post|piece|document|page) (?:covers|explains|will cover|will explain|walks? (?:you )?through|takes? you through|discusses|outlines|includes|details|breaks? down)"
    r"|(?:in|throughout) this (?:article|guide|post|piece|document)"
    r"|(?:is|are|involves?|breaks? down into|divides? into) (?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+) (?:separate|distinct|main|key|different)? (?:jobs|parts|sections|steps|tasks|layers|things|decisions|specs|dimensions|stages)"
    r")\b",
    re.IGNORECASE,
)
SPEC_H3_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 /&.,'()-]{0,40}:\s+\S")
TECH_REF_H2_RE = re.compile(r"\b(?:api|endpoint|syntax|reference|parameters?|configuration)\b", re.IGNORECASE)
TECH_H3_RE = re.compile(r"^(?:GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)\s+|\(\)$|(?:/\w+)+(?:\s|$)", re.IGNORECASE)
INTRO_OVERLAP_THRESHOLD = 0.15
EN_STOPWORDS = frozenset(
    "a an and or but if then else for of in on to from at by with is are was were be been being "
    "it its this that these those as has have had do does did will would can could should may might "
    "must not no so too very just more most less each every any all some none your you their there "
    "they them we our us i my me he she his her who what which while when where why how the".split()
)


class DocumentError(ValueError):
    """Raised when the draft cannot be parsed safely."""


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"^\s*---\s*\n(.*?)\n---\s*(?:\n|$)(.*)$", text, re.S)
    if not match:
        if text.lstrip().startswith("---"):
            raise DocumentError("frontmatter opening marker has no valid closing marker")
        raise DocumentError("missing YAML frontmatter")

    raw = match.group(1)
    if yaml is not None:
        parsed = yaml.safe_load(raw)
    else:  # Minimal fallback for scalar frontmatter if PyYAML is unavailable.
        parsed = {}
        for line in raw.splitlines():
            if ":" not in line or line.lstrip().startswith("#"):
                continue
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip().strip("\"'")
    if not isinstance(parsed, dict):
        raise DocumentError("frontmatter must decode to a mapping")
    return parsed, match.group(2).strip()


def tokens(text: str) -> list[str]:
    return [item.lower() for item in TOKEN_RE.findall(text)]


def phrase_token_count(text: str, phrase: str) -> int:
    haystack = tokens(text)
    needle = tokens(phrase)
    if not needle:
        return 0
    width = len(needle)
    return sum(haystack[i : i + width] == needle for i in range(len(haystack) - width + 1))


def contains_phrase(text: str, phrase: str) -> bool:
    return phrase_token_count(text, phrase) > 0


# Customer-value title contract (TITLE-01). A title must promise a buyer
# answer, decision, comparison, consequence, or outcome. Trend-only and
# self-celebratory framing is rejected even when the keyword is present.
# Question, comparison, how-to, selection, cost/ROI, risk/avoidance,
# diagnostic, and decision titles all satisfy the contract; punctuation is
# not the rule.
TITLE_VALUE_RE = re.compile(
    r"(?i)(?:"
    r"\bhow to\b|\bhow do\b|\bhow does\b|\bhow much\b|\bhow many\b|\bhow\b[^?.]{0,60}\bworks?\b|"
    r"\bwhy\b|\bwhich\b|\bwhat\b|\bwhen to\b|\bwhere to\b|"
    r"\bvs\.?\b|\bversus\b|\bcompared?\b|\bdifference between\b|\bor\b|"
    r"\bchoos(?:e|ing|es|s)\b|\bselect(?:ion|ing|s)?\b|\bevaluat(?:e|ing|es)\b|"
    r"\bdecid(?:e|ing|es)\b|\bdecisions?\b|\bcompare[sd]?\b|\bshould\b|"
    r"\bguide(?:s|d)? (?:to|for)\b|\bguide\b|\bright (?:choice|fit|option|solution)\b|"
    r"\bbest\b|\bchecklist\b|"
    r"\bcost\b|\broi\b|\bprice\b|\bbudget\b|\bafford\b|\bworth it\b|\bworth\b|\bpayback\b|"
    r"\bavoid(?:ing)?\b|\bmistakes\b|\bpitfalls\b|\brisks?\b|\bproblems?\b|\bdon'?t\b|"
    r"\beasier\b|\bsimpler\b|\bfaster\b|\bcheaper\b|\bsafer\b|\bbetter\b|\blower\b|"
    r"\bfewer\b|\breduce[sd]?\b|\bsave[sd]?\b|\bsavings?\b|\bsimplif(?:y|ies|ied|ying)\b|\bimprove[sd]?\b|"
    r"\banalysis\b|\breport\b|\boverview\b|\bexplained\b|\bprimer\b|"
    r"\bfor (?:retailers?|buyers?|stores?|shops?|your|you)\b)"
)
TITLE_TREND_RE = re.compile(
    r"(?i)(?:"
    r"\bthe (?:future|state|rise|next (?:big )?(?:thing|wave)|era|evolution) of\b|"
    r"\brevolutioniz(?:e|ing|ed|es)\b|\btransform(?:ing|ative|ed|es)?\b|"
    r"\bredefin(?:e|ing|ed|es)\b|\breimagin(?:e|ing|ed|es)\b|"
    r"\bunleash(?:ing|ed|es)?\b|\bempower(?:ing|ed|es)?\b|\bsupercharg(?:e|ing|ed|es)\b|"
    r"\bgame[- ]changer\b|\b(?:a|the)? ?new (?:era|frontier|paradigm|normal)\b|"
    r"\bwave[s]?\b|\bbeyond\b)"
)
TITLE_RESCUE_RE = re.compile(
    r"(?i)(?:"
    r"\bhow to\b|\bhow do\b|\bhow much\b|\bhow\b[^?.]{0,60}\bworks?\b|\bwhy\b|\bwhich\b|\bwhat\b|"
    r"\bworth it\b|\bshould\b|\bchoos(?:e|ing|es)\b|\bselect(?:ion|ing|s)?\b|"
    r"\bevaluat(?:e|ing|es)\b|\bdecid(?:e|ing|es)\b|\bdecisions?\b|\bcompare[sd]?\b|"
    r"\bvs\.?\b|\bversus\b|\bcompared?\b|\bdifference between\b|\bor\b|"
    r"\bavoid(?:ing)?\b|\bmistakes\b|\brisks?\b|\bcost\b|\bprice\b|\bbudget\b|\bpayback\b|"
    r"\bguide(?:s|d)? (?:to|for)\b|\bguide\b|\bchecklist\b|\bright (?:choice|fit|option|solution)\b|"
    r"\?$)"
)


def title_value_outcome(title: str) -> str:
    """Return why ``title`` fails the customer-value contract, or ``"ok"``."""
    stripped = title.strip()
    if not stripped:
        return "is empty"
    if TITLE_TREND_RE.search(stripped) and not TITLE_RESCUE_RE.search(stripped):
        return "uses trend-only or self-celebratory framing without a concrete buyer question or decision"
    if not TITLE_VALUE_RE.search(stripped) and not stripped.endswith("?"):
        return "does not promise a buyer answer, decision, comparison, consequence, or outcome"
    return "ok"


def title_value_checks(title: str, seo_title: str) -> list[dict[str, Any]]:
    """Deterministic customer-value title gate (TITLE-01)."""
    issues: list[str] = []
    for label, value in (("title", title), ("seo_title", seo_title)):
        if not str(value).strip():
            continue
        reason = title_value_outcome(str(value))
        if reason != "ok":
            issues.append(f"{label} {reason}")
    if not issues and not str(title).strip() and not str(seo_title).strip():
        return [
            check(
                "TITLE-01",
                "not_run",
                "blocking",
                "draft-deterministic",
                "no title or seo_title present; presence is covered by SEO-01 and SEO-13",
                "Add a frontmatter title and an SEO title that promise a buyer answer",
            )
        ]
    evidence = (
        "; ".join(issues)
        if issues
        else f"title={title!r} and seo_title={seo_title!r} promise a buyer answer, decision, comparison, consequence, or outcome"
    )
    return [
        check(
            "TITLE-01",
            "failed" if issues else "passed",
            "blocking",
            "draft-deterministic",
            evidence,
            "Reword the title to promise a buyer answer, decision, comparison, consequence, or outcome; drop trend-only or self-celebratory framing",
        )
    ]


def check(
    check_id: str,
    result: str,
    severity: str,
    owner: str,
    evidence: str,
    remediation: str = "",
    rerun: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": check_id,
        "result": result,
        "severity": severity,
        "owner": owner,
        "evidence": evidence,
        "remediation": remediation,
        "rerun": rerun or [check_id],
    }


def nested(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def as_strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return []


def blueprint_h1(blueprint: dict[str, Any]) -> Any:
    return nested(blueprint, "seo_constraints", "h1") or blueprint.get("h1")


def blueprint_h2s(blueprint: dict[str, Any]) -> list[str]:
    """Return non-binding heading suggestions from current or legacy Blueprints."""
    raw = nested(blueprint, "structure", "h2_sections") or blueprint.get("h2_sections")
    if not raw:
        raw = [
            item.get("heading_suggestion") or item.get("heading")
            for item in blueprint.get("outline", [])
            if isinstance(item, dict)
        ]
    return as_strings(raw)


def has_value(value: Any) -> bool:
    """Return whether a frontmatter field contains a meaningful value."""
    if value is None:
        return False
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return bool(str(value).strip())


def extract_headings(body: str) -> tuple[list[str], list[str]]:
    h1 = re.findall(r"^#\s+(?!#)(.+?)\s*$", body, re.MULTILINE)
    h2 = re.findall(r"^##\s+(?!#)(.+?)\s*$", body, re.MULTILINE)
    return h1, h2


def extract_internal_urls(body: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for raw in URL_RE.findall(body):
        clean = raw.rstrip(".,;:")
        parsed = urlparse(clean)
        if parsed.scheme != "https" or parsed.netloc.lower() not in {
            "armorlighting.com",
            "www.armorlighting.com",
            "armordigitalscreen.com",
            "www.armordigitalscreen.com",
        }:
            continue
        if clean not in seen:
            seen.add(clean)
            found.append(clean)
    return found


def extract_image_alts(body: str) -> list[str]:
    """Return Markdown image alt text; HTML/live rendering is out of scope."""
    return [alt.strip() for alt in re.findall(r"!\[([^\]]*)\]\([^)]*\)", body)]


def schema_draft_types(body: str) -> list[str]:
    """Extract declared JSON-LD types from a draft/schema comment block."""
    return sorted(set(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', body)))


def protected_spans(body: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for pattern in (
        r"(?ms)```.*?```",
        r"(?m)^>.*$",
        r"(?ms)(?m)^\|.*(?:\n\|.*)+",
        r"(?ms)<!--.*?-->",
    ):
        spans.extend((match.start(), match.end()) for match in re.finditer(pattern, body))
    return sorted(spans)


def overlaps_protected(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    return any(start < right and end > left for left, right in spans)


def mask_protected(body: str, spans: list[tuple[int, int]]) -> str:
    chars = list(body)
    for start, end in spans:
        for index in range(max(0, start), min(end, len(chars))):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return "".join(chars)


def content_words(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"\b[a-z][a-z0-9'-]*\b", text.lower())
        if len(word) > 1 and word not in EN_STOPWORDS
    }


def sentence_span(text: str, offset: int) -> tuple[int, int]:
    start = offset
    while start > 0 and text[start - 1] not in ".!?\n。！？":
        start -= 1
    end = offset
    while end < len(text) and text[end] not in ".!?\n。！？":
        end += 1
    return start, min(len(text), end + 1)


def intro_overlap(body: str, spans: list[tuple[int, int]]) -> tuple[float, int, str] | None:
    masked = mask_protected(body, spans)
    h1 = re.match(r"^#\s+[^\n]*\n?", body)
    start = h1.end() if h1 else 0
    first_h2 = re.search(r"(?m)^#{2,6}\s+[^\n]*\n?", body[start:])
    if not first_h2:
        return None
    intro = masked[start : start + first_h2.start()]
    section_start = start + first_h2.end()
    next_section = re.search(r"(?m)^#{1,2}\s+", body[section_start:])
    section_end = section_start + (next_section.start() if next_section else len(body) - section_start)
    section = masked[section_start:section_end]
    intro_words = content_words(intro)
    section_words = content_words(section)
    shared = intro_words & section_words
    if len(shared) < 5 or not intro_words or not section_words:
        return None
    ratio = len(shared) / len(intro_words | section_words)
    return ratio, section_start, ", ".join(sorted(shared)[:12])


def parallel_spec_tour(body: str, spans: list[tuple[int, int]]) -> list[str]:
    headings = [
        match
        for match in re.finditer(r"(?m)^(#{1,6})\s+(.+)$", body)
        if not overlaps_protected(match.start(), match.end(), spans)
    ]
    if any(TECH_REF_H2_RE.search(match.group(2)) for match in headings if len(match.group(1)) == 2):
        return []
    if any(TECH_H3_RE.search(match.group(2)) for match in headings if len(match.group(1)) == 3):
        return []
    run: list[str] = []
    for match in headings:
        if len(match.group(1)) == 3 and SPEC_H3_RE.match(match.group(2)):
            run.append(match.group(2).strip())
            continue
        if len(run) >= 4:
            return run
        run = []
    return run if len(run) >= 4 else []


def editorial_prose_checks(body: str) -> list[dict[str, Any]]:
    spans = protected_spans(body)
    overlap = intro_overlap(body, spans)
    overlap_failed = bool(overlap and overlap[0] >= INTRO_OVERLAP_THRESHOLD)

    behavior_evidence = ""
    for match in AUDIENCE_BEHAVIOR_RE.finditer(body):
        if overlaps_protected(match.start(), match.end(), spans):
            continue
        start, end = sentence_span(body, match.start())
        if AUDIENCE_ATTRIBUTION_RE.search(body[start:end]):
            continue
        behavior_evidence = body[start:end].strip()
        break

    roadmap = next(
        (
            match.group(0).strip()
            for match in ROADMAP_RE.finditer(body)
            if not overlaps_protected(match.start(), match.end(), spans)
        ),
        "",
    )
    spec_run = parallel_spec_tour(body, spans)

    return [
        check(
            "PROSE-03",
            "failed" if overlap_failed else "passed",
            "blocking",
            "human-editorial-gate",
            f"Intro/first-section lexical overlap={overlap[0]:.3f}; shared={overlap[2]}" if overlap else "No substantial intro/first-section overlap",
            "Keep the introduction as the frame and make the first headed section advance with new information",
        ),
        check(
            "PROSE-04",
            "failed" if behavior_evidence else "passed",
            "blocking",
            "human-editorial-gate",
            behavior_evidence or "No unsupported generalized buyer/shopper behavior claim found",
            "Add a traceable source and scope, or replace the behavior claim with a supported physical or operational constraint",
        ),
        check(
            "PROSE-05",
            "failed" if roadmap else "passed",
            "blocking",
            "human-editorial-gate",
            roadmap or "No article-roadmap or list-count announcement found",
            "Remove the structure announcement and let the argument reveal its sequence",
        ),
        check(
            "PROSE-06",
            "failed" if spec_run else "passed",
            "blocking",
            "human-editorial-gate",
            " | ".join(spec_run) if spec_run else "No mirrored four-or-more H3 spec tour found",
            "Fold the specs into the buyer decision or justify a true technical-reference layout",
        ),
    ]


def deterministic_prose_checks(body: str, blueprint: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Check only objective prose-contract violations; semantics remain expert-owned."""
    results: list[dict[str, Any]] = []
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", body) if item.strip() and not item.lstrip().startswith("#")]
    opening = paragraphs[0] if paragraphs else ""
    scene = re.search(
        r"\b(?:walk into (?:a|any|the) (?:store|shop|supermarket)|picture yourself|"
        r"imagine (?:walking|you are)|we (?:saw|noticed|found) (?:in|at) (?:a|the) store|"
        r"customers? (?:tell|told) us)\b",
        opening,
        re.IGNORECASE,
    )
    results.append(
        check(
            "PROSE-01",
            "failed" if scene else "passed",
            "blocking",
            "draft-deterministic",
            f"Unsupported generic scene opener: {scene.group(0)!r}" if scene else "No generic scene opener found in the first prose paragraph",
            "Supply a traceable experience source or replace the scene with a direct, evidence-bounded problem or decision",
        )
    )

    headings = [item.strip().lower() for item in re.findall(r"^##\s+(?!#)(.+?)\s*$", body, re.MULTILINE)]
    policy = blueprint.get("structure_policy", {}) if isinstance(blueprint, dict) else {}
    faq_present = any(item in {"faq", "frequently asked questions", "常见问题", "常见问题解答"} for item in headings)
    conclusion_present = any(item in {"conclusion", "summary", "结论", "总结"} for item in headings)
    faq_allowed = bool(blueprint and blueprint.get("faq_questions")) or str(policy.get("faq_policy", "")).lower() in {"required", "allowed", "include"}
    conclusion_allowed = str(policy.get("conclusion_policy", "")).lower() in {"required", "allowed", "include"}
    endcap_violations = []
    if faq_present and not faq_allowed:
        endcap_violations.append("FAQ is present but the Blueprint records no distinct FAQ need")
    if conclusion_present and not conclusion_allowed:
        endcap_violations.append("labeled Conclusion/Summary is present but the Blueprint does not require it")
    results.append(
        check(
            "PROSE-02",
            "failed" if endcap_violations else "passed",
            "blocking",
            "draft-deterministic",
            "; ".join(endcap_violations) if endcap_violations else "FAQ/Conclusion headings comply with the Blueprint structure policy",
            "Remove the undeclared template end-cap or return to Blueprint and document a distinct reader need",
        )
    )
    results.extend(editorial_prose_checks(body))
    return results


def citation_gaps(body: str) -> list[str]:
    gaps: list[str] = []
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", body) if item.strip()]
    for index, paragraph in enumerate(paragraphs, start=1):
        if CLAIM_RE.search(paragraph) and not CITATION_RE.search(paragraph):
            preview = re.sub(r"\s+", " ", paragraph)[:180]
            gaps.append(f"paragraph {index}: {preview}")
    return gaps[:10]


def blueprint_checks(
    blueprint_path: str | None,
    h1: list[str],
    h2: list[str],
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    if not blueprint_path:
        return [
            check(
                "SEO-06",
                "not_run",
                "blocking",
                "blueprint-verifier",
                "No --blueprint path supplied",
                "Run the Blueprint verifier with the approved SEO Blueprint JSON",
            ),
            check(
                "SEO-10",
                "not_run",
                "blocking",
                "blueprint-verifier",
                "Article type requires the approved Blueprint",
                "Run the Blueprint verifier before publication",
            ),
            check(
                "SEO-11",
                "not_run",
                "blocking",
                "blueprint-verifier",
                "Image requirements require the Blueprint",
                "Run the Blueprint verifier before publication",
            ),
            check(
                "SEO-12",
                "not_run",
                "blocking",
                "blueprint-verifier",
                "Schema plan requires the approved Blueprint",
                "Run the Blueprint verifier before publication",
            ),
        ], None

    path = Path(blueprint_path)
    try:
        blueprint = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        evidence = f"Blueprint could not be read: {exc}"
        return [
            check("SEO-06", "failed", "blocking", "blueprint-verifier", evidence, "Provide a valid SEO Blueprint JSON"),
            check("SEO-10", "not_run", "blocking", "blueprint-verifier", evidence, "Provide a valid SEO Blueprint JSON"),
            check("SEO-11", "not_run", "blocking", "blueprint-verifier", evidence, "Provide a valid SEO Blueprint JSON"),
            check("SEO-12", "not_run", "blocking", "blueprint-verifier", evidence, "Provide a valid SEO Blueprint JSON"),
        ], None

    suggested_h2_strings = [item.strip() for item in blueprint_h2s(blueprint)]
    actual_h2_strings = [item.strip() for item in h2]
    duplicate_h2s = sorted({item for item in actual_h2_strings if actual_h2_strings.count(item) > 1})
    h2_ok = bool(actual_h2_strings) and not duplicate_h2s
    h2_evidence = (
        f"Blueprint heading suggestions (non-binding): {suggested_h2_strings!r}; "
        f"article H2 sections: {actual_h2_strings!r}; duplicate H2s: {duplicate_h2s!r}. "
        "Semantic intent coverage is owned by the independent expert audit."
    )
    checks = [
        check(
            "SEO-06",
            "passed" if h2_ok else "failed",
            "blocking",
            "blueprint-verifier",
            h2_evidence,
            "Use a readable H2 hierarchy without duplicate headings; verify section-intent coverage in expert audit",
        ),
        check(
            "SEO-10",
            "passed" if blueprint.get("article_type") or blueprint.get("content_type") else "failed",
            "blocking",
            "blueprint-verifier",
            f"article_type={blueprint.get('article_type') or blueprint.get('content_type') or 'not declared'}",
            "Declare the article type in the Blueprint",
        ),
    ]
    schema_plan = blueprint.get("schema_type") or blueprint.get("schema_types") or blueprint.get("schema")
    checks.append(
        check(
            "SEO-12",
            "passed" if schema_plan else "failed",
            "blocking",
            "blueprint-verifier",
            f"Schema plan: {schema_plan or 'not declared'}",
            "Declare the expected Article/BlogPosting schema in the Blueprint",
        )
    )
    image_plan = (
        blueprint.get("image_plan")
        or blueprint.get("image_requirements")
        or blueprint.get("images")
        or blueprint.get("required_images")
    )
    thumbnail_planned = isinstance(image_plan, list) and any(
        isinstance(item, dict)
        and str(item.get("role", "")).strip().lower() in {"thumbnail", "hero", "thumbnail/hero", "featured image"}
        for item in image_plan
    )
    checks.append(
        check(
            "IMG-01",
            "passed" if thumbnail_planned else "failed",
            "blocking",
            "blueprint-verifier",
            f"Required thumbnail/hero image plan declared: {thumbnail_planned}",
            "Add an executable thumbnail/hero entry to image_plan" if not thumbnail_planned else "",
        )
    )
    return checks, blueprint


def run(filepath: str, keyword_override: str | None = None, blueprint_path: str | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    path = Path(filepath)
    if not path.exists():
        checks.append(check("SEO-14", "failed", "blocking", "draft-deterministic", "File not found", "Provide an article Markdown file"))
        return build_report(path, checks, None)

    try:
        content = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
    except (OSError, UnicodeError, DocumentError) as exc:
        checks.append(check("SEO-14", "failed", "blocking", "draft-deterministic", str(exc), "Fix the Markdown/frontmatter structure"))
        return build_report(path, checks, None)

    body_tokens = tokens(body)
    format_issues: list[str] = []
    if not body_tokens:
        format_issues.append("article body is empty")
    if "{{" in content or "}}" in content:
        format_issues.append("unresolved template placeholder found")
    checks.append(
        check(
            "SEO-14",
            "failed" if format_issues else "passed",
            "blocking",
            "draft-deterministic",
            "; ".join(format_issues) if format_issues else f"Article body parsed with {len(body_tokens)} words",
            "Remove unresolved placeholders and provide a complete article body",
        )
    )

    missing = [field for field in REQUIRED_FIELDS if not has_value(fm.get(field))]
    retired = sorted(RETIRED_FIELDS.intersection(fm.keys()))
    frontmatter_issues: list[str] = []
    allowed_sites = {"armorlighting.com", "armordigitalscreen.com"}
    site = fm.get("site")
    if site not in allowed_sites:
        frontmatter_issues.append("site must be armorlighting.com or armordigitalscreen.com")
    if not isinstance(fm.get("labels"), str):
        frontmatter_issues.append("labels must be a comma-separated string")
    if not isinstance(fm.get("tags"), list) or not fm.get("tags"):
        frontmatter_issues.append("tags must be a non-empty YAML array")
    tag_values = [str(item).strip() for item in fm.get("tags", []) if str(item).strip()] if isinstance(fm.get("tags"), list) else []
    labels_values = [item.strip() for item in str(fm.get("labels", "")).split(",") if item.strip()] if isinstance(fm.get("labels"), str) else []
    spaced_tag_values = [item for item in tag_values if re.search(r"\s", item)]
    spaced_label_values = [item for item in labels_values if re.search(r"\s", item)]
    if spaced_tag_values:
        frontmatter_issues.append(
            "tags values must not contain whitespace; use kebab-case for multi-word tags "
            f"(for example store-lighting): {', '.join(spaced_tag_values)}"
        )
    if spaced_label_values:
        frontmatter_issues.append(
            "labels values must not contain whitespace; use the same kebab-case values as tags "
            f"(for example store-lighting): {', '.join(spaced_label_values)}"
        )
    if isinstance(fm.get("labels"), str) and isinstance(fm.get("tags"), list):
        label_values = [item.strip() for item in fm["labels"].split(",") if item.strip()]
        if label_values != tag_values:
            frontmatter_issues.append("labels and tags must contain the same values in the same order")
    expected_author = {
        "armorlighting.com": "ARMOR Lighting",
        "armordigitalscreen.com": "ARMOR Digital Screen",
    }.get(str(site))
    if expected_author and fm.get("author") != expected_author:
        frontmatter_issues.append(f"author must be {expected_author!r} for the selected site")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm.get("date", ""))):
        frontmatter_issues.append("date must use YYYY-MM-DD")
    permalink = fm.get("permalink")
    if not isinstance(permalink, str) or not permalink.startswith("/") or permalink.startswith("/blog/"):
        frontmatter_issues.append("permalink must be a root-relative path and must not start with /blog/")
    thumbnail_prompt = fm.get("thumbnail_prompt")
    if not isinstance(thumbnail_prompt, str) or not thumbnail_prompt.strip() or thumbnail_prompt.strip().upper() == "NOT_REQUIRED":
        frontmatter_issues.append("thumbnail_prompt must contain an executable thumbnail brief and must not be NOT_REQUIRED")
    for field in ("thumbnail_prompt", "images_prompt"):
        value = fm.get(field)
        if isinstance(value, str) and value != "NOT_REQUIRED" and "negative:" in value.lower():
            frontmatter_issues.append(f"{field} must use natural-language Without exclusions, not negative:")
    canonical_url = fm.get("canonical_url")
    if canonical_url:
        parsed_canonical = urlparse(str(canonical_url))
        expected_host = {
            "armorlighting.com": {"armorlighting.com", "www.armorlighting.com"},
            "armordigitalscreen.com": {"armordigitalscreen.com", "www.armordigitalscreen.com"},
        }.get(str(site), set())
        if parsed_canonical.scheme != "https" or parsed_canonical.netloc.lower() not in expected_host:
            frontmatter_issues.append("canonical_url must be an HTTPS URL on the selected ARMOR site")
    governance_block = "# Governance (V7." in content
    if missing or retired or governance_block or frontmatter_issues:
        evidence = []
        if missing:
            evidence.append(f"missing required fields: {', '.join(missing)}")
        if retired:
            evidence.append(f"retired fields: {', '.join(retired)}")
        if governance_block:
            evidence.append("retired Governance block present")
        evidence.extend(frontmatter_issues)
        checks.append(check("SEO-13", "failed", "blocking", "draft-deterministic", "; ".join(evidence), "Align frontmatter with the current ARMOR article format"))
    else:
        checks.append(check("SEO-13", "passed", "blocking", "draft-deterministic", "Required article fields are present and no retired fields were found"))

    keyword = keyword_override or str(fm.get("seo_keywords", "")).split(",")[0].strip()
    title = str(fm.get("seo_title", "")).strip()
    title_issues: list[str] = []
    if not title:
        title_issues.append("seo_title is empty")
    elif len(title) > 60:
        title_issues.append(f"seo_title is {len(title)} characters; maximum is 60")
    checks.append(
        check(
            "SEO-01",
            "failed" if title_issues else "passed",
            "blocking",
            "draft-deterministic",
            "; ".join(title_issues) if title_issues else f"seo_title length={len(title)}",
            "Add a unique SEO title and keep it under 60 characters",
        )
    )

    keyword_issues: list[str] = []
    if not keyword:
        keyword_issues.append("primary keyword is not set")
    elif title and not contains_phrase(title, keyword):
        keyword_issues.append(f"primary keyword '{keyword}' is not present in seo_title")
    checks.append(
        check(
            "SEO-03",
            "failed" if keyword_issues else "passed",
            "blocking",
            "draft-deterministic",
            "; ".join(keyword_issues) if keyword_issues else f"Primary keyword={keyword!r} is present in seo_title",
            "Set a primary keyword and include it naturally in the SEO title",
        )
    )

    doc_title = str(fm.get("title", "")).strip()
    checks.extend(title_value_checks(doc_title, title))

    description = str(fm.get("seo_description", "")).strip()
    desc_ok = bool(description) and 120 <= len(description) <= 170
    checks.append(
        check(
            "SEO-02",
            "passed" if desc_ok else "failed",
            "blocking",
            "draft-deterministic",
            f"seo_description length={len(description)}; accepted range is 120-170",
            "Add a 120-170 character SEO description with a truthful value proposition and CTA",
        )
    )

    h1, h2 = extract_headings(body)
    if len(h1) == 1:
        checks.append(check("SEO-04", "passed", "blocking", "draft-deterministic", "Exactly one H1 found"))
    else:
        checks.append(check("SEO-04", "failed", "blocking", "draft-deterministic", f"Found {len(h1)} H1 headings", "Use exactly one H1 heading"))

    first_100 = " ".join(tokens(body)[:100])
    first_ok = bool(keyword) and contains_phrase(first_100, keyword)
    checks.append(
        check(
            "SEO-05",
            "passed" if first_ok else "warning",
            "non_blocking",
            "draft-deterministic",
            f"Primary keyword in first 100 words: {first_ok}",
            "Place the primary keyword or a natural variant in the opening section",
        )
    )

    density = 0.0
    if keyword and body_tokens:
        density = phrase_token_count(body, keyword) / len(body_tokens) * 100
    density_result = "failed" if density > 3.5 else ("warning" if density == 0 else "passed")
    checks.append(
        check(
            "SEO-07",
            density_result,
            "blocking" if density > 3.5 else "non_blocking",
            "draft-deterministic",
            f"Token-aware keyword density={density:.2f}% (diagnostic range 0.5-3.5%)",
            "Reduce repeated primary-keyword phrasing; density is diagnostic below the stuffing threshold",
        )
    )

    urls = extract_internal_urls(body)
    checks.append(
        check(
            "SEO-08",
            "passed" if len(urls) >= 2 else "warning",
            "non_blocking",
            "link-verifier",
            f"Unique ARMOR internal URLs found: {len(urls)}; network liveness not checked",
            "Add relevant verified internal URLs. Run the separate link verifier before save",
        )
    )

    gaps = citation_gaps(body)
    checks.append(
        check(
            "SEO-09",
            "warning" if gaps else "passed",
            "non_blocking",
            "claim-verifier",
            "; ".join(gaps) if gaps else "No obvious uncited quantitative/authority claims detected",
            "Add a source link or remove/qualify the claim",
        )
    )

    blueprint_results, blueprint = blueprint_checks(blueprint_path, h1, h2)
    if blueprint:
        expected_h1 = blueprint_h1(blueprint)
        if expected_h1:
            h1_check = next(item for item in checks if item["id"] == "SEO-04")
            h1_matches = len(h1) == 1 and (
                h1[0].strip().lower() == str(expected_h1).strip().lower()
                or contains_phrase(h1[0], str(expected_h1))
            )
            h1_check["result"] = "passed" if h1_matches else "failed"
            h1_check["severity"] = "blocking"
            h1_check["evidence"] = f"Blueprint H1={expected_h1!r}; article H1={h1[0] if h1 else 'missing'!r}"
            h1_check["remediation"] = "Regenerate the Blueprint or rewrite the article H1 to match the locked structure"
        primary_blueprint_keyword = str(blueprint.get("primary_keyword", "")).strip()
        if primary_blueprint_keyword:
            keyword_check = next(item for item in checks if item["id"] == "SEO-03")
            keyword_matches = keyword.lower() == primary_blueprint_keyword.lower()
            keyword_check["result"] = "passed" if keyword_matches else "failed"
            keyword_check["severity"] = "blocking"
            keyword_check["evidence"] = f"Blueprint primary_keyword={primary_blueprint_keyword!r}; article primary_keyword={keyword!r}"
            keyword_check["remediation"] = "Use the primary keyword locked in the Blueprint"

        if blueprint.get("article_type") or blueprint.get("content_type"):
            article_type = blueprint.get("article_type") or blueprint.get("content_type")
            blueprint_results = [
                item for item in blueprint_results if item["id"] != "SEO-10"
            ] + [
                check("SEO-10", "passed", "blocking", "blueprint-verifier", f"article_type={article_type}")
            ]

    checks.extend(blueprint_results)

    if not h2:
        h2_check = next((item for item in checks if item["id"] == "SEO-06"), None)
        if h2_check is None:
            checks.append(check("SEO-06", "failed", "blocking", "draft-deterministic", "No H2 headings found", "Add semantic H2 sections that advance the reader decision"))
        else:
            h2_check["result"] = "failed"
            h2_check["severity"] = "blocking"
            h2_check["evidence"] = "No H2 headings found"
            h2_check["remediation"] = "Add semantic H2 sections that advance the reader decision"

    checks.extend(deterministic_prose_checks(body, blueprint))

    image_alts = extract_image_alts(body)
    image_missing_alt = any(not alt for alt in image_alts)
    checks = [item for item in checks if item["id"] not in {"SEO-11", "SEO-12"}]
    image_check = check(
        "SEO-11",
        "failed" if image_missing_alt else ("passed" if image_alts else "not_applicable"),
        "blocking" if image_missing_alt else ("non_blocking" if image_alts else "informational"),
        "draft-deterministic",
        f"Markdown images={len(image_alts)}; empty Alt text={image_missing_alt}",
        "Add descriptive Alt text to every Markdown image",
    )
    checks.append(image_check)

    schema_types = schema_draft_types(body)
    planned_schema = blueprint.get("schema_type") if blueprint else None
    schema_ok = bool(planned_schema) and bool(schema_types) and str(planned_schema) in schema_types
    checks.append(
        check(
            "SEO-12",
            "passed" if schema_ok else ("not_run" if not blueprint else "failed"),
            "blocking",
            "draft-deterministic",
            f"Planned schema={planned_schema or 'not declared'}; draft schema types={schema_types or 'none'}",
            "Add a Schema Draft matching the Blueprint; rendered JSON-LD is checked only at Live URL Gate",
        )
    )
    return build_report(path, checks, {"keyword": keyword, "word_count": len(body_tokens), "internal_urls": urls})


def build_report(path: Path, checks: list[dict[str, Any]], metrics: dict[str, Any] | None) -> dict[str, Any]:
    structural = [
        item for item in checks
        if item["id"].startswith("PROSE-") and item["result"] == "failed"
    ]
    blocking = [
        item
        for item in checks
        if item["severity"] == "blocking" and item["result"] in {"failed", "not_run"}
    ]
    unresolved = [item for item in checks if item["result"] in {"failed", "warning", "not_run"} and item["severity"] != "informational"]
    status = "STRUCTURE_FAILED" if structural else ("BLOCKED" if blocking else ("NEEDS_REVISION" if unresolved else "PASS"))
    return {
        "status": status,
        "article_path": str(path.resolve()),
        "checks": checks,
        "metrics": metrics or {},
        "next_action": "save" if status == "PASS" else ("full_structural_rewrite_or_blueprint_return" if status == "STRUCTURE_FAILED" else ("revise" if status == "NEEDS_REVISION" else "escalate")),
        "limitations": [
            "This is a draft deterministic gate; it does not fetch URLs or validate rendered JSON-LD.",
            "GEO expert review, Blueprint semantics, and Live URL checks remain separate gates.",
        ],
    }


def human_report(report: dict[str, Any]) -> str:
    lines = ["ARMOR ARTICLE DRAFT CHECK", f"Status: {report['status']}"]
    for item in report["checks"]:
        lines.append(f"{item['id']}: {item['result']} [{item['severity']}] — {item['evidence']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="ARMOR deterministic article draft gate")
    parser.add_argument("filepath", help="Path to article Markdown draft")
    parser.add_argument("-k", "--keyword", default=None, help="Override primary keyword")
    parser.add_argument("--blueprint", default=None, help="Locked SEO Blueprint JSON; required for deterministic gate PASS")
    parser.add_argument("--json", action="store_true", help="Emit only the JSON gate report")
    args = parser.parse_args()
    report = run(args.filepath, args.keyword, args.blueprint)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(human_report(report), file=sys.stderr)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
