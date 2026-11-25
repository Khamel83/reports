<!-- janitor:begin:recent -->
- `a0d83f229f8084f5706142128a2022d3d4d24378`: Run the deploy from the content directory (Pagecast writes .pagecast/ in cwd)
- `dc3d5cf276adb8b16cf351f12979f77f50e43292`: Add report-from-task publisher; narrow ID check to exact 32-hex
- `01345f5ac18d57d45e8f7c1a13999fb0321fda10`: Make tables swipeable and tighten layout on phones
- `cc72ecbcf60de057ba9cdd23c7733d6e99c4e254`: Add reports standard, design tokens, template, publisher and secrets check
<!-- janitor:end:recent -->

## Owner decisions

- Nov 24, 2026: reports are dark first and use the band layout in `DESIGN.md` (wide bands, heavy condensed capitals,
  stat tiles, cards). The owner reads in dark mode only. The old narrow warm-paper column is retired.
- Nov 24, 2026: everything the owner is meant to read, plans included, goes out as a report link. No relative paths.
  The same rule is in the shared agent rules (in Infra, merged) and in the `report` skill on the Mac.
- Nov 24, 2026: `reports.khamel.com/` is a dashboard of all pages, newest first, by day or by repo, with kind, repo,
  title, link and date for each page.
- Nov 24, 2026: the owner accepted design v2. A browser can hold an old stylesheet; cause and fix are in `INFRA.md`
  (Cache).
