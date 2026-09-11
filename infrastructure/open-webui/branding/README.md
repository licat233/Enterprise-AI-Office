# Open WebUI Branding Assets

## Source

`logo-source.svg` is a repository copy of `/Volumes/Work/01_品牌资产/armor logo/彩色 logo icon.svg`. The original source file was not modified.

## Generated files

| File | Use |
| --- | --- |
| `favicon.ico` | Browser favicon; includes 16, 24, 32, 48, and 64 px frames |
| `favicon.svg` | Vector favicon |
| `favicon.png` | 32 px transparent favicon |
| `favicon-dark.png` | 32 px favicon for dark backgrounds; same source artwork because the mark is already visible on dark backgrounds |
| `favicon-96x96.png` | Larger favicon / shortcut icon |
| `logo.png` | Transparent page logo, 512 × 454 px |
| `splash.png` | Transparent light-theme splash artwork, 1024 × 512 px |
| `splash-dark.png` | Transparent dark-theme splash artwork; same source artwork |
| `web-app-manifest-192x192.png` | PWA manifest icon |
| `web-app-manifest-512x512.png` | Large PWA manifest icon |

The supplied SVG is already an independent icon mark, so favicon assets use the full mark without cropping or redesign. PNG assets use transparent backgrounds and preserve the source aspect ratio with safe margins where applicable.

## Regenerating after a logo replacement

Use the replacement SVG as `SRC`, keep `OUT` as this directory, and repeat the local rasterization pipeline:

```sh
SRC="/path/to/replacement.svg"
OUT="infrastructure/open-webui/branding"
TMP="$(mktemp -d /tmp/armor-branding.XXXXXX)"

cp "$SRC" "$OUT/logo-source.svg"
cp "$SRC" "$OUT/favicon.svg"
qlmanage -t -s 2048 -o "$TMP" "$SRC"
magick "$TMP/$(basename "$SRC").png" -alpha on -fuzz 10% \
  -fill none -draw 'color 0,0 floodfill' \
  -draw 'color 1024,1920 floodfill' PNG32:"$TMP/master-transparent.png"

render_square() {
  magick "$TMP/master-transparent.png" -trim +repage -resize "$2x$2" \
    -gravity center -background none -extent "$1x$1" PNG32:"$3"
}
render_logo() {
  magick "$TMP/master-transparent.png" -trim +repage -resize "$3x$3" \
    -gravity center -background none -extent "$1x$2" PNG32:"$4"
}

render_square 32 27 "$OUT/favicon.png"
cp "$OUT/favicon.png" "$OUT/favicon-dark.png"
render_square 96 80 "$OUT/favicon-96x96.png"
render_logo 512 454 430 "$OUT/logo.png"
render_logo 1024 512 430 "$OUT/splash.png"
cp "$OUT/splash.png" "$OUT/splash-dark.png"
render_square 192 150 "$OUT/web-app-manifest-192x192.png"
render_square 512 400 "$OUT/web-app-manifest-512x512.png"
render_square 16 14 "$TMP/favicon-16.png"
render_square 24 20 "$TMP/favicon-24.png"
render_square 32 27 "$TMP/favicon-32.png"
render_square 48 40 "$TMP/favicon-48.png"
render_square 64 53 "$TMP/favicon-64.png"
magick "$TMP/favicon-16.png" "$TMP/favicon-24.png" "$TMP/favicon-32.png" \
  "$TMP/favicon-48.png" "$TMP/favicon-64.png" "$OUT/favicon.ico"
```

Downscale the transparent master to the listed PNG dimensions and assemble the ICO with ImageMagick using 16, 24, 32, 48, and 64 px frames. The generated set was created locally with `qlmanage`, `magick`, `cp`, `identify`, and `xmllint`; no external converter or dependency was added.
