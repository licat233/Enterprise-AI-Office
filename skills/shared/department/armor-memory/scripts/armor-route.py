#!/usr/bin/env python3
"""Deterministic path mapper for ARMOR Minimal Stable."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass


OBJECT_CHOICES = ("work-product", "record", "knowledge", "research", "unresolved")
DOMAIN_CHOICES = ("website", "content", "marketing", "products", "operations")
ARTIFACT_CHOICES = (
    "article",
    "landing-page",
    "case-study",
    "blog-post",
    "report",
    "campaign",
    "email-sequence",
    "social-copy",
    "product-manual",
    "spec-sheet",
    "price-list",
    "process-doc",
    "checklist",
    "internal-report",
)
RECORD_TYPE_CHOICES = ("meeting", "email", "conversation", "journal", "feedback", "published")
KNOWLEDGE_TYPE_CHOICES = ("company", "brand", "product", "customer", "rule", "insight")
RESEARCH_KIND_CHOICES = ("source", "note")

FORBIDDEN_NAME_PATTERN = re.compile(r"[\\/;&|<>$`!]")
SEPARATOR_PATTERN = re.compile(r"[\s_]+")
HYPHEN_PATTERN = re.compile(r"-+")

WORK_PRODUCT_ROUTES = {
    ("website", "landing-page"): ("Website/Landing-Pages", "Website/Landing-Pages"),
    ("website", "case-study"): ("Website/Case-Studies", "Content/Case-Studies"),
    ("content", "blog-post"): ("Content/Blog-Posts", "Content/Blog-Posts"),
    ("content", "report"): ("Content/Reports", "Content/Reports"),
    ("content", "case-study"): ("Content/Case-Studies", "Content/Case-Studies"),
    ("marketing", "campaign"): ("Marketing/Campaigns", "Marketing/Campaigns"),
    ("marketing", "email-sequence"): ("Marketing/Email-Sequences", "Marketing/Email-Sequences"),
    ("operations", "process-doc"): ("Operations/Process-Docs", "Operations/Process-Docs"),
    ("operations", "checklist"): ("Operations/Checklists", "Operations/Checklists"),
    ("operations", "internal-report"): ("Operations/Internal-Reports", "Operations/Internal-Reports"),
}

KNOWLEDGE_ROUTES = {
    "company": "01-Knowledge/Company/",
    "brand": "01-Knowledge/Brand/",
    "product": "01-Knowledge/Products/",
    "customer": "01-Knowledge/Customers/",
    "rule": "01-Knowledge/Rules/",
    "insight": "01-Knowledge/Insights/",
}

RECORD_ROUTES = {
    "meeting": "03-Records/Meetings/",
    "email": "03-Records/Emails/",
    "conversation": "03-Records/Conversations/",
    "feedback": "03-Records/Feedback/",
    "published": "03-Records/Published/",
}

RESEARCH_ROUTES = {
    "source": "04-Research/Sources/",
    "note": "04-Research/Notes/",
}


@dataclass(frozen=True)
class RouteResult:
    path: str
    category: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {"path": self.path, "category": self.category, "reason": self.reason}


def slugify_name(value: str) -> str:
    """Normalize names with NFKC, lowercase, and hyphen separators."""
    normalized = unicodedata.normalize("NFKC", value).strip()
    if not normalized:
        raise ValueError("name must not be empty")
    if normalized in {".", ".."} or ".." in normalized:
        raise ValueError("name must not contain path traversal")
    if normalized.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", normalized):
        raise ValueError("name must not be an absolute path")
    if FORBIDDEN_NAME_PATTERN.search(normalized):
        raise ValueError("name contains forbidden characters")

    slug = normalized.lower()
    slug = SEPARATOR_PATTERN.sub("-", slug)
    slug = HYPHEN_PATTERN.sub("-", slug).strip("-")
    if not slug:
        raise ValueError("name must not be empty after normalization")
    return slug


def build_work_product_path(domain: str, artifact: str, project: str | None, entity: str | None) -> str:
    # Channel content has one lifecycle-neutral home. A supplied project is
    # validated for safety/context but does not change the stable destination.
    if domain == "website" and artifact == "article":
        if project:
            slugify_name(project)
        return "02-Projects/Workspaces/Website/Articles/"

    if domain == "marketing" and artifact == "social-copy":
        if project:
            slugify_name(project)
        return "02-Projects/Workspaces/Marketing/Social-Media/"

    if domain == "products":
        if artifact == "product-manual":
            if not entity:
                raise ValueError("entity is required for products/product-manual")
            entity_slug = slugify_name(entity)
            if project:
                project_slug = slugify_name(project)
                return f"02-Projects/Projects/{project_slug}/Products/{entity_slug}/Documentation/"
            return f"02-Projects/Workspaces/Products/{entity_slug}/Documentation/"
        if artifact == "spec-sheet":
            if not entity:
                raise ValueError("entity is required for products/spec-sheet")
            entity_slug = slugify_name(entity)
            if project:
                project_slug = slugify_name(project)
                return f"02-Projects/Projects/{project_slug}/Products/{entity_slug}/Spec-Sheets/"
            return f"02-Projects/Workspaces/Products/{entity_slug}/Spec-Sheets/"
        if artifact == "price-list":
            if not entity:
                raise ValueError("entity is required for products/price-list")
            entity_slug = slugify_name(entity)
            if project:
                project_slug = slugify_name(project)
                return f"02-Projects/Projects/{project_slug}/Products/{entity_slug}/Price-Lists/"
            return f"02-Projects/Workspaces/Products/{entity_slug}/Price-Lists/"
        raise ValueError(f"artifact {artifact!r} is not supported for domain {domain!r}")

    route = WORK_PRODUCT_ROUTES.get((domain, artifact))
    if route is None:
        raise ValueError(f"artifact {artifact!r} is not supported for domain {domain!r}")

    workspace_tail, project_tail = route
    if project:
        project_slug = slugify_name(project)
        return f"02-Projects/Projects/{project_slug}/{project_tail}/"
    return f"02-Projects/Workspaces/{workspace_tail}/"


def route_request(
    *,
    object_type: str,
    domain: str | None = None,
    artifact: str | None = None,
    record_type: str | None = None,
    knowledge_type: str | None = None,
    research_kind: str | None = None,
    project: str | None = None,
    entity: str | None = None,
    year: str | None = None,
) -> RouteResult:
    if object_type == "work-product":
        if domain is None:
            raise ValueError("domain is required for work-product")
        if artifact is None:
            raise ValueError("artifact is required for work-product")
        path = build_work_product_path(domain, artifact, project, entity)
        return RouteResult(path=path, category="work-product", reason="deterministic work-product mapping")

    if object_type == "record":
        if record_type is None:
            raise ValueError("record_type is required for record")
        if record_type == "journal":
            if year is None:
                raise ValueError("year is required for journal records")
            if not re.fullmatch(r"\d{4}", year):
                raise ValueError("year must be a four-digit value")
            return RouteResult(
                path=f"03-Records/Journal/{year}/",
                category="record",
                reason="deterministic record mapping",
            )
        return RouteResult(
            path=RECORD_ROUTES[record_type],
            category="record",
            reason="deterministic record mapping",
        )

    if object_type == "knowledge":
        if knowledge_type is None:
            raise ValueError("knowledge_type is required for knowledge")
        return RouteResult(
            path=KNOWLEDGE_ROUTES[knowledge_type],
            category="knowledge",
            reason="deterministic knowledge mapping",
        )

    if object_type == "research":
        if research_kind is None:
            raise ValueError("research_kind is required for research")
        return RouteResult(
            path=RESEARCH_ROUTES[research_kind],
            category="research",
            reason="deterministic research mapping",
        )

    if object_type == "unresolved":
        return RouteResult(path="90-Inbox/", category="unresolved", reason="explicit unresolved routing")

    raise ValueError(f"unsupported object type: {object_type}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic router for ARMOR Minimal Stable.")
    parser.add_argument("--object", dest="object_type", required=True, choices=OBJECT_CHOICES)
    parser.add_argument("--domain", choices=DOMAIN_CHOICES)
    parser.add_argument("--artifact", choices=ARTIFACT_CHOICES)
    parser.add_argument("--record-type", choices=RECORD_TYPE_CHOICES)
    parser.add_argument("--knowledge-type", choices=KNOWLEDGE_TYPE_CHOICES)
    parser.add_argument("--research-kind", choices=RESEARCH_KIND_CHOICES)
    parser.add_argument("--project")
    parser.add_argument("--entity")
    parser.add_argument("--year")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.object_type == "work-product":
        if args.domain is None:
            parser.error("--domain is required when --object work-product")
        if args.artifact is None:
            parser.error("--artifact is required when --object work-product")
        if args.record_type or args.knowledge_type or args.research_kind or args.year:
            parser.error("record, knowledge, research, and year fields are not allowed for work-product")
    elif args.object_type == "record":
        if args.record_type is None:
            parser.error("--record-type is required when --object record")
        if args.domain or args.artifact or args.knowledge_type or args.research_kind or args.project or args.entity:
            parser.error("domain, artifact, knowledge, research, project, and entity fields are not allowed for record")
        if args.record_type == "journal" and args.year is None:
            parser.error("--year is required when --object record --record-type journal")
        if args.record_type != "journal" and args.year is not None:
            parser.error("--year is only allowed for journal records")
    elif args.object_type == "knowledge":
        if args.knowledge_type is None:
            parser.error("--knowledge-type is required when --object knowledge")
        if args.domain or args.artifact or args.record_type or args.research_kind or args.project or args.entity or args.year:
            parser.error("domain, artifact, record, research, project, entity, and year fields are not allowed for knowledge")
    elif args.object_type == "research":
        if args.research_kind is None:
            parser.error("--research-kind is required when --object research")
        if args.domain or args.artifact or args.record_type or args.knowledge_type or args.project or args.entity or args.year:
            parser.error("domain, artifact, record, knowledge, project, entity, and year fields are not allowed for research")
    elif args.object_type == "unresolved":
        if any(
            value is not None
            for value in (
                args.domain,
                args.artifact,
                args.record_type,
                args.knowledge_type,
                args.research_kind,
                args.project,
                args.entity,
                args.year,
            )
        ):
            parser.error("no additional routing fields are allowed when --object unresolved")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(parser, args)
    try:
        result = route_request(
            object_type=args.object_type,
            domain=args.domain,
            artifact=args.artifact,
            record_type=args.record_type,
            knowledge_type=args.knowledge_type,
            research_kind=args.research_kind,
            project=args.project,
            entity=args.entity,
            year=args.year,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result.as_dict(), ensure_ascii=True, indent=2))
    else:
        print(result.path)
        print(result.category)
        print(result.reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
