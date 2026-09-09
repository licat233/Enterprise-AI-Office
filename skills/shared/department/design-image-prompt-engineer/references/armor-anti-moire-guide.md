# AI 图片伪影避免指南 — ARMOR 产品专用

> 针对 LED 灯珠、ESL 电子价签、货架照明等高频密集结构产品的 AI 图片生成防伪影策略。

---

## 问题本质

AI 生成图片中常见的"摩尔纹样伪影"并非真正光学摩尔纹，而是多种 AI 图像伪影的混合体：

1. **细密重复纹理异常** — 布料、金属网、LED 灯珠、货架孔洞、百叶窗、栅格、屏幕像素出现波纹、彩色干扰线、锯齿感
2. **过度锐化假细节** — AI "猜"出不存在的细节，放大后显假
3. **高频纹理混乱** — 拉丝金属、织物、电子屏幕、灯带灯珠等密集结构生成不稳定重复图案
4. **压缩/二次放大纹理干扰** — 平台压缩、截图、放大、锐化会加剧伪影

---

## 核心原则

> **降低 AI 需要"猜"的高频细节密度，比堆负面提示词有效得多。**

- 产品放大、背景简化
- 减少密集重复结构
- 避免过度锐化
- 不要让 AI 同时处理多个高频细节区域

---

## 一、画面设计策略

### 1. 避免远距离密集结构

远距离看到很多细小灯珠、孔洞、金属网、货架层板边缘时，AI 容易生成干扰纹。

✅ 推荐：
```
close-up product photography, large product in frame, clear main subject, simple background
```

❌ 避免：
```
many tiny LED beads, dense grid, fine mesh, repeated small holes, distant shelf details
```

### 2. 减少重复纹理描述

货架、金属网、LED 灯珠阵列等重复元素过多时，AI 会"编乱"。

✅ 推荐：
```
smooth metal shelf surface, clean matte material, minimal repeated patterns
```

❌ 避免强调：
```
perforated metal, mesh texture, honeycomb pattern, dense LED array
```

### 3. 产品主体占画面比例要大

产品越小，AI 越需要猜细节；产品越大，结构越稳定。

✅ 推荐：
```
medium close-up of one magnetic LED strip light attached under a dark grey iron shelf, product clearly visible, simple shelf structure
```

❌ 避免：
```
wide view of a supermarket aisle with many shelves and small LED strips
```

---

## 二、正面提示词模板

### 通用防伪影关键词

```
clean surface texture, smooth realistic material, natural edge detail, accurate product geometry, clear product structure, controlled sharpness, realistic commercial photography, no artificial micro-texture
```

### LED 产品专用

```
continuous soft LED glow, diffused light surface, no visible individual LED pixels, no dot-matrix pattern
```

> 关键技巧：用 `diffused light surface` 替代对灯珠的直接描述，避免 AI 生成密集点阵伪影。

### ESL 电子价签专用

```
smooth matte plastic frame, large clear E Ink screen, clean product geometry, readable screen content
```

---

## 三、负面提示词模板

### 通用负面提示词

```
moire pattern, interference pattern, aliasing, wavy lines, noisy texture, over-sharpened details, fake micro details, repetitive artifacts, pixel noise, distorted grid, crawling texture, rainbow artifacts
```

### LED 产品额外排除

```
dense mesh, perforated metal, dot matrix, visible LED pixels, dense LED array
```

### ESL 产品额外排除

```
screen interference, distorted text, unreadable text, noisy screen, pixel grid
```

---

## 四、ARMOR 产品推荐提示词

### 磁吸 LED 货架灯

**正面提示词：**
```
photorealistic commercial product photography of an ultra-thin magnetic LED strip light attached directly to the underside of a dark grey iron retail shelf. The LED light has a smooth continuous diffused luminous surface, no visible individual LED beads, clean matte metal and plastic materials, large product in frame, simple modern retail shelf environment, controlled sharpness, natural edge detail, clean surface texture, professional studio lighting, high-end B2B product presentation.
```

**负面提示词：**
```
moire pattern, interference pattern, aliasing, wavy lines, noisy texture, over-sharpened details, fake micro details, repetitive artifacts, pixel noise, distorted grid, rainbow artifacts, dense mesh, perforated metal, dot matrix, visible LED pixels, cluttered background, cartoon, illustration, text overlay, people, watermark, logo
```

### ESL 电子价签

**正面提示词：**
```
photorealistic close-up product photography of electronic shelf labels attached to a clean dark grey metal retail shelf edge. Large clear E Ink screen, smooth matte plastic frame, simple shelf background, minimal repeated patterns, clean product geometry, natural edge detail, controlled sharpness, realistic commercial lighting.
```

**负面提示词：**
```
moire pattern, screen interference, pixel noise, aliasing, wavy lines, rainbow artifacts, fake micro details, over-sharpened texture, dense grid, distorted text, unreadable text, noisy screen, cartoon, illustration, watermark
```

---

## 五、生成参数建议

- **降低锐化** — 不要使用过强的 sharpness / clarity / detail enhancement
- **避免过强 upscaler** — 过度放大会放大伪影
- **不要一次生成超复杂场景** — 分步生成更可控
- **先生成干净构图，再局部修细节**
- **产品图用 close-up / medium close-up**
- **背景尽量简洁**，避免密集货架纹理
- **不要让画面同时出现** 灯珠 + 金属网 + 屏幕 + 货架孔洞

---

## 六、后期处理方案

### 轻微降噪

Photoshop / Lightroom / Topaz / Camera Raw：
- `reduce noise, reduce color noise, reduce texture`
- 重点不是强力磨皮，而是降低高频干扰

### 降低局部锐化

问题区域处理：
- 降低 Texture
- 降低 Clarity
- 轻微 Gaussian Blur
- 局部降噪
- 修复画笔覆盖异常纹理

### 避免二次压缩

- 原图输出更高分辨率
- 不要反复截图保存
- 不要反复 JPG 压缩
- 发布前导出高质量 JPG 或 PNG
- 社媒图按平台尺寸提前裁好，避免平台大幅缩放

---

## 七、推荐工作流

```
第一步：先生成干净主体图
  → 只放一个产品，背景简单，避免复杂细节

第二步：再生成应用场景图
  → 场景不要太远，不要塞满货架和小物品

第三步：局部修图
  → 产品结构错了用局部重绘，不要整张重生

第四步：后期轻微降噪 + 降锐化
  → 特别检查灯面、屏幕、金属边缘、货架孔洞

第五步：最终导出前检查 100% 放大图
  → 100% 看起来有波浪纹、彩色干扰、假纹理，发布后会更明显
```

---

## 关键提示词速查

| 场景 | 推荐关键词 |
|------|-----------|
| LED 表面 | `smooth diffused luminous surface, no visible individual LED pixels` |
| 金属材质 | `clean matte material, controlled sharpness` |
| 纹理控制 | `minimal repeated patterns, no artificial micro-texture` |
| 边缘质量 | `natural edge detail, accurate product geometry` |
| 整体品质 | `realistic commercial photography, clean surface texture` |

---

*Created: 2026-06-11 | Source: ARMOR AI image generation workflow discussion*
*Applicable platforms: Midjourney, Stable Diffusion, Flux, ComfyUI, DALL-E*

---

## 八、批量后处理脚本

### 脚本位置

```
scripts/ai_texture_cleaner/ai_texture_cleaner.py
```

### 依赖安装

```bash
pip install opencv-python pillow numpy
```

### 使用方法

```bash
python3 ai_texture_cleaner.py [强度] [路径...] [--no-compare] [--cleanup]
```

| 参数 | 说明 |
|------|------|
| `light` / `standard` / `strong` | 处理强度 |
| 路径 | 文件或目录，支持多个，省略则处理当前目录 |
| `--no-compare` | 不生成对比图 |
| `--cleanup` | 删除 `_compare` 目录下的所有对比图 |

### 输出逻辑

- **清理后**：输出到原文件同目录，文件名加 `_cleaned` 后缀
- **对比图**：放在原文件同目录的 `_compare/` 子文件夹中（用 `--cleanup` 一键删除）

### 完整工作流

```
Python 批量清理 → 挑选效果好的图 → Photoshop 局部蒙版修复 → 轻微锐化产品边缘
```

> ⚠️ 不要对最终图再次强锐化，否则摩尔纹和假纹理可能被放大。
