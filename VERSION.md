
seed: 1.13.5
protocol: 1.8
project_instructions: 4.10

**Canon write gate:** edits to this file come only from a claimed session of the project that owns it. An instance governed by another project's instructions files a proposal at the owning project's intake (or an exchange note in its Session Exchange) instead of editing. Reviewed exceptions are whitelisted in the lint config. (Conventions Registry: "Cross-project canon write gate"; DataWizard, 2026-09)

## NOTICE - Seed git history rewritten again 2026-10-17 (instances: read this)

On 2026-10-17 the Seed repo's git history was rewritten a second time (privacy and security hygiene). Removed from every past commit: a Telegram session file that an auto-sync had committed, a copy of the operator's private `Vault Config.md`, every committed `*.bak` rollback copy, and two `.pyc` files. Replaced in old file versions: private chat identifiers, local home-directory paths and a private event name (placeholders such as `1234567890` and `/Users/USERNAME` now stand in). Computer names in automatic commit messages now read "on Mac". Today's files did not change; every commit kept its author, date and message text.

**Every commit id changed, including the very first one.** What a clone made before 2026-10-17 sees:

- `git pull` stops with `fatal: refusing to merge unrelated histories`. Nothing is merged. Good. A plain `git push` is rejected (non-fast-forward).
- `git status` after a fetch shows `[ahead N, behind M]` with N equal to M, or one less (a clone from before the rewrite's preparatory commit).
- DW Save from before 1.10.1 (most clones) reports `ERROR: could not reach GitHub - check your connection` on every run. The message is misleading - the connection is fine, the pull refused - and nothing is pushed. DW Save 1.10.1 and later instead reports `BLOCKED: secret file(s) would be published` for the old commits. **Do not follow that message's generic fix (`git reset --soft ...`) in this case** - it would re-stage the old example ids.

**Zip installs** (no `_DataWizard/Seed/.git` folder): nothing to do; run `update_seed.sh` as usual.

**Git clones:** follow `Guides/Git Guide/7.0 Safety and Recovery.md`, section "Recovering a Seed Clone (Remote-Agnostic)". Step 4 there names this rewrite's signature and the command for it: Step 0 backup (branch, plus stash if anything is uncommitted), fetch the canonical remote, run `git diff --stat main <canonical>/main` and confirm it lists nothing or only the three placeholder files (`Guides/Telegram Harvesting.md`, `Scripts/datawizard-aliases.sh`, `Scripts/tg_harvest_thread.py`), then `git reset --keep <canonical>/main`, then `git stash pop` if Step 0 stashed. Any other file in that diff is local committed work: branch it first, re-apply it after the reset. Untracked and ignored files (`Vault Config.md`, `Scripts/.env`, session files) are never touched. A propose-then-review rule applies as before: no reset on one Claude instance's say-so (D109).

**Forks:** a fork made before 2026-10-17 still serves the old commits. Delete it and fork again; re-apply any local work as a new branch on the new `main`. Never merge a pull request that lists hundreds of commits or says "unrelated histories" - that is the old history coming back.

Never use `git pull --allow-unrelated-histories` or any merge to recover. (DataWizard, 2026-10)

## What's New in 1.13.5

**Patch release (2026-11-09): the update scripts now work from a flat git clone, plus two guide rules.** One DataWizard session; a fresh reviewer ran the write paths on copies before install. Shipped in the Seed:

- `update_seed.sh` and `update_seed.ps1` find the Seed from the script's own folder. Nested (`_DataWizard/Seed/`) is the default. A flat clone (the clone at `_DataWizard/` itself) is supported: the scripts no longer update a second, phantom install one folder too high. With `--vault` / `-Vault` they take nested only when `_DataWizard/Seed/VERSION.md` exists, flat only when `_DataWizard/` already holds a Seed, and otherwise do a fresh nested install. In a flat layout they print a one-line notice. A warning shows when both shapes are present. The four git recovery messages name the real guide path. New flag `--print-paths` / `-PrintPaths` shows which Seed would be updated, then stops before any write or download; `--help` shows usage.
- `Guides/Seed Install and Update.md`: new section "Nesting a flat clone" (copy-paste moves for macOS/Linux and PowerShell that keep `.git` and ignored files, move your own project files back up, then verify and re-point autosync and DW Save), and "Bugs and requests" (GitHub Issues for Seed users; issues are public, so no names or session ids). Manual Update names both layouts.
- `README.md`: "Two layouts" points at the nesting section; `Vault Config.md` goes in your Seed folder in either layout; new "Bugs and requests".
- `Guides/Published Artifacts and ArtifactData Behaviors/1.0`: sub-agents in the same container can read the file that an `Artifact` read saves, so a large page can go to a reviewer without passing through the lead.
- `Guides/Cowork Build Environment/8.2`: a cheap-tier search agent's "not found" is a claim to sample - brief it to search case-insensitively with two or three wordings, and re-check a sample before writing.

**Not tested:** Windows PowerShell 5.1 on Windows and macOS bash were checked by reading, not run (tests ran under bash 3.2 and 5, and PowerShell 7 on Linux). Please report what you see.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste; the Project Instructions still expect `_DataWizard/Seed/`, so flat-clone users should nest (see the guide). (DataWizard, 2026-11)

## What's New in 1.13.4

**Patch release (2026-11-09): two skill updates, three guide rules, one corrected guide line and one template note from three meta-learning reviews.** One DataWizard session reviewed the learnings of about forty sessions; fresh reviewers checked every rule named here. Shipped in the Seed:

- `Skills/supervised-build/SKILL.md` v1.6.4: "Probe for silent drops" now covers what a pipeline reports - a bare result word ("not covered", "nothing found", a status code) is a pointer, not a verdict; the output states a reason specific enough to tell an empty target from a broken one, and a check that could not run says so.
- `Skills/model-casting/SKILL.md` v1.2: Handoffs, "Lead to reviewer" - pass the sources, not only a brief; name the unit of any count the reviewer checks.
- `Guides/Multi-Instance Coordination Patterns.md`: Pattern 3 - a review round that adds a new rule or new code gets its own short delta review of just that addition.
- `Guides/Cowork Build Environment/8.2`: a message sent to a sub-agent after it has begun its final answer is not read - send scope changes early, or resume it after.
- `Guides/Chrome MCP and Web Tool Behaviors/4.0`: the Reddit bullet no longer suggests resolving a share link from the shell with a crawler User-Agent (the permission check refuses it); open the link in the browser tools.
- `Templates/Coordination Board - Template.md`: hand path - the render checks hand blocks only when it runs (unknown key, summary over 120 characters) and leaves a refused block in `## Unreconciled`; put free-text notes in a one-line HTML comment.
- `SKILLS.md`: supervised-build and model-casting rows synced.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.13.3

**Patch release (2026-11-09): one skill step and six guide rules from a meta-learning review.** One DataWizard session reviewed the learnings of twelve sessions; a fresh reviewer checked the four rules named here. Shipped in the Seed:

- `Skills/supervised-build/SKILL.md` v1.6.3: In-thread variant, new bullet "A third seat" - after the builder and the first review, a fresh reviewer who did not see the build runs the write paths on a copy and writes exact fix text; a fixer applies it; the lead installs with a hash check. The Scratch bullet now covers every builder, not only device-shell builders. The 12 oldest edit_log lines moved word for word to the new `references/changelog.md`.
- `Guides/Working Principles.md`: "A completion is a disk fact, not a claim" names its fifth home, the session-closer's tracking-claim verification.
- `Guides/Multi-Instance Coordination Patterns.md`: Incidental concurrency, "A ruling can land under you" - re-read the decision log tail before a write a convention governs; list earlier writes as a follow-up, do not redo them mid-session.
- `Guides/MCP Reliability and Write Verification/1.0 Known MCP Issues.md`: append a new `edit_log` line after the whole last entry (long entries wrap), match the file's order, parse the frontmatter after the write.
- `Guides/Cowork Build Environment/`: 8.0 (after Quit, `pgrep` can still list Chrome helper processes that do not hold the session disk - go by `lsof`); 8.1 (install a reviewed Mac-side script beside the live file, then md5, backup and swap by the operator); 8.2 (scratch output outside the vault for every builder on any surface); 9.0 (new first bullet: test under the runtime that will run it - interpreter, flags, environment).
- `SKILLS.md`: supervised-build row synced.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.13.2

**Patch release (2026-11-08): two files sectioned, VERSION.md rotated, 31 tool behaviors planted from six projects.** One DataWizard session. Shipped in the Seed:

- `Protocols/YAML Schema.md` is now a shell plus four section files in `Protocols/YAML Schema/`: 1.0 Core Fields (the two top callouts, Document Weighting, Work-Item Status, Session Log Fields, Creation-Time Metadata Contract, Team Coordination Fields and the rest of the general fields), 2.0 Harvest and Federation, 3.0 Holonic Records and Tool Evaluation, 4.0 Dates, Provenance and AI Content. Content moved byte for byte (Conventions Registry 7.0); no heading was renamed, so a pointer that names a heading still finds it. Edit the section files, never the shell. A link to a heading inside the schema now names the section file: `[[1.0 YAML Schema - Core Fields#Team Coordination Fields]]`.
- `Guides/Published Artifacts and ArtifactData Behaviors.md` is now a shell plus `1.0 Published Artifacts - Publishing and Reading` and `2.0 Published Artifacts - Store, Sharing, Comments, Rendering and Runtime` in the folder of the same name. Content moved byte for byte.
- `VERSION.md` rotated: What's New 1.11.10 to 1.11.15 moved to `VERSION History.md`, and 1.10.0 to 1.11.3 moved from there to a new closed part, `VERSION History - 1.10.0 to 1.11.3.md`. All word for word; nothing deleted.
- `Guides/Cowork Build Environment/`: 3.0 (on a device VM with an older Python, `pip install --target` into a scratch folder works - probe before you rule a test run out); 4.0 (a sub-agent's Write tool can turn escape sequences into real invisible characters; a long heredoc pasted from chat into zsh can be cut off - ship the script as a file and give one command); 5.0 (behind the cloud workspace proxy, GDAL `/vsicurl/` needs the proxy CA bundle; Python `urllib` got 403 where `curl` worked); 8.0 (the default device shell call limit and `timeout_ms`; `nohup` still dies at the end of a call; a vault-wide recursive grep timed out and then the bridge dropped for minutes - scope searches to one folder; on a network loss every remote-device tool drops and comes back on its own; call `get_device_info` before `device_request_folder_access`; a folder added in the desktop app mid-session did not reach the device shell, an in-session grant did); 8.1 (the device shell's `/tmp` can be cleared between calls; a same-path re-commit sent stale bytes again); 9.0 (no Playwright on the device VM; an interrupted git fetch leaves the old HEAD, so a check can look like a broken build); 11.0 (in one cloud session, sub-agents with only Read and Grep never stalled, while one that used Bash once waited on an approval prompt; `add_repo` with push access can be refused - stage and build instead).
- `Guides/MCP Reliability and Write Verification/12.0 Obsidian Behavioral Gotchas.md`: one write path per file per session; `patch_note` with several matches errors; `move_note` creates missing folders and cannot remove the empty one (seen 2026-06); the note-only rule also covers `.yaml` config files.
- `Guides/Cowork Scheduled Tasks.md`: a local desktop task's prompt lives in a protected folder; a scheduled run may mount only the project folders; no probe or write-test files in the vault from a scheduled run; a local desktop task does not run while the Mac is closed.
- `Guides/Editing the Claude Desktop Config.md`: a safe scripted edit of `claude_desktop_config.json`; on macOS a Screen Recording grant needs a full quit and reopen of the app.
- `Guides/Chrome MCP and Web Tool Behaviors/`: 2.0 (`get_page_text` can return nothing on a single-page app while `find` and `read_page` work; a tab on a browser error page cannot be scripted; a shell crawl with a browser User-Agent was refused by the permission check); 4.0 (a map site built as a JS app returns a config blob to web fetch, and the map position is in the URL; rental-site data shapes - amenity JSON, totals for the searched dates, price estimates).
- `Guides/Published Artifacts and ArtifactData Behaviors/1.0`: `publish_files` refuses the id in a page address ("invalid slug") - use the UUID slug that `get_artifact` returns; a Docs-type artifact can be born with its full markdown in one batch call.
- `Guides/Working Principles.md` and `Config/retired-signatures.yaml`: pointers name the YAML Schema section that now holds the part ("Section 4" and "S4" were stale).
- `GUIDES.md`: Published Artifacts row.

Sources: Tech Tools, Kosmosis, Rootland, LocationScout, ReWoven and DataWizard (2026-11).

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. A note that links to a YAML Schema heading with `[[YAML Schema#...]]` should repoint to the section file. (DataWizard, 2026-11)

## What's New in 1.13.1

**Patch release (2026-11-08): Conventions Registry 15.0: solo-project exception for the hub project; session-closer 3.14: branch for hub edits to solo projects (DW D173).** Shipped in the Seed:

- `Protocols/Conventions Registry/15.0 Cross-project canon write gate.md`: new "Exception - the hub project" paragraph after the Rule. The project that keeps the Seed may edit any file of a solo project (one operator, who also runs the hub) directly when necessary; by default the project does its own work. It keeps a pre-edit copy, names its session and the ruling in the edit_log, and lists the file at the cross-project write check. A shared project gets a pickup note instead.
- `Skills/session-closer/SKILL.md` v4.11.6: Step 3.14 gains a branch for a hub-project session that edited a solo project's files - list each file in the session log; check the pre-edit copy and the edit_log line. `references/changelog.md` takes the oldest edit_log line (rolling window).
- `SKILLS.md`: session-closer row synced.
- `Guides/Published Artifacts and ArtifactData Behaviors.md`: ArtifactData store - a whole-store export needs `out_dir` (Cowork desktop `ArtifactData`); the claude.ai chat database tools return documents inline and cannot export a large store.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.13.0

**Minor release: one harvest of a multi-project call, with each project accepting its own section.** A hub project reads a call once and writes one shared note with a section for each project; each project accepts, edits or declines its section in its own session. One DataWizard session (2026-11), from a hand pilot on three calls, an independent review of the pilot, an Opus build on copies and a second independent review; DataWizard decisions D167 and D168. Shipped in the Seed:

- `Protocols/YAML Schema.md`, Harvest Tracking: `harvest_log` for any source routed to two or more projects (link keepers and transcripts), one grammar: `<Project> - <state> - <date> - <session> - decision #<N or -> - <outcome>[ - section: <heading>]`. `<Project>` is the bare project name; each line is one physical line (no continuation lines - check after the edit); lines are only appended, never rewritten (a migration is the one exception). `harvest_status` is a roll-up, never set by hand. A first-touch project's line is `harvested` only when the hub section is pointer-only. `harvest_for` is promoted from deferred; `fathom_id` (the call id in the URL) and `fathom_recording_id` (the API id) on the transcript.
- `Skills/transcript-harvest/SKILL.md` v0.10.0: new step "Accept a hub section" - accept, edit or decline; place it in your own documents; then touch four places (the destination note; the Embed Map row and `embed_targets`; your own `harvest_log` line; your harvest-handoff line in 0.5) and add the Harvest Log row. Step 8 no longer sets `harvest_status` by hand. Segmentation: Fathom speaker labels slip at turn changes - credit by what was said and note the slip. No pointer to a Fathom Meeting Index.
- `Skills/harvest-router/SKILL.md` v1.3.0: the Fathom path is the connector path (find the call, get the transcript, write it, segment; there is no export tool; read long calls in parts). New "Hub mode": an Embed Map with a Project column; `companion:` written at routing as the claim; a checklist pass over every project's Content Interests after the first reading; a direct project-name hit gets a short section even with no Content Interests, plus a board ask to write them; check `_Entities/` and existing notes for a name's spelling; `native` route for shared-layer targets. Every Step 6 action-item line carries `<!-- harvest-handoff -->`.
- `Guides/Orientation Flag Sweep - Query Spec.md`: sub-check (c) also lists open `<!-- harvest-handoff -->` lines in your 0.5 (sectioned 0.5 files included), and runs even when the optional intake check is skipped. The trace format is unchanged.
- `Protocols/Conventions Registry/`: 9.0 (`native` route for any target in a shared layer, `embed` only for private-layer targets; the fixed Embed Map status list - open, accepted, edited, declined; sensitivity marks mandatory when any target is a shared layer), 11.0 (call timestamps as `[@mm:ss](url?timestamp=s)`, plain `@mm:ss` as the fallback), 17.0 (a transcript's shared note is its synth note), 7.0 (raw transcripts are exempt from the split rule; read them by line range).
- `Guides/Harvest Workflow Guide.md`: the multi-project paragraph follows the roll-up rule; speaker-label slip; no Fathom Meeting Index.
- `SKILLS.md`: harvest-router and transcript-harvest rows.

**For vaults that run the intake scripts** (`ih_tool.py` 1.1.3, `intake_apply.py` 0.1.6, vault-specific, not in the Seed): list items folded onto continuation lines by Obsidian's frontmatter tools are now read as one value; unfolded input reads as before.

**Action for other projects:** run `update_seed`. When a hub harvest-handoff line is in your 0.5, follow transcript-harvest "Accept a hub section". Keep each `harvest_log` line on one physical line. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.12.3

**Patch release: edit_log trim rule for script-generated notes (D127 amended).** One DataWizard session (DW-S466, 2026-11). Shipped in the Seed:

- `Protocols/YAML Schema.md`, edit_log rules: trimmed lines are still copied nowhere for hand-stamped files; a script-generated note (an index or catalog a script rewrites) moves its trimmed lines into its own edit-log archive note, because no session-log manifest holds those run records.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.12.2

**Patch release: 3 tool behaviors from Tech Tools, Rootland and DataWizard, and one new tool-note field.** One DataWizard session (2026-11), planted from board asks B-0322, B-0325 and B-0296 (part 1), and from its own repo-scan fix. Shipped in the Seed:

- `Protocols/YAML Schema.md`, Tool Evaluation Notes: new field `source_url` - a tool note born from an intake link carries that link, so a script finds the intake item without parsing `origin:`.

- `Guides/Cowork Build Environment/`: 5.0 (the "not enabled for this session" GitHub API refusal: the cause is a repository not attached to the session, `gh api` fails the same way, and WebFetch of the github.com page still works) and 9.0 (keep test fixtures out of synced folders: a Dropbox client changed folder mtimes on a fixture copy within seconds, so a (size, mtime) snapshot gate failed falsely - use `mktemp -d`) and 10.0 (a clone of a Git LFS repository stops silently when `git-lfs` is not installed; finish it with the LFS filter turned off).
- `VERSION History.md`: the What's New entries for 1.11.9 and 1.11.8 moved there word for word (size rotation). Nothing was cut.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.12.1

**Patch release: 26 tool behaviors from six partner projects (VibeCut, Rootland, LocationScout, Events Map, Common Woods, Tech Tools).** One DataWizard session (2026-11), planted from ten board asks (B-0261, B-0267, B-0274, B-0285, B-0289, B-0290, B-0292, B-0295, B-0297, B-0298), each checked against its source note in a second review. 15 are new items and 11 extend items that were already there; 3 were already covered. Shipped in the Seed:

- `Guides/Cowork Build Environment/`: 1.0 (a `prunable` git worktree in the device shell is harmless - never prune from there), 4.0 (closing a Terminal window kills a long run - use `caffeinate` and a resumable script), 5.0 (a CLI blocked at the run step in the cloud - hand the operator a Mac command; parallel helpers share one site's failures), 8.0, 8.1 (macOS `tar` keeps the Mac uid, so git in the cloud says "dubious ownership" - `chown -R` first; commit only after an edit returns and check the size; a one-off commit failure; builders work on a copy while the bridge is down), 8.2 (a finished sub-agent cannot be resumed - keep briefs self-contained) and 9.0 (run gate bundles one at a time; test a Referer-locked key on its real origin).
- `Guides/Chrome MCP and Web Tool Behaviors/`: 2.0 (two new rungs: a lead Chrome pass for a directory helpers cannot read, after a robots.txt check; a classifier refusal is final), 7.0 (the Drive connector cannot edit an existing Google Doc), 9.0 (built-in browser clicks land off target after `resize_window`), 10.0 (the extension refuses `file://`; a screenshot refused on one domain while `get_page_text` works; a 403 and a hung fetch - do not retry in the same tab) and 12.0 (a database connector that allows one migration and denies another - the fallback is a SQL file the operator runs in the dashboard; PDF text extraction joins words at line breaks - check quoted text against a second copy).
- `Guides/Published Artifacts and ArtifactData Behaviors.md`: `obsidian://` links do nothing inside the desktop app - keep the link and add a copy fallback; large pages via patch mode; `get_artifact` wants the full link, not a short slug.
- `Guides/Script Portability.md`: `set -e` does not stop on a failure inside an `&&` chain.
- `Protocols/Conventions Registry/7.0 Shell and section architecture.md`: split a note at a heading matched at the start of a line, and assert exactly one match.
- `Protocols/DataWizard Universal Protocol.md`: a link to an archived note made plain text.
- `VERSION History.md`: the What's New entries for 1.11.6 and 1.11.7 moved there word for word (size rotation). Nothing was cut.
- Depersonalization: real people's names in examples replaced with neutral placeholders (Person A, a collaborator, `2026-04-22 Meeting Transcript.md`): skills git-onboarding v1.1.1, harvest-router v1.2.1, transcript-harvest v0.9.4, content-interest-scan v0.1.1, design-harvest v1.2.2, block-stamper v2.1.2, document-harvest v0.5.3; guides Harvest Workflow Guide and Vault Structure Guide; three edit_log lines; `SKILLS.md`; `VERSION History - 1.0.0 to 1.9.5.md` (names only).

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.12.0

**Minor release with Project Instructions 4.10 (re-paste): the coordination board splits into a small index and one inbox per project.** Every project read the whole board at orientation, though most need only their own few asks, and the one file kept passing the 50 KB read limit. Now `Board.md` is an index and each project has an inbox file. One DataWizard session (2026-11), built and reviewed on copies first; DataWizard decision D165. Shipped in the Seed:

- `DataWizard Project Instructions.md` v4.10: Orientation 6(d) reads the index `_Coordination/Board.md` plus this project's own inbox `_Coordination/Inbox/<ABBR>.md`. The trace line keeps its format; only the PI version in it changes. Step 1 now says to compare versions part by part: 4.10 is newer than 4.9. History: `Project Instructions - Changelog.md`.
- `Guides/Orientation Flag Sweep - Query Spec.md`, sub-check (d): the two sources; count the asks in your inbox plus the asks in the index `## Live` addressed to you or `all`, each id once; claims are in the index; an `## Unreconciled` section can be in either file.
- `Protocols/Conventions Registry/26.0 Coordination board.md`: new paragraph "The board files" - the index, one inbox per project and the archive parts; each block lives in one file, placed by its `to:` list; one posting point (the end of the index `## Live`, never an inbox); the tie order between files; archive parts `YYYY-MM.md`, `YYYY-MMb.md`, ...; Recently closed is in the index only. "The mirror" now reads "the board files". Action asks still never expire automatically.
- `Protocols/Conventions Registry/28.0 ID families.md`: the board id rule scans every board file (the index with its Unreconciled section, the inboxes, the archive).
- `Templates/Coordination Board - Template.md`: the header says what the index and the inboxes hold, and that a hand post goes at the end of `## Live` in the index, never in an inbox; a line for the count table. `GUIDES.md` row updated.
- `Config/taxonomy.yaml` and `Protocols/Content Type Taxonomy.md`: new infrastructure type `coordination-board-inbox` (no taxonomy version bump).
- `VERSION History.md`: the What's New entries for 1.11.4 and 1.11.5 moved there word for word (size rotation, so this file stays under about 50 KB). Nothing was cut.
- Release check fixes (2026-11-02): 16 links from shipped Seed files to notes that exist only in the maintainer's vault were removed or made generic, so they no longer break in a new install. `Skills/session-closer/SKILL.md` v4.11.5 (Pre-close reflection: the link becomes a two-sentence rationale), `Skills/block-stamper/SKILL.md` v2.1.1, `Skills/research-tracking/SKILL.md` v1.5.2 (template example), `Guides/Harvest Workflow Guide.md`, `Guides/Git Guide/9.0 Troubleshooting.md`, `Guides/MCP Reliability and Write Verification/10.0 MCP Concurrency Practices.md`, `Protocols/YAML Schema.md`, `Protocols/DataWizard Universal Protocol.md`, Conventions Registry 9.0, 11.0 and 23.0. `README.md`: the "What's in the Seed" list names `VERSION History.md`, `Project Instructions - Changelog.md`, `GUIDES.md` and `Templates/`. The expired 2026-06-10 git-rewrite notice moved from this file to `VERSION History.md`, section "Retired notices", word for word.

**For vaults that run the board script** (`board.py`): no schema change. The render writes an inbox for each project that has an ask addressed to it alone, then the index; fold, verify and the next id read every board file. List each project abbreviation that receives asks in `Board - Targets.md` (`- ABBR: path:...`), or the render prints a warning line for it (the inbox is written anyway). An archive month past about 40 KB continues in a new part; rebuild reads every part in name order.

**Action for other projects:** run `update_seed`, then re-paste the Project Instructions (4.10) into your project settings. A project that keeps its own copy of the orientation sweep updates its board step to read `Board.md` plus `Inbox/<ABBR>.md`. Post by hand only at the end of `Board.md` `## Live`; the render moves an ask to one project into that project's inbox. Edit a block in the file where it is; if you change its `to:`, also set `updated`. (DataWizard, 2026-11)

## What's New in 1.11.17

**Patch release: a smaller coordination board. Awareness asks lapse after 30 days, several projects can mark one ask seen, and the archive keeps every version.** The board mirror had grown past the 50 KB read limit, mostly with old awareness asks nobody could close. One DataWizard session (2026-11), built and reviewed on copies first. Shipped in the Seed:

- `Protocols/Conventions Registry/26.0 Coordination board.md`: three new paragraphs. **Awareness asks lapse** at the first render 30 days after `posted` (status `stale`, closed, archived, a `lapse` event); the resolution says who saw it (`lapsed unseen after 30 days`, or `lapsed after 30 days; seen by ...; not seen by ...`, with any earlier resolution kept as ` (was: ...)`). Action asks still never expire. "Stale" now means superseded, withdrawn by the poster, or lapsed. **Seen by several projects:** an ask to two or more projects or to `all` carries `- seen_by:`; each project adds itself; the render closes a named-recipient ask as seen once all are in; a `to: all` ask closes only by lapse or by its poster. A hand `status: seen` on such an ask is refused for the status only (the seen_by mark is kept). **The archive** keeps every version: a closed row changed after archiving gets a new copy; Recently closed shows 5; the well-known targets moved to `Board - Targets.md` beside the board.
- `Guides/Orientation Flag Sweep - Query Spec.md`, sub-check (d): skip an awareness ask whose `seen_by` holds your project; lapsed asks no longer show. The trace format is unchanged.
- `Templates/Coordination Board - Template.md`: the hand-edit sentence and the `seen_by` grammar line match the board script's header; the targets list is now a pointer to `Board - Targets.md`; the example awareness ask shows `seen_by`. `GUIDES.md` row updated.
- `Config/taxonomy.yaml` and `Protocols/Content Type Taxonomy.md`: new infrastructure type `coordination-board-targets` (no taxonomy version bump).

**For vaults that run the board script** (`board.py`; `repo_scan.py` and `holon_index.py` share its operational db): the board table moves to schema 8 (a `seen_by` column). `schema_version` is now a log of applied migrations shared by these scripts, not a counter: each script checks for the version it needs and adds its own row only if absent (DataWizard decision log D147, amended). Deploy order: back up the db; copy `board.py`, `repo_scan.py` and `holon_index.py` into place together; run `board.py migrate` at once; then `board.py render`. Until migrate runs, every board command stops with a "pre-v8" message, and DW Save's board row shows a render error (the save continues).

**Action for other projects:** run `update_seed`. To mark an awareness ask seen that names several projects or `all`, add your project to its `- seen_by:` line and set `updated` - do not set `status: seen`. On an ask to your project alone, `status: seen` still works. If an awareness ask you posted needs a project to act, repost it as an action ask before it lapses. The Project Instructions do not change (still 4.9); no re-paste. (DataWizard, 2026-11)

## What's New in 1.11.16

**Patch release: how Claude Code users load the Project Instructions, and a safe home for the personal pointer in shared git repos.** From a field case in a partner project (Weave, 2026-10): a shared repo's tracked `CLAUDE.md` held one person's path to the Seed, so each fix broke it for the others, and the path never loaded because of the spaces in the file name. The import facts were checked in the Claude Code docs, in the Claude Code program, and in live runs on a Mac. Shipped in the Seed:

- `PI.md` (new, Seed root): one line that imports `DataWizard Project Instructions.md` from its own folder. It works in the nested and the flat Seed layout. Point your Claude Code import at `PI.md`, so you escape spaces only in your own path to the Seed. It has no frontmatter on purpose: it loads on every Claude Code start.
- `Guides/Seed Install and Update.md`: new section "Claude Code and Obsidian sidebar plugins" - where the personal pointer goes (a CLAUDE file you own and git does not track), the import rules (a path is read from the file that holds it; escape every space; no quotes; no import in a code block; at most 4 hops), example pointer lines, the external-import dialog (**"No, disable external imports" is selected by default - press the down arrow and select Yes; a decline is silent**), a self-check question, and notes for Cowork, AGENTS.md repos, two home-folder lines, sidebar plugins and worktrees. "Fresh Install" links to it. An example path is now generic.
- `Protocols/Conventions Registry/33.0` (D96): the personal PI pointer goes in the vault-root `CLAUDE.md` (when the vault is not itself the shared repo) or a gitignored repo-root `CLAUDE.local.md`, never in a shared repo's tracked `CLAUDE.md`; a tracked `CLAUDE.md` may name the repo-relative home folder.
- `Skills/project-guidelines` v1.6.0: for a project in a shared git repo, the skill makes a tracked `CLAUDE.md` with no machine paths (home folder for this repo, a "say so if no Project Instructions are loaded" line, a pointer to the team setup note) and adds `CLAUDE.local.md` to `.gitignore`. `SKILLS.md` row updated.
- `README.md`: a note on the two Seed layouts (nested and flat) and a `PI.md` row.

**Action for Claude Code users:** run `update_seed`, then move your PI import out of any shared tracked `CLAUDE.md` into your own file, pointed at `PI.md`. Then ask the self-check question from the guide. The Project Instructions do not change (still 4.9); the PI wording follows at the next PI release.

## Older releases

The What's New entries for 1.11.4 to 1.11.15 are in `VERSION History.md`, 1.10.0 to 1.11.3 are in `VERSION History - 1.10.0 to 1.11.3.md`, and 1.0.0 to 1.9.5 are in `VERSION History - 1.0.0 to 1.9.5.md` (moved there word for word, 2026-10 and 2026-11). Expired notices (the 2026-06-10 git history rewrite) are in `VERSION History.md`, section "Retired notices".

## Versioning

Seed uses major.minor.patch:
- **Major** (1.x to 2.0): Breaking changes. Project Instructions
  must be re-pasted, folder structure changed, or protocol rewritten.
- **Minor** (1.0 to 1.1): Meaningful additions. New skills, agents,
  taxonomy changes, significant protocol updates. Worth knowing about.
- **Patch** (1.0.0 to 1.0.1): Bug fixes, typos, small refinements.
  Not worth interrupting you for.

How instances handle version mismatches:
- Major mismatch: always prompt, recommend updating before continuing
- Minor mismatch: prompt with What's New summary, user decides
- Patch mismatch: don't prompt, just continue
- Project Instructions mismatch: always prompt (separate from Seed)

## If your Seed version doesn't match

Seed version mismatches are not checked during orientation.
The Seed is updated separately via update_seed.sh or git
sync. If a user suspects their Seed is out of date, tell
them to run:
  bash _DataWizard/Seed/update_seed.sh

If this is a fresh install and update_seed.sh doesn't exist
yet, give them the install command:
  cd ~/path/to/vault && \
  curl -sL https://github.com/andrewalan11/DataWizard/archive/refs/heads/main.zip -o /tmp/dw-seed.zip && \
  unzip -qo /tmp/dw-seed.zip -d /tmp/dw-seed && \
  mkdir -p _DataWizard/Seed && \
  cp -R /tmp/dw-seed/DataWizard-main/. _DataWizard/Seed/ && \
  rm -rf /tmp/dw-seed /tmp/dw-seed.zip && \
  echo "DataWizard Seed installed to _DataWizard/Seed/"

## If your Project Instructions version doesn't match

Compare two values:
- **Local PI version**: the project_instructions field in your
  local _DataWizard/Seed/VERSION.md (this file)
- **Running PI version**: the version in the header of your
  pasted Project Instructions (e.g., "v4.0" or "v4.0-local";
  ignore the "-local" suffix)

Compare the numbers part by part, not as decimals: 4.10 is
newer than 4.9.

Handle each case:

**Local > running (Seed has a newer PI):** Tell the user:
  "Your Project Instructions are v[running] but your Seed has
  v[local]. Copy the updated PI from
  _DataWizard/Seed/DataWizard Project Instructions.md
  into Settings - Project Instructions."
Remind them to keep their Home folder line.

**Running > local (user is ahead of Seed):** The user has
pasted a newer PI version that hasn't been pushed to the
Seed yet. This is normal. Continue with current instructions.

**Running matches but local VERSION.md is stale:** If the
local VERSION.md project_instructions field doesn't match
the running PI version but the running PI is clearly newer,
update VERSION.md silently using patch_note to keep it in
sync. This prevents future instances from seeing a false
mismatch.

**All match:** No action needed.
