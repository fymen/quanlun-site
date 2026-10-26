#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
args=(--gc --minify)
# Cloudflare Pages 的生产域名以 CF_PAGES_URL 为准，不覆盖 Hugo 源配置。
if [[ "${CF_PAGES:-}" == 1 ]]; then
  args+=(--baseURL "/")
  if [[ "${CF_PAGES_BRANCH:-main}" != main ]]; then
    export HUGO_ENV=preview
  fi
fi
if [[ "${NETLIFY:-}" == true ]]; then
  if [[ "${CONTEXT:-}" == production ]]; then
    site_url="${URL:?Netlify URL is required}"
  else
    site_url="${DEPLOY_PRIME_URL:?Netlify preview URL is required}"
  fi
  args+=(--baseURL "$site_url/")
  if [[ "${CONTEXT:-}" != production ]]; then
    args+=(--buildDrafts --noBuildLock)
  fi
fi
hugo "${args[@]}" "$@"
