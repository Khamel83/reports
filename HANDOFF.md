# Handoff

Checkpoint: Nov 25, 2026, 5:54 AM PT. Host and deploy path are in `INFRA.md`; the credential name and location are in Infra's private records.

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
  it there, because the job and every publish run from it. The Nov 25 5:00 AM PT run hung (a hard link hung on the
  Mac's project disk, for every program); I stopped it and published `/morning/` by hand at 5:54 AM PT. The job now
  avoids hard links and stops after 45 minutes. The owner must restart the Mac (or reconnect the disk) to clear the
  hang; the report asks him. Nov 25: owner asked for a combined analysis, not a list; the job now sends all bed
  reports to G2K (`bin/report-morning prompt`, then `build --analysis`); a launchd test call to G2K worked. The Nov 25
  page was written by hand in that form. Next check: the Nov 26 5:00 AM PT run (log has "analysis:" and ends with
  "live:", not "TIMEOUT").

- R-4 reply box (#10). **Live and verified:** Worker `reports-reply` has its inbox secret since Nov 24,
  2026, 10:50 PM PT (deployed from this branch), after the Factory intake change for `reports` items and the Dispatch
  exclusion were deployed. Nov 24, 10:52 PM PT the owner pressed "Works" on `/reports/r4-reply-box/`; Factory made one
  task with the page link, choice and text, at 10:55 PM PT. Way back: delete the Worker's inbox secret
  (binding name in `bin/reply-deploy`); every reply then answers "Not confirmed".
  Known effect: the first R-4 publish put the box in a "report" commit, so five older pages show Nov 24 10:00 PM PT
  on the dashboard (same day). `bin/report` now adds the box in the "restyle" commit.

- R-9 idea ledger plan (Nov 25, 2026, about 7 PM PT): https://reports.khamel.com/reports/idea-ledger/. Plan only, no code.
  It waits for the owner's button reply on the page (goes to Factory as a task). Records: PR #18.
  Worktree note: `.worktrees/bed` is now on branch `idea-ledger-plan`; the old local branch `bed-synthesis` (PR #15,
  closed) is still there. Cleanup after #18 merges: `git -C .worktrees/bed checkout --detach origin/main` and delete
  both local branches.

- Nov 25, 2026, about 8 PM PT (idea-ledger session):
  - Done: plan https://reports.khamel.com/reports/idea-ledger/ (owner decisions in CONTEXT). #20 (answer buttons on
    each decision card) merged after the reviewer's PASS. Factory made DO-905 from the owner's reply 9 minutes after it
    was sent; a comment there says this session handled it.
  - Nov 26, 2026 (reply fix session): #19 merged (`bin/report-replies`, tested on the live inbox: 3 replies read).
    The owner deployed the reply Worker from main with `bin/reply-deploy` (version 0ba1c6b5, secret kept); it now
    keeps decision-card picks. Next check: a reply with a pick on `g2k/gateway-research-review` shows in
    `bin/report-replies g2k gateway-research-review`. Open: a pick still needs the Send button (#21 item 1).
  - Worktree `.worktrees/bed` is detached at origin/main plus this records branch; local branches `report-replies`,
    `ask-buttons`, `idea-ledger-plan`, `bed-synthesis` can be deleted.

## Recheck

- Look: serve the content repo locally (`python3 -m http.server` in a copy that has `_/tokens.css`), open a page in
  headless Chrome with `--force-dark-mode` at 1440 px and in a 390 px iframe.
- Live: the host needs the owner's Google login; `curl -s -o /dev/null -w "%{http_code}" https://reports.khamel.com/`
  gives 302 without it. In the owner's browser, each page must link `/_/tokens.css?v=<checksum>`.
- A design change must be tested in a browser that already has the old stylesheet, or by the `?v=` value in the page.

Open work is in `TODO.md`.

## November 25 session status

The combined morning analysis change merged; the earlier proposal was closed as superseded. A source merge does not by itself prove a scheduled report ran.

GitHub readback November 25: [#15](https://github.com/Khamel83/reports/pull/15): closed; [#16](https://github.com/Khamel83/reports/pull/16): merged. Recheck before action.
