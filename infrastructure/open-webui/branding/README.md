# EAO Open WebUI Branding Assets

## Source

The only brand source is the user-provided EAO Logo Source Pack v1.0. The complete pack is preserved at infrastructure/open-webui/branding/source/EAO-logo-source-pack-v1.0/. The root logo-source.svg is an exact copy of EAO-logo-primary.svg from that pack.

The previous ARMOR logo assets have been replaced; no ARMOR artwork is used by this Open WebUI branding set.

## Asset mapping

| Open WebUI asset | EAO source / treatment | Purpose |
| --- | --- | --- |
| favicon.svg | EAO-app-icon.svg | Vector browser favicon |
| favicon.png, favicon-dark.png, favicon-96x96.png, favicon.ico | EAO-app-icon.svg | Browser and shortcut icons; ICO has 16/24/32/48/64 px frames |
| logo.png | EAO-logo-primary.svg, white canvas removed | Transparent page logo |
| splash.png | EAO-logo-primary.svg on white | Light loading screen |
| splash-dark.png | EAO-logo-dark.svg on Graphite | Dark loading screen |
| web-app-manifest-192x192.png, web-app-manifest-512x512.png | EAO-app-icon.svg | PWA icons |

The app icon keeps the supplied Graphite rounded-square treatment with a white A and AI Teal point. The favicon dark variant is intentionally the same app icon because it is already visible on dark surfaces.

## Replacing the logo

Replace the source pack and regenerate the exact filenames above. Keep the EAO source files unchanged and do not modify the original supplied files in place. The local conversion used macOS Quick Look only when needed for SVG preview, and ImageMagick magick with /System/Library/Fonts/ArialHB.ttc for rasterization and ICO assembly. No new dependency or generation script was added.

After copying the regenerated files to the protected runtime branding directory, recreate only Open WebUI:

~~~sh
cd /Users/Shared/enterprise-ai-office/runtime/OpenWebUI
/Users/armor/.orbstack/bin/docker compose -p eaio-openwebui -f docker-compose.bootstrap.yml up -d --force-recreate --no-deps open-webui
~~~

Preserve the named open-webui-data volume; never use down -v. Recheck /static/ URLs and use a hard refresh if a browser cache shows an older logo. Revalidate the static paths and startup-copy behavior before changing the pinned Open WebUI version.
