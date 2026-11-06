---
name: harvest-router
description: >-
  Use when scanning the vault for unharvested content and routing it to the
  right projects. Triggers on: 'what needs harvesting', 'scan for new content',
  'route this file', 'where does this go', 'check what's new', after bulk
  imports (Fathom, Whisper, Reddit, clippings), or when files accumulate at the
  vault root. Scans content folders and root, classifies files, moves them to
  correct folders, sets routing YAML, and appends action items to target
  projects.
type: skill
version: '1.3.0'
updated: '2026-11-06'
origin: 'DW-S312 2026-09-06 - backfilled DW-S448 from the earliest edit_log entry (D127)'
operator: Andrew
edit_log:
  - 'DW-S312 2026-09-06 - v1.2: Fathom zero-token export folded from the retired Harvest Agent (D128)'
  - 'DW-S448 2026-10-31 - example project name made generic (Media Project); no behavior change'
  - 'DW-S456 2026-11-02 - v1.2.1: depersonalized examples (names replaced with neutral placeholders)'
  - 'DW-S470 2026-11-06 - v1.3.0: Fathom paragraph rewritten to the connector path (no export tool); harvest-handoff marker on the Step 6 line; new Hub mode section (D167, D168)'
---
# Harvest Router Skill

## Overview

Scan the vault for unharvested content — transcripts, articles, clippings,
meeting notes, documents — and route each item to the project(s) that should
harvest it. Sets routing YAML on the source file, moves the file to the
correct content folder, and appends an action item to each target project's
action items file so the harvest happens in that project's next session.

This is the upstream skill in the harvest pipeline. It routes; the
transcript-harvest and document-harvest skills execute.

## When to Use

- User says "what needs harvesting?", "scan for new content", "route this",
  "where does this go?", "check what's new"
- After a bulk import (Fathom calls, Reddit batch, clippings dump, Whisper
  transcripts from Piezo recordings)
- Periodically as vault hygiene — especially when files accumulate at the
  vault root or in `_!nbox/`
- When a new transcript appears at the vault root (common with the
  Signal/Telegram -> Piezo -> Whisper Transcription -> vault flow)
- At the start of a DW session to check what's queued across the vault

### When NOT to Use

- Actually harvesting content into project documents (use transcript-harvest
  or document-harvest)
- Evaluating external tools or repos (use tools-research)
- Triaging Reddit saves specifically (use the Reddit Tech Triage task doc,
  though this skill can handle the routing step afterward)
- Routing content that has already been harvested (`harvest_status: harvested`)

## Before You Start

1. Read this skill fully
2. Read the Vault Project Map: `_DataWizard/Workshop/Vault Project Map.md`
   — internalize the project descriptions AND the "Tech Interests by Project"
   section. This is your routing table.
3. Know which mode you're running (see below)

## Three Modes

### Mode 1: Vault Scan

The full sweep. Scan content folders and the root for unrouted files.

**Folders to scan (in priority order):**
1. **Vault root (`/`)** — highest priority. Transcripts, meeting notes, and
   misc files land here constantly. Look for `.md` files that aren't
   infrastructure (skip legacy `!`-prefixed files, canvas files, image files).
2. **`_Transcripts/`** — all transcript types
3. **`_Meetings/`** — meeting notes
4. **`_Clippings/`** — web clips and articles
5. **`_!nbox/`** — inbox/unsorted content
6. **`_Resources/`** — frameworks, reference docs
7. **`_Seeds/`** — raw ideas and fragments

**What to scan for:**
- Files with NO `harvest_status` field in frontmatter (never been touched)
- Files with `harvest_status: pending` (flagged but not yet routed to a
  specific project)
- Files with `harvest_for` already set but no corresponding action item
  (routed but lost)

**What to skip:**
- Files with `harvest_status: harvested` or `harvest_status: reviewed`
- Files with `triage_status: reviewed` (already triaged by Reddit pipeline)
- Infrastructure files (0.x files, legacy `!`-prefixed, templates)
- Files in `_Companions/` (these are outputs, not sources)
- Files in `xArchive` or `_xArchive` folders
- Files in `.obsidian/`, `.git/`, or other dot-folders

**Chunking:** If a folder has more than 30 unrouted files, process in
chunks of 15. Complete each chunk (read, route, move, write YAML, append
action items) before starting the next. Tell the user which chunks remain
if you're running low on context.

### Mode 2: Single-File

User points at a specific file. Read it, read the Vault Project Map,
assess relevance, propose routing and destination folder. Fast and
conversational.

### Mode 3: Batch-Import

After a bulk import. User tells you what was imported and where. Scan
just those files and route them. Same logic as vault scan but scoped
to the import location.

**Common batch-import sources:**
- Fathom transcripts (filed by hand via the connector - see Fathom Awareness)
- Whisper Transcription app output from Piezo recordings of Signal/Telegram
  calls (land at vault root as `.md` files, typically named with date and
  participant names)
- Reddit save imports (land in Recall Vault, use Reddit Triage task first)
- Web clipper batches (land in `_Clippings/`)

## Fathom Awareness

Before scanning transcripts, optionally check Fathom for recent meetings
that may not have been filed in the vault yet. Use the Fathom MCP
`list_meetings` tool with a `created_after` date (default: 2 weeks ago)
to see what's available. If Fathom tools aren't connected, skip this step.

Cross-reference against files already in `_Transcripts/` and at the vault
root by matching dates and participant names. Flag any Fathom meetings that
don't have a corresponding vault file — these are candidates for filing.

Report Fathom gaps to the user: "Found N Fathom meetings without vault
transcripts: [list with dates and titles]. Want me to file any of these?"

Don't block the routing workflow on Fathom — check it, report gaps, then
continue with what's already in the vault.

**Filing a Fathom call (the connector path).** The Fathom connector has no
export tool: nothing writes the file for you, so file a call in four steps.
(1) **Find the call** - `list_meetings` with a date range, or the call id
from a pasted URL (`fathom.video/calls/<id>`) via the recording-by-call-id
or recording-by-URL tool. (2) **Get the transcript** with
`get_meeting_transcript`; pass the call URL so each turn carries a
timestamp link. (3) **Write it** to `_Transcripts/` as
`YYYY-MM-DD Speaker Name.md`, with `fathom_id` (the URL call id) and
`fathom_recording_id` (the API id) in frontmatter ([[YAML Schema]],
Harvest Tracking). (4) **Segment it** - the connector output has per-turn
`[mm:ss](url)` links but no `##` headers; add them by hand
(transcript-harvest, Segmentation) or prompt for the script (Segmentation
Prompt below), then set `segmented: true`. **Long calls:** a long call's transcript can
overflow the tool output into a container file; build the vault note from
that file rather than retyping it, and from then on read the transcript by
line range (outline first), never whole. Raw transcripts are exempt from
the split rule (Conventions Registry, Shell and section architecture).
Speaker labels slip at turn changes (transcript-harvest, Segmentation).
(DataWizard, 2026-10; 2026-11)

## The Routing Loop

For each unrouted file:

### Step 1: Read and classify

Read the file. Determine its content type:
- **Transcript** — conversation, interview, meeting recording, voice memo
- **Article/clipping** — web content, blog post, newsletter
- **Meeting note** — structured notes from a meeting (not a transcript)
- **Document** — PDF, report, reference material
- **Seed** — idea fragment, observation, raw thought
- **Other** — anything that doesn't fit the above

### Step 2: Assess project relevance

Compare the file's content against the Vault Project Map. For each
project, ask:
- Does this content match the project's description or content interests?
- Does it mention tools, patterns, people, or topics the project cares about?
- Would harvesting this into the project's documents add value?

**Scoring guidance:**
- A file can be relevant to multiple projects — that's expected
- Be generous with routing (it's cheaper to skip during harvest than to
  miss something during routing)
- If a file is clearly personal/administrative with no project relevance,
  mark it `harvest_status: reviewed` with a note and move it to the
  appropriate content folder without setting `harvest_for`

### Step 3: Propose routing and file move

Present your assessment to the user before writing anything:

```
File: 2026-04-22 Meeting Transcript.md
Type: transcript
Current location: / (vault root)
Move to: _Transcripts/
Relevant to:
  - Weave Project — discusses story arc structure
  - Media Project — mentions podcast episode planning
Notes: Conversation between Person A and Person B covering Weave narrative
       and upcoming Media Project recording schedule.
```

For vault scan mode with many files, batch the proposals into groups
of 5-10 and get approval per batch.

For single-file mode, propose and wait for approval.

### Step 4: Move the file

Move the file to the correct content folder based on its type:

| Content type | Destination folder |
|---|---|
| Transcript | `_Transcripts/` |
| Article/clipping | `_Clippings/` |
| Meeting note | `_Meetings/` |
| Document | `_Docs/` |
| Seed | `_Seeds/` |
| Resource/framework | `_Resources/` |

Use `obsidian:move_note` for the move. If the file has a date-based name
(e.g., `2026-04-22 Meeting Transcript.md`), keep the original filename.

**Subfolder routing:** Some content folders have subfolders for further
organization. If the file clearly belongs in a subfolder (e.g., voice memo
transcripts go to `_Transcripts/Voice Memos/`), route it there. When in
doubt, use the top-level folder — the user can refine later.

**Verify after moving.** Confirm the file exists at the new path before
updating YAML. If the move fails, tell the user and skip to the next file.

### Step 5: Set routing YAML

After moving, update the file's frontmatter at its NEW path:

```yaml
harvest_for:
  - "[[Project Name 1]]"
  - "[[Project Name 2]]"
harvest_status: pending
routing_date: YYYY-MM-DD
routing_notes: "Brief note on why each project is relevant"
```

Use the project's display name in `harvest_for` (e.g., "DataWizard",
"Media Project", "Weave Project"), not the folder path.

**For files with no project relevance** (personal, administrative, or
content that's been reviewed and isn't harvestable):

```yaml
harvest_status: reviewed
routing_date: YYYY-MM-DD
routing_notes: "Personal/administrative — no project harvest value"
```

**Compatibility with Harvest Provenance Architecture:** The routing YAML
uses `harvest_for` (project routing) which is distinct from `harvested_into`
(destination tracking set after actual harvesting). The routing skill sets
the former; the harvest skills set the latter.

### Step 6: Append action items

For each project that received routed content, append a line to that
project's action items file (`0.5 Action Items - [Project].md`):

```markdown
- [ ] **Harvest pending content ([date])** — [N] new items routed. Sources: [brief list of filenames]. Use transcript-harvest or document-harvest skill. <!-- harvest-handoff -->
```

**Finding action items files:** Action items files follow the pattern
`0.5 Action Items - [Project Name].md` in the project's
`_Infrastructure - [Project]/` folder. If you can't find one, tell the user rather than
creating one.

The `<!-- harvest-handoff -->` marker lets the orientation sweep list the
project's open handoff lines. When the 0.5 is a sectioned shell, the line
goes in the section file the shell embeds, not in the shell.

**Deduplication:** Before appending, check if there's already a pending
harvest action item. If so, update the count and source list rather than
adding a duplicate entry.

## Hub mode (one reading for many projects)

When the vault runs a harvest hub project - the default first reader for
calls and transcripts - the hub reads each call once against every
project's Content Interests (read from each project's 0.0 on disk) and
writes one embeddable synth note ([[Conventions Registry]], Harvest via
embeddable synth note) with one evidence section per project. Each target
project then accepts, edits or declines its own section in its own session
(transcript-harvest, "Accept a hub section"). The hub never edits another
project's documents. The first-touch rule stays: a project may still
harvest a call itself, and the hub then backfills the other projects.

**What the hub writes, per call:**

1. **The transcript** in `_Transcripts/` (Fathom: the connector path
   above), segmented, with `harvest_for` (canonical project names),
   `fathom_id` and `fathom_recording_id`, and
   `companion: "[[c_<transcript name>]]"` - written **at routing, as the
   claim**: a session that finds `companion:` set knows the call is taken.
2. **One `harvest_log` line per target**, state `pending`, with
   `decision #-` and the section heading last ([[YAML Schema]], Harvest
   Tracking). `harvest_status` is the roll-up; never hand-set it (at
   routing the roll-up is `pending`, which is what Step 5 writes).
3. **The synth note** in `_Companions/_Transcripts/c_<transcript name>.md`:
   a Synopsis (the team-download header: what the call was, and the
   projects that have sections), an **Embed Map** with a Project column
   (Project, Abbr, Section, Embed string, Route, Destination, Status;
   Status starts `open`, from the fixed list in Conventions Registry 9.0,
   Hub mode), a **Segment Map**, then one `##` section per project,
   headed `<Project> - <topic>`. A section is evidence, not a draft: what
   was said, the speaker, a linked timestamp (Conventions Registry,
   Citation format), and the Content Interests line it matched.
4. **The pointer**: the Step 6 line, with its `<!-- harvest-handoff -->`
   marker, in each target's 0.5 - never anything inside the target's own
   documents.

**Rules for the reading:**

- **Route.** The Embed Map Route is `native` for any target whose
  destination is in a shared layer (a shared folder or a team repo);
  `embed` only for private-layer targets (Conventions Registry, Harvest via
  embeddable synth note).
- **The Segment Map names project segments only** - topic, timestamp,
  projects. It never describes a skipped or private part of the call.
- **Second pass.** After the reading, run a checklist pass over the
  Content Interests digest: for each project, check each Content Interests
  line's names, projects and key terms against the call. One reading
  alone tends to miss a project per call.
- **A name hit with no Content Interests.** A project named directly in
  the call gets a short section even when its 0.0 has no Content
  Interests list, and the hub posts that project a board ask to write
  them (content-interests-review skill).
- **Check the spelling of names.** Before writing a person's or an
  organisation's name, check `_Entities/` and existing vault notes for the
  spelling in use. Transcription hears one name many ways, and a new
  spelling mints a duplicate entity across projects. Note the variants
  once in the Synopsis.
- **Sensitivity marks are mandatory** when any target is a shared layer:
  mark candid remarks about named people inline (Conventions Registry,
  Harvest via embeddable synth note, step 3). A very candid call may stay
  in `_Private/`.
- **Backfill.** When a project harvested the call first, its section
  points at that harvest and adds only the evidence the first harvest did
  not carry; its line is `harvested` only when the section is pointer-only
  ([[YAML Schema]], Harvest Tracking, backfill rule).
(DataWizard, 2026-11)

## After the Scan

Summarize what was done:

```
Routing complete.
- Scanned: [N] files across [folders]
- Routed: [N] files to [N] projects
- Moved: [N] files to content folders
- Reviewed (no harvest value): [N] files
- Fathom gaps: [N] meetings without vault transcripts

Action items appended to:
- ! Action Items - DataWizard.md (3 new items)
- ! Action Items - Weave.md (1 new item)
- ! Action Items - Media Project.md (2 new items)
```

## Segmentation Prompt

After routing, check whether any routed transcripts need segmentation
before they can be harvested. The transcript-harvest skill requires `##`
section headers for deep-link citations — without them, harvesting is
less effective.

**Check each routed transcript for:**
- `segmented: true` in YAML — already segmented, skip
- Existing `##` headers in the body — ready. Fathom connector output is
  not pre-structured (per-turn timestamp links, no `##` headers): it needs
  headers
- No headers and no `segmented` field — needs segmentation

**For unsegmented transcripts**, prompt the user to run
`segment_transcript.py` (uses Qwen via Ollama locally):

```
The following transcripts need segmentation before harvest:
- _Transcripts/2026-04-22 Meeting Transcript.md
- _Transcripts/2026-04-20 Team Call.md

Run segment_transcript.py on each:
  python _DataWizard/Seed/Scripts/segment_transcript.py "_Transcripts/2026-04-22 Meeting Transcript.md"

Or batch them:
  for f in [list]; do python _DataWizard/Seed/Scripts/segment_transcript.py "$f"; done

After segmentation, set segmented: true in each file's YAML.
```

Don't run segmentation yourself — it requires the local Ollama/Qwen
stack. Just identify which files need it and give the user the commands.

## Common Mistakes

- **Routing without reading the Vault Project Map.** The map IS the routing
  table. Without it you're guessing. Read it every time.
- **Skipping the move step.** Files at the vault root get lost. Moving them
  to the correct content folder is as important as setting the YAML.
- **Over-routing.** Every file doesn't need five projects. Most files are
  relevant to 1-2 projects. Only route to projects where harvesting would
  actually produce value.
- **Under-routing.** Being too conservative means project instances never
  see the content. When in doubt, route it — the project instance can
  decide to skip during actual harvest.
- **Writing YAML before moving.** Move first, then write YAML at the new
  path. Writing YAML at the old path and then moving can cause frontmatter
  issues.
- **Forgetting to verify the move.** `move_note` can fail silently. Always
  confirm the file exists at the destination before updating YAML.
- **Creating action items files that don't exist.** If a project doesn't
  have an action items file, tell the user. Don't create infrastructure
  that might not match the project's conventions.
- **Routing into xArchive.** Never move files into archive folders. If a
  file should be archived, tell the user.
- **Blocking on Fathom.** The Fathom check is informational. Report gaps
  and move on. Don't stall the vault scan waiting for Fathom calls to be filed.

## Principles

- **Route generously, harvest selectively.** It's the project instance's
  job to decide what's worth extracting. The router's job is to make sure
  the content gets seen.
- **Move files to their home.** A transcript at the vault root is invisible
  to anyone scanning `_Transcripts/`. Routing includes physical placement.
- **One atomic pass per file.** Read, classify, route, move, YAML, action
  item — complete all steps before moving to the next file.
- **The Vault Project Map is the source of truth for routing.** If the map
  is stale, flag it. Don't invent routing logic that isn't grounded in
  what the projects say about themselves.
- **Async handoff via action items.** The router doesn't harvest. It queues
  work for project instances that have the full context to do it well.

## See Also

- `_DataWizard/Workshop/Vault Project Map.md` — the routing table
- `_DataWizard/Workshop/Design/Routing Agent and Dynamic Vault Map.md` —
  the original design doc for this skill
- `_DataWizard/Workshop/Design/Harvest Provenance Architecture.md` —
  YAML schema for harvest tracking (downstream of routing)
- transcript-harvest skill — executes harvests from transcripts
- document-harvest skill — executes harvests from articles/docs
- tools-research skill — for evaluating external tools (not vault content)
- `_DataWizard/Workshop/Triage/Cowork Task - Reddit Tech Triage.md` —
  the Reddit-specific triage workflow (precursor to this skill)
- content-interest-scan skill — bulk scanning of material pools against
  project Content Interests. Complement: harvest-router routes individual
  files on demand, content-interest-scan does systematic bulk scans and
  nightly incremental checks.
