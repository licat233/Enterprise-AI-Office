---
name: mic-optimization-guide
title: MIC Optimization Guide
description: Central knowledge base for Made-in-China.com (MIC) product optimization. Covers product naming, keywords, attributes, pricing, content quality, and scoring optimization. Continuously updated with MIC platform standards and best practices.
version: 1.0.0
triggers:
  - User mentions "MIC optimization" or "optimize MIC"
  - User asks about MIC product score or ranking
  - User wants to improve MIC product quality
  - User mentions "产品优化" or "优化产品" in MIC context
  - User asks about MIC standards, rules, or guidelines
---

# MIC Optimization Guide

## Purpose

This skill serves as the **central knowledge base** for all MIC (Made-in-China.com) optimization knowledge. It consolidates platform standards, best practices, and lessons learned from actual upload/optimization sessions.

**When to use:**
- Optimizing existing MIC products for higher scores (4.6+)
- Creating new MIC products with best practices
- Resolving MIC platform standard questions
- Understanding MIC scoring factors

**Related skills (auto-load for MIC tasks):**
- `armor-mic-product-optimization` — canonical closed-package MIC workflow
- `armor-content-writing` — Brand content standards
- `seo-optimization` — SEO keyword strategy

**Legacy skills (已删除，规则已迁移到本 skill):**
- ~~`mic-product-fill`~~ → paste-ready stage is owned by `armor-mic-product-optimization`
- ~~`mic-product-audit`~~ → audit stage is owned by `armor-mic-product-optimization`
- ~~`mic-product-detail-page`~~ → detail-page stage is owned by `armor-mic-product-optimization`

**Reference files in this skill:**
- `references/platform-input-safety-rules.md` — 平台输入安全规则（适用于所有上传方式）
- `references/category-attribute-differences.md` — 分类属性字段对照表
- `references/product-scoring-checklist.md` — 产品评分检查清单

---

## 1. Product Name Standards

### 1.1 Official MIC Standard
- **Source**: https://service.made-in-china.com/help/promotionskill/product/3243.htm
- **Length**: 5-12 words
- **Structure**: Modifier + Noun + for + Application + with + Certification/Feature
- **Capitalization**: Title Case (first letter of each word capitalized)

### 1.2 Exact Structure (User-Confirmed 2026-05-18)

```
Modifier + Noun + for + Application + with + Certification/Feature
```

**Examples:**
- ✅ `Custom LED Neon Sign for Home Bar Decoration with RGB Color Changing` (9 words)
- ✅ `360 Degree LED Tube Light for Commercial Decoration with G13 Base and TUV Certification` (12 words)
- ✅ `10.1 Inch Electronic Shelf Label LCD Color Display for Retail with IP65` (10 words)
- ❌ `LED COB Strip Light Flexible 5mm 12V 24V COB LED Strip` — keyword stuffing, no application, no feature

### 1.3 Common Naming Mistakes

| Mistake | Bad Example | Why It Fails |
|---------|-------------|--------------|
| Keyword stuffing | `LED Strip Light and COB LED Strip` | Repeats core noun, wastes words |
| Missing application | `Flexible 5mm COB LED Strip` | No "for" clause = no use case |
| Missing feature/cert | `COB LED Strip Light for Cabinet` | No "with" clause = no differentiation |
| Wrong word order | `5mm Flexible COB LED Strip Light` | Modifier should lead with size/feature |
| Too short | `LED Strip` | < 5 words, no context |
| Too long | `Ultra Narrow 5mm Width Flexible COB LED Strip Light for Under Cabinet and Shelf Lighting with Dual Voltage 12V 24V and CE Certification` | > 12 words, bloated |

### 1.4 Center Word Rules
- Center word must match the product name's core noun
- All keywords' center words must match the product name's center word
- Example: For "LED Neon Sign", center word is "Sign"; for "LED Tube Light", center word is "Light"
- Trigger center words via onblur event (click elsewhere after filling product name)

---

## 2. Keywords Rules

### 2.1 Official MIC Standard
- **Source**: https://service.made-in-china.com/help/promotionskill/product/473.htm
- **Format**: Modifier + Product Center Word
- **Quantity**: Up to 10 keywords (MIC page supports 10 slots)
- **Rule**: Not case-sensitive, not plural-sensitive
- **First 3 keywords**: Most important, place most representative keywords first

### 2.2 Keyword Quality Checklist
- [ ] All keywords' center words match product name's center word
- [ ] First 3 keywords are the most important
- [ ] No duplicate or overly similar terms
- [ ] Each keyword follows "Modifier + Center Word" format
- [ ] Fill all 10 slots when product information supports it

### 2.3 Example Keywords (LCD ESL)

| Order | Keyword | Evaluation |
|-------|---------|------------|
| 1 | Electronic Shelf Label Display | ✅ Core product + center word |
| 2 | LCD Color Display | ✅ Feature + center word |
| 3 | Digital Price Tag Display | ✅ Application + center word |
| 4 | Retail Display Screen | ✅ Scenario |
| 5 | Supermarket ESL Display | ✅ Scenario + abbreviation |
| 6 | Store Digital Signage | ✅ Alternative name |
| 7 | Wireless Price Label | ✅ Feature |
| 8 | Electronic Label System | ✅ System level |
| 9 | Smart Retail Display | ✅ Smart feature |
| 10 | Commercial LCD Monitor | ✅ Commercial use |

---

## 3. Product Highlights Optimization

### 3.1 Platform Standard
- **Location**: Between basic info and product attributes
- **Purpose**: "产品亮点信息将参与站内外搜索，填写越完善，曝光机会更多"
- **Quantity**: Up to 10 highlights (fill all 10 when product supports it)

### 3.2 Writing Rules
- Each highlight: 1 sentence, 10-20 words
- Lead with feature name, follow with benefit
- Include keywords naturally
- Use Title Case for feature names

### 3.3 Template
```
[Feature Name]: [Specific capability] + [Benefit to buyer]
```

### 3.4 Examples by Product Type

**Electronic Shelf Label (ESL):**
| # | Highlight |
|---|-----------|
| 1 | `1.54 inch E-Ink display with 152x152 resolution, ultra-clear price visibility` |
| 2 | `Wireless 2.4GHz update, price changes in seconds without manual replacement` |
| 3 | `IP65 protection, 5-year battery life, maintenance-free operation` |
| 4 | `Multi-language support with barcode and QR code display` |
| 5 | `Tool-free slot-in installation, fits standard retail shelving` |

**Shelf Edge LCD Display (AD Player):**
| # | Highlight |
|---|-----------|
| 1 | `Custom Size Availability: Offers custom screen sizes to fit specific shelf dimensions and retail layouts` |
| 2 | `Industrial Grade Durability: Built with rugged hardware, dustproof and anti-collision design for 50,000+ hours operation` |
| 3 | `Real-Time Data Sync: Seamlessly integrates with POS, ERP systems for automatic price and promotion updates` |
| 4 | `Centralized Management: Cloud-based CMS allows batch editing and remote updates for multiple displays simultaneously` |
| 5 | `Flexible Installation: Supports shelf clamp, magnetic suction, and screw fixing for quick assembly without damage` |
| 6 | `ODM & OEM Customization: Accepts customization for sizes, interfaces, functions, logos, and software per client needs` |
| 7 | `Low Power Consumption: Optimized energy design supports 24/7 uninterrupted operation with minimal power usage` |

**LED Round Screen:**
| # | Highlight |
|---|-----------|
| 1 | `P2 High Density Pixel Pitch: 250,000 dots/m² delivers crisp visuals even at close viewing distances` |
| 2 | `3840Hz High Refresh Rate: Ensures flicker-free display for professional photography and broadcast applications` |
| 3 | `Magnetic Modular Design: Tool-free front maintenance with quick-detach modules for easy servicing` |
| 4 | `Custom Diameter Options: Available in 500mm, 1000mm and custom sizes to fit any installation space` |
| 5 | `Wi-Fi & Cloud Control: HD-C08L controller supports wireless content updates and remote cluster management` |
| 6 | `Wide Viewing Angle 140°: Consistent color and brightness from virtually any viewing position` |
| 7 | `Adjustable Color Temperature: 3200K-7000K range adapts to ambient lighting and content requirements` |

---

## 4. FAQ Optimization

### 4.1 Platform Standard
- **Location**: Between sample settings and product details
- **Purpose**: "产品FAQ信息将参与站内外搜索，填写越完善，曝光机会更多"
- **Quantity**: Up to 10 Q&A pairs (fill all 10 when product information supports it)

### 4.2 Quality Rules
1. **Questions must be real buyer questions** — not marketing speak
2. **Answers must be specific** — include numbers, specs, procedures
3. **No duplicate questions** — check for repeats
4. **Grammar must be correct** — buyers judge professionalism
5. **Answers must not contradict** — ensure consistency across Q&A

### 4.3 Common FAQ Topics by Product Type

**ESL Products:**
- Battery lifetime and replacement
- Server deployment options (cloud vs on-premise)
- Integration with POS/ERP systems
- Shipping and battery handling
- Security level and data protection
- Pre/post sales support
- Training and documentation
- Pricing and discounts

**LCD Display / AD Player Products:**
- What is the product / how does it differ from standard displays
- Installation methods and compatibility
- Networking and synchronous refresh
- Long-term usage and maintenance
- Data update procedures
- Customization options
- How to choose the right model

**LED Round Screen:**
- What pixel pitch should I choose for my viewing distance?
- How is the circular screen controlled and updated?
- What is included in the standard package?
- Can the diameter be customized to fit my space?
- What is the typical lifespan and warranty coverage?
- How is the screen installed — wall mount or hanging?
- Does it support video playback or only static images?
- What is the power consumption for continuous operation?

### 4.4 Grammar Checklist
Before delivering FAQ content, verify:
- [ ] "life time" → "lifetime"
- [ ] "how to shipping" → "how to ship"
- [ ] "Did we receive" → "Will we receive" / "Do you provide"
- [ ] No duplicate questions
- [ ] No contradictory answers
- [ ] Technical terms consistent with product attributes

---

## 5. Sample Description Optimization

### 5.1 Platform Standard
- **Location**: Sample order settings section
- **Purpose**: "建议输入样品颜色、规格、数量及备注等信息，方便买家快速下样品单"
- **Impact**: Providing samples significantly improves conversion rates
- **Limit**: ≤50 characters (page input has 50-character limit)

### 5.2 Sample Settings Checklist
- [ ] Provide samples: **Yes** (recommended)
- [ ] Sample price: Equal to or slightly higher than unit price
- [ ] Max sample quantity: ≤ MOQ (typically 1-10)
- [ ] Description includes: color, specs, quantity, notes

### 5.3 Examples

**LED Round Screen Sample:**
```
Sample: P2 500mm round LED screen with controller
- Pixel pitch: P2, Diameter: 500mm
- Includes: power supply, HD-C08L controller, cables
- Packaging: Wooden box for safe transport
- Note: Sample includes 1 unit. Custom sizes available for bulk orders. MOQ 10 pcs.
```

---

## 6. Product Attributes by Category

### 6.1 Critical Rule
**Different MIC categories have COMPLETELY DIFFERENT attribute fields. Never assume — always extract from current page.**

**Edit page is authoritative, templates are not (user-confirmed 2026-08-13):** the standard
attributes in this skill's tables are historical caches.
The product edit page (`membercenter...productmanage.do`) may show different standard fields —
per category AND over time. Workflow:

1. **Get the edit-page extraction first** — use the MIC Product Edit Page Extractor Chrome
   extension (JSON schema `mic-product-edit-context/v1`; see
   `mic-upload-data-sources/references/mic-edit-context-plugin.md`). Generate `# 产品属性`
   from `fieldOrigin: mic_standard_property` + `mic_builtin_property` + existing custom pairs.
2. Only fill standard fields that actually exist on the target page. If the page lacks a
   field this skill's template lists (e.g. Neon Light category has NO 认证/功率/电压 standard
   fields — they are custom pairs), do NOT force it.
3. Categories can also change over time — never assume last month's page equals today's.

### 6.2 Category Reference Tables

**Neon Light Category (verified from edit page 2026-08-13):**
| Field | Type | Verified options |
|-------|------|------------------|
| IP等级 | select | IP20; IP33; IP44; IP54; IP55; IP65; IP66; IP67; IP68; Other |
| 发光颜色 | select | Single Color; Changeable Color; Other |
| 应用 | checkbox | Home; Outdoor; Commercial; Other |
| 运输包装 | text | Anti-Static Bags / Carton |
| 规格 | text | e.g. 107*58.5*9(mm) |
| 商标 | text | OEM / Armor lighting |
| 原产地 | text | China |

Custom pairs carry the technical specs in this category: Voltage, Wattage (W/M),
Color Temperature(CCT), Color Rendering Index(Ra), Lamp Luminous Efficiency(Lm/W),
Light Source, Working Temperature(℃), LED Type, LEDs/M, Usage, Material, Feature,
Working Life, Certification.

**LCD Price Tag Category:**
| Field | Type | Typical Selection |
|-------|------|-------------------|
| 适用门店 | checkbox | Supermarket; Electronics Store; Convenience Store |
| 安装方式 | dropdown | Slot-in; Wall-Mounted; Magnetic Mount |
| 内容支持 | dropdown | Price + Barcode; QR Code Display; Multi-language Text |
| 显示颜色 | dropdown | Full Color; 3-Color (BWR); Black & White |
| 分辨率 | dropdown + custom | Other → 1280x800 |
| 屏幕尺寸 | dropdown + custom | Other → 10.1" |
| 显示技术 | dropdown | LCD |

**AD Player Category:**
| Field | Type | Typical Selection |
|-------|------|-------------------|
| 应用 | checkbox | Indoor AD Player; Outdoor AD Player; Other |
| 屏幕尺寸 | dropdown | Other → Custom size |
| 安装方式 | dropdown | Other → Mounting Bracket / Shelf Clamp |
| 类型 | dropdown | Other → Shelf Edge Digital Signage |
| 触摸屏类型 | dropdown | Other → Non-Touch (Standard) |
| 屏幕显示技术 | dropdown | LCD |
| 接口类型 | dropdown | Other → TF Card, Micro-USB OTG, Type-C |
| 可否遥控 | dropdown | With Remote Control |
| 操作系统 | dropdown | Other → Android 11 (Optional) |
| 是否定制 | dropdown | Customized |

**LED Display Category (for Round Screen):**
| Field | Type | Typical Selection |
|-------|------|-------------------|
| 应用 | checkbox | Indoor; Outdoor; Commercial |
| 像素间距 | dropdown | P1.25; P2; P2.5; P3; Other |
| 屏幕尺寸 | dropdown + custom | Other → 500mm / 1000mm diameter |
| 显示技术 | dropdown | LED |
| 亮度 | dropdown | ≥600 CD/㎡ |
| 刷新率 | dropdown | 3840Hz |
| 防护等级 | dropdown | IP43; IP65 |
| 安装方式 | dropdown | Wall-Mounted; Hanging; Other |
| 是否定制 | dropdown | Customized |

### 6.3 "Other" → Custom Input Pattern
When a dropdown has "Other" option:
1. Select "Other" from dropdown
2. Check if a custom input field appears next to the dropdown
3. Fill the custom input with the specific value

### 6.4 "折中" Calculation Rule
**"折中" means EXACT mathematical middle: (min + max) / 2, then pick closest available option.**

Example: Range 10-25ms → (10+25)/2 = 17.5 → closest available = **16ms** (NOT 20ms)

---

## 7. Custom Attributes

### 7.1 Rules
- Maximum 15 custom attributes per product
- Attribute names: **English only** — Chinese characters NOT allowed
- Each attribute value: ≤50 characters
- Unit Size belongs in "规格管理" section, NOT custom attributes

### 7.2 Common Custom Attributes by Product Type

**LCD ESL:**
| Attribute | Value Source |
|-----------|-------------|
| Weight | Spec sheet |
| Case Material | Domain knowledge (Plastic typical) |
| Case Color | User confirmed or inferred |
| Protection Level | Domain knowledge (IP65 typical) |
| Viewing Angle | Domain knowledge (TFT LCD: 120°-160°) |
| Operating Temperature | Domain knowledge (indoor: -10°C ~ 50°C) |
| Frequency | Spec sheet (2.4GHz) |
| Communication | Spec sheet (Wi-Fi) |
| Ota Updates | Domain knowledge (Supported) |
| Certification | Domain knowledge (RoHS, CE, FCC) |
| Technical Support | Domain knowledge (Lifetime) |
| Warranty Period | Domain knowledge (2 Year) |
| Carton Weight | Spec sheet |

**LED Round Screen:**
| Attribute | Value Source |
|-----------|-------------|
| Weight | Spec sheet (6.4kg for 500mm) |
| Diameter | Spec sheet (500mm / 1000mm) |
| Pixel Density | Spec sheet (250,000 dots/m²) |
| Refresh Rate | Spec sheet (3840Hz) |
| Brightness | Spec sheet (≥600 CD/㎡) |
| Viewing Angle | Spec sheet (140°) |
| Power Consumption | Spec sheet (Max 680W/㎡, Avg 250W/㎡) |
| Input Voltage | Spec sheet (110V/220V, 50-60Hz) |
| Control System | Spec sheet (HD-C08L / 摩西尔) |
| Operating Temperature | Spec sheet (-20°C ~ +50°C) |
| Protection Level | Spec sheet (IP43) |
| Lifespan | Spec sheet (100,000 hours) |
| Certification | Domain knowledge (CE, RoHS, FCC) |
| Warranty Period | Domain knowledge (2 Year) |

---

## 8. Pricing & Packaging

### 8.1 Currency & Conversion
- **Currency**: Always USD on MIC platform
- **Conversion**: USD = RMB Price ÷ 7.2 × Markup
- **Markup factors**: B2B platform premium 1.2-1.5x; Small MOQ premium 1.1-1.3x

### 8.2 Pricing Modes
| Mode | Fields | Use Case |
|------|--------|----------|
| 一口价 (Fixed) | 规格最小起订量 / 规格商品编码 / 规格库存 / 规格单价 | Single SKU |
| 阶梯价 (Ladder) | 价格区间N起订量 / 价格区间N单价 + unified 库存 | Most common for ARMOR |
| 区间价 (Range) | 区间价最小起订量 / 区间价最低价 / 区间价最高价 / 区间价库存 | Reference pricing |

### 8.3 Ladder Price Format
```
价格区间1起订量：10
价格区间1单价：3.10
价格区间2起订量：499
价格区间2单价：2.95
价格区间3起订量：1000
价格区间3单价：2.83
库存：100000
```

### 8.4 MOQ Guidelines
- Standard: 100 pcs
- Small batch support: 10 pcs (when user says "我们支持小批量订购")
- **Customization: 10+ units support customization**
- **General MOQ: 1 unit**
- Always confirm MOQ with user before filling

### 8.5 Shipping & Delivery
- **Shipping template**: ARMOR 未开通运费模板 — 一般不选择/不填写（用户确认 2026-08-13）。不是扣分项，不要建议"选择官方模板"
- **Port**: Huangpu (统一填写)
- **Delivery format**: `发货期数量` + `发货期时间` (max 3 rows)
```
发货期数量：100
发货期时间：15
发货期数量2：1000
发货期时间2：20
```

### 8.6 Package Dimensions
- Quantity per carton
- Carton dimensions (L × W × H in cm)
- Carton weight (kg)

---

## 9. Scoring Optimization (4.6+)

### 9.1 Scoring Factors by Weight

| Factor | Weight | Optimization Target |
|--------|--------|---------------------|
| Product Name | High | 5-12 words, proper structure |
| Center Word | Medium | Matches product name core noun |
| Keywords | High | 10 keywords, first 3 most important |
| **Product Highlights** | **High** | **10 highlights, feature + benefit** |
| Product Attributes | High | Complete, accurate, minimal "Other" |
| Custom Attributes | Medium | Up to 15, value ≤50 chars |
| **FAQ** | **Medium** | **10 Q&A, real buyer questions** |
| **Sample Description** | **Medium** | **≤50 chars, provide samples** |
| Product Details | High | Structured, keyword-rich, no errors |
| Images | Medium | High quality, proper alt text |
| Pricing | Low | Competitive, clear MOQ |
| **Shipping Info** | **Medium** | **Template selected, delivery filled** |
| **Package Info** | **Low** | **Dimensions, weight, quantity** |

### 9.2 Common Low-Score Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| Empty highlights | High | Add 10 feature+benefit highlights |
| Empty FAQ | Medium | Add 10 real buyer Q&A |
| No sample offered | Medium | Enable samples, add description |
| Missing shipping template | Medium | Select template, fill delivery time |
| Keyword stuffing in name | High | Rewrite with proper structure |
| "Other" overused in attributes | Medium | Select standard options when possible |
| Grammar errors in FAQ | Medium | Proofread before publishing |

---

## 10. Platform Input Rules

### 10.1 Character Restrictions
**All form inputs ONLY accept English, numbers, and English punctuation — NO Chinese characters.**

| Allowed | Forbidden |
|---------|-----------|
| A-Z, a-z, 0-9 | Chinese characters (中文) |
| Space, hyphen `-`, comma `,` | Chinese punctuation（，。！？：；） |
| Period `.`, slash `/`, parentheses `()` | Full-width symbols |
| Colon `:`, semicolon `;`, apostrophe `'` | |
| Quote `"`, percent `%`, degree `°` | |
| Plus `+`, equals `=`, less/greater `<>` | |

**Exception**: Category dropdown options provided by MIC system may contain Chinese — these are system labels, not user inputs.

### 10.2 agent-browser Limitations

| Element | Support | Workaround |
|---------|---------|------------|
| Text input | ✅ Reliable | Direct fill |
| Checkbox | ✅ Reliable | Direct click |
| Button | ✅ With verification | Verify text first |
| **Dropdown** | ❌ **Unreliable** | **User manual selection** |
| File upload | ❌ Not supported | User manual upload |
| Rich text editor | ❌ Not supported | User manual edit |

---

## 11. Domain Knowledge Reference

### 11.1 LCD ESL Typical Values
| Parameter | Typical Value | Reasoning |
|-----------|--------------|-----------|
| Case Material | Plastic | Most ESL products use plastic housing |
| Case Color | Black/White | Common colors |
| Viewing Angle | 120°-160° | TFT LCD typical range; IPS = 178° |
| Operating Temperature | -10°C ~ 50°C | Indoor climate-controlled environments |
| Response Time | 10-25ms | TFT LCD typical; "折中" → 16ms |
| Communication | Wi-Fi 2.4GHz | Standard for wireless ESL |
| Power Supply | 12V DC | Common for LCD displays |
| Protection Level | IP65 | Typical for retail environments |
| Warranty Period | 2 Year | Standard for commercial B2B |

### 11.2 LED Display Typical Values
| Parameter | Typical Value | Reasoning |
|-----------|--------------|-----------|
| Case Material | Aluminum | LED displays typically use aluminum |
| Viewing Angle | 140°-160° | LED typical range |
| Operating Temperature | -20°C ~ +50°C | Standard for indoor LED |
| Refresh Rate | 1920Hz-3840Hz | Higher = better for photography |
| Lifespan | 100,000 hours | LED theoretical lifespan |
| Protection Level | IP43-IP65 | Indoor IP43, outdoor IP65 |
| Warranty Period | 2 Year | Standard for commercial B2B |

---

## 12. Optimization Report Template

When analyzing existing products, use this structure:

```markdown
## Optimization Report for [Product Name]

### 1. Product Name
| Current | [current name] |
| Issue | [what's wrong] |
| Optimized | [new name] |

### 2. Center Word
| Current | [current] |
| Suggested | [new] |
| Reason | [why] |

### 3. Keywords (Top 10)
| Order | Current | Optimized | Reason |
|-------|---------|-----------|--------|
| 1 | ... | ... | ... |

### 4. Product Attributes
| Attribute | Current | Issue | Suggested |
|-----------|---------|-------|-----------|
| ... | ... | ... | ... |

### 5. Custom Attributes
| Attribute | Current | Format Fix | Add/Remove |
|-----------|---------|------------|------------|
| ... | ... | ... | ... |

### 6. Product Details
| Issue | Fix |
|-------|-----|
| ... | ... |

### 7. Pricing & Shipping
| Suggestion | Details |
|------------|---------|
| ... | ... |
```

---

## 13. Knowledge Update Log

| Date | Update | Source |
|------|--------|--------|
| 2026-05-18 | Product name structure confirmed: Modifier + Noun + for + Application + with + Feature | User instruction |
| 2026-05-19 | Custom attributes max 15 (was 45), English-only names | User instruction |
| 2026-05-19 | FOB ladder price uses unified 库存 field | User instruction |
| 2026-05-19 | Shipping format: 发货期数量 + 发货期时间 | User instruction |
| 2026-05-19 | MIC naming: 5-12 words, Title Case | MIC official |
| 2026-05-21 | 删除 mic-upload-workflow 和 mic-product-upload，规则迁移到本 skill | User decision |
| 2026-05-21 | 包裹尺寸估算需用户显式确认，禁止静默估算 | User correction |
| 2026-05-21 | 产品信息查询顺序：KB V3 → Obsidian → CSV → session → user | Workflow established (gbrain removed 2026-06) |
| 2026-05-21 | 定制政策：10+ units support customization, MOQ generally 1 unit | Business rule update |
| 2026-08-13 | 编辑页提取优先：标准属性以编辑页实测为准，模板仅历史缓存（Neon Light 分类实测仅 7 标准属性，认证/功率/电压为自定义对） | Edit page verification |
| 2026-08-13 | 运费模板：ARMOR 未开通，不选择/不填写，非扣分项 | User confirmation |
| 2026-08-13 | 关键词槽位 10 → 20（页面实测）；计量单位加"平方米"；IP等级选项含 IP55/IP20；发光颜色选项 Single/Changeable/Other | Edit page verification |
| 2026-08-13 | 自定义属性去重：添加前检查标准属性是否已有相似字段；只输出编辑页已存在的字段（不发明 Package Gross Weight 等） | User rule |

---

## 14. Quick Reference Checklist

Before publishing ANY MIC product:

### 14.1 Data Source Verification
- [ ] **先获取编辑页提取 JSON（插件）**，标准属性/自定义对以提取为准，模板仅参考
- [ ] 所有技术参数标注来源（规格书/PDF/PI/用户确认/编辑页提取）
- [ ] 价格数据来自最新 PI 或用户确认
- [ ] 包裹尺寸有明确来源，非估算值
- [ ] 估算值已标记 `[估算]` 并说明计算逻辑
- [ ] 用户已确认关键字段（价格、样品、包装）
- [ ] 自定义属性不与页面已有标准属性重复（用户规则 2026-08-13）

### 14.2 Content Quality
- [ ] Product Name: 5-12 words, proper structure, Title Case
- [ ] Center Word: matches product name core noun
- [ ] Keywords: 10 slots filled (first 3 most important)
- [ ] Highlights: 10 items, feature + benefit format
- [ ] Product Attributes: complete, minimal "Other" selections
- [ ] Custom Attributes: ≤15, English names, values ≤50 chars
- [ ] 规格管理: at least 1 spec group if applicable
- [ ] FAQ: 10 Q&A, real buyer questions, no duplicates
- [ ] Sample: offered, description ≤50 chars
- [ ] Pricing: competitive USD, clear MOQ
- [ ] Shipping: template selected, delivery time filled
- [ ] Package: dimensions, weight, quantity per package
- [ ] Port: Huangpu
- [ ] All inputs: English only, no Chinese characters
- [ ] Grammar check: no "life time", "how to shipping", etc.

---

## 15. Data Source & Estimation Rules

### 15.1 Source Annotation Requirement

For ALL product data fields, annotate the source in the Markdown version:

| Field | Source | Example |
|-------|--------|---------|
| 产品名称 | User confirmed | "Round LED Display" |
| 产品型号 | User confirmed | "HM-RD-P2-500" |
| 技术参数 | Spec sheet | "P2 pixel pitch from PDF" |
| 价格 | PI document | "$545 from PI dated 2026-05-20" |
| 包裹尺寸 | **ASK USER** | "Not in spec — need confirmation" |
| 重量 | Spec sheet | "6.4Kg net from PDF" |

### 15.2 Estimation Protocol

When source data is incomplete:

1. **First**: State clearly "规格书/PI中未找到 [字段]"
2. **Second**: Apply domain knowledge with explicit reasoning
3. **Third**: Mark as `[估算]` and explain calculation
4. **Never**: Silently invent values without marking them

**Example for package dimensions when not in spec:**
```markdown
| 字段 | 值 | 来源 |
|------|-----|------|
| 单个包裹长 | 55cm | [估算] 产品直径50cm + 包装余量5cm |
| 单个包裹毛重 | 8.5kg | [估算] 产品净重6.4kg + 包装2.1kg（待确认） |
```

### 15.3 User Confirmation Triggers

ALWAYS ask user confirmation for:
- 包裹尺寸（当规格书/PI未提供时）
- 价格（当PI数据与当前市场差异大时）
- 海关编码（当产品分类不明确时）
- 样品价格（通常高于批量单价，需确认）
