<!-- janitor:begin:todo -->
- Open items are in "Open" below (R-1 to R-8); this block adds none.
<!-- janitor:end:todo -->

## Open

- [ ] R-1 Factory calls `bin/report-from-task` automatically at the end of a task (today a session runs it by hand).
- [ ] R-2 Agents on Homelab and OCI can publish a report or plan directly (the `report` skill is on the Mac only).
- [ ] R-3 Pages from the visual-explainer plugin publish in this design (they do not link `/_/tokens.css`, so
      `bin/report` refuses them).
- [ ] R-5 Slack thread link for every report that answers a voice note.
- [ ] R-8 Bed skill and 5 AM morning report (owner ask, Nov 24, 2026): https://github.com/Khamel83/reports/pull/11,
      merged Nov 25, 2026, 12:12 AM PT (reviewer PASS). Owner decision: no #inbox message; the newest morning report is
      at `/morning/` and on top of the dashboard. A launchd run from main at 12:16 AM PT published
      `/reports/morning-2026-11-25/` (exit 0). The first scheduled run (Nov 25, 5:00 AM PT) started on time but hung 30
      minutes in its first `git pull`: on the Mac's project disk a hard link hung for every program. I stopped it and ran
      the same script by hand; `/morning/` was published 5:54 AM PT. The job now writes git objects without hard links
      and stops after 30 minutes (details in the `bed` skill). Nov 25 (owner): the morning page must think across all bed reports, not list them;
      `bin/report-morning prompt` and `build --analysis` with one G2K request. Open: one scheduled 5 AM run that ends
      with "live:" and has the analysis.
- [ ] R-6 Look at light mode and at a real phone after design v2 (the owner uses dark mode; tokens only).

## Done

- [x] R-4 Reply box on each page, with a Worker that sends the reply to the agent: https://github.com/Khamel83/reports/pull/10,
      merged Nov 24, 2026, 11:50 PM PT. Live since 10:50 PM PT; first real reply made one Factory task at 10:55 PM PT.

- [x] R-7 Version the stylesheet link at publish: https://github.com/Khamel83/reports/pull/9. Done in effect: live from the
      branch since Nov 24, 2026, 8:39 PM PT (content commit `fe5ec7f`). Merged Nov 24, 2026, 11:30 PM PT
      with the one-publish-at-a-time lock.

- [x] Design v2, dashboard, `report:kind`, plans as reports: https://github.com/Khamel83/reports/pull/6, live
      Nov 24, 2026, 8:32 PM PT, accepted by the owner.
- [x] Shared agent rule for report links (in Infra, merged).

