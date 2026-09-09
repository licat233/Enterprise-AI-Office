# Product Category → Standard Attributes Map

Each Made-in-China product category has its own set of standard attributes (dropdowns, checkboxes, and required text fields). This file caches the known attributes per category so the agent does not need to re-investigate every time.

**How to use:** Before generating product info, look up the product category in this file. If the category is listed, use its standard attributes directly. If the category is missing, investigate the MIC product upload page for that category, then add the results here.

**How to investigate a new category:**
1. Open the MIC product upload page for the target category
2. Inspect all `.J-stand-prop` blocks in the `# 产品属性` section
3. Record each attribute's Chinese label, type (select/checkbox/text), and known options
4. Add the entry below in the same format

---

## LED Neon Light / LED 霓虹灯带

**Verified from backend edit page 2026-08-13 (HM-N1220V24-DMX512-RGB).**
**This category has only 7 standard attributes — 认证/功率/电压 are NOT standard fields here,
they exist as custom name/value pairs.**

| 属性 | 类型 | 已知选项 |
|------|------|----------|
| IP等级 | select | IP20, IP33, IP44, IP54, IP55, IP65, IP66, IP67, IP68, Other |
| 发光颜色 | select | Single Color, Changeable Color, Other |
| 应用 | checkbox | Home, Outdoor, Commercial, Other |
| 运输包装 | text | Anti-Static Bags, Carton |
| 规格 | text | e.g. 107*58.5*9(mm) |
| 商标 | text | OEM, Armor lighting |
| 原产地 | text | China |

Verified custom pairs used in this category (name: value): Voltage, Wattage (W/M),
Color Temperature(CCT), Color Rendering Index(Ra), Lamp Luminous Efficiency(Lm/W),
Light Source, Working Temperature(℃), LED Type, LEDs/M, Usage, Material, Feature,
Working Life, Certification.

**Pitfall:** do NOT force the 9 universal standard attrs (认证/功率/电压) onto this
category — the plugin would fail to match them; output them as custom pairs instead.

---

## LED Strip Lights / LED 灯带

| 属性 | 类型 | 已知选项 |
|------|------|----------|
| 认证 | checkbox | CE, RoHS, FCC, EMC, LVD, CCC, FDA, GS, SAA, VDE |
| 功率 | select | `<6W`, `6-10W`, `11-15W`, `16-20W`, `21-30W`, `>30W` |
| 发光颜色 | select | White, Warm White, Red, Blue, Green, Yellow, Changeable |
| 电压 | select | 12V, 24V, 36V, 110V, 220V |
| 防护等级 | select | IP33, IP44, IP54, IP65, IP66, IP67, IP68 |
| 运输包装 | text | Carton, etc. |
| 规格 | text | product dimensions |
| 商标 | text | brand name |
| 原产地 | text | China, etc. |

Required fields: 认证, 功率, 发光颜色, 电压, 防护等级, 运输包装, 规格, 商标, 原产地

---

## Electronic Shelf Labels (ESL) / 电子价签

| 属性 | 类型 | 已知选项 |
|------|------|----------|
| 适用门店 | checkbox | Electronics Store, Convenience Store, Supermarket, Pharmacies, Other |
| 安装方式 | select | Slot-in, Magnetic Mount, Adhesive Back, Power Supply by The Guide Rail Support, Other |
| 内容支持 | select | QR Code Display, Multi-language Text, Price + Barcode |
| 显示颜色 | select | Full Color, 3-Color (BWR), Black & White |
| 分辨率 | select/custom | e.g. 1280*800 |
| 屏幕尺寸 | select/custom | e.g. 10.1 |
| 显示技术 | select | LCD, LED Segment, E-Ink Carta |
| 认证 | checkbox | CE, RoHS, FCC, etc. |
| 功率 | select | `<6W`, etc. |
| 发光颜色 | select | White, etc. |
| 电压 | select | 12V, etc. |
| 防护等级 | select | IP33–IP68 |
| 运输包装 | text | |
| 规格 | text | |
| 商标 | text | |
| 原产地 | text | |

Required fields: 认证, 功率, 发光颜色, 电压, 防护等级, 运输包装, 规格, 商标, 原产地

---

## LED Display / LED 显示屏

| 属性 | 类型 | 已知选项 |
|------|------|----------|
| 认证 | checkbox | CE, RoHS, FCC, etc. |
| 功率 | select | `>30W`, etc. |
| 发光颜色 | select | Changeable, etc. |
| 电压 | select | 220V, 110V, etc. |
| 防护等级 | select | IP43, IP65, etc. |
| 运输包装 | text | Carton |
| 规格 | text | product dimensions |
| 商标 | text | Armor lighting |
| 原产地 | text | China |

Required fields: 认证, 功率, 发光颜色, 电压, 防护等级, 运输包装, 规格, 商标, 原产地

---

## Template for New Category

```markdown
## [Category Name] / [中文名]

| 属性 | 类型 | 已知选项 |
|------|------|----------|
| 认证 | checkbox | ... |
| 功率 | select | ... |
| 发光颜色 | select | ... |
| 电压 | select | ... |
| 防护等级 | select | ... |
| 运输包装 | text | ... |
| 规格 | text | ... |
| 商标 | text | ... |
| 原产地 | text | ... |

Required fields: 认证, 功率, 发光颜色, 电压, 防护等级, 运输包装, 规格, 商标, 原产地
```
