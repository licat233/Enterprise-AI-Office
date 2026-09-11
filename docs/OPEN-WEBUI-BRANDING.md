# Open WebUI Branding

This deployment uses the user-provided 彩色 logo icon.svg as the only brand source. The repository source master is [infrastructure/open-webui/branding/logo-source.svg](../infrastructure/open-webui/branding/logo-source.svg); the original source file is preserved outside this repository.

## Generated assets

| File | Purpose |
| --- | --- |
| favicon.ico | Browser favicon with common 16/24/32/48/64 px frames |
| favicon.svg | Vector favicon |
| favicon.png, favicon-dark.png, favicon-96x96.png | Transparent browser/shortcut icons |
| logo.png | Transparent full page logo |
| splash.png, splash-dark.png | Centered light/dark loading artwork |
| web-app-manifest-192x192.png, web-app-manifest-512x512.png | PWA manifest icons |

The source SVG is already an independent icon mark, so the favicon set uses the complete mark without cropping or redesign. The dark variants currently use the same source artwork because the white mark remains visible on dark backgrounds.

## Runtime integration

The pinned Open WebUI v0.11.3 service mounts each asset read-only at /app/build/static/<filename>. At startup, this release copies the frontend static files into its backend static directory, so the same assets are served through /static/ after startup. WEBUI_NAME=Enterprise AI Office is set; this release appends the upstream attribution and displays Enterprise AI Office (Open WebUI).

The public Compose blueprint uses OPEN_WEBUI_BRANDING_DIR:-./branding. The protected enterprise runtime uses the absolute repository path on armor@MacStudio.local. The named open-webui-data volume is unchanged.

## Replacing the logo

1. Replace the repository assets while keeping the exact filenames and transparency/safe-margin rules.
2. Validate the SVG and PNG/ICO files locally, then compare checksums against the repository.
3. From the protected runtime directory, recreate only Open WebUI:

~~~sh
cd /Users/Shared/enterprise-ai-office/runtime/OpenWebUI
/Users/armor/.orbstack/bin/docker compose -p eaio-openwebui -f docker-compose.bootstrap.yml up -d --force-recreate --no-deps open-webui
~~~

Do not run down -v; preserve the named data volume. After an asset change, verify /static/ URLs and use a hard refresh/private window if a browser cache shows the previous logo. If the pinned Open WebUI version changes, re-check its static paths and startup-copy behavior before reusing these mounts.

## Generation tooling

The asset set was generated locally with qlmanage, ImageMagick magick, cp, identify, and xmllint; no new dependency or generation script was added. The exact rasterization recipe is kept in infrastructure/open-webui/branding/README.md.
