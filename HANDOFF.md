# Handoff
Live host `reports.khamel.com` (Pages project `reports-khamel`, Cloudflare Access app "Reports", Google login, owner
email; `*.pages.dev` addresses also gated). Publish token `reports-pages-publish` (Pages Write only) is in Infra's
vault `secrets/reports-cloudflare.env.encrypted`. The `report` skill on the Mac calls `bin/report`.

Nov 24, 2026, design v2: `tokens.css` is dark first with full-width bands; `DESIGN.md` lists the parts (hero, stats,
cards, ask, steps, flow, timeline); `template/report.html` and `bin/report-from-task` write `header.hero` plus one
`section` for each `h2`. Pages link the shared `/_/tokens.css`, so every page takes the new look when it deploys.
Recheck: serve the content repo locally, open a page in headless Chrome with `--force-dark-mode` at 1440 px and in a
390 px iframe.

Open: reply box + Worker, Factory step that calls `bin/report` automatically, Slack thread link on every Penny note,
light mode not looked at after design v2 (tokens only; the owner uses dark).
