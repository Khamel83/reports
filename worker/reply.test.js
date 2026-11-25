// node --test worker/
import assert from "node:assert/strict";
import test from "node:test";
import worker, { buildReply } from "./reply.js";

const HOST = "reports.example";

function form(fields) {
  const data = new FormData();
  for (const [key, value] of Object.entries(fields)) data.append(key, value);
  return data;
}

function post(fields, headers = { "Cf-Access-Authenticated-User-Email": "owner", Origin: `https://${HOST}` }) {
  return new Request(`https://${HOST}/_/reply`, { method: "POST", body: form(fields), headers });
}

function inbox(answer, status = 200) {
  const calls = [];
  return {
    calls,
    env: {
      DROP_INTAKE_TOKEN: "intake-test",
      DROP: { fetch: async (url, init) => { calls.push({ url, init }); if (answer instanceof Error) throw answer; return Response.json(answer, { status }); } },
    },
  };
}

const page = { repo: "infra", slug: "a2ui-check", ticket: "DO-12", title: "A2UI check" };

test("a reply is saved once as one inbox item and the browser goes to the sent page", async () => {
  const { calls, env } = inbox({ ok: true, drop_id: "0b6f-11aa" });
  const response = await worker.fetch(post({ ...page, choice: "B", text: "Do R-4." }), env);
  assert.equal(response.status, 303);
  assert.equal(response.headers.get("Location"), "/_/reply?sent=0b6f-11aa&back=%2Finfra%2Fa2ui-check%2F");
  assert.equal(calls.length, 1);
  assert.equal(new URL(calls[0].url).pathname, "/ingest/drop");
  const headers = calls[0].init.headers;
  assert.equal(headers.Authorization, "Bearer intake-test");
  assert.equal(headers["X-Drop-Client"], "reports");
  assert.equal(headers["X-Drop-Kind"], "json");
  const saved = JSON.parse(calls[0].init.body);
  assert.equal(saved.schema, "reports.reply.v1");
  assert.equal(saved.page_url, `https://${HOST}/infra/a2ui-check/`);
  assert.deepEqual([saved.ticket, saved.title, saved.choice, saved.text], ["DO-12", "A2UI check", "B", "Do R-4."]);
  assert.match(saved.reply_id, /^[0-9a-f]{32}$/);
  assert.equal(saved.sender, "owner");
});

test("the same reply twice has the same id; another text has another", async () => {
  const { calls, env } = inbox({ ok: true, drop_id: "a-1" });
  for (const text of ["Do R-4.", "Do R-4.", "Other."]) await worker.fetch(post({ ...page, choice: "B", text }), env);
  const ids = calls.map((call) => JSON.parse(call.init.body).reply_id);
  assert.equal(ids[0], ids[1]);
  assert.notEqual(ids[0], ids[2]);
});

test("no Access identity or another origin saves nothing", async () => {
  const { calls, env } = inbox({ ok: true, drop_id: "a-1" });
  for (const headers of [{ Origin: `https://${HOST}` }, { "Cf-Access-Authenticated-User-Email": "owner", Origin: "https://evil.example" }]) {
    assert.equal((await worker.fetch(post({ ...page, text: "hi" }, headers), env)).status, 403);
  }
  assert.equal(calls.length, 0);
});

test("an inbox failure says not sent and gives the text back", async () => {
  for (const answer of [{ ok: false, reason: "unauthorized" }, new Error("down")]) {
    const { env } = inbox(answer, 401);
    const response = await worker.fetch(post({ ...page, text: "keep <this>" }), env);
    assert.equal(response.status, 502);
    const body = await response.text();
    assert.match(body, /Not confirmed/);
    assert.match(body, /keep &lt;this&gt;/);
  }
});

test("empty, too long or pageless replies are refused before the inbox", async () => {
  const { calls, env } = inbox({ ok: true, drop_id: "x" });
  for (const fields of [{ ...page }, { ...page, text: "x".repeat(4001) }, { ...page, repo: "../x", text: "hi" }, { text: "hi" }]) {
    const response = await worker.fetch(post(fields), env);
    assert.equal(response.status, 400);
  }
  assert.equal(calls.length, 0);
});

test("the sent page links only back to a report path", async () => {
  const good = await worker.fetch(new Request(`https://${HOST}/_/reply?sent=abc-1&back=%2Finfra%2Fx%2F`), {});
  assert.equal(good.status, 200);
  assert.match(await good.text(), /href="\/infra\/x\/"/);
  const evil = await worker.fetch(new Request(`https://${HOST}/_/reply?sent=abc-1&back=https%3A%2F%2Fevil.example%2F`), {});
  assert.match(await evil.text(), /href="\/"/);
  assert.equal((await worker.fetch(new Request(`https://${HOST}/_/reply?sent=%3Cx%3E`), {})).status, 400);
  assert.equal((await worker.fetch(new Request(`https://${HOST}/other`), {})).status, 404);
});

test("buildReply keeps the sender and the time", () => {
  const { value } = buildReply(form({ ...page, text: "ok" }), { host: HOST, sender: "owner", now: "T", id: "I" });
  assert.equal(value.sender, "owner");
  assert.equal(value.sent_at, "T");
  assert.equal(value.reply_id, "I");
});
