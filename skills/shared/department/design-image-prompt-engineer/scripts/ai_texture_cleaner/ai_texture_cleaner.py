"""
AI Texture / Moire Cleaner
批量处理 AI 生成图里的摩尔纹、假纹理、脏噪点、过度锐化细节。

思路：边缘保护降噪 + 轻微去高频纹理 + 细节回补 + 输出对比图
适用：LED 产品图、ESL 产品图、货架灯场景图

Usage:
    python ai_texture_cleaner.py [强度] [路径...] [--no-compare] [--cleanup]

    强度: light | standard | strong (默认 standard)
    路径: 文件或目录，支持多个，省略则处理当前目录
    --no-compare: 不生成对比图
    --cleanup: 删除 _compare 目录下的所有对比图

示例:
    python ai_texture_cleaner.py light photo1.jpg photo2.png
    python ai_texture_cleaner.py strong ./product_images/
    python ai_texture_cleaner.py standard <output-dir>/ai_photos/
    python ai_texture_cleaner.py --cleanup <output-dir>/ai_photos/
"""

import os
import sys
import argparse
import shutil
import cv2
import numpy as np


SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")


def is_image(filename):
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


def collect_files(paths):
    """Collect image files from paths (files and/or directories)."""
    files = []
    for p in paths:
        if os.path.isfile(p) and is_image(p):
            files.append(os.path.abspath(p))
        elif os.path.isdir(p):
            for f in os.listdir(p):
                if is_image(f):
                    files.append(os.path.abspath(os.path.join(p, f)))
        else:
            print(f"  Skipped (not found): {p}")
    return files


def cleanup_compare(paths):
    """Delete _compare subdirectories from given paths."""
    for p in paths:
        if os.path.isdir(p):
            compare_dir = os.path.join(p, "_compare")
            if os.path.isdir(compare_dir):
                shutil.rmtree(compare_dir)
                print(f"  Removed: {compare_dir}")
            else:
                print(f"  No _compare/ in: {p}")


def read_image_unicode(path):
    """Read image with Unicode path support."""
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def write_image_unicode(path, img, quality=95):
    """Write image with Unicode path support."""
    ext = os.path.splitext(path)[1].lower()

    if ext in [".jpg", ".jpeg"]:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    elif ext == ".png":
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
    elif ext == ".webp":
        encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), quality]
    else:
        encode_param = []

    success, encoded_img = cv2.imencode(ext, img, encode_param)

    if success:
        encoded_img.tofile(path)
    else:
        raise RuntimeError(f"Failed to save image: {path}")


def edge_mask(gray):
    """
    Create edge mask to protect important product outlines.
    White = strong edge area (preserve original).
    Black = flat/texture area (apply cleaning).
    """
    edges = cv2.Canny(gray, 60, 160)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    edges = cv2.GaussianBlur(edges, (5, 5), 0)
    mask = edges.astype(np.float32) / 255.0
    return np.expand_dims(mask, axis=2)


def remove_ai_texture(img, strength="standard"):
    """
    Remove AI-style texture artifacts while preserving edges.

    strength:
    - light:    轻微处理，保留更多细节（ESL 屏幕、产品边缘、Logo）
    - standard: 标准处理，适合大部分 AI 产品图（产品主体、磁铁、导电轨道）
    - strong:   强力处理，适合明显摩尔纹/脏纹（LED 发光面、背景墙、远处货架）
    """

    if strength == "light":
        bilateral_d = 5
        bilateral_sigma_color = 30
        bilateral_sigma_space = 30
        blur_radius = 3
        blend_clean = 0.35
        detail_back = 0.35
    elif strength == "strong":
        bilateral_d = 9
        bilateral_sigma_color = 70
        bilateral_sigma_space = 70
        blur_radius = 7
        blend_clean = 0.70
        detail_back = 0.20
    else:  # standard
        bilateral_d = 7
        bilateral_sigma_color = 50
        bilateral_sigma_space = 50
        blur_radius = 5
        blend_clean = 0.55
        detail_back = 0.28

    img_float = img.astype(np.float32) / 255.0

    # 1. Edge-preserving denoise (bilateral filter)
    bilateral = cv2.bilateralFilter(
        img,
        d=bilateral_d,
        sigmaColor=bilateral_sigma_color,
        sigmaSpace=bilateral_sigma_space,
    )

    # 2. Smooth low-frequency version
    low_freq = cv2.GaussianBlur(
        bilateral, (0, 0), sigmaX=blur_radius, sigmaY=blur_radius
    )

    # 3. Extract original detail (high-frequency from original)
    detail = cv2.subtract(
        img, cv2.GaussianBlur(img, (0, 0), sigmaX=blur_radius)
    )

    # 4. Reduce abnormal high-frequency texture
    cleaned = cv2.addWeighted(
        bilateral, 1.0 - blend_clean, low_freq, blend_clean, 0
    )

    # 5. Add a small amount of real-looking detail back
    cleaned = cv2.addWeighted(cleaned, 1.0, detail, detail_back, 0)

    # 6. Protect strong product edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = edge_mask(gray)

    cleaned_float = cleaned.astype(np.float32) / 255.0
    result_float = cleaned_float * (1.0 - mask * 0.65) + img_float * (mask * 0.65)
    return np.clip(result_float * 255.0, 0, 255).astype(np.uint8)


def make_comparison(original, cleaned):
    """Create side-by-side comparison image (left=original, right=cleaned)."""
    h1, w1 = original.shape[:2]
    h2, w2 = cleaned.shape[:2]
    if h1 != h2:
        cleaned = cv2.resize(cleaned, (w2, h1))
    return np.hstack([original, cleaned])


def process_files(file_paths, strength="standard", make_compare=True):
    if not file_paths:
        print("No images found.")
        return

    processed = 0
    for input_path in file_paths:
        directory = os.path.dirname(input_path)
        name, ext = os.path.splitext(os.path.basename(input_path))

        # Output next to input, with _cleaned suffix
        output_path = os.path.join(directory, f"{name}_cleaned{ext}")

        # Compare images go into _compare subfolder (easy to delete later)
        compare_dir = os.path.join(directory, "_compare")
        compare_path = os.path.join(compare_dir, f"{name}_compare{ext}")

        print(f"Processing: {input_path}")

        img = read_image_unicode(input_path)
        if img is None:
            print(f"  Skipped unreadable: {input_path}")
            continue

        cleaned = remove_ai_texture(img, strength=strength)
        write_image_unicode(output_path, cleaned)
        print(f"  → {output_path}")

        if make_compare:
            os.makedirs(compare_dir, exist_ok=True)
            comparison = make_comparison(img, cleaned)
            write_image_unicode(compare_path, comparison)

        processed += 1

    print(f"\nDone. {processed}/{len(file_paths)} images processed.")
    print(f"Cleaned files saved next to originals (_cleaned suffix).")
    if make_compare:
        print(f"Compare images in _compare/ subfolders (delete with --cleanup).")


def main():
    parser = argparse.ArgumentParser(
        description="AI Texture / Moire Cleaner — 批量清理 AI 图片伪影"
    )
    parser.add_argument(
        "strength",
        nargs="?",
        default=None,
        choices=["light", "standard", "strong"],
        help="处理强度: light/standard/strong",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="文件或目录路径（省略=当前目录）",
    )
    parser.add_argument(
        "--no-compare",
        action="store_true",
        help="不生成对比图",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="删除 _compare 目录下的所有对比图",
    )

    args = parser.parse_args()

    # Cleanup mode
    if args.cleanup:
        cleanup_compare(args.paths or ["."])
        return

    # Determine strength
    strength = args.strength
    if strength is None:
        print("AI Texture / Moire Cleaner")
        print("1 = Light      轻微处理，保留更多细节")
        print("2 = Standard   标准处理，适合大部分 AI 产品图")
        print("3 = Strong     强力处理，适合明显摩尔纹/脏纹")
        choice = input("Choose strength [1/2/3], default 2: ").strip()
        if choice == "1":
            strength = "light"
        elif choice == "3":
            strength = "strong"
        else:
            strength = "standard"

    print(f"\nStrength: {strength}")
    files = collect_files(args.paths)
    process_files(files, strength=strength, make_compare=not args.no_compare)


if __name__ == "__main__":
    main()
