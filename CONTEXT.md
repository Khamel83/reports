<!-- janitor:begin:recent -->
### Owner decisions
- 2026-11-24: Reports are dark first and use the band layout in `DESIGN.md`. The old narrow warm-paper column is retired.
- 2026-11-24: Everything the owner is meant to read, including plans, goes out as a report link. No relative paths (Khamel83/infra#2421, merged).
- 2026-11-24: `reports.khamel.com/` is a dashboard of all pages, newest first, by day or by repo.

### Recent source activity (past commits, not open tasks)
- 054be465b3aa45b5e03e3d688d4ed67fcd283dc9: Handoff recorded design v2 and the dashboard as live, and recorded open gaps (#8).
- 1610c99fec9e663c8503facd276c1975003a840f: Design v2 (dark first, bands, layout parts) and the dashboard at / (#6).
- a0d83f229f8084f5706142128a2022d3d4d24378: Deploy runs from the content directory.
- dc3d5cf276adb8b16cf351f12979f77f50e43292: Added report-from-task publisher and narrowed the ID check to exact 32-hex.
- 01345f5ac18d57d45e8f7c1a13999fb0321fda10: Tables are swipeable and the layout is tighter on phones.
- cc72ecbcf60de057ba9cdd23c7733d6e99c4e254: Added reports standard, design tokens, template, publisher and secrets check.

Source commit: 16a226033e1953fb0f90cac4e9c94608af73e9de

Deployed runtime state is not verified by this remote evidence.
<!-- janitor:end:recent -->

## Owner decisions

- Nov 24, 2026: reports are dark first and use the band layout in `DESIGN.md` (wide bands, heavy condensed capitals,
  stat tiles, cards). The owner reads in dark mode only. The old narrow warm-paper column is retired.
- Nov 24, 2026: everything the owner is meant to read, plans included, goes out as a report link. No relative paths.
  The same rule is in the shared agent rules (Khamel83/infra#2421, merged) and in the `report` skill on the Mac.
- Nov 24, 2026: `reports.khamel.com/` is a dashboard of all pages, newest first, by day or by repo, with kind, repo,
  title, link and date for each page.
