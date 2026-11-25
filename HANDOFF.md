# Handoff

Checkpoint: Nov 24, 2026, 8:50 PM PT. Host, deploy path and credential location are in `INFRA.md`.

## Done and live

- Design v2 (#6): dark first, full-width bands, parts in `DESIGN.md`. The owner saw it live and accepted it
  ("MUCH better", Nov 24, about 8:40 PM PT).
- Dashboard (#6): `/` by day, `/_/by-repo/` by repo. `bin/report` runs `bin/report-index` at each publish.
- The five pages published before design v2 have the hero + section layout and a `report:kind` tag; words unchanged.
- Stylesheet version (#9): `bin/report` stamps `?v=<checksum>` on the stylesheet link in every page. Live from the
  branch since 8:39 PM PT (content commit `fe5ec7f`); all seven live pages carry `?v=2496485213`.
- Rule "owner-readable output, plans included, goes out as a report link": README, the `report` skill on the Mac,
  and the shared agent rules (Khamel83/infra#2421, merged).

## In flight

- R-4 reply box (#10, stacked on #9). Live from the branch since Nov 24, 2026, about 10:15 PM PT: all pages have the
  box and the Worker answers on `/_/reply*` behind the access gate (no login: 302).
  **Paused on purpose:** the Worker has no inbox secret, so every reply answers "Not confirmed" and shows the text
  again. Reason: the installed Factory intake moves past `reports` items, so a reply sent now would be lost.
  Trigger: the Factory intake change (Khamel83/factory#648) deployed. Restore: `bin/reply-deploy` with the inbox
  token set (names, vault paths and exact steps are in Infra's TODO, "A2UI trial and reports R-4"). Then the owner
  presses "Works" on `/reports/r4-reply-box/`; check one Factory task with the page link. Decide by Nov 27, 2026.
  Known effect: the first R-4 publish put the box in a "report" commit, so five older pages show Nov 24 10:00 PM PT
  on the dashboard (same day). `bin/report` now adds the box in the "restyle" commit.

- #9 waits for the reviewer bot. After the merge: `git checkout main && git pull --ff-only`, delete the branch.
- The shared rule from infra#2421 was not in `~/.agents/shared-rules.md` on the Mac at 8:50 PM PT. Infra's rules
  sync installs it. Check: `grep -c "report link" ~/.agents/shared-rules.md` (expect 1).

## Recheck

- Look: serve the content repo locally (`python3 -m http.server` in a copy that has `_/tokens.css`), open a page in
  headless Chrome with `--force-dark-mode` at 1440 px and in a 390 px iframe.
- Live: the host needs the owner's Google login; `curl -s -o /dev/null -w "%{http_code}" https://reports.khamel.com/`
  gives 302 without it. In the owner's browser, each page must link `/_/tokens.css?v=<checksum>`.
- A design change must be tested in a browser that already has the old stylesheet, or by the `?v=` value in the page.

Open work is in `TODO.md`.
