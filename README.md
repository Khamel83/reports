# reports

One standard for every report an AI agent (Claude Code, Codex, Grok, OpenCode, anything) sends its owner.
Public on purpose: this repo holds the rules, the look and the tools. It holds **no reports and no secrets**.

## The standard

- **Scope:** everything the owner is meant to read is a report: results, plans, research, reviews, comparisons,
  status pages. Give the owner the full `https://` link. Never give a relative path such as `docs/plan.md`: it does
  not say which repo it is in and it does not open on a phone.
- **URL:** `https://<host>/<repo>/<slug>/` — `<repo>` is the project that produced it, `<slug>` is short and readable
  (`desk-a-vs-desk-b`); use a ticket or date when no good name exists.
- **File:** one self-contained `index.html` per report at `<repo>/<slug>/index.html`. No external scripts or images.
- **Look:** link `/_/tokens.css` (from `tokens.css` here) and start from `template/report.html`. Read `DESIGN.md`.
  The publisher adds `?v=<checksum>` to that link in every page, because browsers keep the stylesheet for hours.
- **Metadata:** the `<meta name="report:*">` tags in the template: `kind` (one lowercase word: `report`, `plan`,
  `research`, `review`, `status`), `repo`, `ticket`, `created`.
- **Dashboard:** `https://<host>/` lists every page, newest first, by day; `/_/by-repo/` lists them by repo. Each row
  shows kind, repo, title, link and the time of its last change (a publish of identical HTML keeps the date).
  `bin/report-index` writes both pages at each publish.
- **Honesty:** mark anything you did not verify. Say what you could not find.
- **Access:** the host must be behind an access gate. Reports hold personal facts.

Any model can write a plain HTML file, so any model can follow this. No model-specific format is used.

## Publish

```sh
bin/report publish <repo> <slug> <file.html>
```

It copies the file into the content tree, commits it to the **private** content repo, and deploys the whole tree to
Cloudflare Pages with [Pagecast](https://github.com/Amal-David/pagecast)'s `pages deploy` (MIT, telemetry off).
Settings come from the environment, never from this repo:

| Variable | Meaning |
|---|---|
| `REPORTS_CONTENT_DIR` | Local clone of the private content repo |
| `REPORTS_PROJECT` | Cloudflare Pages project name |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Pages-edit token; the owner's vault supplies it |

## Bed reports and the morning report

The `bed` skill (on the owner's Mac) is for work that runs while the owner sleeps. The session asks all its
questions first, then works alone and publishes a bed report at `<repo>/bed-<date>/` (or `<repo>/bed-<date>-<topic>/`
for a second one in the same repo that night), where `<date>` is the date of the next 5 AM. A bed report has `report:kind` `bed`, a `<meta name="bed:status">` of `done`, `working` or
`blocked`, a `.lede`, `.stats` and one `.card.ask` for each thing the owner must do.

At 5:00 AM PT the morning job makes one page, `reports/morning-<date>/`, that thinks across all bed reports of that
date. Each bed report sees only its own project; the morning report finds what they do not see: one chain of causes
under several reports, two sessions that did the same work, a change in one project that affects another, facts that
do not agree, and one merged list of owner actions. `bin/report-morning prompt <content-dir> <date>` prints the full
text of every bed report with those instructions. The job sends it as one tool-free request through G2K
(`g2k-review`) and gives the answer to `bin/report-morning build <content-dir> <date> <out.html> --analysis <file>`,
which keeps only a small set of tags, the stylesheet's classes and safe links, and adds one card for each project.
If the model call fails, the page still goes out with a note and the project cards. `bin/report-index` copies the newest morning report to `/morning/` and puts a
link to it at the top of the dashboard. No bed reports: no page. The morning page is a snapshot at 5 AM. A session still working then is in it with
status `working` (each session publishes its first bed report when it starts), and its card links to the live bed
report; changes after 5 AM show only there. A session that starts after 5 AM has the next day's date, so it is in the
next morning report.

## Reply

Every report page ends with a reply box (the dashboard pages, `/` and `/_/`, have none): a text field, one button for each answer in
`<meta name="report:choices" content="A|B">` (optional, at most 6), and **Send**. It is a plain form with no
script. Each decision card (`.card.ask`) gets its own answer: one pick for each choice in its `data-choices` and a note
field. These fields belong to the same form (HTML `form` attribute), so one **Send** sends all answers. The Worker
keeps them as `answers` (question, choice, note) and also writes them into `text` under "Decisions:". `bin/report` adds the box to every report page at each publish (`bin/report-reply-box`).

The form posts to `/_/reply`. The reply Worker (`worker/reply.js`) saves the reply as one JSON item
(`schema` `reports.reply.v1`, `reply_id`, `repo`, `slug`, `page_url`, `ticket`, `title`, `choice`, `text`, `sent_at`,
`sender`) in the owner's inbox with client name `reports`, then shows a "sent" page (its link carries an HMAC of the inbox receipt, so only a saved reply shows "Reply sent"). `reply_id` is a hash of page,
choice and text. **Read replies:** `bin/report-replies [<repo> [<slug>]]` prints every reply to your pages from the inbox. The session that wrote a page reads its replies here; it does not wait for Factory. It needs `REPORTS_DROP_API` (the inbox read API; the value is in the `report` skill) and runs on demand only, with a cached cursor. Factory's inbox intake (in the Factory repo, not here) keys its tasks on that hash, so it opens one task for each reply and the same reply sent twice counts once. This is permanent: the same choice and text sent to the same page later (also after a republish) opens no second task; change the text to send it again. When the
inbox does not confirm it, the page says "Not confirmed" and shows the text again. The host's access gate covers
`/_/reply` too; the Worker refuses a post without the gate's identity header or from another site. Deploy: `bin/reply-deploy` (settings in its header, from the environment; it needs its own token with Workers Scripts and Workers Routes write, not the Pages-edit token).

## Rules for this repo

Never commit a token, a key, a report, a vault path, a stored credential's name, or a private hostname/ID (tailnet or
provider-default addresses). CI fails a commit that does (`scripts/check.sh`); environment variable names such as
`CLOUDFLARE_API_TOKEN` are the interface and stay.
