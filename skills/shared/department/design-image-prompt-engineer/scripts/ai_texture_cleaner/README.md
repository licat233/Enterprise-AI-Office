# AI Texture / Moire Cleaner

批量处理 AI 生成图里的摩尔纹、假纹理、脏噪点、过度锐化细节。

## 依赖

```bash
pip install opencv-python pillow numpy
```

## 使用

```bash
python3 ai_texture_cleaner.py [强度] [路径...] [--no-compare] [--cleanup]
```

### 参数

| 参数 | 说明 |
|------|------|
| `light` / `standard` / `strong` | 处理强度，省略则交互选择 |
| 路径 | 文件或目录，支持多个，省略则处理当前目录 |
| `--no-compare` | 不生成对比图 |
| `--cleanup` | 删除 `_compare` 目录下的所有对比图 |

### 示例

```bash
# 处理单张图
python3 ai_texture_cleaner.py light photo.jpg

# 处理整个目录
python3 ai_texture_cleaner.py standard <output-dir>/ai_photos/

# 多个文件
python3 ai_texture_cleaner.py strong img1.png img2.jpg img3.webp

# 不生成对比图
python3 ai_texture_cleaner.py standard ./product_images/ --no-compare

# 清理对比图
python3 ai_texture_cleaner.py --cleanup <output-dir>/ai_photos/
```

## 输出逻辑

- **清理后的图**：输出到原文件同目录，文件名加 `_cleaned` 后缀
  - `photo.jpg` → `photo_cleaned.jpg`
- **对比图**：放在原文件同目录的 `_compare/` 子文件夹中
  - `photo.jpg` → `_compare/photo_compare.jpg`

## 清理

用 `--cleanup` 一键删除 `_compare` 目录：
```bash
python3 ai_texture_cleaner.py --cleanup <output-dir>/ai_photos/
```

## 强度选择

| 强度 | 适用场景 | ARMOR 产品对应 |
|------|---------|---------------|
| `light` | 轻微处理，保留更多细节 | ESL 屏幕、产品边缘、Logo、高质量原图 |
| `standard` | 标准处理，大部分 AI 产品图 | 产品主体、磁铁、导电轨道、传感器 |
| `strong` | 强力处理，明显摩尔纹/脏纹 | LED 发光面、背景墙、远处货架 |

## 工作流

```
python3 批量清理 → 挑选效果好的图 → Photoshop 局部蒙版修复 → 轻微锐化产品边缘
python3 ai_texture_cleaner.py --cleanup ./   ← 清理对比图
```
