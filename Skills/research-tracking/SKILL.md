---
name: research-tracking
description: >-
  Use when managing research to prevent duplicate work and make past evaluations
  findable. Triggers on: starting any research task (always check tracking
  first), 'have we looked at this before', 'check the tracking index', 'update
  research tracking', completing a batch of evaluations, noticing research notes
  accumulating without a tracking system, or any time you are about to evaluate
  a tool, repo, framework, or external resource.
type: skill
updated: '2026-11-19'
version: '1.6.0'
edit_log:
  - "DW-S243 2026-08-05 - v1.5: After Fan-Out routing subsection (routing loop
    for fan-out outputs)"
  - 'DW-S400 2026-10-12 - v1.5.1: memory-surface sources (web-primary, lead lists not figures) under the Output column; After Research -- Fold Verdicts Back'
  - 'DW-S456 2026-11-02 - v1.5.2: references/tracking-index-template.md example link made generic'
  - 'Seed 1.15.0 2026-11-19 - v1.6.0: look lines written by look_write.py replace hand-typed table rows (Conventions Registry 38.0); duplicate check, queueing, and the first look rewritten'
---

# Research Tracking

## Overview

Track research evaluations so they compound instead of getting lost.
A tracking index prevents duplicate work, preserves key details from
light evaluations, and makes past research findable when it becomes
relevant. This skill is about the tracking layer, not the research
methodology itself.

## When to Use

- Before starting any research (check if it's already been evaluated)
- After completing research (log what was found)
- When noticing 5+ research notes without a tracking system
- When a user asks "have we already looked at this?"

### When NOT to Use

- For the research methodology itself (how to evaluate, how deep to
  go, how to write research notes). Use tools-research for that.

## The Tracking Index

The tracking index is a markdown index -- the master lookup for all
evaluated items. It is a shell note with one section note per year
(and a new part when a note reaches 40 KB), made by `look_write.py init`
(Conventions Registry 38.0); see the shell + section pattern in the
[[Conventions Registry]]. The markdown is always canonical: a project
may add a database or other derived index for fast queries, but that
index is rebuilt from the markdown, never hand-edited as a parallel
source of truth. See `references/tracking-index-template.md` for the
full template and field guide.

Each look at a subject is one **look line** in the index. New looks are
look lines written by `look_write.py add`; never type a row by hand
(Conventions Registry 38.0 is the canon for the fields, the words and the
line grammar). Your project's first look creates the ledger (see "The
First Look Creates the Ledger" below).

**The twelve fields:** Subject, Kind, Key, Date, Depth, Relevance, For,
Outcome, Trigger, Finding, View note, and By. The words (one value per
field):
- Kind: `tool`, `org`, `link`, `work`, `place`, `question`.
- Depth: `listed`, `light`, `moderate`, `deep`, `tested`, `not set`.
- Relevance: `high`, `medium`, `low`, `none`, `not set`.
- Outcome: `queued`, `adopt`, `test`, `watch`, `applied`, `confirms`,
  `reference`, `pass`, `duplicate`, `superseded`, `unavailable`.

`For` names another project's abbreviation, only when the relevance is
about that project. `Trigger` is required for `queued` and empty for
every other outcome. `By` is filled in from `--session`.

**Finding and View note.** The Finding holds the verdict, in one to three
sentences, with key details. The View note holds one wikilink to a full
research note, for moderate and deep looks that have one. A light look
has a Finding and no View note.

Findings should capture both the assessment AND any standout
details -- specific phrases, formulations, or insights worth
preserving even when a full note isn't warranted. The Finding should
always answer: what was it, why didn't it warrant a full note, and
was there any standout detail worth preserving?

**Memory-surface sources.** Some tracked items come from a memory or search surface (a large clipping archive queried by search, for example), not from a file you can open:
- Mark the row's source as a memory surface, not a vault file, so nobody tries to open a file that is not there. When the item needs a deeper read, go web-primary: re-find the source on the web. (ReWoven, 2026-07)
- Treat these sources as lead lists, not as figures. They are good at surfacing providers and candidates. Re-verify any number taken from them against the web source before it lands in a working draft. (ReWoven, 2026-08)

## Workflow

### Before Research

Check the tracking index before evaluating anything new. Run `find`
by URL, or by name when the subject has no URL ($V is your vault root):

```
python3 -I -B "$V/_DataWizard/Seed/Scripts/look_write.py" find --vault "$V" --url "<URL>"
python3 -I -B "$V/_DataWizard/Seed/Scripts/look_write.py" find --vault "$V" --name "<name>"
```

A printed line means a project already looked; don't re-research. Don't
grep the ledger tables by hand. `find` writes nothing. A `queued` line may
have a Trigger that is now active. If `find` and a database disagree,
`find` wins. Until your project's old index is converted, also look in that
old index for the subject, reading it by name (not a grep).

On Windows, use `python` or `py` instead of `python3` in every command in
this skill.

### Before Triage -- Categorize Large Link Sets

When triaging a link batch over ~100 items, categorize before triaging. Group links by topic (graph DBs, RDF tools, agent memory, etc.) and triage per-category. This enables two efficiency patterns:

1. **Uniform relevance filter.** When a relevance question applies equally to all items in a category (e.g., "does DW use RDF?" for 22 Rust RDF libraries), batch-assess the entire category without individual searches. S129 applied this to save significant time on the ARK TG triage.

2. **Priority ordering.** Triage high-relevance categories first. If context runs out, low-relevance categories are the ones that get deferred. S128-S130 triaged 204 links across 8 categories using this approach.

### After Triage -- Queue High-Value Items

When a triage batch produces Medium-High or High items at Light
depth, write a look line for each with Outcome `queued`:
- Subject and Key (the URL)
- `--trigger` (what design context would make this worth a
  deep read -- e.g., "when D12 graph threshold becomes active")
- Finding (what specifically to investigate in the deep read)

This closes the gap between triage (capturing what exists) and
design harvest (applying what was learned). Without it, Light-
depth findings sit in the RTI but never get pulled deeper.

### Before Design Work

When starting work on a design doc, list your project's looks and check
the queued ones against the current design context:

```
python3 -I -B "$V/_DataWizard/Seed/Scripts/look_write.py" find --vault "$V" --all --json
```

Keep the lines whose `project` is your abbreviation, take the newest line
per subject, and keep those whose `outcome` is `queued`; compare each
`trigger` with the current design context. If matches
exist, do the deep read first -- research is most valuable when it feeds
live design decisions. The deep read is a new look line; the newest line
per subject is the current one.

### After Research -- Single Target

Run `add` once:

```
python3 -I -B "$V/_DataWizard/Seed/Scripts/look_write.py" add --ledger "<newest Looks note of this year>" --map "$V/_DataWizard/Seed/Vault Config.md" --subject "<name>" --kind tool --key url:<https URL> --date <YYYY-MM-DD> --depth light --relevance medium --outcome watch --finding "<one to three sentences>" --view-note "[[<note>]]" --session <SESSION>
```

The verdict goes in `--finding`; the research note, if there is one, goes
in `--view-note`. The ledger is the newest part of the year of the line's
Date: the last `![[... Looks <year> ...]]` embed for that year in your
index note; give that note's path in the sections folder as `--ledger`.
`add` refuses a Date in another year. Leave out `--view-note` when there
is no research note. With no URL, use `--key name:<name>` (the writer
slugs it). An outcome of `queued` needs `--trigger "<text>"`;
any other outcome must have none. Use `--for <ABBR>` only when the
relevance is about another project. If `add` exits with 4, the note is 40
KB or more: run `init` for the next part, then `add` again.

### After Research -- Batch

Hold all tracking updates until the batch is complete. This prevents
context-switching and lets you capture batch-level observations.
Run one `add` per item after the batch.

### After Research -- Fold Verdicts Back

Before you start the next research item, fold this pass's verdicts into the live artifacts they inform: the meeting agenda, the open-questions list, the partner or roster doc. The tracking index records *that* an item was evaluated. The live docs take in *what* it concluded. If you skip this step, research piles up in the index without changing the working state. (ReWoven, 2026-07)

### After Fan-Out -- Route Each Output

When a parallel fan-out (see tools-research, Parallel Fan-Out) produces many
outputs at once, each usually needs to land on more than the tracking index.
A repeatable routing loop for outside-project research, validated across
several passes: write the research note, write the look line, index it in the relevant MOC, add a harvest-log row if it fed a
harvest, and refresh any stale stub the item updates. Run the same loop per
output so nothing lands in only one place.

### Where Patterns Go

The tracking index stays at the item level. When a batch reveals
cross-cutting patterns (themes that emerge across multiple items),
write those patterns where they belong architecturally:
- Design docs (if the pattern has architectural implications)
- Session log learnings (if it's a process or tool insight)
- Relevant skill files (if it refines a methodology)

The tracking index can note which items were processed in the same
batch, but the pattern itself lives in a document with more context.
See design-harvest for the full integration workflow.

## The First Look Creates the Ledger

You don't need a ledger on day one. Start researching and write notes.
Start the ledger when you notice yourself wondering "did we already
look at this?" -- that's the signal. Usually around 5+ research notes.
Your project's first look then does two things, once:

1. Add your project to the `holon_lens_map` row in the Paths table of
   `_DataWizard/Seed/Vault Config.md`: append `; <project folder>/=<ABBR>`
   inside the backticks of its value cell. If the row is missing, add
   `| holon_lens_map | `<project folder>/=<ABBR>` |` (Seed Install and
   Update guide, "Look ledgers"). The abbreviation is a capital
   letter, then up to nine capitals or digits.
2. Make your project's sections folder (for example
   `_Sections - <Project>/Research Tracking Index/`), then run:

```
python3 -I -B "$V/_DataWizard/Seed/Scripts/look_write.py" init --sections "<folder>" --shell "<index note>" --abbr <ABBR> --year <YYYY> --map "$V/_DataWizard/Seed/Vault Config.md" --session <SESSION> --operator "<name>"
```

`init` makes the year note, flags it `look_ledger: <ABBR>`, and embeds it
in the index note. Later years and parts are made the same way. See
`references/tracking-index-template.md` and Conventions Registry 38.0.

## Common Mistakes

- **Not checking before researching.** The whole point is preventing
  duplicate work. Always check first.
- **Empty Finding for light items.** If an item doesn't warrant a full
  note, the Finding IS the output. Don't leave it blank --
  capture why it wasn't worth a note so nobody re-evaluates it.
- **Updating item-by-item during a batch.** Hold updates until the
  batch is done. You'll write better entries with full context.
- **Putting patterns in the tracker.** The tracker is a lookup table.
  Patterns and synthesis belong in design docs or session logs.

## See Also

- Tracking index template: `references/tracking-index-template.md`
- tools-research skill (research methodology that feeds into tracking)
- design-harvest skill (integrating tracked research findings into
  design docs and living project documents)

**REQUIRED BACKGROUND:** tools-research (for the research methodology
that produces the evaluations this skill tracks)
