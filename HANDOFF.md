# Handoff

Checkpoint: Nov 25, 2026, 12:17 AM PT. Host and deploy path are in `INFRA.md`; the credential name and location are in Infra's private records.

## Done and live

- Design v2 (#6): dark first, full-width bands, parts in `DESIGN.md`. Accepted live on Nov 24, 2026.
- Dashboard (#6): `/` by day, `/_/by-repo/` by repo. `bin/report` runs `bin/report-index` at each publish.
- The five pages published before design v2 have the hero + section layout and a `report:kind` tag; words unchanged.
- Stylesheet version and one-publish-at-a-time lock (#9): merged Nov 24, 2026, 11:30 PM PT after the reviewer's PASS.
  `bin/report` stamps `?v=<checksum>` on the stylesheet link in every page.
- Janitor docs (#7): merged 11:19 PM PT after the reviewer's PASS.
- Reply box (#10): merged 11:50 PM PT. Bed skill and morning report (#11): merged Nov 25, 12:12 AM PT; it also fixed
  main CI, red since #10 (the reply Worker's stalled-inbox test ended early on Node 22). Main CI passed on the #11
  merge commit `f2af4c9`: https://github.com/Khamel83/reports/actions/runs/45574338718.
- Rule "owner-readable output, plans included, goes out as a report link": README and the publishing skill.

## In flight

- Bed night Nov 24 to 25: all four PRs (#7, #9, #10, #11) merged. Report: https://reports.khamel.com/reports/bed-2026-11-25/.
- Bed (R-8): the Mac parts (the `bed` skill, its morning job at 5:00 AM PT, the log and the macOS disk-access note)
  are installed on the Mac and described in the skill, not here. The reports checkout on the Mac is on `main`; keep
  it there, because the job and every publish run from it. Next check: the 5 AM run on Nov 25 (`/morning/` changes,
  log ends with "live:").

- R-4 reply box (#10). **Live and verified:** Worker `reports-reply` has its inbox secret since Nov 24,
  2026, 10:50 PM PT (deployed from this branch), after the Factory intake change for `reports` items and the Dispatch
  exclusion were deployed. Nov 24, 10:52 PM PT the owner pressed "Works" on `/reports/r4-reply-box/`; Factory made one
  task with the page link, choice and text, at 10:55 PM PT. Way back: delete the Worker's inbox secret
  (binding name in `bin/reply-deploy`); every reply then answers "Not confirmed".
  Known effect: the first R-4 publish put the box in a "report" commit, so five older pages show Nov 24 10:00 PM PT
  on the dashboard (same day). `bin/report` now adds the box in the "restyle" commit.

## Recheck

- Look: serve the content repo locally (`python3 -m http.server` in a copy that has `_/tokens.css`), open a page in
  headless Chrome with `--force-dark-mode` at 1440 px and in a 390 px iframe.
- Live: the host needs the owner's Google login; `curl -s -o /dev/null -w "%{http_code}" https://reports.khamel.com/`
  gives 302 without it. In the owner's browser, each page must link `/_/tokens.css?v=<checksum>`.
- A design change must be tested in a browser that already has the old stylesheet, or by the `?v=` value in the page.

Open work is in `TODO.md`.
