
seed: 1.11.15
protocol: 1.8
project_instructions: 4.9

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

## NOTICE - Seed git history rewritten 2026-06-10 (instances: read this)

On 2026-06-10 the Seed repo's git history was rewritten to remove a
user-specific config file (security hygiene). All commit hashes changed.

**Claude instances: surface this notice to your user if their Seed is a
git clone.** Check: does `_DataWizard/Seed/.git` exist? If NOT (they
installed via the zip / update_seed.sh), no action is needed -- updates
work normally. If it IS a git repo, their next `git pull` may fail with
"refusing to merge unrelated histories" or report divergent branches.

**Recovery (rewritten 2026-08-31, remote-agnostic):** do not run any
reset straight from this notice. Follow the single safe procedure in
`Seed/Guides/Git Guide/7.0 Safety and Recovery.md`, section
"Recovering a Seed Clone (Remote-Agnostic)". In brief:

0. Back up first, unconditionally: `git branch backup/pre-recovery-<date>`,
   plus `git stash -u` if the tree is dirty.
1. Identify the canonical remote BY URL
   (`github.com/andrewalan11/DataWizard`), never by the name `origin`.
   On a fork-shaped clone (`origin` = a personal fork, `upstream` =
   canonical), `reset --hard origin/main` silently rolls the Seed back
   to the fork's stale state while every check looks clean -- this
   nearly downgraded a collaborator's Seed on 2026-08-30.
2. `git fetch <canonical> --prune`
3. `git merge --ff-only <canonical>/main` -- fails closed, can never
   lose a commit. If it succeeds, you are done.
4. Only if ff-only refuses AND the guide's triage confirms unrelated
   histories from this rewrite: `git reset --hard <canonical>/main`,
   human-reviewed. No reset runs on one Claude instance's say-so --
   propose on paper and get a second instance's review first
   (Weave D39; DW D109). `Vault Config.md` is untracked/gitignored
   and is not touched either way.

**Never** use `git pull --allow-unrelated-histories` or any merge-based
recovery here -- merging reattaches the old history that the rewrite
removed. (A fast-forward is not that kind of merge: `--ff-only` creates
no merge commit and cannot reattach anything.)

Also in this update: `update_seed.sh` moved from `Seed/Scripts/` to the
Seed root (`_DataWizard/Seed/update_seed.sh`) to match the path the
Project Instructions reference. Zip-install users who updated previously
may have a stale copy at `Seed/Scripts/update_seed.sh` -- it can be
deleted. If a launchd auto-update job was set up per the Seed Auto-Sync
Design, edit its plist to point at the new root path.

This notice can be removed from VERSION.md after 2026-09. The recovery
procedure itself lives durably in Git Guide 7.0 ("Recovering a Seed
Clone (Remote-Agnostic)") and survives this notice's retirement.

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

## What's New in 1.11.9

**Patch release: 13 lessons from a meta-learning review and a partner project (ReWoven).** One DataWizard session (2026-10-21). Ten lessons come from the review of two meta-learning reports, two tool behaviors were sent by ReWoven, and one web-fetch behavior comes from a DataWizard research run (re-tested before planting). Shipped in the Seed:

- `Guides/MCP Reliability and Write Verification/`: 7.0 (the filesystem MCP `outputSchema` failure was seen on one link in 2026-09; in 2026-10 the same tools worked in five sessions in a row, on files up to 84 KB - test one call before you assume the server is broken); 1.0 (the same note on the `filesystem:edit_file` bullet).
- `Guides/Cowork Build Environment/`: 8.0 (`mv` inside one connected folder needs no delete grant, and between two connected folders it copies, then fails to remove the source; the device shell's `$HOME` outlasted a six-hour pause but is no place for the only rollback copy; the `pkill -f` bullet points at the cloud-container case); 4.0 (an always-on launchd job always shows a PID, so an idle check names the jobs that write the store); 6.0 (on macOS a read-only open of a WAL-mode database fails with "unable to open database file" when no `-shm` file exists, and the fix that worked); 8.1 (a stale commit was also seen two turns after the edit - patch a small vault edit on the device instead; staging from the device shell's scratch folder was refused even when `get_device_info` described it as stageable); 8.2 (ids that must be unique are given by the installer at write time; drafts carry a placeholder); 9.0 (`2>&1 | tail` can hide the unittest summary - send the output to a file and grep it).
- `Guides/Chrome MCP and Web Tool Behaviors/4.0 web_fetch Behaviors.md`: the gitlab.com REST API answers `ROBOTS_DISALLOWED`; a gitlab.com project page was blocked for research sub-agents in one session and read fine from another; the GitHub API and the Docker Hub v2 tags API were readable.
- `Guides/Cowork Scheduled Tasks.md`, Other known failure modes: a task prompt's stated premise is a snapshot from when it was written; read the live `last_*` stamp first.
- `Guides/Script Portability.md`: new short section "SQLite builds differ", pointing at the WAL read-only failure in Cowork Build Environment 6.0.
- `Protocols/Conventions Registry/`: 17.0 Holonic records (when you rule on a relation's predicate, read the schema's definition, not only whether the predicate exists); 30.0 Carry the probe, not the snapshot (notes about tools and platforms rot too - read the live source before acting on a recorded tool fact).

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.8

**Patch release: five lessons from the last builds.** One DataWizard session (2026-10-21). Each had been written down in the project's backlog but was not yet in the Seed. Shipped in the Seed:

- `Skills/supervised-build/SKILL.md` (v1.6.1): Reviewer Steps, new paragraph "Fix text goes in the review file" - a reviewer writes the exact current text and its replacement into the review file the fixer reads, never only into its hand-back. In-thread variant, "Scratch, never the vault" - brief every `device_bash` builder to write its output to an absolute path outside the vault. `SKILLS.md`: the row is now v1.6.1.
- `Guides/Cowork Build Environment/8.2 Device Bridge - Sub-agents and Orchestration.md`: new bullet - a `device_bash` sub-agent that did `cd` into the vault and wrote a relative file name left a file in the vault root that the sub-agent could not delete; give the agent a scratch folder and full paths.
- `Protocols/Conventions Registry/26.0 Coordination board.md`: new paragraph - post claims for a step the operator runs by hand just before the run, and re-post them (old blocks `reclaimed`) if the run slips past the ttl.
- `Protocols/YAML Schema.md`, Holonic Records: new paragraph "Stored form of a key" - a key whose value has a "/" (every `github-repo` key) is stored hashed in the operational database; a consumer hashes the plain key from the core's `keys:` with the index's key function and checks the active keys, never plain text.
- `Guides/Cowork Build Environment/9.0 Verification Discipline for Builds.md`: two new bullets - an apply that says `unchanged` is expected when a fix changes only the JSON report (verify on the report); `python3 -I` drops the script folder from `sys.path`, so a test that imports a sibling script needs a run without `-I`.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.7

**Patch release: 2 tool behaviors from a partner project (LocationScout).** One DataWizard session (2026-10-20). Of the 5 behaviors sent, 3 were already in the guides (translated page text in Chrome, the `[BLOCKED: Cookie/query string data]` result on link URLs, the artifact republish handshake); two of those gain one phrase each. Shipped in the Seed:

- `Guides/Chrome MCP and Web Tool Behaviors/`: 2.0 (new rung 12: a site whose robots.txt blocks `web_fetch` was read in the lead's Chrome pass, so route blocked sources back to the lead; rung 7: `innerText` is auto-translated too, so note the source language when you quote); 10.0 (the "unparseable URLs" refusal also hit a page opened from a hand-built deep URL; follow the site's own link from its home page).
- `Guides/Cowork Build Environment/9.0 Verification Discipline for Builds.md`: when the explicit-path Playwright launch also fails, match the npm version to the cached browser build (`ls /opt/pw-browsers`), then launch plainly.
- `Guides/Published Artifacts and ArtifactData Behaviors.md`, "Publishing": `Artifact list` with `scope: files` does not count as viewed either; a second sighting of the refused, refused, publishes sequence.
- `GUIDES.md`: the Chrome MCP row names the robots-blocked-source route.
- `VERSION History.md`: the What's New entries for 1.9.1 to 1.9.5 moved there word for word (size rotation, so this file stays under about 50 KB). Nothing was cut.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.6

**Patch release: 9 tool behaviors from two partner projects (LocationScout, MetaMyth).** One DataWizard session (2026-10-19). Of the 12 behaviors sent, 3 were not planted: two were facts about particular public data sources (they stay in the project that found them) and one was already in the guides. Shipped in the Seed:

- `Guides/Cowork Scheduled Tasks.md`: a one-time (`run_once_at`) run can start about seven minutes late; `fire_trigger` with `text` makes the run work twice; a run started from a published page reached the artifact store every time but the vault only sometimes; in a timed run the Obsidian MCP wrote the vault while the device shell showed no folders (load the tools with an exact `select:` list); scheduled runs wrote the artifact store with no approval.
- `Guides/Published Artifacts and ArtifactData Behaviors.md`, "Page runtime calls": a page can start a scheduled task through the `mcp` capability (the task's owner only; gate the button with `user.isOwner()`); count every live subscription before checking the `db` cap (64 per view).
- `Guides/Cowork Build Environment/5.0 Network and GitHub Data.md`: the device shell failed on Overpass too (HTTP 406, then a timeout); a `fetch` POST from a Chrome tab on `overpass-turbo.eu` worked; one sub-agent got through only on two mirrors after retries. `8.2 Device Bridge - Sub-agents and Orchestration.md`: web-only research sub-agents ran in parallel without the shared-Chrome problem.
- `Guides/Chrome MCP and Web Tool Behaviors/`: 2.0 (reduce the data in the page before slicing it); 10.0 (the `[BLOCKED: Cookie/query string data]` result also fires on plain text that looks like query parameters; replace `[&=?%]` with spaces).
- `GUIDES.md`: the Cowork Scheduled Tasks and Published Artifacts rows list the new topics.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.5

**Patch release: 8 tool behaviors from three partner projects (ReWoven, MetaMyth, Rootland).** One DataWizard session (2026-10-19). Shipped in the Seed:

- `Guides/Published Artifacts and ArtifactData Behaviors.md`: the side-panel window a published page opens in (about 780-900 px wide) and a fit pass for fixed-size pages; `sample` takes a size, not a model, and the viewer who clicks pays; where the platform shows comments and the two artifact link forms (a sent comment carries the uuid one); the publish result's sharing line is the live state; clearing a comment history means a new artifact. `sample` and the existing second-HTML-page bullet now sit under a new heading, "Page runtime calls".
- `Guides/Chrome MCP and Web Tool Behaviors/`: 9.0 (the built-in browser as a route when the extension is not connected; it reaches a server started on the operator's computer; its `resize_window` does change the layout); 1.0 (pointer to that resize); 2.0 (rung 11: a page that loads its screens in same-origin iframes is read through `contentDocument`); 10.0 (the "not connected" bullet points to the built-in browser).
- `Guides/Cowork Build Environment/8.0 Device Bridge.md`: the device shell held for a full session after the inode fix; a pointer to the built-in browser for operator-started localhost servers.
- `GUIDES.md`: the Published Artifacts and Chrome MCP rows list the new topics.
- `VERSION History.md`: the What's New entry for 1.9.0 moved there word for word (size rotation, so this file stays under about 50 KB). Nothing was cut.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## What's New in 1.11.4

**Patch release: 17 tool behaviors from five partner projects (Rootland, Kosmosis, MetaMyth, ReWoven, Community Stack).** One DataWizard session (2026-10-19). Shipped in the Seed:

- `Guides/Cowork Build Environment/`: 8.0 (adding a folder to the claude.ai Project does not connect the bridge; with no connected folder the Obsidian MCP writes notes and the Mac filesystem MCP writes other files; more wedged-shell sightings); 8.1 (macOS Terminal `tar` bundles carry AppleDouble `._*` files, use `COPYFILE_DISABLE=1`; `device_commit_files` creates missing folders; `expectedMtimeMs` as a guarded batch overwrite); 8.2 (sub-agents read the Mac through the filesystem MCP with the shell down; resume the builder by message to apply a review); 9.0 (scripted checks by cheaper tiers from a stronger tier's check plan).
- `Guides/Published Artifacts and ArtifactData Behaviors.md`: the multi-file publish root, slide speaker notes in `<aside>`, an `as_level` check of the db rules, comments not sent to Claude (read-only), comment-list paging, and the entry-page rule for capabilities (a second HTML page is untested).
- `Guides/Chrome MCP and Web Tool Behaviors/12.0`: a negative web finding needs a second check before it changes data; Claude Docs chart embeds can be hand-drawn SVG.
- `Guides/MCP Reliability and Write Verification/`: 6.0 (`filesystem__read_multiple_files` overflows); 12.0 (`filesystem:edit_file` echoes every hunk, so a small edit to a long-line file floods the context).
- `GUIDES.md`: the Published Artifacts row lists the new topics.
- `VERSION History.md`: the What's New entry for 1.8.0 moved there word for word (size rotation, so this file stays under about 50 KB). Nothing was cut.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-10)

## Older releases

The What's New entries for 1.10.0 to 1.11.3 are in `VERSION History.md`, and 1.0.0 to 1.9.5 are in `VERSION History - 1.0.0 to 1.9.5.md` (moved there word for word, 2026-10).

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
