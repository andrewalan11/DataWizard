---
title: VERSION History
type: guide
created: 2026-10-18
updated: 2026-10-31
operator: Andrew
origin: DW-S421 2026-10-18 - What's New entries 1.0.0 to 1.5.0 moved from VERSION.md word for word (size rotation, archivist rule)
edit_log:
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

## What's New in 1.11.15 (in progress, DW-S443, DW-S446)

*Draft, not released: VERSION.md still reads 1.11.14. At release, move this entry into VERSION.md above 1.11.14 and finish the summary line.*

**Patch release: tool behaviors from partner projects (MetaMyth, Mesocosm, Community Stack, Future Visions, Events Map), mostly about the device mount, cloud sessions and links, plus fixes for stale or contradicting rules found by a Seed error check.** Two DataWizard sessions (2026-10-28, 2026-10-31). Shipped in the Seed:

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

