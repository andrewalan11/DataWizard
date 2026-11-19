---
title: Research Tracking Index Template
type: skill-reference
parent: research-tracking
updated: '2026-11-19'
edit_log:
  - 'DW-S456 2026-11-02 - example link made generic (it named a maintainer-only note; release smoke test)'
  - 'Seed 1.15.0 2026-11-19 - template and guide rewritten for look lines (Conventions Registry 38.0); no hand-typed tables'
---

# Research Tracking Index Template

## When to Create One

Create this when you have 5+ research notes and start wondering
"did we already look at this?" That's the signal.

## Setup

Create a note in your project's research or workshop area, named
`Research Tracking Index.md` (a plain descriptive title -- no
sort-prefix). The first look makes it a shell with one section note per year (and per
40 KB part), through `look_write.py init`; the markdown stays canonical. See the
research-tracking skill and the [[Conventions Registry]] (file naming;
shell + section pattern).

## Template

You do not type the tables. `look_write.py init` makes the year note,
and `look_write.py add` appends the lines (see the research-tracking skill
for the commands). The year note it makes looks like this:

```
---
title: "<n>.0 Looks YYYY - <ABBR> Research Tracking Index"
(birth metadata, written by init)
look_ledger: <ABBR>
---

*Part of the [[Research Tracking Index]]*

## Looks YYYY

*Lines are written only by `look_write.py add` (D183). Do not edit or delete a line.*

| Subject | Kind | Key | Date | Depth | Relevance | For | Outcome | Trigger | Finding | View note | By |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

Your index note (the shell) embeds each year note as `![[<note name>]]`.
One table per note, one line per look, and a note is started anew when it
reaches 40 KB.

## Depth Key

- **Listed**: Saw the title or a listing only.
- **Light**: Read the landing page, the post, or the README summary. No
  full note -- the Finding captures the verdict and any standout details.
- **Moderate**: Read the full piece or the docs; no source code read.
  Usually a structured research note, linked in View note.
- **Deep**: Read the source code or the primary material in depth, with
  a full research note with transferable patterns.
- **Tested**: Ran it.
- **Not set**: No depth was recorded.

## Field Guide

The twelve fields, in order: Subject, Kind, Key, Date, Depth, Relevance,
For, Outcome, Trigger, Finding, View note, By. The words are in
Conventions Registry 38.0; the research-tracking skill lists them.

**Finding and View note examples:**

For moderate/deep looks with a note (a wikilink in View note, and the
verdict in Finding):
> View note: [[Example Research Note]]

For light looks (verdict and key details in Finding, no View note):
> Community consensus: md for context/intent, code for execution.
> Key detail: break files ~500 lines per domain, load only what's
> relevant. No new patterns beyond existing architecture.

The Finding should always answer three questions:
1. What was it?
2. Why didn't it warrant a full note?
3. Was there any standout detail worth preserving?

**Trigger (Outcome `queued`):**
Describes when this becomes worth investigating. Prevents premature
research on things that only matter at a future milestone. Examples:
- "When building the search layer"
- "When publishing skills externally"
- "When the enrichment pipeline reaches Step 3"

A Trigger is required for `queued` and must be empty for every other
outcome.

## No Extra Columns

The table has these twelve fields and no more. Put a design-doc pointer
or a batch note in the Finding. A look that matters to another project is
a second line with `--for <ABBR>`.

## Maintenance

- Write a look line after every evaluation, even light ones
- Check the queued lines when starting new work -- a queued line's
  Trigger may now be met (`find --all --json`; newest line per subject, outcome `queued`)
- A changed view of a subject is a new line; the newest line per subject
  is current and older lines stay as history. Never edit a line.
