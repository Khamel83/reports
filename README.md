# reports

One standard for every report an AI agent (Claude Code, Codex, Grok, OpenCode, anything) sends its owner.
Public on purpose: this repo holds the rules, the look and the tools. It holds **no reports and no secrets**.

## The standard

- **Scope:** everything the owner is meant to read is a report: results, plans, research, reviews, comparisons,
  status pages. Give the owner the full `https://` link. Never give a relative path such as `docs/plan.md`: it does
  not say which repo it is in and it does not open on a phone.
- **URL:** `https://<host>/<repo>/<slug>/` — `<repo>` is the project that produced it, `<slug>` is short and readable
  (`ioniq-5-vs-6-vs-egolf`); use a ticket or date when no good name exists.
- **File:** one self-contained `index.html` per report at `<repo>/<slug>/index.html`. No external scripts or images.
- **Look:** link `/_/tokens.css` (from `tokens.css` here) and start from `template/report.html`. Read `DESIGN.md`.
- **Metadata:** the `<meta name="report:*">` tags in the template (repo, ticket, created).
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

## Rules for this repo

Never commit a token, a key, a report, or a private hostname/ID. CI fails a commit that does (`scripts/check.sh`).
