# Product Type to MIC Fields Mapping Table

> **Purpose:** When generating MIC product info, FIRST identify the product type, THEN use this table to determine which sections, fields, custom attributes, highlights, and FAQs to produce.
> **Usage:** Load this file at the START of every product fill task. Match the product to a type below.

---

## Universal Sections (All Product Types)

Every product MUST fill these 11 sections in order:

| # | Section | Fields | Required |
|---|---------|--------|----------|
| 1 | # 基本信息 | 产品名称, 中心词, 关键词, 产品分组, 产品型号 | YES |
| 2 | # 产品亮点 | 产品亮点1-10 | YES (fill all 10) |
| 3 | # 产品属性 | 9 required standard + category-specific + custom | YES |
| 4 | # 规格管理 | >=1 spec group | YES |
| 5 | # FOB价格设置 | Exactly one mode (一口价/阶梯价/区间价) | YES |
| 6 | # 计量单位 | 计量单位 | YES |
| 7 | # 包裹尺寸 | 数量, 长, 宽, 高, 毛重 (5 fields) | YES |
| 8 | # 发货效率信息 | 港口 + delivery rows (up to 3) | YES |
| 9 | # 样品单交易设置 | 提供, 单价, 单位, 数量, 描述 (5 fields) | YES |
| 10 | # 其他信息设置 | 支付方式, 产量, 海关编码(optional) | YES |
| 11 | # FAQ | FAQ问题/答案 1-10 | YES (fill all 10) |

---

## Type 1: LED Rigid Bar / LED Shelf Light

**MIC Category:** LED Strip Lights
**ARMOR examples:** HM-2835 series, HM-SLHR series, HM-SLIBS, HM-SL07, ARM-FPSA

### Required Standard Attributes (always fill all 9)

| Field | Type | Options |
|-------|------|---------|
| 认证 | checkbox | CE, RoHS, FCC, EMC, LVD, CCC, GS, SAA, VDE |
| 功率 | select | <6W / 6-10W / 11-15W / 16-20W / 21-30W / >30W |
| 发光颜色 | select | White / Warm White / Changeable |
| 电压 | select | 12V (pick ONE, others go to 规格管理) |
| 防护等级 | select | IP20 / IP44 / IP65 |
| 运输包装 | text | Carton |
| 规格 | text | Customized |
| 商标 | text | Armor lighting |
| 原产地 | text | China |

### Recommended Custom Attributes (pick 8-12)

LED Chip, LED Density, CRI, R9 Value, Beam Angle, Lifespan, Installation, Housing Material, Housing Color, Dimmable, Warranty, Connector Type, Operating Temperature, Max Daisy Chain

### Spec Groups

Length (4-8 values from page), Voltage (12V; 24V)

### Highlight Themes

1. Core differentiator (CRI / low temp / slim / power)
2. Installation method (magnetic / clip / tool-free)
3. Housing quality (aluminum / heat dissipation)
4. LED technology (chip, density, uniformity)
5. Light quality (CRI, R9, no glare)
6. Customization (length, CCT, connector)
7. Certifications
8. IP / environment rating
9. Energy efficiency
10. Application scenarios

### FAQ Themes

1. Operating temperature / cold storage
2. Available lengths / customization
3. Installation method
4. Power consumption per meter
5. CRI / light quality
6. Certifications
7. MOQ / sample
8. Lead time
9. Warranty
10. OEM/ODM scope

---

## Type 2: Low Temperature / Freezer Light

**MIC Category:** LED Strip Lights
**ARMOR examples:** HM-1510Q, HM-SLIBS060W06, HM-SLIBD060W12

### Inherits ALL from Type 1, PLUS:

### Extra Highlight Themes

- Low temperature engineering (cold storage operation)
- IP65 waterproof (humidity, frost protection)
- Wide CCT range with food-specific recommendations
- Anti-fog / anti-condensation design

### Extra FAQ Themes

- Exact operating temperature range
- Freezer vs refrigerated cabinet suitability
- Waterproof rating for humid environments
- Recommended CCT by food type (2500K bakery, 4000K produce, 6000K seafood, 6500K jewelry)

---

## Type 3: Magnetic Shelf Light

**MIC Category:** LED Strip Lights
**ARMOR examples:** HM-SLBT, HM-SLHR SERIES, customed magnetic series

### Inherits ALL from Type 1, PLUS:

### Extra Custom Attributes

Max Daisy Chain, Magnet Type (N52/Standard), Power Track (Included/Optional)

### Extra Highlight Themes

- Magnetic mount speed (5-second snap-on)
- Daisy-chain capability
- Power track system
- No-drill / no-wire installation
- Retrofit-friendly

### Extra FAQ Themes

- Max daisy-chain count
- Non-metal shelf adapters
- Power supply requirements
- Track length customization

---

## Type 4: Electronic Shelf Label (ESL)

**MIC Category:** Electronic Shelf Labels
**ARMOR examples:** ESL LCD series, ESL E-Ink series

### Category-Specific Standard Attributes (beyond universal 9)

| Field | Type | Options |
|-------|------|---------|
| 适用门店 | checkbox | Supermarket, Electronics Store, Convenience Store, Pharmacies |
| 安装方式 | select | Slot-in / Magnetic Mount / Adhesive Back |
| 内容支持 | select | Price + Barcode / QR Code Display / Multi-language Text |
| 显示颜色 | select | Full Color / 3-Color (BWR) / Black & White |
| 分辨率 | select/custom | e.g. 1280*800 |
| 屏幕尺寸 | select/custom | e.g. 10.1 |
| 显示技术 | select | LCD / E-Ink Carta / LED Segment |

### Recommended Custom Attributes

Weight, Case Material, Case Color, Viewing Angle, Communication (Wi-Fi/BLE), Battery Life, Update Speed, Operating Temperature, Warranty, OTA Updates

### Highlight Themes

1. Display technology (resolution, color)
2. Wireless update speed
3. Battery life (E-Ink)
4. Multi-language / multi-content
5. Installation (slot-in / magnetic)
6. POS/ERP integration
7. IP rating / durability
8. Centralized cloud management
9. Custom screen sizes
10. Global certifications

### FAQ Themes

1. Battery life and replacement
2. POS/ERP compatibility
3. Wireless protocol and range
4. Screen size options
5. Color vs BWR vs B/W
6. Cloud vs on-premise server
7. MOQ and sample
8. Lead time
9. Warranty and after-sales
10. Logo and case customization

---

## Type 5: LED Neon Light

**MIC Category:** LED Neon Light
**ARMOR examples:** 360-degree neon, flat neon, HM-N1220V24-DMX512-RGB (1220), DHM512 series

### Standard Attributes — VERIFIED from backend edit page (2026-08-13, HM-N1220V24)

**IMPORTANT: LED Neon Light category has only 7 standard attributes — NOT the 9 universal ones.
认证 / 功率 / 电压 are NOT standard fields in this category; they exist as 自定义属性对
(English name/value pairs). Do NOT output them under # 产品属性 as standard fields for this type.**

| Field | Type | Options / example |
|-------|------|-------------------|
| IP等级 | select | IP33 / IP44 / IP54 / IP65 / IP66 / IP67 / IP68 |
| 发光颜色 | select | White / Warm White / Changeable Color / etc. |
| 应用 | checkbox | Home / Outdoor / Commercial / Other |
| 运输包装 | text | Anti-Static Bags / Carton |
| 规格 | text | e.g. 107*58.5*9(mm) |
| 商标 | text | OEM / Armor lighting |
| 原产地 | text | China |

### Verified custom attribute pairs (name: value, in page order)

Voltage, Wattage (W/M), Color Temperature(CCT), Color Rendering Index(Ra),
Lamp Luminous Efficiency(Lm/W), Light Source, Working Temperature(℃),
LED Type, LEDs/M, Usage, Material, Feature, Working Life, Certification

Pitfall: 发光颜色 standard field DOES exist (IP等级 / 发光颜色 / 应用 are the only
select/checkbox standard fields). Everything technical beyond those 7 is a custom pair.

### Recommended Custom Attributes

Neon Type (360/Flat/Side-lit), Shell Material (Silicone/PVC), Shell Color, Bend Radius, Cutting Unit, Lifespan, UV Resistant, Warranty

### Highlight Themes

1. 360-degree uniform illumination
2. Flexible bending radius
3. Silicone shell (anti-UV, anti-yellowing)
4. IP65/IP67 outdoor use
5. Cuttable at marked intervals
6. RGB / single color / tunable white
7. Energy efficient vs traditional neon
8. No glass, no mercury, no neon gas
9. Easy mounting clips
10. Custom shapes and lengths

### FAQ Themes

1. Minimum bend radius
2. Indoor vs outdoor use
3. Cutting and reconnection
4. Power supply requirements
5. Color options
6. Lifespan vs traditional neon
7. IP rating for outdoor
8. Custom logo and shape
9. MOQ and sample
10. Lead time and shipping

---

## Type 6: Custom Neon Sign

**MIC Category:** Custom Neon Sign
**ARMOR examples:** Custom letter signs, logo signs, event signs

### Recommended Custom Attributes

Sign Type (Letter/Logo/Shape), Backboard (Acrylic/Metal), Mounting (Wall/Hang/Free), Control (On-Off/Dimmer/Remote/App), Color Mode (Single/RGB/Multi), Size Range, Indoor/Outdoor

### Highlight Themes

1. Full customization (text, logo, shape, color)
2. Acrylic backboard options
3. Energy-efficient LED vs glass neon
4. Safe (low voltage, no heat, no gas)
5. Easy wall/hanging installation
6. Remote/dimmer options
7. Indoor and outdoor versions
8. Fast turnaround for events
9. OEM packaging for gift/resale
10. Long lifespan, low maintenance

### FAQ Themes

1. Custom design process (file format, steps)
2. Maximum/minimum size
3. Color options and mixing
4. Indoor vs outdoor differences
5. Mounting methods
6. Power consumption
7. Lead time for custom
8. Sample/mockup before production
9. Packaging for shipping safety
10. MOQ (usually 1 piece)

---

## Quick Reference: Total Fields by Section

| Section | Min Fields | Max Fields | Notes |
|---------|-----------|-----------|-------|
| # 基本信息 | 5 | 5 | Always same |
| # 产品亮点 | 10 | 10 | Always fill all 10 |
| # 产品属性 | 9 std + 0 custom | 9 std + 7 cat + 15 custom | Category adds 0-7 std fields |
| # 规格管理 | 1 group | 5 groups | MIC max 300 combinations |
| # FOB价格设置 | 3 fields (区间价) | 9 fields (阶梯价 4 tiers) | Exactly one mode |
| # 计量单位 | 1 | 1 | Always same |
| # 包裹尺寸 | 5 | 5 | Always: 数量, 长, 宽, 高, 毛重 |
| # 发货效率信息 | 3 (port+1 row) | 7 (port+3 rows) | Always: 港口: Huangpu |
| # 样品单交易设置 | 5 | 5 | Always fill all 5 |
| # 其他信息设置 | 2 | 3 | 支付方式, 产量, (海关编码) |
| # FAQ | 10 pairs | 10 pairs | Always fill all 10 Q&A |

---

## How to Use

1. **Identify product type** from source (page title, URL, model, application)
2. **Look up type** in this table (if type not listed, use Type 1 as base)
3. **Copy field checklist** for Phase 1 (Plan)
4. **Fill fields** using type-specific attribute options and highlight/FAQ themes
5. **Audit** against checklist in Phase 3 (Verify) - all 11 sections, all fields
6. If product spans multiple types (e.g., Type 2 + Type 3), merge both

---

## Update Log

| Date | Update | Source |
|------|--------|--------|
| 2026-06-12 | Initial version: 6 types, full field mapping | User feedback on missing fields |
