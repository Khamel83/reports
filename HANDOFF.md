# Handoff

Checkpoint: Nov 24, 2026, 8:50 PM PT. Host and deploy path are in `INFRA.md`; the credential name and location are in Infra's private records.

## Done and live

- Design v2 (#6): dark first, full-width bands, parts in `DESIGN.md`. Accepted live on Nov 24, 2026.
- Dashboard (#6): `/` by day, `/_/by-repo/` by repo. `bin/report` runs `bin/report-index` at each publish.
- The five pages published before design v2 have the hero + section layout and a `report:kind` tag; words unchanged.
- Stylesheet version (#9): `bin/report` stamps `?v=<checksum>` on the stylesheet link in every page. Live from the
  branch since 8:39 PM PT (content commit `fe5ec7f`); all seven live pages carry `?v=2496485213`.
- Rule "owner-readable output, plans included, goes out as a report link": README and the publishing skill.

## In flight

- Bed night Nov 24 to 25 (goal: land #7, #9, #10, #11). Report: https://reports.khamel.com/reports/bed-2026-11-25/.
  At 11:06 PM PT #9 and #10 had pushes from their own sessions (less than 1 hour old), so they are left alone until quiet.
  Recheck: `gh pr list`; `for b in stylesheet-version feat/r4-reply-box; do git log -1 --format=%cd origin/$b; done`.

- Bed (R-8): PR #11 from branch `bed` (stacked on #9). The Mac parts (the `bed` skill, its morning job at 5:00 AM PT,
  the log and the macOS disk-access note) are installed on the Mac and described in the skill itself, not here. No
  #inbox message (owner decision): the newest morning report is at `/morning/` and on top of the dashboard. The
  reports checkout on the Mac must stay on `bed`, or on `main` after the merge, because the job runs
  `bin/report-morning` from it.

- #9 waits for the reviewer bot. After the merge: `git checkout main && git pull --ff-only`, delete the branch.

## Recheck

- Look: serve the content repo locally (`python3 -m http.server` in a copy that has `_/tokens.css`), open a page in
  headless Chrome with `--force-dark-mode` at 1440 px and in a 390 px iframe.
- Live: the host needs the owner's Google login; `curl -s -o /dev/null -w "%{http_code}" https://reports.khamel.com/`
  gives 302 without it. In the owner's browser, each page must link `/_/tokens.css?v=<checksum>`.
- A design change must be tested in a browser that already has the old stylesheet, or by the `?v=` value in the page.

Open work is in `TODO.md`.
