# Infrastructure

This repo is public and holds no secrets. Private paths and IDs stay in the `report` skill and in Infra's vault.

| Fact | Value |
|---|---|
| Live host | `reports.khamel.com`, Cloudflare Pages project `reports-khamel` |
| Access | Cloudflare Access app "Reports": Google login, owner email. The `*.pages.dev` addresses are gated too |
| Content | A private content repo (one `<repo>/<slug>/index.html` for each page, `/_/tokens.css`, the dashboard pages) |
| Publish | `bin/report publish <repo> <slug> <file.html>`: stamp, index, commit, push, `pagecast pages deploy` |
| Caller on the Mac | The `report` skill (`publish.sh`): sets the content path and project, reads the token with `sops` |
| Caller for Factory | `bin/report-from-task` (markdown result in, page out, Slack thread reply) |
| Credential | Token `reports-pages-publish` (Pages Write only) in Infra's vault, `secrets/reports-cloudflare.env.encrypted` |
| Needs on the host | `git`, `python3`, `perl`, `cksum`, `npx` (Pagecast 0.7.0); `markdown` for `report-from-task` |

## Cache

The host serves HTML with `max-age=0` and `/_/tokens.css` with `max-age=14400` (seen Nov 24, 2026). A browser keeps
the stylesheet for 4 hours. `bin/report` therefore writes `?v=<checksum of tokens.css>` on the stylesheet link of
every page; a new stylesheet restamps all pages in one commit that starts with `restyle:`.

## Deploy of a design change

Merge the change, then publish any page with `bin/report`. The publish copies `tokens.css`, restamps all pages and
deploys the whole tree. There is no separate deploy step and no CI deploy.
