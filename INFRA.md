# Infrastructure

This repo is public. It holds no secrets, no token or credential names, no vault paths, no private IDs, no tailnet
or provider-default hostnames and no report content. Those stay in the `report` skill on the owner's machine and in
Infra's private repo. The public host `reports.khamel.com` and the names of the owner's systems (Factory, Homelab,
OCI) are public facts, not secrets: the host is behind the access gate.

| Fact | Value |
|---|---|
| Live host | `reports.khamel.com`, a Cloudflare Pages project |
| Access | Cloudflare Access: Google login, owner only. The provider's default addresses are gated too |
| Content | A private content repo (one `<repo>/<slug>/index.html` for each page, `/_/tokens.css`, the dashboard pages) |
| Publish | `bin/report publish <repo> <slug> <file.html>`: stamp, index, commit, push, `pagecast pages deploy` |
| Caller on the Mac | The `report` skill (`publish.sh`): sets the content path and project, reads the token with `sops` |
| Caller for Factory | `bin/report-from-task` (markdown result in, page out, Slack thread reply) |
| Morning report | launchd on the Mac at 5:00 AM PT runs the `bed` skill's `morning.sh`: `bin/report-morning`, then publish |
| Latest morning report | `/morning/` (a copy that `bin/report-index` writes at each publish) |
| Credential | One token with Pages write permission only, in Infra's vault. Its name and path are in Infra |
| Needs on the host | `git`, `python3`, `perl`, `cksum`, `cmp`, `find`, `npx` (Pagecast 0.7.0); `markdown` for `report-from-task` |

## Cache

The host serves HTML with `max-age=0` and `/_/tokens.css` with `max-age=14400` (seen Nov 24, 2026). A browser keeps
the stylesheet for 4 hours. `bin/report` therefore writes `?v=<checksum of tokens.css>` on the stylesheet link of
every page; a new stylesheet restamps all pages in one commit that starts with `restyle:`.

## Deploy of a design change

Merge the change, then publish any page with `bin/report`. The publish copies `tokens.css`, restamps all pages and
deploys the whole tree. There is no separate deploy step and no CI deploy.
