<!-- janitor:begin:recent -->
- Source `1610c99fec9e663c8503facd276c1975003a840f` (2026-11-24 subject): Design v2 (dark first, bands, layout parts) and the dashboard at `/` (#6). This subject is past activity, not a live-site check.
- Owner decisions recorded 2026-11-24 still stand in the project record: dark-first band layout in `DESIGN.md` (narrow warm-paper column retired); reader-facing material, including plans, goes out as a report link, not a relative path (also in the shared agent rules in Infra, merged, and the Mac `report` skill); `reports.khamel.com/` is the dashboard of all pages, newest first, by day or by repo, with kind, repo, title, link, and date.
- Earlier subjects on this history, not rechecked here: deploy from the content directory (`a0d83f229f8084f5706142128a2022d3d4d24378`); report-from-task publisher and exact 32-hex ID check (`dc3d5cf276adb8b16cf351f12979f77f50e43292`); swipeable tables and tighter phone layout (`01345f5ac18d57d45e8f7c1a13999fb0321fda10`); reports standard, design tokens, template, publisher, and secrets check (`cc72ecbcf60de057ba9cdd23c7733d6e99c4e254`). Deployment and runtime effect of these commits are not in this evidence.
<!-- janitor:end:recent -->

## Owner decisions

- Nov 24, 2026: reports are dark first and use the band layout in `DESIGN.md` (wide bands, heavy condensed capitals,
  stat tiles, cards). The owner reads in dark mode only. The old narrow warm-paper column is retired.
- Nov 24, 2026: everything the owner is meant to read, plans included, goes out as a report link. No relative paths.
  The same rule is in the shared agent rules (Khamel83/infra#2421, merged) and in the `report` skill on the Mac.
- Nov 24, 2026: `reports.khamel.com/` is a dashboard of all pages, newest first, by day or by repo, with kind, repo,
  title, link and date for each page.
