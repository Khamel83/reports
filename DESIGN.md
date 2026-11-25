# Design

Dark first: the owner reads in dark mode. Deep navy page, one cobalt hero band, a coral colour only for
"this needs you". Heavy condensed capitals for `h1`, `h2` and big numbers; plain sans for text. Full-width bands,
one 1180 px column, text lines held to 70 characters. Light mode and print follow the system.
Everything comes from `tokens.css`: add no colours, fonts, scripts, images or inline styles.

A report is a designed page, not an article. Do not send a column of paragraphs and tables. For each block of
content, pick the part that shows its shape: counts become `.stat`, parallel items become a `.grid` of `.card`,
owner decisions become `.card.ask`, a sequence becomes `.steps` or `.timeline`, a pipeline becomes `.flow`.

## Page

`<main>` holds `<header class="hero">`, then one `<section>` for each `h2`, then `<footer class="meta">`.
Sections get alternate band colours automatically. Start from `template/report.html`.

## Parts

| Part | Markup | Use for |
|---|---|---|
| Hero | `.kicker` (repo · ticket · date), `h1`, `.lede` | The answer in one sentence |
| Numbers | `<div class="stats"><div class="stat"><b>4</b>wait on you</div>…</div>` | 2 to 4 numbers, in the hero or a section |
| Verdict | `<div class="card verdict"><strong>…</strong><p>…</p></div>` | The recommendation, first section |
| Needs you | `<div class="card ask"><h3>…</h3><p>…</p></div>`, link as `<a class="btn">` | Each decision or input the owner owes |
| Cards | `<div class="grid">` of `<div class="card"><h3>…</h3><p>…</p></div>` | Parallel items, options, findings |
| Two columns | `<div class="cols"><div>…</div><div>…</div></div>` | Two things side by side |
| Table | `table` with `th` row | Comparisons with 3 or more columns |
| Status | `<span class="tag">`, with `.good` `.warn` `.bad` | A state word in a table or card |
| Progress | `<progress value="4" max="11"></progress>` | Share done |
| Tracker | `<ol class="steps"><li class="done">Name <span>Done</span></li>…` (`.done`, `.now`, none) | Stages of one job |
| Flow | `<div class="flow"><div><h3>…</h3><p>…</p></div>…</div>` | 2 to 4 boxes joined in order |
| Timeline | `<ol class="timeline"><li class="done"><b>M0</b><h3>…</h3><p>…</p></li>…` | Milestones or dates in a row |
| Rows | `<ul class="rows"><li><span class="tag">plan</span><span>repo</span><span><a href="…">Title</a><small>full link</small></span><time>Nov 24</time></li>…` | A list of links with a label, a source and a date |
| Reply box | Added by `bin/report`; answer buttons from `<meta name="report:choices" content="A\|B">` | Owner answers. Do not write your own form |
| Caveat | `<p class="note">` | Limits of the evidence |
| Footer | `<footer class="meta">` | Author, date, sources, what is unverified |

A plan is a report. Put `plan` in the `report:kind` meta tag and the kicker, the goal in the `.lede`, the steps in `.steps` or `.timeline`,
and each decision the owner must make in a `.card.ask`.

Write order: answer first, then evidence, then what to do next. Short sentences. No filler.
Check the page at 1440 px and 390 px in dark mode before you publish.
