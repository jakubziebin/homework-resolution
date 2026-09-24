# Take-home assignment (Low) — Fix the API docs

Thanks for getting this far! This is a small, practical exercise that mirrors real
work on the Integrations & Automations team. We expect it to take **1.5–2 hours**,
and you have **48 hours** to turn it around. Please don't over-invest — we care
about how you think, not polish.

## The scenario

Our published StyleZone API docs have drifted out of date — a few things are wrong,
and customers keep tripping over them. You've been handed a **draft doc page**
(`api-reference-draft.md`) and a **running copy of the API** (`mock_server.py`).

**The running API is the source of truth.** The draft doc may not match it.

## What you'll do

1. **Find the discrepancies.** Compare the draft doc against how the API actually
   behaves. Call the endpoints and see what really happens.
2. **Produce a corrected `api-reference.md`** — fix every error you find.
3. **Add a working example** for each endpoint (a `curl` command and/or a short
   Python snippet) that you've actually run against the mock.
4. **List what you found** in a short `FINDINGS.md`: each discrepancy, what the doc
   said, what's actually true, and how you confirmed it.
5. **Prevent it happening again** — a short thought exercise, *no code required*.
   Docs drift because nothing keeps them honest. In `FINDINGS.md`, add a short
   section on how you'd stop this recurring: what would you build or change so the
   docs stay in sync with the API going forward? A few paragraphs is plenty — we'll
   dig into it on the call.

## Use AI — we want you to

This role uses AI coding agents (Claude Code, Codex, etc.) every day, so please use
them here too. We're interested in how you *direct* the tools and how you *verify*
their output — a confident-but-wrong doc is exactly the problem we're trying to fix,
so don't just trust what a model tells you the API does. Check it.

## What's in this pack

| File | What it is |
|------|-----------|
| `api-reference-draft.md` | The out-of-date doc you're correcting |
| `mock_server.py` | A runnable copy of the API — the source of truth |

### Running the API

```bash
python3 mock_server.py
```

It serves `http://localhost:8080`. Every request needs the header:

```
Authorization: Bearer sz-demo-token-abc123
```

The startup message prints a few known IDs to test with. It's a throwaway toy with
canned responses — nothing to break.

## What to submit

A zip or git repo with: your corrected `api-reference.md`, the examples, and
`FINDINGS.md`. We'll book a short call afterward to walk through what you found.

## Ground rules

- Toy exercise on mock data — no Browzwear accounts or production access needed,
  and nothing here ships.
- If the draft documents something the running API doesn't do at all, that's worth
  noting too.
- Questions welcome — asking good ones is a plus.

Good luck!
