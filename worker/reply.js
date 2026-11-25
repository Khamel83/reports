// Reply Worker: /_/reply on the reports host. See README.md ("Reply").
//
// POST: a reply box form from a report page. The Worker saves it as one JSON item in the owner's inbox (a Drop
// capture, client "reports") and answers 303 to the "sent" page, so a browser refresh does not send it twice.
// Factory's intake reads new inbox items and opens one task for each reply.
// GET ?sent=<id>&back=<path>: the "sent" page.
//
// Cloudflare Access protects the whole host, so every request here comes from the owner's signed-in browser.
// env.DROP: service binding to the inbox Worker. env.DROP_INTAKE_TOKEN: its intake token (a Worker secret).

const NAME = /^[a-z0-9][a-z0-9._-]{0,63}$/;
const SLUG = /^[a-z0-9][a-z0-9-]{0,127}$/;
const ID = /^[A-Za-z0-9-]{1,80}$/;
const LIMITS = { text: 4000, choice: 80, ticket: 64, title: 200 };

export function buildReply(form, { host, sender, now, id }) {
  const get = (key) => String(form.get(key) ?? "").trim();
  const repo = get("repo");
  const slug = get("slug");
  if (!NAME.test(repo) || !SLUG.test(slug)) return { error: "This reply has no valid page. Send it from a report page." };
  const value = { schema: "reports.reply.v1", reply_id: id, repo, slug, page_url: `https://${host}/${repo}/${slug}/` };
  for (const key of ["ticket", "title", "choice", "text"]) {
    const field = get(key);
    if (field.length > LIMITS[key]) return { error: `The ${key} is too long (at most ${LIMITS[key]} characters).` };
    value[key] = field;
  }
  if (!value.choice && !value.text) return { error: "The reply is empty. Write an answer or press a choice." };
  value.sent_at = now;
  value.sender = sender;
  return { value };
}

function escape(text) {
  return String(text).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

function page(status, heading, detail, back, kept) {
  const link = back ? `<p><a class="btn" href="${escape(back)}">Back to the report</a></p>` : "";
  const copy = kept ? `<p class="note">Your text, so that you can copy it:</p><pre>${escape(kept)}</pre>` : "";
  const body = `<!doctype html><html lang="en"><head><meta charset="utf-8">` +
    `<meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(heading)}</title>` +
    `<link rel="stylesheet" href="/_/tokens.css"></head><body><main><header class="hero">` +
    `<p class="kicker">reports · reply</p><h1>${escape(heading)}</h1><p class="lede">${escape(detail)}</p></header>` +
    `<section>${copy}${link}</section></main></body></html>`;
  return new Response(body, { status, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
}

function backPath(value) {
  return /^\/[a-z0-9][a-z0-9._-]*\/[a-z0-9][a-z0-9-]*\/$/.test(value || "") ? value : "/";
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/_/reply") return new Response("Not found", { status: 404 });
    if (request.method === "GET") {
      const sent = url.searchParams.get("sent");
      if (!ID.test(sent || "")) return page(400, "No reply here", "Use the reply box at the end of a report.", "/");
      return page(200, "Reply sent", `Saved as ${sent}. Factory opens a task for it within 5 minutes.`,
        backPath(url.searchParams.get("back")));
    }
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, POST" } });

    let form;
    try {
      form = await request.formData();
    } catch {
      return page(400, "Not sent", "The reply could not be read. Go back and try again.", "/");
    }
    const built = buildReply(form, {
      host: url.host,
      sender: request.headers.get("Cf-Access-Authenticated-User-Email") || "",
      now: new Date().toISOString(),
      id: crypto.randomUUID(),
    });
    const text = String(form.get("text") ?? "");
    if (built.error) return page(400, "Not sent", built.error, "/", text);
    const reply = built.value;
    const back = `/${reply.repo}/${reply.slug}/`;

    let receipt = null;
    try {
      const response = await env.DROP.fetch(`https://${url.host}/ingest/drop`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.DROP_INTAKE_TOKEN}`,
          "Content-Type": "application/json",
          "X-Drop-Kind": "json",
          "X-Drop-Client": "reports",
          "X-Filename": `reply-${reply.repo}-${reply.slug}.json`,
        },
        body: JSON.stringify(reply),
      });
      const result = await response.json();
      if (response.ok && result && result.ok && ID.test(result.drop_id || "")) receipt = result.drop_id;
      else console.log(JSON.stringify({ message: "reply_not_saved", status: response.status, reason: result && result.reason }));
    } catch (error) {
      console.log(JSON.stringify({ message: "reply_not_saved", error: String(error && error.message || error) }));
    }
    if (!receipt) return page(502, "Not sent", "The inbox did not save the reply. Nothing was sent. Try again.", back, text);
    const next = `/_/reply?sent=${encodeURIComponent(receipt)}&back=${encodeURIComponent(back)}`;
    return new Response(null, { status: 303, headers: { Location: next, "Cache-Control": "no-store" } });
  },
};
