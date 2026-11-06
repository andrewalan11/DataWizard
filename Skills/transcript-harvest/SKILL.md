---
name: transcript-harvest
description: >-
  Use when harvesting content from transcripts into project documents. Triggers
  on: 'harvest from this transcript', 'extract from this recording', processing
  transcripts with harvest_status: pending, or any transcript with harvest_for
  YAML set. Covers video, podcast, meeting, and voice memo transcripts.
type: skill
updated: '2026-11-06'
version: '0.10.0'
edit_log:
  - DW-S158 2026-06-08
  - "MMM meta-learning plant 2026-06-09: added Step 4 (check existing vault
    sources), Step 6 (triage multi-topic), renumbered"
  - "DW-S182 2026-06-13: folded Protocol 8.0 (segmentation, chunk-and-route,
    lexicon criteria); repointed See Also to post-demolition homes"
  - "DW-S202 2026-06-25: added Block-Level Citations section (stamp-on-cite,
    ^tN/@mm:ss) pointing at block-stamper + Conventions Registry"
  - "DW-S232 2026-08-04: added companion-vs-harvest default-granularity pointer
    (D112)"
  - "DW-S262 2026-08-08: added Harvest via embeddable synth note pointer (D116)"
  - "DW-S312 2026-08-30: stale STUB status label corrected to Active (the full
    workflow has long shipped; S312 Seed review)"
  - 'DW-S330 2026-09-04 - v0.9.1: See Also gains the shared-layer-redaction overlay pointer (required when the harvest destination is a shared layer)'
  - "DW-S349 2026-09-08 - v0.9.2: Reader-Facing Output rule added (load the
    Reader-Facing Prose Style guide when the destination is read-aloud-class)"
  - 'DW-S446 2026-10-31 - Seed error-check fixes: v0.9.3 Harvest Log name'
  - 'DW-S456 2026-11-02 - v0.9.4: depersonalized examples (names replaced with neutral placeholders)'
  - 'DW-S470 2026-11-06 - v0.10.0: Step 8 harvest_status is a roll-up on multi-project sources; new Accept a hub section step; speaker-label slip line in Segmentation; Step 2 stops pointing at the Fathom Meeting Index (D167, D168)'
---

# Transcript Harvest Skill

**Status:** Active

## Overview

Harvest content from transcripts (video, podcast, meeting, voice memo) into project-specific destination documents. Ensures segmentation, proper citation, and YAML state tracking.

## When to Use

- Processing a transcript that has been flagged for harvesting
- User says "harvest from this transcript" or "extract content from this recording"
- A transcript has `harvest_status: pending` or `harvest_for:` YAML fields set

### When NOT to Use

- Harvesting from articles, clippings, or non-transcript sources (use document-harvest)
- Researching external content (use research skill)
- Segmenting a transcript without harvesting (run `segment_transcript.py` directly)

## Workflow

1. **Check source YAML** — read `harvest_status`. If already `harvested`, confirm with user before re-harvesting.
2. **Check project assignment** — look for `harvest_for` in the transcript's YAML. If a harvest hub has already read the call for several projects (the transcript has a `companion:` synth note with an Embed Map and your project has a `harvest_log` line), do not re-harvest: work your section ("Accept a hub section" below). If `harvest_for` is missing and the transcript sits in a project folder, the project is implicit; otherwise ask the user which project this transcript belongs to. Do not harvest without knowing the destination project.
3. **Check segmentation** — look for `segmented: true` in YAML. If missing, the transcript needs `##` section headers first. Either run `segment_transcript.py` or add headers manually.
4. **Check for existing vault sources** -- before declaring any referenced source inaccessible (paywalled, offline, video-only), search `_Clippings/` and `_Transcripts/` for existing copies. YouTube auto-transcripts, previously clipped articles, and federated documents are easy to overlook and may already be in the vault. In MMM S07, a DISI talk initially dismissed as "YouTube-only" was already in `_Clippings/` as a full transcript and turned out to be the most project-relevant source of the entire batch.
5. **Read the transcript** — understand the full content before extracting anything.
6. **Triage multi-topic sources** -- if the transcript covers multiple topics or threads, surface the topic list to the user and offer to skip stale or low-relevance items before writing. This keeps the harvest lean and avoids over-capturing content the user has already moved past. Especially valuable for chat-style transcripts and multi-meeting catch-up conversations where some threads may be outdated by harvest time.
7. **Harvest into destination docs** — synthesize relevant content into project documents. Use citation format: `([[NoteTitle#Section Header|YYYY-MM-DD — Section Name]])`. Don't transcribe — synthesize.
8. **Update source YAML** -- set `harvested_into` (with section-level anchors), `harvest_date`, and `harvest_notes`. For re-harvests, append to `harvested_into` and convert `harvest_date` to an array (most recent last). **Single-project source:** also set `harvest_status` (`harvested`, or `reviewed` with `harvest_notes` explaining why nothing was harvested). **Source routed to two or more projects** (`harvest_for` lists two or more): add your own `harvest_log` line instead and never hand-set `harvest_status` - it is a roll-up of every project's latest line (grammar, roll-up and backfill rule: [[YAML Schema]], Harvest Tracking).
9. **Update Harvest Log** -- add or update a row in `0.4 Harvest Log - [Project].md` with source, harvest date, destinations, and agent.
10. **Session log** -- add harvest details to `0.2 Session Log.md` at the end of the session as part of normal session logging -- not after each individual source.

## Segmentation (before you harvest)

Transcripts are the densest, highest-value content type in many vaults, but structurally noisy. Three properties make them distinct: topic shifts mid-stream (the raw transcript has no headers marking where topics change, so companion citations can't deep-link to specific moments), speaker-attributed ideas (who said something matters - preserve attribution, don't smooth it away), and high lexicon density (specialized language in its most authentic, unrehearsed form).

**Segment before extracting anything** (Workflow Step 3). Add `##` section headers at major topic shifts - without headers there are no anchor targets for deep-link citations.

Format:
```
## Section Name (@timestamp if available)
```

Good headers (specific, navigable):
- `## Threshold Design and Overflow Logic (@14:23)`
- `## Simon's Tension Around Ownership`
- `## Bonding Curves as Coordination Mechanism (@22:15)`

Bad headers (too generic):
- `## Discussion`
- `## Part 3`
- `## Continued`

Add headers on a first read-through, before extracting content. For very short transcripts (under ~1,000 words) headers may not be necessary - use judgment.

**Speaker labels slip.** Automatic transcription (Fathom especially) often swaps speaker labels at turn changes. Credit a point to the speaker by what was said - the content, who the call is about, who answers whom - not by the label alone, and note the slip where you correct a label (for example "label shows B; the content is A's"). (DataWizard, 2026-11)

## Chunk and Route

1. **First pass: read the whole source** before routing anything.
2. **Second pass: identify chunks.** A chunk is a contiguous passage addressing one project topic. A single section may contain multiple chunks; one chunk may span multiple sections if they stay on one topic.
3. **Route each chunk to the most specific destination section** by title. When uncertain, read the first paragraph of a candidate section to confirm fit.
4. **Multi-topic chunks:** put primary content in the most specific section; add a brief cross-reference from the other. Don't duplicate full paragraphs.
5. **Draft all placements for human review** before writing anything to the vault.

## What Makes a Good Lexicon Candidate

When harvesting from transcripts, watch for a phrase or framing that:
- Is a specific phrase or framing, not a vague topic
- Says something in a distinctive way (not generic)
- Has a clear claim or idea embedded in it
- Could stand alone as a meme-seed with the right context

## Block-Level Citations (stamp-on-cite)

Section anchors (the `## Section Header` citations in Step 7) are the default. When a harvest claim points at a **specific transcript turn** rather than a whole section, cite the turn directly with a block ID:

- Stamp as you cite: use the block-stamper skill to give that turn an ID (reuse the existing one if present; otherwise the next unused `^tN`), then link to it. Don't pre-stamp the whole transcript -- stamping is the act of citing.
- Format: `([[TranscriptName#^t15|@22:15]])` -- the visible label is the **cited turn's own `@mm:ss`** timestamp. Use the `§` glyph as the label only when the turn has no derivable timestamp (an unsegmented or headerless transcript with no per-turn times). (Confirmed S236; supersedes the earlier section-header-derived rule.)
- Whole-section synthesis keeps the section-anchor form from Step 7.

Mechanic: block-stamper skill. Full format canon: [[Conventions Registry]].

Harvest destinations keep section anchors as their default *by design* - this differs from companions, which are block-default (D112, S232). See the Conventions Registry citation section for why the two regimes differ; it is the canonical statement, not a contradiction to resolve.

## Harvest via embeddable synth note

When a harvest routes to **multiple destinations, or to a destination that is contested or not yet ready** (mid-edit under concurrent operation, or awaiting a team decision), don't synthesize straight into those docs. Harvest once into a `c_` synth note built from self-contained, embeddable `##` sections, add an Embed Map near the top, and let each destination transclude the section it needs (`![[synth-note#Section]]`) when its thread is ready. The full convention -- synth-note structure, Embed Map with per-section embed-vs-native routing, team-download header, sensitivity marking, graduation, and the on-disk heading-parity close step -- is the canonical statement in [[Conventions Registry]] (Harvest via embeddable synth note); the `embed_targets` provenance field is in [[YAML Schema]]. For a single ready destination the instance owns, the standard direct synthesis above is simpler.

## Accept a hub section

When a harvest hub project has read a call once for every project (harvest-router, Hub mode), the target project does not re-harvest the call: it works its own section of the hub's synth note. The pointer is a line marked `<!-- harvest-handoff -->` in the project's 0.5 Action Items; the orientation sweep lists the open ones. The hub never edits the target's documents, so these steps run in the target project's own session.

1. **Read your section** in the synth note (the transcript's `companion:`), and the transcript turns it cites where you need more context (read a long transcript by line range). A section is evidence - what was said, the speaker, the timestamp, the Content Interests line it matched - not a finished draft.
2. **Decide:** accept it, edit it (take part of it or rework it), or decline it (nothing worth placing; say why).
3. **Place it** in your own documents (accept or edit). Follow the section's Route in the Embed Map: `native` (write the content in, cite the section) for a destination in a shared layer, `embed` for a private-layer destination ([[Conventions Registry]], Harvest via embeddable synth note). Keep the section's sensitivity marks, and run [[shared-layer-redaction]] when the destination is a shared layer.
4. **Close it in four places**, in the same sitting:
   - (a) **The destination note** - the content is placed (step 3); on a decline, nothing is.
   - (b) **The Embed Map row** for your project in the synth note: fill Destination (a wikilink, or `-` on a decline) and set Status to one word from the fixed list in [[Conventions Registry]] 9.0 (Hub mode), followed by your session id in parentheses; and, unless you declined, append the same destination wikilink to the synth note's `embed_targets` (same note, same edit).
   - (c) **Your `harvest_log` line** on the transcript: add one new line after your project's latest line - `harvested` for accepted or edited, `reviewed` for declined - with `decision #-` and, last, `section: <your section heading>` ([[YAML Schema]], Harvest Tracking). Make it a one-line text edit of the frontmatter, quoted; never rewrite the list with a frontmatter tool, which rewrites the whole list and rewraps long strings. The line must stay one physical line however long: check after the edit that every `harvest_log` item is one line beginning `  - "` with no continuation line under it (the tools read only an item's first line). Then recompute `harvest_status` by the roll-up rule (compute it, never choose it) and parse the frontmatter back.
   - (d) **Tick your `<!-- harvest-handoff -->` line** in your 0.5 (in a sectioned 0.5, the line lives in the section file the shell embeds). Tick it when every section that handoff names is closed; otherwise update its count.
5. **Log it.** Add the 0.4 Harvest Log row as in Step 9 (source: the synth-note section), and log the harvest in your session log at close (Step 10).

## Common Mistakes

- Harvesting without checking segmentation first -- citations can't deep-link without `##` headers
- Transcribing instead of synthesizing -- one idea per paragraph, don't reproduce the conversation
- Flattening tensions and disagreements -- preserve nuance
- Forgetting to update source YAML -- the next agent won't know this was already processed
- Hand-setting `harvest_status` on a source routed to two or more projects -- it is a roll-up of the `harvest_log` lines; close your own line instead
- Rewriting the `harvest_log` list with a frontmatter tool -- it rewraps long strings and can change other projects' lines; add your one line as a text edit
- Re-harvesting a call a hub has already read -- accept, edit or decline your section instead
- Skipping `harvest_notes` -- the "commit message" is the most valuable part, especially for `reviewed` or partial harvests
- Forgetting the Harvest Log -- source YAML is the truth, but the log is how humans and agents scan routing at a glance
- Harvesting without checking project assignment -- content ends up in the wrong project docs or gets orphaned
- Processing multiple sources without completing all 10 steps per source first (session log excepted -- that waits til end)
- Declaring a referenced source inaccessible without checking `_Clippings/` and `_Transcripts/` first -- existing vault copies are easy to overlook
- Using read-write-delete to relocate a transcript instead of `move_note` -- wastes tokens sending the entire body through the tool call for no content-level reason

## Note Relocation

When a transcript needs to move (e.g., from vault root to a project folder during harvest):

1. Use `move_note` to relocate the file -- this is atomic, zero-token, and preserves wikilinks.
2. Then use `update_frontmatter` or `patch_note` to add/update harvest metadata separately.

Never read-write-delete to move a note. Transcripts can be thousands of words long and the content doesn't change during a move. This rule applies to all note relocations, not just transcripts.

## Routing Patterns

### Research brief as harvest destination

When a transcript contains a researcher's verbal walkthrough of their work -- describing what documents they found, what's in a folder, what seems high leverage -- the harvest output can be the research brief the researcher didn't have time to write. This is especially common in collaborative projects where one person does research and another does synthesis.

The brief becomes a new file (not a patch to an existing doc) with: which documents were mentioned, which ones the researcher flagged as high leverage, and enough context for the next person or agent to know where to start. Tag with `priority: high` and `type: research-brief`.

Example: Weave Session 24 harvested a call where a collaborator walked through their funding research. The harvest output was `Funding Research - Research Brief.md` -- the brief the operator had asked them to write, assembled from the verbal tour.

This pattern applies when: (a) the transcript is someone describing research they've done, (b) no written brief exists yet, (c) the research is in a folder or set of documents that others need to navigate. The brief is a harvest destination alongside the usual synth docs.

## Document Structure Lock

When harvest output requires creating a substantial new document (reconciliation paper, research overview, multi-section analysis, research brief), lock the file structure with the user before writing begins. Use AskUserQuestion (if available) or ask in prose. Key decisions to lock:

- **Document type and posture** -- research brief vs. synthesis doc vs. design doc? Descriptive vs. prescriptive vs. exploratory?
- **Section structure** -- what sections does the user expect? Flat or nested? How granular?
- **Audience** -- is this for the operator, the team, or external readers?
- **Scope ceiling** -- what's explicitly out of scope? Where should you stop?

This applies to new file creation only. Patching existing docs with harvest extracts doesn't need a structure lock -- the structure already exists.

Rationale: document structure, posture, and scope ceiling are expensive to reverse after writing. Locking them upfront with explicit choices prevents rework. (Source: WV-S86 via FR)

## Batch Mode

When processing large transcript batches (total word count exceeding ~50k words, typically 15+ sources), single-agent sequential processing exceeds context capacity and degrades quality. Use parallel subagent extraction instead.

**When to use batch mode:**
- Total word count of routed transcripts exceeds ~50k words
- More than ~10 transcripts need harvesting in one session
- Sources are long-form (conference panels, multi-hour meetings, lecture series)

**Setup:**
- Divide sources into subsets of ~3 files each
- Each subagent receives: its file subset, the project's Content Interests, exact citation format requirements (`[[NoteTitle#Section Header|YYYY-MM-DD -- Section Name]]`), and the list of destination documents
- Subagents run in parallel, each completing Steps 1-9 for their files

**Coordination:**
- A coordinator agent merges results across subagents and deduplicates cross-references
- Citation anchors (section headers, timestamps) must be preserved through the merge -- verify anchors resolve after merge
- The coordinator handles Step 10 (session log) for the full batch

**Validated:** WV-S91 (Katapult batch, 15 transcripts, 5 parallel agents, ~3 files each). Parallel extraction preserved citation fidelity and produced higher-quality extracts than sequential processing under context pressure.

## Principles

- Treat each source as one atomic unit -- complete steps 1-9 before the next source (step 10 waits til session end)
- Synthesize, don't transcribe. One idea per paragraph.
- Preserve tensions and disagreements -- don't flatten nuance.
- Include speaker attribution where relevant.
- Extract `lexicon_candidates` if the transcript contains novel language or framings.

## Reader-Facing Output

If the harvest destination is a document a person will read start to finish - a research resource, a brief, a report, an onboarding doc - load `Seed/Guides/Reader-Facing Prose Style.md` before drafting prose there and run its verification pass before shipping. Segmentation headers, routing YAML, tracking rows, and triage verdicts are exempt.

## See Also

- [[shared-layer-redaction]] -- REQUIRED overlay whenever the harvest destination is a shared layer (a repo or folder readable by the people discussed in the material): run its per-passage test before anything enters the shared layer
- [[Harvest Workflow Guide]] -- full walkthrough, edge cases, and the 3-step end-of-harvest checklist
- [[YAML Schema]] -- harvest field definitions
- [[Editorial Principles]] -- synthesis guidance
- [[Conventions Registry]] -- citation format and source tags
- Segmentation and lexicon criteria: see the sections above (folded in from the retired Universal Protocol transcript-prep section)
