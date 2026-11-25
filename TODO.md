<!-- janitor:begin:todo -->
- Open items are in "Open" below (R-1 to R-6); this block adds none.
<!-- janitor:end:todo -->

## Open

- [ ] R-1 Factory calls `bin/report-from-task` automatically at the end of a task (today a session runs it by hand).
- [ ] R-2 Agents on Homelab and OCI can publish a report or plan directly (the `report` skill is on the Mac only).
- [ ] R-3 Pages from the visual-explainer plugin publish in this design (they do not link `/_/tokens.css`, so
      `bin/report` refuses them).
- [ ] R-4 Reply box on each page, with a Worker that sends the reply to the agent.
- [ ] R-5 Slack thread link for every report that answers a voice note.
- [ ] R-8 Bed skill and 5 AM morning report (owner ask, Nov 24, 2026). Source: `bin/report-morning`, tests, docs
      (https://github.com/Khamel83/reports/pull/11). Mac: skill `~/.agents/skills/bed`, launchd `com.khamel.bed-morning`.
      Full launchd run Nov 24, 10:59 PM PT for 2026-11-25: published `reports/morning-2026-11-25` (2 bed reports:
      factory, reports), then `NOT SENT` (exit 5, no grant yet). Open: (a) the #inbox send waits on the Drop grant, Khamel83/drop#359; (b) the
      first real 5 AM run with a delivered receipt; (c) the grant expires after 30 days, renewal through Drop.
- [ ] R-6 Look at light mode and at a real phone after design v2 (the owner uses dark mode; tokens only).

## Done

- [x] R-7 Version the stylesheet link at publish: https://github.com/Khamel83/reports/pull/9. Done in effect: live from the
      branch since Nov 24, 2026, 8:39 PM PT (content commit `fe5ec7f`). Merge and deploy are separate: the
      merge makes this source what the next `bin/report` publish runs from main.

- [x] Design v2, dashboard, `report:kind`, plans as reports: https://github.com/Khamel83/reports/pull/6, live
      Nov 24, 2026, 8:32 PM PT, accepted by the owner.
- [x] Shared agent rule for report links (in Infra, merged).

