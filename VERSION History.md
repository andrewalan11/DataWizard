---
title: VERSION History
type: guide
created: 2026-10-18
updated: 2026-10-31
operator: Andrew
origin: DW-S421 2026-10-18 - What's New entries 1.0.0 to 1.5.0 moved from VERSION.md word for word (size rotation, archivist rule)
edit_log:
  - 'DW-S448 2026-10-31 - 1.11.15 released: entry moved word for word to VERSION.md; What''s New 1.11.3 to 1.11.0 moved in from VERSION.md word for word (size rotation at 1.11.15)'
  - 'DW-S448 2026-10-31 - draft 1.11.15: tool-behavior and doc-fix plants from VibeCut, Kosmosis, Rootland, LocationScout and DataWizard (B-0272, B-0275, B-0278, B-0279, B-0281); split bullet'
  - 'DW-S448 2026-10-31 - What''s New 1.9.5 to 1.0.0 moved word for word to VERSION History - 1.0.0 to 1.9.5.md (size rotation before 1.11.15)'
  - 'DW-S446 2026-10-31 - Seed error-check fixes: draft 1.11.15 doc-fix bullets'
  - 'DW-S443 2026-10-28 - draft entry 1.11.15 (in progress) added: tool-behavior plants from five partner projects'
  - Seed 1.11.11 2026-10-26 - What's New 1.10.0 to 1.10.4 moved in from VERSION.md word for word (size rotation before 1.11.11)
  - DW-S428 2026-10-20 - What's New 1.9.1 to 1.9.5 moved in from VERSION.md word for word (size rotation before 1.11.7)
  - DW-S427 2026-10-19 - What's New 1.9.0 moved in from VERSION.md word for word (size rotation before 1.11.5)
  - DW-S426 2026-10-19 - What's New 1.8.0 moved in from VERSION.md word for word (size rotation before 1.11.4)
  - DW-S424 2026-10-19 - What's New 1.7.0 moved in from VERSION.md word for word (size rotation before 1.11.3)
  - DW-S422 2026-10-18 - What's New 1.6.0 to 1.6.2 moved in from VERSION.md word for word (size rotation before 1.11.0)
  - DW-S421 2026-10-18 - created
---

# VERSION History

Older "What's New" entries of the Seed, moved here from `VERSION.md` word for word. The current version and the newer entries are in `VERSION.md`. When `VERSION.md` passes about 50 KB again, move its oldest entries to the top of the list below, newest first, and leave the pointer in `VERSION.md`. Entries 1.0.0 to 1.9.5 are in `VERSION History - 1.0.0 to 1.9.5.md`; when this file passes about 50 KB, start the next part the same way.

## What's New in 1.11.3

**Patch release: rows that a script can close.** One DataWizard session (2026-10-19). A tracking row that waits on something written only in words keeps saying "pending" after the thing it waited on has closed somewhere else. About a third of the leaked items in two look-backs were rows of this kind. This release gives such rows an id a script can read. The scripts that read it (a board render flag and a lint check) come in a later release. Shipped in the Seed:

- `Protocols/Conventions Registry/23.0 Tracking Model.md`: new sub-rule **Dependencies name their id** - a line or gate row that waits on another tracked item writes `after: G-NNN` / `B-NNNN` / `Tnn` (comma-separated for several); where it goes; when a target counts as done; a dependency on something with no id stays in words (the check's named blind spot).
- `25.0 Operator Gate Queue.md`: two row fields - `ask` (required in the waiting-on-people class: the board ask id, or `-` when a person, not a project, is the actor) and `after`. Admission: work that waits on another project's session is a board ask, not a gate row; existing rows of that kind move to the board when next touched.
- `26.0 Coordination board.md`: a gate row that waits on an ask carries `- ask: B-NNNN`; the ask may end its summary with `[G-NNN]`.
- `30.0 Carry the probe, not the snapshot.md`: extended to tracking lines - no file size, count or version that will change; write the probe.
- `Templates/Operator Gate Queue - Template.md`: `- ask: -` on the example row; a note under the waiting-on-people class.
- `VERSION History.md`: the What's New entry for 1.7.0 moved there word for word (size rotation).
- Tool behaviors: `Guides/Cowork Scheduled Tasks.md` - a task created without `folders` gets none (pass them explicitly); test a new task with a one-time copy of its exact prompt. `Guides/MCP Reliability and Write Verification/12.0 Obsidian Behavioral Gotchas.md` - filesystem `edit_file` applies a multi-edit call all or nothing.

**Adopters:** nothing breaks - scripts ignore unknown row keys. Add `- ask:` to the rows of your waiting-on-people class when you next touch them, and move rows that wait on another project to the board.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.2

**Patch release: the cause and the fix for a device shell that fails in every session.** One DataWizard session (2026-10-18 to 2026-10-19). From 2026-10-16 `device_bash` failed in every new Cowork session on one computer, in every project, for three days. The cause was not a wedged session: the desktop app keeps one Linux user and home folder per session on a fixed 10 GB session disk inside its VM and does not remove them, and that disk ran out of file entries (inodes). Shipped in the Seed:

- `Guides/Cowork Build Environment/8.0 Device Bridge.md`: the wedged-shell bullet is rewritten around the cause - the signs (only "device_bash failed in the device workspace", no `scratchFolder`, every new session in every project, a restart does not help), the confirm step (`df -i /sessions` in an older session whose shell still works), and the operator fix as observed once (quit Claude with Cmd-Q, check with `lsof`, move `sessiondata.img` aside to a backup, start Claude - the app made a new, empty disk; if it does not, move the backup back and report). The bullet is split in two: the cause and fix, and how to work without the shell until the swap.

**Adopters:** if your device shell fails in every new session, follow the 8.0 bullet. Once in a while, run `df -i /sessions` in a working device shell; when it nears 100%, plan the swap before the shell stops.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.1

**Patch release: a session look-back report has a home.** One DataWizard session (2026-10-19). A look-back scan reads the session logs closed since the last look-back and reports open items that slipped (on no tracking list) or sit on an out-of-date tracking line. It is the safety net behind the 1.11.0 landing rule. Shipped in the Seed:

- `Skills/session-closer` v4.11.1: Step 3.10 also surfaces a pending `Look-Back Report - *` at a full close, the same way as the other review reports. The v4.10.1 edit_log line moved into `references/changelog.md` (rolling window).
- `Guides/Review Automation.md`: the "Backlog + FR triage" row names the session look-back scan as its between-triage producer, with `Look-Back Report - *.md` as its pending report. The full triage stays manual at its own cadence; a look-back review stamps `last_backlog_triage` only when it also covered the full triage. Producer maturity: the look-back producer runs in one project's workshop and is not yet shipped in the Seed.
- `SKILLS.md`: session-closer row synced; Workshop table gains a session-lookback row.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. A project without a look-back scan sees no change. (DataWizard, 2026-10)

## What's New in 1.11.0

**Minor release: open items must land on a list.** One DataWizard session (2026-10-18). Two look-backs over 53 session logs found that about one open item in three was not where the next reader would look: it had faded out of "What's next", or it lived only inside a handoff or design doc, or a done parent line hid it. This release closes those gaps at moments that already exist (the close, the chunk done-mark, the moment a document is written). Shipped in the Seed:

- `Skills/session-closer` v4.11.0: Step 4's optional "Action items" bullet is now the required **landing rule**. The closer re-reads the previous "What's next"; each item ends done (struck, with where it landed), carried (it is in the new "What's next"), or landed on a tracking list (a Backlog line, gate row, board ask or ledger row), and the entry quotes that line - its file and its title, id or first few words. "Queued in X" without the quoted line is not allowed. Rulings and small tasks for the operator go to one dated `Waiting on <operator>` checklist, never to a paragraph in "What's next". The rule applies at every close tier (Step 0's lite list names it). Step 2.6: the ledger `next:` is written as the arc's owed list, current state only. Step 3.5: new **tracking-claim verification** - every "tracked in / queued in / see `<list>`" claim must resolve to a line on disk, checked like a planted learning. New Common Mistakes bullet. `references/output-format.md`: the What's next template starts with a **Landing check** line and a **Waiting on `<operator>`** pointer line. `references/changelog.md`: the v4.10.0 edit_log line moved in from the frontmatter (rolling window).
- `Protocols/Conventions Registry/23.0 Tracking Model.md`: four sub-rules - **follow-ups are born on a list** (a handoff, exchange note, pre-flight answer, build-plan limits list or design doc that names a follow-up writes its Backlog line or board ask at the same moment and keeps only a pointer); **parents do not close over open children**; **no new Unlocks in design docs** (the State Board plus a Backlog line do that job; existing lists stay as history); **rulings and small tasks for the operator** live on one dated Waiting-on checklist. One new fact-class row for that checklist.
- `Protocols/Conventions Registry/24.0 Active Threads ledger row schema.md`: `next:` is the owed list (one short line per item the arc still owes), not a narrative; the example is in list form.
- `Skills/supervised-build` v1.6.0: at each chunk's done-mark (Builder Step 5), every leftover - a deferred item, a known limit, a follow-up the chunk names - becomes its own tracking line before the chunk is marked done, and the chunk report quotes the lines; the reviewer checks they exist (Reviewer Step 2); in the in-thread variant the done-mark is the lead's.
- `Guides/Cowork Build Environment/8.1 Device Bridge - Staging, Commits and Transport.md`: an outputs file edited after the copy can commit as its pre-edit (or part-edited) copy on the FIRST commit, not only on path re-use (4 of 13 files in one run); write the final version to a fresh outputs path, commit, then compare the on-disk size or checksum with the local copy.
- `Templates/Operator Gate Queue - Template.md`: class F holds only built or decided items; rulings and small operator tasks go on the Waiting-on checklist (the Tracking Model gives the test).
- `SKILLS.md`: session-closer and supervised-build rows synced.

**Adopters:** the landing rule needs a home for the `Waiting on <operator>` checklist in each project. Pick one - typically a section of your action items or backlog - and move any "rulings waiting" paragraphs from your last "What's next" into it (one dated line per item, with its source session). If a project has none yet, the closer asks the operator where it goes at the first close that needs it (with no answer at hand, it opens one as a section at the end of the action items file and says so). An orientation sub-check that shows the checklist's count and oldest item waits for a later Project Instructions bump. Closes take one to three minutes longer; lite closes run the landing rule too.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.10.4

**Patch release: the Conventions Registry and the session-closer skill are sectioned. No rule changed.** One DataWizard session (2026-10-18). Both files were past the ~50 KB line where vault tools turn unreliable. Text moved byte for byte; a reassembly check matched the originals exactly. Shipped in the Seed:

- `Protocols/Conventions Registry.md` is now a short shell (frontmatter, intro, a navigation paragraph, 37 `![[embeds]]`) plus one section file per entry in `Protocols/Conventions Registry/` (`1.0 Link, don't restate.md` .. `37.0 Intake capture placement.md`). Two file names drop a character that is not filename-safe: `4.0 Operator personal - scratch folders.md` and `19.0 Provenance - by and via.md` (the H1 keeps the original). Cite an entry by name as before (Conventions Registry, "Entry name"). Through the Obsidian MCP an embed does not expand: open the section file. Edit the section file, never the shell. Block ids travel with their entries (`^b42` is in `30.0 Carry the probe, not the snapshot`, `^b43` in `36.0 Attention requests live in the flag cluster, not banners`).
- `Skills/session-closer` v4.10.4: SKILL.md keeps every step (0 to 5), the step numbers, `name` and `description`. Long, seldom-used blocks moved word for word into `Skills/session-closer/references/` (progressive disclosure, not embeds, because skill loaders do not expand embeds): `output-format.md` (entry templates; read at Step 2), `multi-operator-flags.md` (Step 3.12 team flag prompt, Step 3.13 flag expiry pass), `no-ledger-roster.md` (Step 2.6 roster for projects with no ledger), `action-items-triage.md` (periodic triage), `changelog.md` (older edit_log lines, kept). Each step that needs a reference file says so. SKILL.md drops from about 60 KB to about 42 KB. `SKILLS.md` row synced.
- `Protocols/Content Type Taxonomy.md` and `Config/taxonomy.yaml`: infrastructure types `protocol-section` and `skill-reference` registered.

**Adopters:** a `[[Conventions Registry#Heading]]` or `[[Conventions Registry#^blockid]]` link in your own notes no longer resolves (headings and block ids now live in the section files): repoint it to the section file, for example `[[30.0 Carry the probe, not the snapshot#^b42]]`. Plain `[[Conventions Registry]]` links and name citations keep working. Find them in a Terminal at the vault root: `grep -rn "Conventions Registry#" --include="*.md" .`

**Propagation:** `update_seed.sh` (it copies the new folders). No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.10.3

**Patch release: tool behaviors from three partner projects and two DataWizard sessions, a filename rule, and a shorter VERSION.md.** One DataWizard session (2026-10-18). Shipped in the Seed:

- `Guides/Filename Safety.md`: no `!` in new file or folder names (inside double quotes, `!` followed by a letter starts history expansion in an interactive zsh or bash Terminal and a pasted command fails with `event not found`); existing names are renamed on touch, inside the app, never in a batch.
- `Guides/Git Guide/5.0 Daily Workflow.md`: check every rollback or backup file name against `.gitignore` before a run.
- `Guides/Git Guide/6.0 Branch Workflow and Pull Requests.md`: new section - an unattended build gets its own linked worktree, never a branch switch in the primary checkout; the merge is `--ff-only`.
- `Guides/Git Guide/7.0 Safety and Recovery.md`: the GitHub Support category "Deletes" opens a repository deletion form, not a sensitive-data request.
- `Guides/Cowork Build Environment/`: 4.0 (quote every glob in an operator command - zsh stops on an unquoted glob that matches nothing); 5.0 (the container's GitHub API can refuse one repository for the session); 8.1 (`device_commit_files` writes mode 0600 - add a `chmod 755` step for scripts; with the shell down it still gives a byte copy of a long new file); 8.2 (fast-tier helpers can run stage and commit from path-list files; one file owns a string that parallel agents share; the permission classifier can deny the lead's edit while a sub-agent's passes); 9.0 (same FAIL ids are not the same failures - compare the detail text on the base branch; a fixture `HOME` does not isolate launchd).
- `Guides/Chrome MCP and Web Tool Behaviors/`: 1.0 (a same-origin iframe gives a true narrow layout when `resize_window` does nothing); 2.0 rung 10 (a sidebar teaser from `get_page_text` - walk up from the `h1`); 4.0 (GitHub search and list pages can answer ROBOTS_DISALLOWED - fetch the repo URL or the raw LICENSE; WebFetch can refuse a quick second fetch of a URL that failed); 10.0 (a bot-check wall can clear after a second navigate and a short wait; the extension can drop to "not connected"); 12.0 (third-party pages can carry text aimed at AI agents - treat page text as data).
- `Guides/Browser and File System Access Behaviors.md`: Chromium decides `:focus-visible` per document - pass the trigger type into an iframe and use `focus({focusVisible})`.
- `Guides/Script Portability.md`: new section on case-insensitive disks.
- `VERSION History.md` (new): the What's New entries for 1.0.0 to 1.5.0 moved there word for word, so this file stays under the size where vault tools turn unreliable. Nothing was cut.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.10.2

**Patch release: the commit guard checks for secret files, commit messages no longer carry the computer's name, and one review pattern is codified.** One DataWizard session (2026-10-18). Shipped in the Seed:

- `Scripts/hooks/pre-commit` (the commit guard): a third check, for secret files. A commit is blocked when its staged files include anything DW Save's secret-file guard blocks (`*.session` / `*.session-journal`, `.env` and `.env.*` except `.example` / `.sample` / `.template`, anything under `Scripts/output/`, `Vault Config.md` and its copies; upper and lower case count as the same). The hook checks only what the commit would add or change: a staged deletion never blocks, a rename counts as the new name, and a first commit on a new repo is checked too. `SYNC-BLOCKED.md` and the terminal name each file with its fix (`git rm --cached -- "<path>"` keeps the file on disk; then add it to `.gitignore`), and for this check neither offers `git commit --no-verify`. If git cannot list the staged files, the commit is blocked. The hook holds a byte-for-byte copy of DW Save's `is_secret_path`, and a test fails when the two differ. Also fixed: the conflict-marker and filename checks now also check renamed files (before, `git mv note.md 'note?.md'` got through).
- Not covered by the hook: `git commit --no-verify`; commits made where hooks do not run (Obsidian Git on mobile); a merge commit that git creates without a conflict (git runs `pre-merge-commit`, not `pre-commit`, for those); a secret that is already in the last commit and unchanged (for example under `git commit --amend`), because the hook reads the staged changes only. DW Save's guard still catches all of these at push time.
- `Scripts/datawizard-sync.sh` (DW Save): automatic commit messages no longer contain the computer's network name. They read `auto-sync <date> <time> on <label>`, where `<label>` comes from a new lower-case `machine: <label>` line in `~/.datawizard-sync.conf`: one word made of letters, digits, `.`, `_` or `-`. With no such line the label is `Mac`. With an invalid value (for example `machine: my mac`) the label is also `Mac`, and the log gets one warning per run. `--install` adds `machine: Mac` to a conf that lacks the line and keeps any value already there; because of the new line, the first re-install after this update rewrites the conf once (with a backup). `Scripts/datawizard-sync-setup.md` and `Guides/Git Guide/10.0 Commit Guards.md` describe both changes.
- `Guides/Multi-Instance Coordination Patterns.md`, Pattern 3 step 3: for a runbook an operator pastes into a terminal, the reviewer rehearses it on a copy, writes every number the operator will see into each step with a STOP condition, and checks the live run against those numbers. `Skills/supervised-build` v1.5.2 (Reviewer Steps): check scripts for the operator travel as vault files with a sha256 to compare, never as pastes. `SKILLS.md` synced.

**Propagation:** `update_seed.sh` for zip installs. Then re-run `datawizard-sync.sh --install` (or `install-git-hooks.sh` in each repo) to pick up the new hook. Repos that keep the hook in a tracked `.githooks/` folder (Weave) need that copy updated in the repo. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.10.1

**Patch release: DW Save refuses to publish secret files, and the Seed history is clean.** One DataWizard session (2026-10-17). Shipped in the Seed:

- `Scripts/datawizard-sync.sh` (DW Save): a secret-file guard. Before committing, and again right before pushing, each repo is checked for `*.session` / `*.session-journal`, `.env` and `.env.*` (except `.example`, `.sample`, `.template`), anything under `Scripts/output/`, and `Vault Config.md` (including copies such as `Vault Config.md.<suffix>`); upper and lower case count as the same. It checks the staged files and every local commit not yet pushed. A hit blocks that repo (other repos still save), names the file and the fix on the status card, and never unstages or deletes anything; if the check itself cannot run, the repo is blocked too. The pattern list is owned by one function, `is_secret_path`; since 1.10.2 the commit guard holds a verbatim copy, kept identical by a drift test. `Scripts/datawizard-sync-setup.md` describes it. Operators running a `~/Scripts` copy: re-run `datawizard-sync.sh --install` to point the hotkey and the scheduled job at the Seed copy.
- History rewrite (see the NOTICE above) and placeholder examples in `Scripts/tg_harvest_thread.py`, `Guides/Telegram Harvesting.md` and `Scripts/datawizard-aliases.sh`.
- `Guides/Git Guide/7.0 Safety and Recovery.md`: Step 4 names the 2026-10 rewrite signature, the file-diff gate for local work, the `reset --keep` then `stash pop` path, and what a pre-1.10.1 DW Save shows on an old clone (`could not reach GitHub`, nothing pushed).

Not yet covered: the commit guard (`Scripts/hooks/pre-commit`) has no secret check, so a manual `git commit` plus `git push` outside DW Save is not stopped. *(Covered since 1.10.2: the commit guard now has the same check.)*

**Propagation:** `update_seed.sh` for zip installs; git clones follow the NOTICE. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.10.0

**Minor release: tool evaluations get one canonical home.** One DataWizard session (2026-10-17). Shipped in the Seed:

- `Protocols/Conventions Registry.md`, new entry "Tech tool evaluations": a vault that keeps a tool-evaluation project evaluates each tech tool (a code repo, an app, a model or a service) once, in one shared note that every other project reads first. Up to three notes per tool, each answering a different question: the `_Entities/` core (identity and relations), the shared evaluation note, and each project's short "fit for us" view. The entry also says who may write the shared note, when a tool gets a core (an evaluated note plus at least one project in `fit:`; minted on touch, never in a batch), that existing evaluations adopt on touch, and that a non-repo tool note is named by the plain tool name. The "Holonic records" sync rules point at it.
- `Protocols/YAML Schema.md`: new section "Tool Evaluation Notes" - `repo_key`, `one_liner`, `license`, one platform field per operator platform (for example `mac`), `tool_maturity` (the tool's state; `maturity` stays the document field), `categories`, `reviewed_by`, `fit`, `verdict` (clone / later / skip / `cloned`; the operator's answer only), `safety`, `safety_checked`, `safety_by`. Holonic Records gains the anchor scheme `github-repo~<owner>/<repo>` (one repository, lower-cased; the login alone stays `github`).
- `Guides/Make Your Project Data Holonic.md`: the cores-on-touch paragraph points at the stricter test for tools.

**Adopters (only if your vault keeps a tool-evaluation project):** add two rows to your own `Vault Config.md` (it is git-ignored, so `update_seed.sh` never touches it): `tool_eval_dir` - the project's folder, for example `_Tech Tools/` (scripts that write tool notes read it and refuse to run without it); and the project's lens in `holon_lens_map`, for example `_Tech Tools/=TT`. A vault without such a project can ignore the entry.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

