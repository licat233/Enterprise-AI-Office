---
name: mic-product-fill
description: Generate paste-ready product upload text for the Made-in-China Bulk Fill Chrome extension. Use when the user wants an AI/Hermes agent to turn product specs, catalog copy, supplier notes, spreadsheets, PDFs, images, or rough product descriptions into the exact `字段名：内容` format that can be pasted into the Made-in-China product upload autofill plugin.
version: 1.1.1
---

# Made-in-China Bulk Fill Text

Use the Product Knowledge Base and current ARMOR facts before turning product
facts into customer-facing MIC copy. This skill owns the exact paste-ready
field format, claims boundary, and buyer intent checks.

## Source of Truth

- Long-term memory: `{VAULT}/`
- Default output: use the current router for a MIC product upload package:
  `route.sh --object work-product --domain products --artifact product-manual --entity mic-product --project mic-ops --json`
- ARMOR product lookup CSV: `{VAULT}/01-Knowledge/Products/ARMOR_Product_Knowledge_Base.csv`

Do not use legacy external work folders for MIC product facts. If the current ARMOR Vault and Product KB CSV do not confirm a claim, omit the field, mark it `[TO CONFIRM]` in the `.md` reference file, or ask the user.

## Output Contract

Produce plain text only, using one field per line.

The Chrome extension expects Chinese field names. Do not output Markdown tables, JSON, bullets, explanations, or code fences unless the user explicitly asks for them.

**CRITICAL: File output rule for ARMOR Vault users**

When saving a routed MIC product upload package, ALWAYS create TWO files in the same router-returned folder:

1. **`.md` file** — Markdown format with tables, headers, and structured data for Obsidian reading
2. **`.txt` file** — Raw paste-ready plain text for the Chrome extension

Example folder structure:
```
Router result: `02-Projects/Active/mic-ops/Products/mic-product/Documentation/`
├── MIC-BulkFill-Input.md    ← Markdown version for Obsidian
└── MIC-BulkFill-Input.txt   ← Raw paste format for Chrome extension
```

The `.md` file should include:
- YAML frontmatter with product name and date
- Markdown tables for structured data (attributes, pricing, FAQ)
- A code block at the bottom containing the raw paste-ready text

The `.txt` file should contain ONLY the raw paste-ready text with `# 板块名` section headers.

Use semicolons for list fields:

```text
关键词：Full Color ESL; LCD Price Tag; Inventory Management Display
支付方式：L/C; T/T; Paypal
```

Keep values concise enough for product form inputs. Preserve English product-facing copy for Made-in-China listings unless the user asks for Chinese.

### Text Format Specification

The paste-ready text contains **only two types of lines**. The plugin has **no comment syntax** — every line is either a section header or a field-value pair.

**Line type 1 — Section header:**
```text
# 板块名
```
A line starting with `#` marks the beginning of a new section. The plugin's `parseBulkText()` strips the `#` prefix and uses the rest as the section name. Section names must match one of the 14 recognized section names listed in Supported Fields. The section name determines which DOM region on the Made-in-China page receives the fields that follow.

**Line type 2 — Field-value pair:**
```text
字段名：内容
```
A line matching the pattern `字段名：内容` (or `字段名:内容`) is parsed as a key-value entry. The key is everything before the first `：` or `:`, the value is everything after. The entry is associated with the most recent section header.

**Empty lines** are ignored by the parser.

**Forbidden line types:**
- Do NOT add descriptive text, explanations, or annotations as standalone lines — they will be misinterpreted as malformed field entries or corrupt the current section context.
- Do NOT add `# -- comment` style lines — any line starting with `#` is parsed as a section header, not a comment. Adding `# -- 一口价销售：适合…` creates a phantom section that overrides the real section name.
- Do NOT add `# 产品详情` — this section must be edited manually in the product details editor page (see Plugin Limitations).

**Section order must follow page visual order** because the Chrome extension uses section headings to scope field matching to the corresponding Made-in-China DOM region.

## Plugin Limitations

The following fields **cannot** be auto-filled by the plugin and require manual handling:

- **产品展示** — Image/video upload. Max 6 images + 1 video/GIF. Not supported by the plugin. Do not output `# 产品展示` in the paste-ready text.
- **运费信息** — Destination region (`region4estimate`) selector only. The freight template is auto-selected to the default recommended option. Omit this section if no fields are fillable.
- **产品详情** — Rich text editor with module-based layout. The Chrome extension skips this section because it must be edited in the separate product details editor page. Do not include `# 产品详情` in the raw paste-ready `.txt` file; put any suggested detail copy only in the readable `.md` file as manual reference.

## Core Workflow
0. **GET THE EDIT PAGE EXTRACTION FIRST (hard rule, user-confirmed 2026-08-13):** standard
   properties on the product edit page are authoritative and may differ from this skill's
   templates (category, product type, and even the same category over time). The MIC template
   standard attributes and the edit page standard attributes are NOT guaranteed to match.
   - If the user provides the extractor-plugin JSON (schema `mic-product-edit-context/v1`,
     see `mic-upload-data-sources/references/mic-edit-context-plugin.md`), generate ALL
     `# 产品属性` fields from `fieldOrigin: mic_standard_property` + `mic_builtin_property`
     + existing custom pairs in that JSON. Templates below are fallback only.
   - **Field names: use each field's `bulkFillFieldName` (NOT `fieldName`) when writing
     paste-ready text** — `fieldName` is the page slot name (e.g. `规格1值1`), while
     `bulkFillFieldName` is the name the Bulk Fill parser accepts (e.g. `规格值`).
   - If no extraction exists, ask the user to run the extractor extension first (preferred),
     or fall back to the templates below with the explicit caveat that fields may not match
     the real page.
1. **Identify product type and load field mapping.** Load `references/product-type-field-mapping.md` to get the full section + field checklist for this product type (LED Rigid Bar, Low Temp, Magnetic, ESL, Neon, Custom Sign). Then load `references/category-standard-attributes.md` for the exact MIC category's standard attribute options. If the product type or category is missing, investigate the MIC product upload page, then add the results to the reference files for future reuse. **These references are historical caches, NOT authoritative — the edit-page extraction (step 0) wins on any conflict.**
2. Extract all available product facts from the user's source material.
3. Normalize facts into the supported field names below.
4. Infer reasonable marketing copy only when the source clearly supports it.
5. **Pricing determination** (FOB价格设置):
   - If the source provides price, MOQ, or stock → use those values directly.
   - If the source has no pricing → search MIC (Made-in-China.com) and other B2B e-commerce platforms for comparable products to establish a reference price range.
   - If no reference pricing can be found → ask the user before filling any price fields. Never fabricate prices.
6. Leave unknown fields (other than price) out instead of fabricating precise values such as stock, dimensions, HS code, weight, certification, or warranty.
7. Return the paste-ready text block.

## Plan-Verify Workflow (Mandatory)

Every product info generation MUST follow this three-phase workflow. Do NOT skip phases.

### Phase 1: Plan (Before Writing)

Before writing any content, produce a **field checklist** listing every section and field to be filled. Present it to the user or keep it as an internal reference.

Template:

    Field Checklist - [Product Name]

    Sections to fill:
    - [ ] # 基本信息 (5 fields: 产品名称, 中心词, 关键词, 产品分组, 产品型号)
    - [ ] # 产品亮点 (10 fields: 产品亮点1-10)
    - [ ] # 产品属性 (9 required standard + N custom)
      Required: 认证, 功率, 发光颜色, 电压, 防护等级, 运输包装, 规格, 商标, 原产地
      Custom: [list from source data]
    - [ ] # 规格管理 (N spec groups)
    - [ ] # FOB价格设置 (mode: 阶梯价/一口价/区间价, N tiers)
    - [ ] # 计量单位 (1 field)
    - [ ] # 包裹尺寸 (5 fields: 数量, 长, 宽, 高, 毛重)
    - [ ] # 发货效率信息 (port + up to 3 delivery rows)
    - [ ] # 样品单交易设置 (5 fields: 提供样品, 样品单价, 样品单位, 单次最多拿样数量, 样品描述)
    - [ ] # 其他信息设置 (支付方式, 产量, 海关编码)
    - [ ] # FAQ (10 Q&A pairs)

    Data sources confirmed:
    - [field]: [source] (page/CSV/user)

### Phase 2: Write

Generate the paste-ready text following all rules in this skill.

### Phase 3: Verify (After Writing)

After generating the output, run an automated audit that checks EVERY planned field against the actual output:

1. **Section completeness**: Every planned `# 板块名` exists in the output
2. **Field completeness**: Every planned `字段名：` exists under its section
3. **Character audit**: All values contain ONLY ASCII (no Unicode symbols)
4. **Length limits**: 样品描述 <=45 chars, custom attr values <=50 chars, product name 5-12 words
5. **Single-select fields**: 电压 contains no semicolons
6. **FOB mode consistency**: Only one pricing mode's fields present
7. **No forbidden sections**: No # 产品详情 or # 产品展示 in .txt
8. **Section order**: Matches page visual order

Report format:

    Audit Result

    Sections: 11/11 PASS
    Fields: XX/XX PASS
    Issues: 0

    Overall: PASS

If FAIL: fix the issues, then re-audit until PASS.

---

## Supported Fields

Always use the Made-in-China page's visual order below, grouped by section. Omit any section or field that the source material does not provide. Keep section headings in this order because the Chrome extension uses them for DOM-scoped matching.

**Strict section rules:**

- Use the exact section headings shown below. Do not rename them.
- Do not output legacy headings such as `# 样品交易设置` or `# 其它信息`.
- If a section has no fillable fields, omit the whole section instead of outputting an empty placeholder line.
- Do not output `# 产品详情` in the raw paste-ready text. Product details must be edited manually in the separate product details editor page.
- `# 样品单交易设置` and `# 其他信息设置` are the only accepted names for those two sections.
- Prefer exact page option text for units, for example `计量单位：米` and `样品单位：米`, not `Meter`.
- Keep `样品描述` within 45 characters.
- Do not output `Package Gross Weight：` when the value is unknown or empty.
- In `# 产品属性`, the required standard fields are: `认证`, `功率`, `发光颜色`, `电压`, `防护等级`, `运输包装`, `规格`, `商标`, `原产地`. Always output these fields when generating paste-ready Made-in-China product information.

### Output Template

The template below shows all recognized sections and fields in the correct order. Fill in values from the source material; omit fields with no data. For `# FOB价格设置`, output only one pricing mode's fields (see FOB Price Settings rules below).

```text
# 基本信息
产品名称：
中心词：
关键词：
产品分组：
产品型号：

# 产品亮点
产品亮点1：
产品亮点2：
产品亮点3：
产品亮点4：
产品亮点5：

# 产品属性
适用门店：
安装方式：
内容支持：
显示颜色：
分辨率：
屏幕尺寸：
显示技术：
认证：
功率：
发光颜色：
电压：
防护等级：
运输包装：
规格：
商标：
原产地：
CustomPropertyName：CustomPropertyValue

# 规格管理
规格名称：
规格值：
规格2名称：
规格2值：

# FOB价格设置
# (see FOB Price Settings rules — output exactly one mode's fields)

# 计量单位
计量单位：

# 包裹尺寸
Package Gross Weight：
单个包裹内产品数量：
单个包裹长：
单个包裹宽：
单个包裹高：
单个包裹毛重：

# 发货效率信息
港口：
发货期数量：
发货期时间：
发货期数量2：
发货期时间2：

# 样品单交易设置
提供样品：
样品单价：
样品单位：
单次最多拿样数量：
样品描述：

# 其他信息设置
支付方式：
产量：
海关编码：

# FAQ
FAQ问题1：
FAQ答案1：
FAQ问题2：
FAQ答案2：
FAQ问题3：
FAQ答案3：
```

### Custom Attributes

The extension also maps existing custom attributes on the page. If the source has a product attribute whose label already appears on the Made-in-China page, output it exactly as the label, for example:

```text
Battery Life：5 years
Waterproof Rating：IP65
Connectivity：2.4G WiFi
```

**Custom Attribute Rules:**
- Maximum 15 custom attributes per product
- Each attribute value must not exceed 50 characters
- Attribute names must be in English only — Chinese characters are NOT allowed in attribute name fields
- Fill as many relevant attributes as product information supports
- **Dedupe against standard properties (user rule 2026-08-13): before adding a custom attribute, check whether the page already has a similar standard property (e.g. IP等级 / 防护等级 exists → do NOT add `IP Rating` custom attr). A real page bug found: custom pair `Outdoor/Indoor Festival Decoration: Home, Office, Shopping Mall, Restaurant` duplicated the `Usage` value and mixed in application text — remove such duplicates instead of preserving them.**
- **Only output custom attributes whose name:value pair already exists on the extracted page form, or genuinely new attributes the user wants to add. If the extracted form lacks a field, omit it (do not invent `Package Gross Weight` etc.).**

## Field Rules

### Product Name

Write an English B2B listing title. Aim for 8-12 words when possible. Include product type and main use. Avoid phone numbers, email, company slogans, unsupported certifications, and keyword stuffing.

**Input type:** Textarea (`name="prodName"`), max 160 characters.

### Center Words

Use 3-6 short core words from the product name, separated by semicolons:

```text
中心词：label; shelf; lcd; retail; display
```

### Keywords

Use up to 20 English keyword phrases (page verified 2026-08-13: 20 keyword slots). Put the most important three first. Use 2-4 words per phrase where possible. Separate with semicolons. The current Made-in-China page supports 20 keyword slots.

**Input type:** Multiple textarea fields (`name="prodKeyword"`). The page starts with 1 slot and has an "添加关键词" button to add more.

### Highlights

Write benefit-oriented English highlights, one sentence each. Up to 20 highlights supported. The page starts with 3 textarea slots (`class="highlight-text"`) and has a "+ 添加亮点" button to add more. Fill as many slots as product features and benefits support. Avoid claims that require proof unless the source provides them.

### Product Attributes — Standard

These appear as dropdown selects (`class="J-prop-select"`) or checkboxes (`name="propertyValue"`) on the page. Use exact option text when known because the plugin matches page options by label:

**Standard attributes vary by product category AND by actual edit page.** The lists below are
historical caches from past pages — the edit-page extraction (Core Workflow step 0) is
authoritative. Only fill a standard field if it actually exists on the target page; if the
page lacks it (e.g. Neon Light category has no 认证/功率/电压 standard fields — they are custom
pairs), do NOT force it. Always consult `references/category-standard-attributes.md` first
(Core Workflow step 0/1); the reference file has category-specific fields and options.

These standard fields are required WHEN they exist on the target page's edit form (verify via
edit-page extraction first; they are common to most categories but NOT guaranteed — e.g.
Neon Light category lacks 认证/功率/电压 as standard fields):

```text
认证：
功率：
发光颜色：
电压：
防护等级：
运输包装：
规格：
商标：
原产地：
```

Use product-source values first. If the source only implies the value, choose the closest page option conservatively. `电压` is required but single-select, so choose one primary/default option such as `12V`; list additional voltage variants in `# 规格管理`.

- `适用门店`: `Electronics Store; Convenience Store; Supermarket; Pharmacies; Other`
- `安装方式`: known options include `Slot-in`, `Magnetic Mount`, `Adhesive Back`, `Other`; use a precise custom value if the source says another mounting method.
- `内容支持`: known options include `QR Code Display`, `Multi-language Text`, `Price + Barcode`.
- `显示颜色`: known options include `Full Color`, `3-Color (BWR)`, `Black & White`.
- `显示技术`: known options include `LCD`, `LED Segment`, `E-Ink Carta`.
- LED strip/light category fields may include:
  - `认证` (checkbox): known options include `CE`, `RoHS`, `FCC`, `EMC`, `LVD`, `CCC`, `FDA`, `GS`, `SAA`, `VDE`.
  - `功率` (select): known options include `<6W`, `6-10W`, `11-15W`, `16-20W`, `21-30W`, `>30W`.
  - `发光颜色` (select): known options include `White`, `Warm White`, `Red`, `Blue`, `Green`, `Yellow`, `Changeable`; use exact page option text when known.
  - `电压` (select): known options include `12V`, `36V`, `110V`, `220V`.
  - `防护等级` (select): known options include `IP33`, `IP44`, `IP54`, `IP65`, `IP66`, `IP67`, `IP68`.

For single-select standard attributes such as `电压`, output only one page option. If the product has multiple variants such as 12V and 24V, put those variants in `# 规格管理` as `规格名称：Voltage` and `规格值：12V; 24V`. Do not output `电压：12V; 24V`.

For resolution and screen size, output the actual value from the source. If it does not match a built-in option, the plugin will select `Other` and fill the custom value.

The plugin can also fill other current-page Made-in-China standard attributes by exact field label. If a category page shows a standard attribute, output its label exactly as shown.

### Product Attributes — Custom

These are English-name text input pairs (`name="customPropName"` + `name="customPropValue"`) with an "添加自定义属性" button to add more rows. Do not put the required fixed fields `运输包装`, `规格`, `商标`, or `原产地` here; keep them as standard attributes in `# 产品属性`.

Do not output `IP Rating` as a custom attribute. The page already has the standard attribute `防护等级` for this meaning, and adding `IP Rating` as a custom attribute triggers a duplicate-name validation error.

### Specification Management

Use these fields when the Made-in-China "规格管理" section should be filled. **规格管理 is REQUIRED for MIC product star rating (user-confirmed 2026-08-13) — always output at least one spec group even when the edit-page extraction shows the section as `empty: true`.** Maximum 300 spec combinations allowed.

Each spec group has a name input (`name="specName"`) and value input (`name="specValue"`), with an "添加规格值" button for values and "添加规格" button for new groups.

```text
# 规格管理
规格名称：Size
规格值：Single Screen; Double Screen
```

For multiple spec groups, use numbered fields. The plugin will click "添加规格" to create new groups as needed:

```text
规格1名称：Size
规格1值：Single Screen; Double Screen
规格2名称：Color
规格2值：Black; White; Silver
规格3名称：Material
规格3值：Plastic; Metal
```

If the listing uses spec-based fixed price fields (visible under "按规格价格销售/一口价销售" mode in FOB价格设置), output only values provided by the source. When `# 规格管理` creates multiple spec combinations, the plugin will apply these values to every generated SKU row and sync the hidden `prodSku` payload:

```text
规格最小起订量：10
规格库存：100000
规格单价：32.13
```

### FOB Price Settings

The Made-in-China page has three mutually exclusive pricing modes. The plugin auto-detects which mode to activate based on which fields are present in the text. **Output exactly one mode's fields — never mix fields from different modes.**

**Mode detection logic** (plugin source: `determineFobPriceMode()`):

| Fields present in text | Mode activated | Page radio button |
|---|---|---|
| `规格最小起订量` / `规格单价` / `规格库存` / `规格商品编码` | 一口价销售 | `fobPriceType='0'` (radio label: 一口价/按规格价格销售) |
| `价格区间1起订量` / `价格区间1单价` | 阶梯价 | `fobPriceType='1'` (radio label: 按采购数量-阶梯价销售) |
| `区间价最低价` / `区间价最高价` / `区间价最小起订量` / `区间价库存` | 区间价 | `fobPriceType='2'` (radio label: 按采购数量-区间价销售) |

An explicit field `FOB价格模式` (aliases: `FOB价格类型`, `价格模式`, `价格类型`, `定价方式`) overrides auto-detection. Accepted values: keywords like `一口价`/`固定`/`规格` for mode 0, `阶梯` for mode 1, `区间`/`范围`/`参考` for mode 2.
**MOQ rule:** ARMOR supports single-piece wholesale. `规格最小起订量` and `价格区间1起订量` can be `1` when the source does not specify a higher MOQ. Always use the source's MOQ when provided; default to `1` only when the source is silent.
**库存 rule (user-confirmed 2026-08-13):** 库存 0 会被买家视为无货 — ARMOR 库存统一填 `99999`（最高值，表示有充足库存）。不要输出 `库存：0` 或留空。

**Mode 1 — 一口价销售** (fixed/spec price):
Use when the source gives one MOQ/stock/unit price for the product, or when every SKU/spec combination should share the same values.
```text
# FOB价格设置
规格最小起订量：1
规格商品编码：HM-RD-P2-500
规格库存：1000
规格单价：545
```

**Mode 2 — 阶梯价** (ladder/tier price):
Use when the source gives quantity breaks (e.g. 10/500/1000) with different unit prices. All tiers share one `库存`.

```text
# FOB价格设置
价格区间1起订量：10
价格区间1单价：32.13
价格区间2起订量：3000
价格区间2单价：26.78
价格区间3起订量：5000
价格区间3单价：25.44
价格区间4起订量：10000
价格区间4单价：23.50
库存：100000
```

**Mode 3 — 区间价** (reference/range price):
Use when the source gives only a price range (min–max) instead of exact ladder prices.

```text
# FOB价格设置
区间价最小起订量：10
区间价最低价：25
区间价最高价：32
区间价库存：100000
```

Only output price, stock, package dimensions, weight, port, sample, payment, production capacity, or HS code when provided by the user/source. Do not invent them.

Use numbers without currency symbols for price fields.

### Unit

The page has a dropdown select (`name="prodMinimumOrderTypeOfLadder"` or similar) with options: 个, 平方英尺, 吨, 码, 千克, 包, 箱, 英尺, 米, 双, 令, 卷, 套, 其他, 平方米. (平方米 verified 2026-08-13.) Prefer exact page option text such as `米` instead of `Meter` when possible. The plugin also maps common English unit aliases.

### Package Dimensions

**Input type:** Text inputs (`name="packProdNum"`, `packDepth`, `packWidth`, `packHeight"`, `grossWeight"`). Dimensions are in cm, weight in kg.

**Data source requirement:**
- ONLY use exact values from product spec sheets, PI documents, or user-provided packaging data
- If packaging dimensions are NOT provided in source material, EXPLICITLY ask the user: "包裹尺寸未在规格书中找到，请提供外箱尺寸（长×宽×高 cm）和毛重，或确认是否按估算填写？"
- NEVER silently estimate package dimensions from product dimensions — packaging varies by transport mode (air/sea), protection level, and supplier
- Document the data source in the `.md` version (e.g., "包裹尺寸来源：PI文档 / 用户确认 / 估算"）

**Package dimension estimation (ONLY when user explicitly approves):**
If user confirms estimation is acceptable:
- Add 5-10cm to product dimensions for packaging buffer
- Add 20-50% to product weight for packaging materials
- Clearly mark as "估算值" in the `.md` document
- Use conservative (larger) estimates to avoid underquoting freight

### Delivery Efficiency

The "发货效率信息" section has two text inputs per row (`name="stockingNum"` for quantity, `name="stockingDay"` for days) with an "添加数量区间" button (max 3 rows). Use `发货期数量` + `发货期时间` for the first row, or add numeric suffixes for additional rows:

```text
发货期数量：100
发货期时间：15
发货期数量2：1000
发货期时间2：20
```

### Port

Always fill `港口：Huangpu` unless the source specifies another port. This is a text input (`class="J-port"`).

### Sample

The page has a radio button (`name="provideMode"`, values 1/0) to enable/disable sample fields. When enabled, the following text/select inputs become active: `samplesPrice`, `samplesPricePacking` (select), `maxSamplesCount`, `samplesDesc`.

**Note:** The plugin switches `提供样品` to `是` when requested and then fills the sample price, unit, max quantity, and description fields.

When outputting `提供样品：是`, ALWAYS include `单次最多拿样数量：` with the actual supported maximum sample quantity from the product/source or the user's business rule. Do not rely on the Chrome extension to invent a default. If the maximum sample quantity is unknown, ask for confirmation or omit the sample section instead of guessing.

The `samplesPricePacking` select uses value codes: `0` = 个, `10` = 平方英尺, `11` = 吨, etc. Output the unit name and the plugin will select the correct value.

Keep `样品描述` within 45 characters because the page input has a 50-character limit and the plugin should avoid visible truncation.

For LED strip samples, a safe concise example is:

```text
单次最多拿样数量：10
样品描述：COB strip sample, 1m, 12V/24V
```

### Payment Methods

The page shows checkboxes (`name="prodPaymentType"`) with options: L/C, T/T, D/P, Western Union, Paypal, Money Gram, Others. Selecting "Others" enables a custom text input. Use semicolons to specify multiple methods:

```text
支付方式：L/C; T/T; Paypal
```

### FAQ

Create short buyer-facing FAQs from real product information. Keep answers specific but safe. If facts are missing, omit the FAQ fields.

The page starts with 3 FAQ pairs (question + answer textarea, `class="atom-faq__textarea"`) and has a "+ 添加FAQ" button to add more.

### Product Details

Write concise English overview copy only for the readable `.md` file when useful. Do not include `# 产品详情` or `产品详情：` in the raw paste-ready `.txt` file.

The page uses a rich text editor with Normal (普通编辑) and Pro (编辑器Pro) modes. It must be edited in the separate product details editor page. The Chrome extension skips this section and must not write `newDescStr` / `newDescHtml`.

## Example Output

Below is a complete example using 阶梯价 (ladder price) mode. Every `#` line is a section header; every non-empty, non-`#` line is a `字段名：值` pair.

```text
# 基本信息
产品名称：Dynamic Full Color LCD Electronic Shelf Label for Retail Inventory Management
中心词：label; management; shelf; lcd; color
关键词：Full Color ESL; LCD Price Tag; Inventory Management Display; Digital Shelf Labeling; Smart Retail Display; Dynamic Price Display; Electronic Label System; Color LCD Signage; Wireless Price Tag; Retail Automation
产品分组：Armor Digital
产品型号：HM-2026-02

# 产品亮点
产品亮点1：Full-color LCD display supports dynamic price, image, and barcode updates.
产品亮点2：Wireless updates reduce manual labeling work for retail teams.
产品亮点3：Slim guide-rail power design fits shelves and digital signage scenarios.
产品亮点4：High-resolution 1280x800 screen ensures crisp visuals from any angle.
产品亮点5：Scalable across retail chains with centralized content management.

# 产品属性
适用门店：Electronics Store; Convenience Store; Supermarket; Pharmacies
安装方式：Power Supply by The Guide Rail Support
内容支持：Price + Barcode
显示颜色：Full Color
分辨率：1280*800
屏幕尺寸：10.1
显示技术：LCD
认证：CE; RoHS; FCC
功率：<6W
发光颜色：White
电压：12V
防护等级：IP65
运输包装：Carton
规格：35.00cm * 25.00cm * 20.00cm
商标：Armor lighting
原产地：China
Logic：LCD Video Display
Weight：315g
Update Efficiency：<10s
Work Efficiency：2.4G wifi
Technology：Ultra-Thin, Narrow Frame Design
Power Supply Mode：Power Supply by The Guide Rail Support

# 规格管理
规格名称：Size
规格值：Single Screen; Double Screen
规格2名称：Color
规格2值：Black; White; Silver

# FOB价格设置
价格区间1起订量：10
价格区间1单价：32.13
价格区间2起订量：3000
价格区间2单价：26.78
价格区间3起订量：5000
价格区间3单价：25.44
价格区间4起订量：10000
价格区间4单价：23.50
库存：100000

# 计量单位
计量单位：个

# 包裹尺寸
Package Gross Weight：1.000kg
单个包裹内产品数量：20
单个包裹长：110
单个包裹宽：60
单个包裹高：40
单个包裹毛重：10

# 发货效率信息
港口：Huangpu
发货期数量：100
发货期时间：15

# 样品单交易设置
提供样品：是
样品单价：32.13
样品单位：个
单次最多拿样数量：10
样品描述：COB strip sample, 1m, 12V/24V

# 其他信息设置
支付方式：L/C; T/T; Paypal
产量：5000PCS/Month
海关编码：8528729000

# FAQ
FAQ问题1：What is the lead time?
FAQ答案1：Please contact us for current lead time based on order quantity.
FAQ问题2：Can you customize the screen size?
FAQ答案2：Yes, we offer customization for bulk orders over 5,000 units.
```

## Quality Check

Before final output:

- Confirm the paste-ready text contains **only two line types**: `# 板块名` section headers and `字段名：值` field-value pairs. No standalone descriptive text, no `# --` pseudo-comment lines.
- Confirm the section order is exactly: 基本信息, 产品亮点, 产品属性, 规格管理, FOB价格设置, 计量单位, 包裹尺寸, 运费信息, 发货效率信息, 样品单交易设置, 其他信息设置, FAQ. (Omit sections with no fillable fields.)
- Confirm `# 产品展示` and `# 产品详情` are omitted from the raw paste-ready text.
- Confirm legacy section names are not used: `样品交易设置`, `其它信息`.
- Confirm every field line uses `：`.
- Confirm list fields use semicolons.
- Confirm no unsupported facts were invented.
- Confirm fields unknown from the source are omitted.
- Confirm required product attribute fields are included: `认证`, `功率`, `发光颜色`, `电压`, `防护等级`, `运输包装`, `规格`, `商标`, `原产地`.
- Confirm custom attributes do not include `IP Rating`; use `防护等级` only.
- Confirm `# FOB价格设置` uses exactly one pricing mode: either 一口价 fields, 阶梯价 fields, or 区间价 fields. Do not mix mode fields.
- Confirm unsupported fields (product images, destination region selector) are omitted.
- Confirm sample description is 45 characters or shorter.
- Confirm ALL FAQ, highlight, and attribute values contain ONLY ASCII characters (English letters, digits, English punctuation). Unicode symbols like >=, <=, Deg, x must be replaced with ASCII equivalents: >=, <=, Deg/C, x. (User-confirmed 2026-06-12)
