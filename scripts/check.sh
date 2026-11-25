#!/usr/bin/env bash
# Fail on secret-like strings, report files, or private IDs in this public repo.
set -euo pipefail
bad=$(git ls-files | grep -v -E '^(scripts/check.sh|\.github/)' | xargs grep -n -I -E '(AKIA[0-9A-Z]{16}|xox[bap]-[0-9A-Za-z-]{10,}|ghp_[0-9A-Za-z]{30,}|BEGIN [A-Z ]*PRIVATE KEY|CLOUDFLARE_API_TOKEN=[^ $]|[a-z0-9-]+\.(pages\.dev|ts\.net|workers\.dev)|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.(com|net|org|io|dev)|\\b[0-9a-f]{32}\\b)' || true)
[ -z "$bad" ] || { echo "secret-like content:"; echo "$bad"; exit 1; }
git ls-files | grep -E '\.env($|\.)|\.encrypted$|^[a-z0-9._-]+/[a-z0-9-]+/index\.html$' | grep -v '^template/' && { echo "report or secret file committed"; exit 1; } || true
