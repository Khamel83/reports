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

## Reply

Every page ends with a reply box: a text field, one button for each answer in
`<meta name="report:choices" content="A|B">` (optional, at most 6), and **Send**. It is a plain form with no
script. `bin/report` adds the box to every page at each publish (`bin/report-reply-box`).

The form posts to `/_/reply`. The reply Worker (`worker/reply.js`) saves the reply as one JSON item
(`schema` `reports.reply.v1`, `reply_id`, `repo`, `slug`, `page_url`, `ticket`, `title`, `choice`, `text`, `sent_at`,
`sender`) in the owner's inbox with client name `reports`, then shows a "sent" page. `reply_id` is a hash of page,
choice and text, so the same reply sent twice counts once. Factory's inbox intake opens one Factory task for each reply. When the
inbox does not confirm it, the page says "Not confirmed" and shows the text again. The host's access gate covers
`/_/reply` too; the Worker refuses a post without the gate's identity header or from another site. Deploy: `bin/reply-deploy` (settings in its header, from the environment).

## Rules for this repo

Never commit a token, a key, a report, or a private hostname/ID. CI fails a commit that does (`scripts/check.sh`).
