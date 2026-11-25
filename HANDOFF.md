# Handoff
Live host `reports.khamel.com` (Pages project `reports-khamel`, Cloudflare Access app "Reports", Google login, owner
email; `*.pages.dev` addresses also gated). Publish token `reports-pages-publish` (Pages Write only) is in Infra's
vault `secrets/reports-cloudflare.env.encrypted`. The `report` skill on the Mac calls `bin/report`.

Nov 24, 2026, design v2: `tokens.css` is dark first with full-width bands; `DESIGN.md` lists the parts (hero, stats,
cards, ask, steps, flow, timeline); `template/report.html` and `bin/report-from-task` write `header.hero` plus one
`section` for each `h2`. Pages link the shared `/_/tokens.css`, so every page takes the new look when it deploys.
Dashboard: `bin/report` runs `bin/report-index` at each publish. It writes `/` (by day) and `/_/by-repo/` (by repo)
from each page's `report:kind` meta tag, folder, `<title>` and last commit time in the content repo.
Recheck: serve the content repo locally, open a page in headless Chrome with `--force-dark-mode` at 1440 px and in a
390 px iframe.

Live since Nov 24, 2026, 8:32 PM PT (content commit `a711dea`): the new look, the dashboard and the five old pages in
the hero + section layout with a `report:kind` tag. Seen in the owner's Chrome at `/` and `/float/whats-left/`.
The shared agent rule "owner-readable output goes out as a report link" merged as Khamel83/infra#2421; it was not yet
in `~/.agents/shared-rules.md` on the Mac at 8:35 PM PT (Infra's rules sync installs it).

Open: the `report` skill and its publish path exist on the Mac only (Homelab and OCI agents reach reports through
Factory); pages from the visual-explainer plugin do not link `/_/tokens.css`, so `bin/report` refuses them;
Open: reply box + Worker, Factory step that calls `bin/report` automatically, Slack thread link on every Penny note,
light mode not looked at after design v2 (tokens only; the owner uses dark).
