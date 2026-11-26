// Reply Worker: /_/reply on the reports host. See README.md ("Reply").
//
// POST: a reply box form from a report page. The Worker saves it as one JSON item in the owner's inbox (a Drop
// capture, client "reports") and answers 303 to the "sent" page, so a browser refresh does not send it twice.
// The reply id is a hash of page, choice and text; Factory keys on the same hash, so a resend is one task.
// Factory's intake reads new inbox items and opens one task for each reply.
// GET ?sent=<id>&sig=<hmac>&back=<path>: the "sent" page. sig is an HMAC of the inbox receipt with the Worker
// secret, so only a real 303 after a saved reply can show "Reply sent"; a typed or crafted link cannot.
//
// Cloudflare Access protects the whole host, so every request here comes from the owner's signed-in browser.
// env.DROP: service binding to the inbox Worker. env.DROP_INTAKE_TOKEN: its intake token (a Worker secret).

const NAME = /^[a-z0-9][a-z0-9._-]{0,63}$/;
const SLUG = /^[a-z0-9][a-z0-9-]{0,127}$/;
const ID = /^[A-Za-z0-9-]{1,80}$/;
export const INBOX_WAIT_MS = 10000;
const MAX_BODY = 65536;  // all fields at their limits, percent-encoded, stay under about 40 KB
const LIMITS = { text: 4000, choice: 80, ticket: 64, title: 200 };
const MAX_ASKS = 12;  // decision cards with an answer on one page (bin/report-reply-box)

// One reply = one id: the same page, choice and text give the same id, so a double click or a retry is one reply.
export async function replyId(repo, slug, choice, text) {
  const bytes = new TextEncoder().encode(JSON.stringify([repo, slug, choice, text]));
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
  return Array.from(digest.slice(0, 16), (b) => b.toString(16).padStart(2, "0")).join("");
}

// HMAC-SHA256(secret, receipt id), first 16 bytes as hex.
export async function sign(secret, id) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" },
    false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(id)));
  return Array.from(mac.slice(0, 16), (b) => b.toString(16).padStart(2, "0")).join("");
}

// Constant-time compare of two hex strings.
function same(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export function buildReply(form, { host, sender, now, id }) {
  // Browsers send textarea line breaks as CRLF but count them as one character for maxlength: count them as one too.
  const get = (key) => String(form.get(key) ?? "").replace(/\r\n?/g, "\n").trim();
  const repo = get("repo");
  const slug = get("slug");
  if (!NAME.test(repo) || !SLUG.test(slug)) return { error: "This reply has no valid page. Send it from a report page." };
  const value = { schema: "reports.reply.v1", reply_id: id, repo, slug, page_url: `https://${host}/${repo}/${slug}/` };
  for (const key of ["ticket", "title", "choice", "text"]) {
    const field = get(key);
    if (field.length > LIMITS[key]) return { error: `The ${key} is too long (at most ${LIMITS[key]} characters).` };
    value[key] = field;
  }
  // Answers from the decision cards (q<n> question, a<n> pick, n<n> note; bin/report-reply-box). They are kept as
  // "answers" and also written into the text, so every reader of the text (Factory, bin/report-replies) sees them.
  const answers = [];
  for (let n = 1; n <= MAX_ASKS; n += 1) {
    const question = get(`q${n}`).slice(0, 200);
    const pick = get(`a${n}`).slice(0, 80);
    const note = get(`n${n}`).slice(0, 500);
    if (question && (pick || note)) answers.push({ question, choice: pick, note });
  }
  if (answers.length) {
    const lines = answers.map((x) => `- ${x.question}: ${[x.choice, x.note].filter(Boolean).join(". ")}`);
    value.text = [value.text, `Decisions:\n${lines.join("\n")}`].filter(Boolean).join("\n\n");
    if (value.text.length > LIMITS.text) return { error: `The reply is too long (at most ${LIMITS.text} characters).` };
    value.answers = answers;
  }
  if (!value.choice && !value.text) return { error: "The reply is empty. Write an answer or press a choice." };
  value.sent_at = now;
  value.sender = sender;
  return { value };
}

async function readCapped(request, limit) {
  if (Number(request.headers.get("Content-Length") || 0) > limit) return null;
  if (!request.body) return new Uint8Array();
  const reader = request.body.getReader();
  const parts = [];
  let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > limit) { await reader.cancel(); return null; }
    parts.push(value);
  }
  const all = new Uint8Array(size);
  let at = 0;
  for (const part of parts) { all.set(part, at); at += part.byteLength; }
  return all;
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
      const sig = url.searchParams.get("sig") || "";
      if (!ID.test(sent || "") || !env.DROP_INTAKE_TOKEN || !same(sig, await sign(env.DROP_INTAKE_TOKEN, sent))) {
        return page(400, "No reply here", "Use the reply box at the end of a report.", "/");
      }
      const who = request.headers.get("Cf-Access-Authenticated-User-Email");
      return page(200, "Reply sent", `The inbox saved it as ${sent}. The session of this page reads it (bin/report-replies), and Factory gets it on its next inbox pass (about 5 minutes). The same choice and text sent again count once.` +
        (who ? ` Signed in as ${who}.` : ""),
        backPath(url.searchParams.get("back")));
    }
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, POST" } });
    // Access is the gate. These checks only make sure it is there: no Access identity or a form from another
    // site means the request did not come from the owner's signed-in page, so nothing is saved.
    const origin = request.headers.get("Origin");
    if (!request.headers.get("Cf-Access-Authenticated-User-Email") || (origin && origin !== `https://${url.host}`)) {
      return page(403, "Not sent", "This reply did not come from a signed-in report page.", "/");
    }

    let form;
    try {
      const body = await readCapped(request, MAX_BODY);  // stops reading past the cap, with or without Content-Length
      if (body === null) return page(413, "Not sent", "The reply is too long. Go back and shorten it.", "/");
      form = await new Response(body, { headers: { "Content-Type": request.headers.get("Content-Type") || "" } }).formData();
    } catch {
      return page(400, "Not sent", "The reply could not be read. Go back and try again.", "/");
    }
    const built = buildReply(form, {
      host: url.host,
      sender: request.headers.get("Cf-Access-Authenticated-User-Email"),
      now: new Date().toISOString(),
      id: "",
    });
    const text = String(form.get("text") ?? "");
    if (built.error) return page(400, "Not sent", built.error, "/", text);
    const reply = built.value;
    reply.reply_id = await replyId(reply.repo, reply.slug, reply.choice, reply.text);
    const back = `/${reply.repo}/${reply.slug}/`;

    if (!env.DROP_INTAKE_TOKEN) {  // no secret: the box is paused (bin/reply-deploy); never call the inbox without it
      return page(503, "Not confirmed", "The reply box is paused. Your text is below; send it later.", back, text);
    }
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
        signal: AbortSignal.timeout(INBOX_WAIT_MS),  // a stalled inbox gives "Not confirmed", not an open request
      });
      const result = await response.json();
      if (response.ok && result && result.ok && ID.test(result.drop_id || "")) receipt = result.drop_id;
      else console.log(JSON.stringify({ message: "reply_not_saved", status: response.status, reason: result && result.reason }));
    } catch (error) {
      console.log(JSON.stringify({ message: "reply_not_saved", error: String(error && error.message || error) }));
    }
    if (!receipt) {
      return page(502, "Not confirmed", "The inbox did not confirm the reply. Send it again: the same reply counts once.", back, text);
    }
    const sig = await sign(env.DROP_INTAKE_TOKEN, receipt);
    const next = `/_/reply?sent=${encodeURIComponent(receipt)}&sig=${sig}&back=${encodeURIComponent(back)}`;
    return new Response(null, { status: 303, headers: { Location: next, "Cache-Control": "no-store" } });
  },
};
