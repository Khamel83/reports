# Handoff

Checkpoint: Nov 24, 2026, 11:05 PM PT. Host and deploy path are in `INFRA.md`; the credential name and location are in Infra's private records.

## Done and live

- Design v2 (#6): dark first, full-width bands, parts in `DESIGN.md`. Accepted live on Nov 24, 2026.
- Dashboard (#6): `/` by day, `/_/by-repo/` by repo. `bin/report` runs `bin/report-index` at each publish.
- The five pages published before design v2 have the hero + section layout and a `report:kind` tag; words unchanged.
- Stylesheet version (#9): `bin/report` stamps `?v=<checksum>` on the stylesheet link in every page. Live from the
  branch since 8:39 PM PT (content commit `fe5ec7f`); all seven live pages carry `?v=2496485213`.
- Rule "owner-readable output, plans included, goes out as a report link": README and the publishing skill.

## In flight

- R-4 reply box (#10, stacked on #9). **Live and verified:** Worker `reports-reply` has its inbox secret since Nov 24,
  2026, 10:50 PM PT (deployed from this branch), after the Factory intake change for `reports` items and the Dispatch
  exclusion were deployed. Nov 24, 10:52 PM PT the owner pressed "Works" on `/reports/r4-reply-box/`; Factory made one
  task, DO-894, with the page link, choice and text, at 10:55 PM PT. Way back: delete the Worker's inbox secret
  (binding name in `bin/reply-deploy`); every reply then answers "Not confirmed".
  Known effect: the first R-4 publish put the box in a "report" commit, so five older pages show Nov 24 10:00 PM PT
  on the dashboard (same day). `bin/report` now adds the box in the "restyle" commit.

- #9 waits for the reviewer bot. After the merge: `git checkout main && git pull --ff-only`, delete the branch.

## Recheck

- Look: serve the content repo locally (`python3 -m http.server` in a copy that has `_/tokens.css`), open a page in
  headless Chrome with `--force-dark-mode` at 1440 px and in a 390 px iframe.
- Live: the host needs the owner's Google login; `curl -s -o /dev/null -w "%{http_code}" https://reports.khamel.com/`
  gives 302 without it. In the owner's browser, each page must link `/_/tokens.css?v=<checksum>`.
- A design change must be tested in a browser that already has the old stylesheet, or by the `?v=` value in the page.

Open work is in `TODO.md`.
