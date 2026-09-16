# EAO Open WebUI Branding

This deployment uses the user-provided EAO Logo Source Pack v1.0 as its only logo source. The full source pack is committed under infrastructure/open-webui/branding/source/EAO-logo-source-pack-v1.0/; infrastructure/open-webui/branding/logo-source.svg is the primary EAO wordmark source master.

## Generated and deployed assets

The following ten Open WebUI assets are EAO-branded and are mounted read-only at /app/build/static/<filename>:

- favicon.ico
- favicon.svg
- favicon.png
- favicon-dark.png
- favicon-96x96.png
- logo.png
- splash.png
- splash-dark.png
- web-app-manifest-192x192.png
- web-app-manifest-512x512.png

Mapping: the EAO app icon supplies favicon/ICO/PWA assets; the EAO primary wordmark supplies the transparent page logo and light splash; the EAO dark wordmark supplies the dark splash. The old ARMOR artwork is no longer used.

## Runtime

- Open WebUI: v0.11.3
- Image: ghcr.io/open-webui/open-webui:v0.11.3
- Container: eaio-open-webui
- Runtime branding directory: /Users/Shared/enterprise-ai-office/runtime/OpenWebUI/branding
- Compose project: eaio-openwebui
- Static target: /app/build/static/<filename>
- Data volume: eaio-openwebui_open-webui-data (unchanged)
- Application name: WEBUI_NAME=Enterprise AI Office

Open WebUI copies the frontend static files into its backend static directory during startup. Restart and recreate checks therefore validate both the mounted frontend path and the backend-served /static/ path.

## Recreate procedure

~~~sh
cd /Users/Shared/enterprise-ai-office/runtime/OpenWebUI
/Users/armor/.orbstack/bin/docker compose -p eaio-openwebui -f docker-compose.bootstrap.yml up -d --force-recreate --no-deps open-webui
~~~

Do not run down -v; this task does not alter authentication, users, groups, conversations, Hermes, WeKnora, ports, or networking. When the upstream version changes, re-check its actual static references and startup-copy behavior before reuse.
