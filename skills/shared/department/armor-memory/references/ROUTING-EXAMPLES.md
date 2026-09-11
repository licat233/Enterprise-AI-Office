# Routing Examples

These examples illustrate current ARMOR Minimal Stable behavior. Directory location represents operational purpose, not lifecycle state.

## Website article

User request:

> 帮我写一篇 ARMOR 官网磁吸货架灯文章。

Classification:

```yaml
object: work-product
domain: website
artifact: article
project: null
```

Expected path:

```text
02-Projects/Workspaces/Website/Articles/
```

If a project is supplied, the project value is validated but the article still uses this one stable channel-content home. Publishing the article does not move its editable source file.

## Social copy

User request:

> 写三条 LinkedIn 社媒文案。

Classification:

```yaml
object: work-product
domain: marketing
artifact: social-copy
project: null
```

Expected path:

```text
02-Projects/Workspaces/Marketing/Social-Media/
```

Official social content keeps this one stable content home whether or not a project is supplied.

## Published snapshot

User request:

> 保存这个已经发布页面的快照。

Classification:

```yaml
object: record
record_type: published
```

Expected path:

```text
03-Records/Published/
```

A published snapshot is evidence of what was actually published. It is separate from the editable work-product source.

## Named-project content case study

User request:

> 为 Q4 内容项目写一个 case study。

Classification:

```yaml
object: work-product
domain: content
artifact: case-study
project: q4-content
```

Expected path:

```text
02-Projects/Projects/q4-content/Content/Case-Studies/
```

Project completion does not move this tree.

## Product manual without project

User request:

> 给磁吸货架灯产品写一份安装手册。

Classification:

```yaml
object: work-product
domain: products
artifact: product-manual
entity: magnetic-shelf-light
```

Expected path:

```text
02-Projects/Workspaces/Products/magnetic-shelf-light/Documentation/
```

## Product manual with project

Classification:

```yaml
object: work-product
domain: products
artifact: product-manual
entity: magnetic-shelf-light
project: manual-refresh
```

Expected path:

```text
02-Projects/Projects/manual-refresh/Products/magnetic-shelf-light/Documentation/
```

## Marketing campaign

Classification:

```yaml
object: work-product
domain: marketing
artifact: campaign
```

Expected path:

```text
02-Projects/Workspaces/Marketing/Campaigns/
```

## Operations checklist

Classification:

```yaml
object: work-product
domain: operations
artifact: checklist
```

Expected path:

```text
02-Projects/Workspaces/Operations/Checklists/
```

## Meeting record

Classification:

```yaml
object: record
record_type: meeting
```

Expected path:

```text
03-Records/Meetings/
```

## Journal entry

Classification:

```yaml
object: record
record_type: journal
year: "2026"
```

Expected path:

```text
03-Records/Journal/2026/
```

## Product knowledge

Classification:

```yaml
object: knowledge
knowledge_type: product
```

Expected path:

```text
01-Knowledge/Products/
```

## Brand knowledge

Classification:

```yaml
object: knowledge
knowledge_type: brand
```

Expected path:

```text
01-Knowledge/Brand/
```

## Reusable rule

Classification:

```yaml
object: knowledge
knowledge_type: rule
```

Expected path:

```text
01-Knowledge/Rules/
```

## Research source

Classification:

```yaml
object: research
research_kind: source
```

Expected path:

```text
04-Research/Sources/
```

## Explicit unresolved input

Classification:

```yaml
object: unresolved
```

Expected path:

```text
90-Inbox/
```

Once the user later supplies enough information to classify an Inbox item, the Agent should re-route and move it in the same task rather than leaving manual cleanup to the human.
