---
title: VERSION History - 1.14.0 to 1.14.4
type: guide
created: 2026-11-19
updated: '2026-11-19'
operator: Andrew
origin: 'Seed 1.15.0 2026-11-19 - What''s New 1.14.0 to 1.14.4 moved from VERSION.md word for word (size rotation before 1.15.0; VERSION.md was 26.5 KB)'
edit_log:
  - 'Seed 1.15.0 2026-11-19 - created: What''s New 1.14.0 to 1.14.4 moved in from VERSION.md word for word'
---

# VERSION History - 1.14.0 to 1.14.4

A closed part of the Seed's version history: the "What's New" entries 1.14.0 to 1.14.4, newest first, moved here from `VERSION.md` word for word. Newer entries are in `VERSION.md`; older entries are in `VERSION History - 1.11.16 to 1.13.5.md`, `VERSION History.md`, `VERSION History - 1.10.0 to 1.11.3.md` and `VERSION History - 1.0.0 to 1.9.5.md`.

## What's New in 1.14.4

**Patch release (2026-11-11): plants from a meta-learning review, a tool-behavior batch from a partner project (Knowledge Commons), and a size rotation.** Docs only; no script changes. Shipped in the Seed:

- `Guides/Working Principles - continued.md` (new): the continuation of `Working Principles.md`, which passed the 30 KB soft size. First principle: a delegated agent's verdict ("not found", "not planted", "done") is a claim until the lead reads the live line; re-check every negative verdict and every verdict you act on. `Working Principles.md` embeds it and points to it from "Verify the drift". `GUIDES.md`: a row for it.
- `Skills/meta-learning-review/SKILL.md` v1.5.7: Step 2 - a verifier sub-agent errs both ways on long paragraphs; re-check every "not planted" and "already removed" claim on the live line. `SKILLS.md` row updated.
- `Guides/Review Automation.md`, Backlog + FR triage row: before a bulk close, check each "close done" verdict on disk, independently of the agent that gave it.
- `Guides/Cowork Build Environment/8.2`: a search agent's "not found" is a claim to re-check at any model tier; links to the new principle.
- `Protocols/Conventions Registry/7.0`: How to split safely - step 6, the shell keeps the original `origin:` (origin is immutable) and the split is recorded in the section files' first edit_log line and the session log; step 1, also grep scripts and skill files for the old file path. `Protocols/YAML Schema.md` and `Guides/Published Artifacts and ArtifactData Behaviors.md`: each shell's `origin:` is back to its first entry.
- `Protocols/Conventions Registry/9.0` Hub mode: first-touch exception for the Embed Map Status. `26.0`: a hand-posted board block takes only known keys and a summary of at most 120 characters; the render refuses any other block and leaves it in `## Unreconciled`. `30.0`: the reader's half - re-read a report, count or gate state at the moment of action or approval.
- Tool behaviors: `Guides/Cowork Scheduled Tasks.md` - a launchd job's blocked folder still passes `os.path.isdir`, and the first open fails with `PermissionError` (Errno 1); only Full Disk Access lifts the block; `create_trigger` takes no model choice. `Guides/Published Artifacts and ArtifactData Behaviors/2.0` - interactive Cowork threads offered no `ArtifactData` (2026-11); run a whole-store export as a one-time scheduled task. `Guides/MCP Reliability and Write Verification/12.0` - a title-only `search_notes` can return non-matching titles; `3.0` - a timeout right after a write can be the first sign of a bridge drop.
- `VERSION.md` rotated: What's New 1.11.16 to 1.13.5 moved word for word to a new closed part, `VERSION History - 1.11.16 to 1.13.5.md`. Nothing deleted. `VERSION History.md`: the intro names the new part and says that the next rotation starts a new closed part, named by its version range. `README.md`: the file list names every history part.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.3

**Patch release (2026-11-11): tool behaviors from partner projects (LocationScout, ReWoven) and two DataWizard learnings.** Docs only; no script changes. Shipped in the Seed:

- `Guides/Chrome MCP and Web Tool Behaviors/2.0`: rung 18 - a status word in raw HTML ("no longer available") can be a template attribute on every page; parse the DOM and read the named elements.
- `Guides/Published Artifacts and ArtifactData Behaviors/2.0`: `profiles()` can return no names unless the `user` capability declares `scopes: ["profile"]`; declare first, then publish the code.
- `Guides/Browser and File System Access Behaviors.md`: the `hidden` bullet - test the computed style, not the attribute; new bullet - scope `.list > li` so nested lists are not styled.
- `Guides/Cowork Build Environment/8.1`: a fixed name in the device shell's `/tmp` can hold another session's script (use a session-specific folder in `$HOME`); the session disk can be full while the vault mount has room (build in the cloud container and commit back).
- `Guides/Working Principles.md`: new principle - a size cap on an append-only record makes room (the naming grows) instead of stopping.
- `Guides/Script Portability.md`: "Case-insensitive disks" - the cloud container's disk is case-sensitive, so run tests that create files on the Mac before the build counts as done. `Guides/Cowork Build Environment/9.0` points to it.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.2

**Patch release (2026-11-10): `classify.py` reads quoted frontmatter values correctly.** Its simple frontmatter reader only stripped the outer quotes, so a single-quoted value with an apostrophe (`'Let''s GROW'`) came back with the doubled `''`, and a double-quoted value kept its escapes. A new helper `_fm_unquote` reads a single-quoted value with `''` undoubled and a double-quoted value with its escapes decoded; a plain value reads as before. This matters once a frontmatter writer quotes every string. Standard library only.

- `Scripts/classify.py`: new `_fm_unquote()`; `parse_frontmatter()` calls it for each scalar. No other behaviour change.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.1

**Patch release (2026-11-10): the capture pointer rule now lives in the YAML Schema.** Docs only; no script changes. Release 1.14.0 said not to add `core_id` to a clipping by hand until the YAML Schema described the pointer. It now does, so that hold is lifted: you may add `core_id` to a `homepage` or a clipped `person` page once you have confirmed the match (the name matches, or the clipping's URL host is exactly the core's `website` host). Never guess a match, and never add `hid`, `entity_kind` or other `core_*` fields to a clipping. Shipped in the Seed:

- `Protocols/YAML Schema/3.0 YAML Schema - Holonic Records and Tool Evaluation.md`: new entry "Capture pointer". A capture carries `core_id` only; the value is the core's `core_id` string, not a wikilink or a path; the core does not list its captures and the index derives the back-list; `core_id` is written only for a human-confirmed match, never by the classifier. A note about several subjects joins cores through its companion's `entities:` list (`slug` = `core_id`); no core is made from a mention. The projection writer rule now names a capture's `core_id` as its one exception. The "On every projection" block is unchanged.
- `Protocols/Content Type Taxonomy.md` (still v2.8): the `homepage` and `person` entries point at that rule instead of saying to wait for it.
- `Config/taxonomy.yaml` (taxonomy_version still 2.8): the `homepage` and `person` `yaml_note` say the same.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.0

**Minor release (2026-11-10): a new content type `homepage`, and `entity` now means a core record only.** A clipped web page of one organization was typed `entity`, the same type as the one canonical core record for that organization. The two now have separate types: a clipped organization page is `homepage` and stays in `_Clippings/`, where the web clipper saves it; `entity` is kept for core records (with `entity_kind` and `core_id`), which the federating skill makes and the classifier never assigns.

A `homepage`, or a clipped `person` page, carries `core_id` when its subject has a core; never `hid` or `entity_kind`. The note points at the core; the core does not list its clippings. One DataWizard session. Shipped in the Seed:

- `Protocols/Content Type Taxonomy.md` v2.8: new `homepage` entry; `entity` narrowed to core records; `person` says a person core is `type: entity`, `entity_kind: person`; `event` and the Classifier Decision Tree name `homepage` where they named `entity`; 20 active types.
- `Config/taxonomy.yaml` (taxonomy_version 2.8): new `homepage` key with `yaml_additions: [core_id]`; `entity` described as a core record, `classifier_assignable: false`; `person` gains `yaml_additions: [core_id]`.
- `Scripts/classify.py`: `homepage` is a valid type and is in the prompt; `entity` stays valid (existing cores count as classified) but the classifier never outputs it - an `entity` answer from the model, a rule or an old dry-run log is written as `homepage`, and a note already typed `entity` is never rewritten, by any path. The classifier never writes `core_id`. Stale taxonomy version and type count fixed.
- `Scripts/route_notes.py`: `homepage` routes to `_Clippings`; one already there stays put. `entity` routes to `_Entities` only when the note carries `core_id`; an `entity` note without one is listed for a human, not moved.

**Existing notes:** a clipping already typed `entity` keeps that type until it is retyped to `homepage`; the classifier skips notes that already carry a valid type. Nothing breaks if you leave them. To convert one, change `type: entity` to `type: homepage` by hand; no script does it. `route_notes.py` then moves it to `_Clippings/`. Until then it is listed under "needs human routing" and not moved. Do not add `core_id` to a clipping by hand until YAML Schema, "Holonic Records" describes this pointer.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)
