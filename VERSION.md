
seed: 1.13.0
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

## What's New in 1.11.15

**Patch release: tool behaviors from partner projects (MetaMyth, Mesocosm, Community Stack, Future Visions, Events Map, VibeCut, Kosmosis, Rootland, LocationScout), about the device mount, cloud sessions, links, web tools and git, plus fixes for stale or contradicting rules found by a Seed error check.** Four DataWizard sessions (2026-10-28 to 2026-10-31). Shipped in the Seed:

- `Guides/Published Artifacts and ArtifactData Behaviors.md`: `Artifact list` with `scope: "assets"` on another owner's artifact can return `not_found`, so `from_url` cannot copy its assets; publish a checked copy as a supporting file.
- `Guides/Chrome MCP and Web Tool Behaviors/12.0`: the Drive connector reads a Google Sheet as a sample of the first tab; ask for a CSV or xlsx export.
- `Guides/Cowork Build Environment/10.0`: a font safety check with the OpenType sanitizer and fontTools (`brotli` for WOFF2; the licence is often not in the file).
- `Guides/Cowork Build Environment/8.0`: a full vault scan through the mount took about 10 times longer than in the cloud container (different vault sizes) - print the scan time, run heavy steps on the Mac.
- `Guides/Git Guide/5.0 Daily Workflow.md`: the Obsidian Git plugin committed while "paused" - check the intervals and `git log` before a vault-wide script.
- `Guides/Script Portability.md`: new section - the macOS temp folder is a symlink (`/var/folders` to `/private/var/folders`); `realpath` the temp path in tests.
- `Guides/MCP Reliability and Write Verification/11.0`: a strict "unchanged since plan" check trips on any other writer; run `plan ... && apply ...` as one command line.
- `Guides/Cowork Build Environment/11.0`: `gh api` is blocked (403) for sub-agents in a cloud session and WebFetch cannot read commit pages; `add_repo` or `gh` on the Mac. 5.0 points to it.
- `Guides/Working Principles.md`: "Verify the drift" - a gap found by name needs a grep for the other names (aliases) first.
- `Guides/Telegram Harvesting.md`: run the first login without a pipe; a pipe hides the phone prompt.
- `Guides/Chrome MCP and Web Tool Behaviors/4.0`: the stale-GitHub-page bullet - check the project's changelog or release page, not a news page date.
- `Guides/Cowork Build Environment/8.0`: folder grants for a `~/Downloads` subfolder and a vault subfolder mounted in the same turn; sub-agents read a leaf-name mount and in-place writes work there.
- `Guides/Cowork Build Environment/8.1`: the `tar --overwrite` bullet gains the safe fix - `mv` the old folder aside and extract fresh, which keeps the old version.
- `Guides/MCP Reliability and Write Verification/12.0`: the short-name embed bullet is rewritten - Obsidian resolves a bare link by exact path, then same folder, then shortest path, so a new same-named note can take over a link; use path links for generic or numbered names. Its example path is now generic.
- `Skills/session-closer` v4.11.3: Step 3.5 - when a planted tool behavior came from another project's note or board ask, close both in the same pass.
- `Protocols/Editorial Principles.md`: the chunking step no longer says embeds resolve "by filename regardless of folder path"; it gives the exact path, same folder, shortest path order and asks for section names that are unique in the vault.
- `Protocols/YAML Schema.md`: the "Wikilinks everywhere" callout gives the same order (exact path, same folder, shortest path) and links MCP Reliability 12.0.
- `Protocols/Conventions Registry/7.0 Shell and section architecture`: section names are unique in the vault; a generic numbered name gets a distinguishing word (`2.0 UX - Map`, not `2.0 Map`).
- `Guides/Federation Guide.md`: the example paths are generic (`_Example Project/`, `~/path/to/vault`).
- `Skills/harvest-router`: the example project name is generic ("Media Project").
- `Guides/Cowork Build Environment/8.0`: a connected folder on an external drive (`/Volumes/...`) never mounts in the device shell; the device file tools still reach it by its Mac path.
- `Guides/Cowork Build Environment/5.0`: on some repos `git clone` through the proxy fails with `expected flush after ref listing`; `git -c protocol.version=0 clone` works. The OSM API node history and Nominatim answer from the device shell.
- `Guides/Cowork Build Environment/1.0`: read-only recon reads git state as files (`.git/HEAD`, `refs/heads`, `packed-refs`), and a linked worktree's rebase state through the primary checkout (`.git/worktrees/<name>/`).
- `Guides/Git Guide/6.0 Branch Workflow and Pull Requests.md`: a rebase that stopped partway can pass a clean-tree guard; operator blocks also check the branch and stop on `rebase-merge` or `rebase-apply`. The linked-worktree bullet notes that its state files can still be read (Cowork Build Environment 1.0).
- `Guides/Cowork Build Environment/6.0`: a backup of a database on the vault mount, taken through the device shell, failed with `disk I/O error` and left a partial `.bak` and a `-journal`; run such applies on the Mac.
- `Guides/Cowork Build Environment/8.1`: a tarball for a cloud copy excludes `*.session*` and `Scripts/output` (a plain `tar` packs git-ignored secrets); a reviewed patch is applied through a `/tmp` copy, in-place writes and a hash list.
- `Guides/Chrome MCP and Web Tool Behaviors/4.0`: Pinterest boards read from the operator's own scroll (no scripting around the robots block); Reddit `/api/morechildren` answers 403 in a logged-in console session; Google Maps short links resolve with `curl -sI` in the device shell, one link at a time; a WebFetch "quote" can be a paraphrase; what German and Austrian property portals let the web tools read.
- `Guides/Chrome MCP and Web Tool Behaviors/2.0`: rung 13 - an in-page `fetch()` loop is not a way past a robots block: the operator opens and scrolls the blocked search page, the agent reads only what it shows or the operator clips it, and the ad ids go to web-only helpers for the allowed detail reads; on a bot check or 401, stop and hand the step to the operator.
- `Guides/Chrome MCP and Web Tool Behaviors/2.0`: rung 12 reworded - a robots-blocked site is not a job for an automated Chrome pass; the lead hands it to the operator, who opens the page (the agent reads only what it shows) or clips it. `4.0`: the Pinterest and portal bullets say the same - no scripting around a robots block or a SITE_BLOCKED answer.
- `Guides/Chrome MCP and Web Tool Behaviors/5.0`: search snippets can carry a Q&A answer that WebFetch cannot read; when helpers come back thin, the lead runs one narrow search per clue before widening.
- `Guides/Published Artifacts and ArtifactData Behaviors.md`: a self-publishing page carries other pages as base64 blocks inside itself; embedded prototypes run in a `sandbox="allow-scripts"` srcdoc iframe (Escape does not reach the parent page, so add a Close button).
- `Guides/Working Principles.md`: "Hallucination vigilance" - a web tool's quote can be a paraphrase; label it and spot-check a sample.
- `VERSION History.md` was split by version range; entries 1.0.0 to 1.9.5 now in `VERSION History - 1.0.0 to 1.9.5.md`.

**Doc fixes from a Seed error check (scout test of 1.11.12, checked against 1.11.14):**

- `Guides/Git Guide/10.0 Commit Guards.md`: "Three guards", not two; says where each guard runs (conflict markers in the hook and CI, filenames in the hook only for now, secret files in the hook with DW Save at push time); no longer claims a shipped `check-filenames.yml`; a session id in the text is replaced by a date.
- `Protocols/Conventions Registry/10.0 Archiving`: the example now follows the mirror pattern (`xArchive - ProjectName/Strategy/Old Strategy.md`).
- `Protocols/Conventions Registry/2.0 Infrastructure file slots`: the core rule says when each slot appears (0.0-0.3 at setup, 0.4 at the first harvest, 0.5 at the first open item); the example says "start with", not "ship only".
- `Protocols/Conventions Registry/1.0 Link, don't restate`: the Review Automation guide owns cadence numbers, not the session-closer; the slot table pointer reads "(entry 2.0)".
- `Protocols/Conventions Registry/26.0 Coordination board`: the Rule and the Example now post the ask when the outbound item is written, with the close-time check as the safety net; a gate row naming another project's actor is no longer listed as an outbound item.
- `Protocols/YAML Schema.md`: its own edit_log is in date order again; the birth table says edit_log is not on shells, and the edit_log section says a new file gets it at birth; `team_attention*` fields are migrated in one sweep, not on next touch; "Harvest Log" and "harvest-log queries".
- `Guides/Filename Safety.md`: inside double quotes, `!` followed by anything but a space starts history expansion (was "a letter or digit").
- `Guides/Orientation Flag Sweep - Query Spec.md`: the null-literal note is corrected - `NULL` sorts last; the harm is that the item counts as dated.
- `Skills/session-closer`: Step 4 gate rows name an operator or a person only (work that waits on another project's session is a board ask); Step 3.14 links the board id rule instead of restating it and drops gate rows from the outbound kinds; Step 2.5 lists `origin`; "Harvest Log" in Step 4 and the related-files list. `references/output-format.md`: the sweep trace line links the Query Spec instead of carrying an old copy; both session-log templates gain `origin` and `edit_log`.
- `Skills/project-guidelines`: the 0.0 template drops the retired `datawizard_protocol_version` pin and gains `operator`, `origin`, `edit_log` and `seed_version`.
- `Guides/Harvest Workflow Guide.md`, `Skills/document-harvest`, `Skills/transcript-harvest`: the 0.4 file is the "Harvest Log" everywhere, matching the slot table ("the ledger" becomes "the log").
- `Skills/project-health-audit`: Action Items (0.5) is required once the first item is filed, matching the slot rule.
- Skill versions: project-health-audit v2.1.2, session-closer v4.11.4, project-guidelines v1.5.2, document-harvest v0.5.2, transcript-harvest v0.9.3; `SKILLS.md` rows synced; session-closer `references/changelog.md` takes the oldest edit_log line (rolling window).

**Adopters:** the 0.4 slot file is named "Harvest Log". A project whose file is named "Harvest Ledger" renames it when next touched.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.14

**Patch release: eight lessons from a review of outside agent tools and write-ups, about stale writes, index reads, long jobs, claims and failing visibly.** One DataWizard session (2026-10-27). Shipped in the Seed:

- `Guides/Agent Tool Contract Checklist.md`: a new group, "Reads, writes and long jobs", with items 12 to 14 - an index read says how fresh and how complete it is (a query that finds nothing says what the index does not cover); a write names the revision it read and refuses a stale write; a long job returns a job ID and a status tool.
- `Guides/Working Principles.md`: "A completion is a disk fact, not a claim" gains its failure-side twin - fail closed and fail visibly, and a check that could not run is UNKNOWN, never a pass. "Verify the drift before scheduling its fix" now covers memory, notes and search hits as claims - keep the source, label how strong it is, say what was not checked.
- `Protocols/YAML Schema.md`: the "Wikilinks everywhere" callout says to quote the link, because an unquoted `[[Note Name]]` parses as a nested list.
- `Guides/Cowork Build Environment/10.0 Scanning Third-Party Code.md`: AI scan reports are candidate findings that a person triages before a fix or a disclosure.
- `Guides/MCP Reliability and Write Verification/11.0`: at apply time, re-check that the input still matches what the dry run previewed, and refuse on a mismatch.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.13

**Patch release: 34 tool behaviors from seven partner projects (Rootland, Common Woods, Mesocosm, Kosmosis, VibeCut, ReWoven, MetaMyth) and DataWizard sessions, mostly about folder access, cloud sessions, git in cloud clones and published artifacts.** One DataWizard session (2026-10-27). Shipped in the Seed:

- `Guides/Cowork Build Environment/11.0 Claude Code Cloud Sessions.md`: a cloud clone can be shallow (depth 1) and old commit ids then fail (fix: unshallow or a bounded fetch; pin by sha256 in tests); a branch fetched into a depth-1 clone needs explicit refspecs; `gh` can be installed but not logged in (test with `gh auth status`; make a draft pull request optional); a repo agent type (`.claude/agents/`, `tools: Read`) cuts a sub-agent's start-up text 2 to 5 times and enforces the tool list; `add_repo` for a whole private repository can be refused.
- `Guides/Cowork Build Environment/`: 8.0 (a folder request can be refused with no prompt - ask in chat first and use the `filesystem` MCP meanwhile; a folder added with "Add folder" can take a long time to reach a running session; the folders under `$HOME/mnt/` may not be the vault; ask for the vault root once for a vault-wide grep; a per-URL grep loop timed out at 180 s, one keys-file pass worked); 8.1 (macOS `tar` sidecars also break a test runner's glob; `move_note` with `overwrite: true`); 8.2 (a container restart stops background sub-agents and jobs - resume the builder by message; keep a checker's batch at 10 or fewer); 6.0 (`immutable=1` also works on rollback-journal databases, with a torn-read caveat); 3.0 (the container's default `python3` was 3.13 - call `python3.12` by name; an openpyxl save drops charts); 1.0 (git on an online-only Dropbox or iCloud clone: "Resource deadlock avoided").
- `Guides/Chrome MCP and Web Tool Behaviors/`: 7.0 (Google Doc tabs and formatted paste through Chrome; the Drive connector cannot edit); 4.0 (LinkedIn short links via Chrome); 6.0 (a second same-day browser download is saved as `name (1).json` - take the newest file); 12.0 (Fathom summary and transcript calls worked); 1.0 and 10.0 (a resize applied only after a later navigation; screenshots saved in the container can be read by sub-agents).
- `Guides/Published Artifacts and ArtifactData Behaviors.md`: .xlsx, .docx, .pptx and .zip are not served as supporting files (base64 text plus the `downloads` capability; a live click was still untested); the "declares connector but no successful call observed" warning is per session; a sub-agent can build a page but the lead publishes it.
- `Guides/MCP Reliability and Write Verification/8.0` and `Protocols/YAML Schema.md`: parse the frontmatter block back after any frontmatter write; free-text fields are the usual source of an unquoted colon; a new `edit_log` line goes after the last line of the last entry (a line inside a wrapped entry breaks the parse or joins two entries). `Protocols/Conventions Registry/7.0` and the YAML Schema `section` row: quote a dotted section number (`'2.10'`).
- `Guides/Orientation Flag Sweep - Query Spec.md`: a Board block ends at the first blank line, not the next `### ` heading.
- `Guides/Script Portability.md`: an unmatched glob in zsh leaves a command-substitution result empty; scripts refuse an empty file name.
- `Skills/supervised-build/SKILL.md` (v1.6.2): Reviewer Steps - when a private source feeds a build, the builder gets only the team-safe extract and the reviewer greps the seeds for names and remarks from the private source. `SKILLS.md` row synced.
- `GUIDES.md`: three rows name the new topics.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.12

**Patch release: four tool behaviors from two partner projects (Future Visions, Rootland), all about reading outside sources.** One DataWizard session (2026-10-26). Shipped in the Seed:

- `Guides/Chrome MCP and Web Tool Behaviors/4.0 web_fetch Behaviors.md`: WebFetch can serve an old snapshot of a GitHub repo page (old star and commit counts) - read raw files and the API instead; `api.github.com/repos/...` can be blocked or stale for a sub-agent while the commits, releases and search routes answer; Kickstarter project pages are unreadable by the web tools (header data only, HTTP 403 from curl).
- `Guides/Cowork Build Environment/5.0 Network and GitHub Data.md`: the repo landing page is no longer named a reliable source for counts without a cross-check (pointer to the bullet above).
- `Guides/Cowork Build Environment/8.2 Device Bridge - Sub-agents and Orchestration.md`: a research sub-agent's `curl` to a site's public API was refused by the permission check before it ran - plan a browser check or a call by the lead.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.11

**Patch release: 24 tool behaviors from partner projects (Rootland, VibeCut, Tech Tools, ReWoven, Holonic Canvas) and DataWizard sessions, with a new section on Claude Code cloud sessions.** One DataWizard session (2026-10-26). Shipped in the Seed:

- `Guides/Cowork Build Environment/11.0 Claude Code Cloud Sessions.md` (new section, embedded in the shell `Guides/Cowork Build Environment.md`): a promotional cloud-session credit did not cover Cowork tasks; a private repository is reachable only when the Claude GitHub App is installed on it (authorized is not enough); a session cannot create a repository; the "Limited" network takes one domain per line, and the safety scanners need four hosts beyond the defaults; GuardDog installed only through pipx; an unattached public repository can be cloned.
- `Guides/Cowork Build Environment/`: 10.0 (the scanners and `sqlite3` are not in the device shell - run them from the Mac Terminal; a scanner's risk label says where to read, not what is wrong; OSV-Scanner 2.7.0 can stop on one lockfile and counts every lockfile in a monorepo; GuardDog 3.2.0 runs the same 54 rules for every ecosystem subcommand and needs its Landlock sandbox; licensee 10.1.0 exits 1 with valid JSON when it finds no license; pointer to 11.0 for the cloud hosts); 1.0 (the device shell cannot run git inside a linked worktree - the operator writes `git diff`, `git log` and `git status` output into a review bundle on the Mac; read-only `git status` and `git diff` can leave `.git/index.lock`, so on the Mac use `GIT_OPTIONAL_LOCKS=0`; git-ignore `.fuse_hidden*`; git-ignore a backup of private data before it is written); 3.0 (Python run on the device shell writes `__pycache__` into the vault - use `python3 -B` or `ast.parse`); 4.0 (Claude Code reports "Not logged in" without `USER` and `LOGNAME`; the flags a look-only headless run needs); 5.0 (where `api.github.com` was blocked, the npm, PyPI and crates.io registries still worked); 8.0 (a tool's data folder under `~/Library/Application Support/` is protected - the operator copies the run folder into a connected folder; `device_bash` can answer "downloading the isolated Linux environment" and recover within minutes).
- `Guides/Git Guide/`: 6.0 (a linked worktree is read through the operator's review bundle); 2.0 (`.fuse_hidden*` in the `.gitignore` template); 9.0 (stale index.lock: read-only git through the device bridge can leave it; pointer to `GIT_OPTIONAL_LOCKS=0`).
- `Protocols/Conventions Registry/10.0 Archiving.md`: backups of private data are git-ignored before they are written (an auto-sync plugin pushes anything else within about half an hour).
- `Guides/Published Artifacts and ArtifactData Behaviors.md`: an `Artifact` read of an artifact the session did not publish saves the full HTML to a local file that sub-agents can read.
- `Guides/Chrome MCP and Web Tool Behaviors/`: 10.0 (the extension refuses `old.reddit.com` too); 4.0 (Reddit share links, `old.reddit.com` and `.json` URLs are blocked as well; ask the operator to read an image-only post).
- `Guides/MCP Reliability and Write Verification/12.0 Obsidian Behavioral Gotchas.md`: `search_notes` returns at most 20 results - an exhaustive link check is a `grep`.
- `Guides/Script Portability.md`: new short section - a tool started by launchd can run on `/usr/bin/python3` (3.9).
- `GUIDES.md`: the Cowork Build Environment row names Claude Code cloud sessions and where the scanners run.
- `SKILLS.md`: Workshop table gains the cloud-triage row (new DataWizard Workshop skill: batch research and safety checks in Claude Code cloud sessions, decided on a click page) and the missing intake-handoff row.
- `VERSION History.md`: the What's New entries for 1.10.0 to 1.10.4 moved there word for word (size rotation, so this file stays under about 50 KB). Nothing was cut.

**Propagation:** `update_seed.sh` (it copies the new section file). No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.10

**Patch release: one written method for splitting big files, for every project.** One DataWizard session (2026-10-21), answering a partner project (Community Stack) and an older request for a migration guide (ReWoven). Shipped in the Seed:

- `Protocols/Conventions Registry/7.0 Shell and section architecture.md`: the method is now the standard and the layout an option. Besides its embeds a shell may carry its H1, an intro line, an entry template, grow lines and script-owned marked blocks. A group grows by continuation files with the next free number (never move items, never renumber), and a one-line grow comment in the shell says where new sections go (default: after the group's last embed). Sizes: 50 KB hard, 30 KB soft, about 25 KB per piece when splitting. New "How to split safely" steps: plan, slice by script, prove the byte rejoin with sha256, keep a pre-split copy in the archive mirror, write the sections first and the shell last; the flat-log migration rule; a SKILL.md sections by `references/`, never by embeds.
- `Skills/session-closer/SKILL.md` (v4.11.2): Step 2 - a Decision Log entry that waits for approval has its proposed text written into the session entry or a working doc before close. Step 3.11 - the file-size check uses the 30 / 50 KB sizes and points at Registry 7.0. `references/changelog.md` takes the oldest edit_log line (rolling window).
- `Skills/meta-learning-review/SKILL.md` (v1.5.6) and `Skills/meta-learning-scan/SKILL.md` (v1.4.3): a "tracked in X" claim must resolve to a quoted line on disk; one that does not means the item is not homed (pointer to session-closer Step 3.5).
- `Guides/Cowork Build Environment/8.0 Device Bridge.md` and `Guides/Multi-Instance Coordination Patterns.md` (Pattern 2): pointers to Registry 7.0 for the splitting procedure.
- `SKILLS.md`: the three rows carry the new versions.

A script that finds oversize files and splits them by these steps is planned; this release is the written method it will follow.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## Older releases

The What's New entries for 1.10.0 to 1.11.9 are in `VERSION History.md`, and 1.0.0 to 1.9.5 are in `VERSION History - 1.0.0 to 1.9.5.md` (moved there word for word, 2026-10). Expired notices (the 2026-06-10 git history rewrite) are in `VERSION History.md`, section "Retired notices".

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
