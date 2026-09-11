# MIC Category Attribute Differences

## Critical Rule

**Different MIC categories have COMPLETELY DIFFERENT product attribute fields. Never assume — always extract from current page.**

This reference documents known attribute fields for categories ARMOR has used. When uploading a new product, always verify the actual fields on the current page.

---

## Category: Electronic Price Tag (电子价签)

### Sub-category: LCD Price Tag

| Field | Type | Options | Typical Selection |
|-------|------|---------|-------------------|
| 适用门店 (Store Type) | checkbox | Supermarket; Electronics Store; Convenience Store; Pharmacies; Other | Supermarket; Electronics Store; Convenience Store |
| 安装方式 (Installation) | dropdown | Slot-in; Wall-Mounted; Magnetic Mount; Adhesive Back; Other | Slot-in |
| 内容支持 (Content Support) | dropdown | Price + Barcode; QR Code Display; Multi-language Text; Image Display; Other | Price + Barcode |
| 显示颜色 (Display Color) | dropdown | Full Color; 3-Color (BWR); Black & White; Other | Full Color |
| 分辨率 (Resolution) | dropdown + custom | 800x480; 1024x600; 1280x800; 1920x1080; Other | Other → 1280x800 |
| 屏幕尺寸 (Screen Size) | dropdown + custom | <5"; 5-7"; 7-10"; 10-15"; >15"; Other | Other → 10.1" |
| 显示技术 (Display Technology) | dropdown | LCD; E-Ink Carta; LED Segment; Other | LCD |

### Sub-category: ESL (Ink Price Tag)

| Field | Type | Options | Typical Selection |
|-------|------|---------|-------------------|
| 适用门店 | checkbox | Same as above | Supermarket |
| 安装方式 | dropdown | Slot-in; Magnetic; Adhesive; Other | Slot-in |
| 内容支持 | dropdown | Price; Price + Barcode; QR Code; Other | Price + Barcode |
| 显示颜色 | dropdown | Black & White; 3-Color (BWR); 3-Color (BWRY); Other | 3-Color (BWR) |
| 屏幕尺寸 | dropdown + custom | 1.54"; 2.13"; 2.66"; 2.9"; 3.5"; Other | Per product |
| 显示技术 | dropdown | E-Ink Carta; E-Ink Pearl; Other | E-Ink Carta |

---

## Category: LCD Display (LCD显示屏)

| Field | Type | Options | Typical Selection |
|-------|------|---------|-------------------|
| 屏幕尺寸 (Screen Size) | dropdown + custom | <15"; 15-20"; 20-30"; 30-40"; 40-50"; 50-60"; >60"; Other | Per product |
| 应用场景 (Application Scenario) | checkbox | Indoor; Outdoor; Semi-Outdoor; Other | Indoor |
| 用途 (Usage) | checkbox | Advertising Display; Information Display; Monitor; TV; Other | Advertising Display |
| 宽屏 (Widescreen) | dropdown | Widescreen; Standard; Other | Widescreen |
| 最佳分辨率 (Optimal Resolution) | dropdown + custom | 1920x1080; 1280x800; 1024x768; Other | Other → 1280x800 |
| 类型 (Type) | dropdown | TFT; IPS; OLED; Other | TFT |
| 响应时间 (Response Time) | dropdown | <5ms; 5-10ms; 10-16ms; 16-25ms; >25ms | 16ms (for 10-25ms range) |
| 接口类型 (Interface Type) | dropdown + custom | HDMI; VGA; DVI; DisplayPort; USB; Other | Other → Wi-Fi |
| 显示颜色 (Display Colors) | dropdown | 16.7M; 1.07B; Other | 16.7M |
| 特征 (Feature) | checkbox | Touch Display; LED Backlight; With Remote Control; Support TV Function; 3D Display; Other | With Remote Control; Support TV Function |

**Note**: Do NOT check "LED Backlight Display" for LCD products — LCD and LED are different technologies.

---

## Category: AD Player (广告机)

| Field | Type | Options | Typical Selection |
|-------|------|---------|-------------------|
| 应用 (Application) | checkbox | Indoor AD Player; Outdoor AD Player; Bus/Car AD Player; Semi Outdoor AD Player; Other | Indoor + Other |
| 屏幕尺寸 (Screen Size) | dropdown + custom | <15"; 15-20"; 20-30"; 30-40"; 40-50"; 50-60"; >60"; Other | Other → Custom size |
| 安装方式 (Installation) | dropdown | Vertical; Wall-Mounted; Combined; Other | Other → Mounting Bracket |
| 类型 (Type) | dropdown | Touch Screen Panel; Network Version; Standalone Version; Bluetooth; Other | Other → Shelf Edge Digital Signage |
| 触摸屏类型 (Touch Screen) | dropdown | Resistive; Capacitive; Infrared; Surface Acoustic Wave; Piezoelectric; Other | Other → Non-Touch |
| 屏幕显示技术 (Display Tech) | dropdown | LCD; LED; Other | LCD |
| 接口类型 (Interface) | dropdown + custom | VGA; DVI; USB; HDMI; Other | Other → TF Card, Micro-USB OTG, Type-C |
| 可否遥控 (Remote Control) | dropdown | With Remote Control; Without Remote Control; Other | With Remote Control |
| 操作系统 (OS) | dropdown | LINUX; Windows; Android; Other | Other → Android 11 |
| 是否定制 (Customizable) | dropdown | Customized; Non-Customized; Other | Customized |

---

## Category: LED Display (LED显示屏)

| Field | Type | Options | Typical Selection |
|-------|------|---------|-------------------|
| 应用 (Application) | checkbox | Indoor; Outdoor; Semi-Outdoor; Rental; Fixed Installation; Other | Indoor; Fixed Installation |
| 像素间距 (Pixel Pitch) | dropdown + custom | P1.25; P1.56; P1.875; P2; P2.5; P3; P4; P5; P6; P8; P10; Other | Per product |
| 屏幕尺寸 (Screen Size) | dropdown + custom | <1㎡; 1-5㎡; 5-10㎡; 10-20㎡; >20㎡; Other | Other → Custom diameter |
| 显示技术 (Display Technology) | dropdown | SMD LED; COB LED; DIP LED; Other | SMD LED |
| 亮度 (Brightness) | dropdown | <500 CD/㎡; 500-1000 CD/㎡; 1000-2000 CD/㎡; 2000-5000 CD/㎡; >5000 CD/㎡ | 500-1000 CD/㎡ |
| 刷新率 (Refresh Rate) | dropdown | <960Hz; 960-1920Hz; 1920-3840Hz; >3840Hz | 1920-3840Hz |
| 防护等级 (Protection Level) | dropdown | IP20; IP43; IP54; IP65; IP67; IP68 | IP43 (indoor); IP65 (outdoor) |
| 安装方式 (Installation) | dropdown | Wall-Mounted; Hanging; Floor Standing; Rental Stacking; Other | Per application |
| 是否定制 (Customizable) | dropdown | Customized; Non-Customized; Other | Customized |

---

## Category: LED Lighting / Strip (LED灯/灯带)

| Field | Type | Options | Typical Selection |
|-------|------|---------|-------------------|
| 认证 (Certification) | checkbox | CE; RoHS; FCC; EMC; LVD; CCC; FDA; GS; SAA; VDE | CE; RoHS; FCC |
| 功率 (Power) | dropdown | <6W; 6-10W; 11-15W; 16-20W; 21-30W; >30W | Per product |
| 发光颜色 (Light Color) | dropdown | White; Warm White; Red; Blue; Green; Yellow; Changeable; RGB | Per product |
| 电压 (Voltage) | dropdown | 12V; 24V; 36V; 110V; 220V; Other | 12V or 24V |
| 防护等级 (Protection Level) | dropdown | IP33; IP44; IP54; IP65; IP66; IP67; IP68 | IP65 |
| 运输包装 (Transport Packing) | text | Carton; Wooden Box; Pallet; Other | Carton |
| 规格 (Specification) | text | Size, volume, composition | Per product |
| 商标 (Trademark) | text | Brand name | ARMOR |
| 原产地 (Origin) | text | Country | China |

---

## Universal Fields (All Categories)

These fields appear in ALL categories after the category-specific attributes:

| Field | Type | Notes |
|-------|------|-------|
| 运输包装 (Transport Packing) | text input | Carton, Wooden Box, etc. |
| 规格 (Specification) | text input | Size, volume, composition |
| 商标 (Trademark) | text input | Brand name |
| 原产地 (Origin) | text input | Country |

---

## "Other" → Custom Input Pattern

When any dropdown has "Other" option:
1. Select "Other" from dropdown
2. **Check if a custom input field appears next to the dropdown**
3. Fill the custom input with the specific value
4. Common fields requiring custom input: 分辨率, 屏幕尺寸, 接口类型

---

## Tips for New Categories

When encountering a category not listed here:
1. Run `agent-browser snapshot` to extract all fields
2. Identify each field's type (dropdown, checkbox, text input)
3. Document the options for dropdown/checkbox fields
4. Note which fields require "Other" + custom input
5. Add findings to this reference file
