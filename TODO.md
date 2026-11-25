<!-- janitor:begin:todo -->
- No explicit open TODO items are established by the supplied published evidence. Commit summaries describe past activity, not open tasks.
<!-- janitor:end:todo -->

## Open

- [ ] R-1 Factory calls `bin/report-from-task` automatically at the end of a task (today a session runs it by hand).
- [ ] R-2 Agents on Homelab and OCI can publish a report or plan directly (the `report` skill is on the Mac only).
- [ ] R-3 Pages from the visual-explainer plugin publish in this design (they do not link `/_/tokens.css`, so
      `bin/report` refuses them).
- [ ] R-4 Reply box on each page, with a Worker that sends the reply to the agent. Source in this PR; live after
      deploy, the Factory intake change and the Dispatch exclusion (see HANDOFF.md).
- [ ] R-5 Slack thread link for every report that answers a voice note.
- [ ] R-6 Look at light mode and at a real phone after design v2 (the owner uses dark mode; tokens only).

## Done

- [x] R-7 Version the stylesheet link at publish: https://github.com/Khamel83/reports/pull/9. Done in effect: live from the
      branch since Nov 24, 2026, 8:39 PM PT (content commit `fe5ec7f`). The merge of #9 only moves the source to main.

- [x] Design v2, dashboard, `report:kind`, plans as reports: https://github.com/Khamel83/reports/pull/6, live
      Nov 24, 2026, 8:32 PM PT, accepted by the owner.
- [x] Shared agent rule for report links: https://github.com/Khamel83/infra/pull/2421 (merged).

