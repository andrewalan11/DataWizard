
seed: 1.15.6
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

## What's New in 1.15.6

**Patch release (2026-11-22): harvest point ids when several projects harvest one call.** Registry and YAML Schema wording only; no script changes.

- `Protocols/Conventions Registry/28.0 ID families.md`: the Harvest point ids row. One call has one id space, kept on the transcript. Whoever files the transcript writes `point_id_prefix:`. Each project that harvests the call claims its own number block there, in the new list field `point_id_blocks:` (one line per block, with `project` and `range`; blocks are 001-999, then 1000-1999, and so on). A claim is checked by a re-read; on a clash, the later line moves to the next free block. A retired id stays in its harvest note as a line marked retired. A planted passage cites its point with a normal block citation. The row is still a pilot.
- `Protocols/Conventions Registry/11.0 Citation format.md`: new paragraph "Harvest point ids" - a harvest point id is a valid block anchor, a planting link is a normal citation, and a passage gets its own `^bN` only when something cites it.
- `Protocols/YAML Schema/2.0 YAML Schema - Harvest and Federation.md`: new section "Harvest point ids (pilot)" - the form of the two transcript fields `point_id_prefix:` and `point_id_blocks:`; the rules stay in Registry 28.0.

**What to do:** nothing breaks. Run `update_seed.sh`. Projects that do not harvest calls need no change. A project that already mints point ids on a call adds `point_id_prefix:` and its block line to the transcript before its next id.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.15.5

**Patch release (2026-11-22): seven tool behaviors planted in the guides, and optional status words for decision-log entries.** Guide, Registry and skill wording only; no script changes.

- `Guides/Chrome MCP and Web Tool Behaviors/4.0 web_fetch Behaviors.md`: parallel WebFetch calls to one site are rate limited - groups of at most 4, no two links of one site; YouTube video pages mostly fail.
- `Guides/Chrome MCP and Web Tool Behaviors/6.0 Scripted Downloads from the Shells (Container and Device).md`: a `device_bash` curl loop over many links can be denied by the auto-mode classifier; use WebFetch in small groups or the operator's Terminal.
- `Guides/Cowork Build Environment/8.2 Device Bridge - Sub-agents and Orchestration.md`: a sub-agent has a large fixed token cost; size link-reading batches at 30 or more.
- `Guides/Git Guide/5.5 DW Save.md`: `launchctl unload` without `-w` lasts until logout (RunAtLoad syncs at the next login), `launchctl load` starts one sync; the hotkey is an Obsidian Shell Commands binding (works with the job unloaded, not with Obsidian closed).
- `Protocols/Conventions Registry/13.0 Decision-log conventions.md`: optional decision status - `Status: Binding` or `Status: Working approach - test and revise` with `Revisit when:`, a `Guardrail (binding):` line, and four guards. Entries without a Status line are unchanged.
- `Skills/session-closer/SKILL.md` (v4.11.7): Step 2 asks whether a proposed Decision Log entry is Binding or Working approach.

**What to do:** nothing breaks. Run `update_seed.sh`. Existing decision logs need no edits; use the status words on new entries if you want them.

**Propagation:** `update_seed.sh`. The session-closer change is in the skill file, so it takes effect at the next close. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.15.4

**Patch release (2026-11-22): seven tool behaviors planted in the platform guides.** Guide wording only; no script changes.

- `Guides/Cowork Build Environment/8.1 Device Bridge - Staging, Commits and Transport.md`: a copy longer than the call limit runs in parts with `dd` (`skip`, `seek`, `conv=notrunc`, then `md5sum`); the Dropbox mount bullet notes that the failure is not constant.
- `Guides/Cowork Build Environment/3.0 Python and Packages.md`: packages installed with `pip install --break-system-packages` in the device shell stay for the session.
- `Guides/Cowork Build Environment/8.2 Device Bridge - Sub-agents and Orchestration.md`: a builder can be resumed several times with `SendMessage` and a short brief; reviewers stay fresh agents.
- `Guides/Chrome MCP and Web Tool Behaviors/6.0 Scripted Downloads from the Shells (Container and Device).md`: a large download as repeated resumable foreground `curl` calls, because a background download dies with the `device_bash` call.
- `Guides/Chrome MCP and Web Tool Behaviors/10.0 Claude-in-Chrome Extension from a Cowork Cloud Session.md`: Chrome screenshots are files in the cloud container and can be archived; `browser_batch` stops at a site change; a scroll can zoom a canvas app.

**What to do:** nothing breaks. Run `update_seed.sh`.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.15.3

**Patch release (2026-11-22): a shared spelling list for harvests, and three small harvest rules.** Canon and skill wording; no script changes.

- `Protocols/Conventions Registry/39.0 Shared add-only registers.md` (new): a shared register is a data file that sessions of several projects may add lines to. Only files listed under `shared_registers:` in your `Vault Config.md` count. Add a line at the end, with the operator's yes and your session id; never edit or delete another session's line; the latest line wins; the owning project tidies by rotating to an archive. Data, not canon: the canon write gate (15.0) is unchanged. First register type: the spelling list, line form `- heard | correct | project | core_id | session | note`. `Conventions Registry.md` embeds it.
- `Protocols/Conventions Registry/28.0 ID families.md`: a row for harvest point ids (`h<YYMMDD>-NNN`, prefix claimed in the transcript's frontmatter; pilot).
- `Protocols/Conventions Registry/7.0 Shell and section architecture.md`: a large non-markdown data file beside a source (for example a harvest trace in JSON) is exempt from the 50 KB split rule.
- Skills: `transcript-harvest` v0.10.1 (Step 5 reads the spelling list before naming people; the speaker matters in three cases only: an idea someone may claim, a decision or agreement, a task taken on), `harvest-router` v1.3.2 (Hub mode name check reads the spelling list; new variants are added as register lines). `SKILLS.md` rows synced.

**What to do:** nothing breaks. Run `update_seed.sh`. To use a spelling list, add `spelling_list:` (the file's vault-relative path) and `shared_registers:` (the same path) to the Paths table of your `Vault Config.md`. Without them, harvests skip the step.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.15.2

**Patch release (2026-11-19): a harvest hub reads documents, and PDF conversion honours the output folder.** One script fix with a new test; canon and skill wording.

- `Scripts/batch_pdf_convert.py`: new `--output-dir` (one PDF only; a folder input with it exits with an error). The .md, `PDF Sections/` and the log go there; without it, nothing changes. `Scripts/convert_to_md.sh` now passes the output folder for PDFs and strips a trailing slash (no more `//` in paths). `Scripts/test_batch_pdf_convert.py` (new): 9 tests, standard library only, no PDF engine needed.
- `Protocols/YAML Schema/2.0 YAML Schema - Harvest and Federation.md`, Harvest Tracking: new "Document sources" block (`received_from`, `source_origin`, `source_file`, optional `source_path`, `author`, `source_url`; on the synth note `source_format` and `source_origin`).
- `Protocols/Conventions Registry/9.0 Harvest via embeddable synth note.md`: document synth notes go in `_Companions/_Docs/`. `11.0 Citation format.md`: a hub reading of a document cites by section heading (a third named exception to the block default).
- Skills: `harvest-router` v1.3.1 (Hub mode: a Documents bullet; the Content Interests digest is an aid - check it against each project's 0.0 on disk), `document-harvest` v0.5.4 and `content-interest-scan` v0.1.3 (a "Not for" pointer to hub reading). `SKILLS.md` rows synced.

**What to do:** nothing breaks. Run `update_seed.sh`. Web-page sources in a hub reading are provisional (tested once).

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.15.1

**Patch release (2026-11-19): tool behaviors from partner projects (Earth Changes, Mesocosm, DataWizard).** Docs only; no script or Seed skill changes.

- `Guides/Cowork Build Environment/8.0 Device Bridge.md`: a folder refusal is not constant (the vault root was refused in one session and granted in a later one); a folder added in the project settings did not reach an open chat (Mesocosm). A folder granted at project level can be missing in a new session; check `ls $HOME/mnt/` first (Earth Changes).
- `Guides/Cowork Build Environment/8.2 Device Bridge - Sub-agents and Orchestration.md`: a message to a running sub-agent is queued; a finished agent returned its report on `SendMessage` (seen once); `run_in_background: false` did not hold for a single sub-agent either - plan every Agent call as background; new bullet: token counts are in the task notification, not visible to the agent (seen once) (Earth Changes).
- `Guides/Cowork Build Environment/4.0 Shell and File-Tool Quirks.md`: overwrite in place and `os.replace` work on the vault mount, only delete is refused; `cp -p` backups keep the source mtime, so `find -newer` misses them (DataWizard).
- `Guides/MCP Reliability and Write Verification/12.0 Obsidian Behavioral Gotchas.md`: the git bullet no longer says overwrite fails (it contradicted the same guide).
- `Guides/Cowork Scheduled Tasks.md`: a device-bound task accepts prompt edits but refuses a model change from a session (seen once) (DataWizard).
- `Guides/Chrome MCP and Web Tool Behaviors/4.0 web_fetch Behaviors.md`: more routes for blocked papers (institutional repositories, OpenAlex); PMC was blocked in one run and worked in another; "the exact sentence that contains X" gave verbatim text in 13 of 13 checks (seen once) (Earth Changes).
- `SKILLS.md`: the intake-handoff Workshop row synced to v1.0.8.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.15.0

**Minor release (2026-11-19): the look line writer and the ledger method.** A project's look at a subject (a tool, an org, a link, a work) is one line in that project's ledger note. One script writes the lines, and the decision word (adopt, watch, pass and so on) lives on the line, not in a fit view. Shipped in the Seed:

- `Scripts/look_write.py` (new, 0.1.2): commands `init`, `add`, `check`, `find`, `confirm`; every writing command has `--dry-run`. Standard library only, ASCII. Its header docstring is the manual (flags, exit codes, line grammar). `Scripts/test_look_write.py` (new): 79 tests.
- `Protocols/Conventions Registry/38.0 Project looks - the ledger line.md` (new): the rule, the twelve fields, the word lists (Kind, Depth, Relevance, Outcome), the line grammar, where lines go, the line id, the frozen banner, the `(D183)` token and the `holon_lens_map` row. `Conventions Registry.md` embeds it. `23.0 Tracking Model.md`: one row. `10.0 Archiving.md`: a named exception for frozen research tables. Until the rewrite of `18.0 Tech tool evaluations.md`, 38.0 wins over the Fit view bullet of 18.0.
- `Protocols/YAML Schema/1.0 YAML Schema - Core Fields.md`: new heading "Ledger Flag" (`look_ledger: <ABBR>`; scripts find ledgers by this flag only; the writer does not stamp `updated:` or `edit_log` on a ledger note). `2.0 YAML Schema - Harvest and Federation.md`: the `reviewed` wording, and a pointer from the Roll-up paragraph.
- `Guides/Seed Install and Update.md`: new section - add your project's row to `holon_lens_map` before its first look.
- Skills: `research-tracking` v1.6.0 (and `references/tracking-index-template.md`) - the duplicate check runs `look_write.py find`, a new look is `look_write.py add`, and the first look of a project makes the ledger with `init`. `tools-research` v1.5.0 - batch and light verdicts are look lines; the depth tiers map to the Depth words. `content-interest-scan` v0.1.2 - dedup uses `find`. `design-harvest` checked, no change.
- `SKILLS.md`: rows for the three skills, and the intake-handoff, dw-research-workflow and batch-triage rows synced to their versions. `README.md`: the Scripts line and the file list. `VERSION.md`: What's New 1.14.0 to 1.14.4 moved word for word to a new closed part, `VERSION History - 1.14.0 to 1.14.4.md`; `VERSION History.md` names it. Nothing deleted.

**What to do:** nothing breaks. Hand-typed tracking tables keep working, and nothing converts by itself. To start using the writer in a project: add the project's folder to the `holon_lens_map` row in your `Vault Config.md`, make the sections folder, run `look_write.py init` once, then `add` for each look. On Windows, use `python` or `py` in place of `python3`.

**Heads-up:** until a project's old index is converted, `find` does not see that project's old rows. The skills say to also read the old index by name until then.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.10

**Patch release (2026-11-16): tool behaviors from partner projects (Earth Changes, Flow Funding, Slide Canvas).** Docs only; no script or skill changes.

- `Guides/Chrome MCP and Web Tool Behaviors/4.0 web_fetch Behaviors.md`: publisher pages (Nature, Science, PNAS, Wiley, some ScienceDirect, PMC) block WebFetch - fallback routes, and mark each fact opened, abstract only or could not open (Earth Changes). WebFetch summarizes HTML pages too and caps quotes near 125 characters; `curl` plus `pandoc` gives verbatim text (Flow Funding).
- `Guides/Chrome MCP and Web Tool Behaviors/5.0 WebSearch Behaviors.md`: an empty `site:` result is not evidence that a small static site lacks a page (Flow Funding).
- `Guides/Cowork Build Environment/5.0 Network and GitHub Data.md`: `web.archive.org` is blocked from the container but the Wayback availability API answers; snapshots open from the device shell (Flow Funding, DataWizard).
- `Guides/Cowork Build Environment/8.0 Device Bridge.md`: a chat open before a session-disk swap keeps no device shell after it (Slide Canvas).
- `Guides/Cowork Build Environment/8.1 Device Bridge - Staging, Commits and Transport.md`: build a large file in the container and commit it instead of typing it into a heredoc; sizes seen once (Earth Changes, Slide Canvas). `4.0 Shell and File-Tool Quirks.md`: a cross-link to it.
- `Guides/Cowork Build Environment/8.2 Device Bridge - Sub-agents and Orchestration.md`: `run_in_background: false` did not hold for parallel sub-agents (Earth Changes); the restart bullet names a session-server restart (Slide Canvas).
- `Guides/Published Artifacts and ArtifactData Behaviors/1.0 Published Artifacts - Publishing and Reading.md`: `upload_asset` refuses a file under `/tmp` (Slide Canvas).
- `Guides/Published Artifacts and ArtifactData Behaviors/2.0 Published Artifacts - Store, Sharing, Comments, Rendering and Runtime.md`: a refused `db_write` can return `not-found`; external links must be real `<a href>`; the two publish paths differ on a page fragment (Slide Canvas).

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.9

**Patch release (2026-11-16): four tool behaviors from partner projects (ReWoven, Flow Funding), and two out-of-date warnings.** Docs only; no script or skill changes. Shipped in the S512 session.

- `Guides/Cowork Build Environment/8.1 Device Bridge - Staging, Commits and Transport.md`: `device_commit_files` takes `stagedPath` under `/mnt/user-data/outputs/` (or `/mnt/project-files/` in a project thread); a file under `/home/claude/` or the uploads path from `device_stage_files` is refused - copy it into outputs first, then commit (ReWoven). New bullet: `zip` cannot write straight into a vault folder ("Operation not permitted", it leaves its temp file behind); zip into the device shell's `$HOME`, then `cp` the zip in (Flow Funding).
- `Guides/Cowork Build Environment/8.0 Device Bridge.md`: the auto mode classifier can block a `mv` to a destination the operator did not name; ask the operator to name it, and do not work around the block (Flow Funding).
- `Guides/Published Artifacts and ArtifactData Behaviors/2.0 Published Artifacts - Store, Sharing, Comments, Rendering and Runtime.md`: the `obsidian://` link bullet names the tested link form (ReWoven).
- `Protocols/Conventions Registry/18.0 Tech tool evaluations.md` and `Protocols/YAML Schema/3.0 ...` (Tool Evaluation Notes): a warning at the top says the text is out of date in part. D169 (one note per tool; a project's fit is a section; the Tech Tools note is the core; an id only when a join needs one) wins until the rewrite lands.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.8

**Patch release (2026-11-15): the meta-learning stamp always exists, scans check earlier rulings, and three tool behaviors from partner projects (Kosmosis).** Docs and skill text only; no script changes. Shipped in the Seed:

- `Skills/project-guidelines/SKILL.md` v1.6.1: the 0.0 frontmatter template carries `last_meta_learning_review: none`, so the field always exists (Kosmosis, EM and ReWoven each had a 0.0 without it, and every scan guessed its own start point).
- `Skills/meta-learning-scan/SKILL.md` v1.4.4: Step 2 - when the stamp is absent, the scan adds it once with a baseline value (the end of the newest reviewed report, else `none`) or posts a one-line flag, and writes the start point it used into a new report field `scan_baseline:`; the no-update rule stays, with this one named exception. Step 4 - before reporting a recurring family as new, read earlier Review Outcomes; a family already named or ruled is reported as `confirm-home: <family>, ruled <review>`.
- `Skills/meta-learning-review/SKILL.md` v1.5.8: Step 5 creates the reviewed-through stamp when 0.0 lacks it. `Skills/project-health-audit/SKILL.md` v2.1.3: a 0.0 without the stamp is a finding (J1). `SKILLS.md`: four rows updated.
- `Protocols/Conventions Registry/26.0 Coordination board.md`: the board script's `seen` command works only on awareness asks; it refuses an action ask, and an action ask to `all` stays open after one project does the work - read its `resolution:` line before acting (seen once).
- `Guides/Git Guide/9.0 Troubleshooting.md`: a check script fails after an interrupted `git fetch` because HEAD stays on the old commit; compare `git log -1` with the expected head before reading the failure (seen once).

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.7

**Patch release (2026-11-15): two plants from a meta-learning review, and a batch of tool behaviors from partner projects (Common Woods, ReWoven, LocationScout, Flow Funding, Kosmosis, Tech Tools).** Docs only; no script changes. Shipped in the Seed:

- `Guides/Script Portability.md`, "Case-insensitive disks": a test's fixture folder, not the test file's location, decides which disk the test really runs on. A suite run from the mounted folder still passes on the container's case-sensitive disk if the fixtures go to a temp folder there. `Guides/Cowork Build Environment/9.0`: one clause points to it.
- `Guides/Git Guide/5.5 DW Save.md`: new section "Pausing Both Auto-Committers". For a step that must land as one commit, pause the Obsidian Git plugin and the DW Save job. Quitting Obsidian stops only the plugin. `Guides/Git Guide/3.0` and `7.0`: a pointer each. The unload command is linked from its home in `6.0`, not restated.
- `Guides/Chrome MCP and Web Tool Behaviors/7.0 Google Docs via Chrome.md`: the Drive-connector line now says only the Drive connector cannot edit a Doc; new bullets - the Google Docs connector edits a Doc in place and `addDocumentTab` works; `read_doc` of a tabbed Doc is very large, always saved to a file, with no per-tab read, and each write needs a fresh `revisionId`; a new table's multi-line cells work but bullets need a second pass; a one-page check by PDF export. A scope line says the section also covers the Docs connector.
- `Guides/Chrome MCP and Web Tool Behaviors/4.0 web_fetch Behaviors.md`: Kleinanzeigen location ids from `/s-ort-empfehlungen.json`; Zenodo PDFs - WebFetch returns only binary, so download with curl in the cloud container, one record at a time.
- `Guides/Published Artifacts and ArtifactData Behaviors/1.0`: `list_files` and `read_file` refuse an artifact someone else has written to. `2.0`: the chat `db_*` tools cannot patch inside a large nested document (use a small inbox doc); Chrome sends no mouseup after an HTML5 drag; an internal drag can type its id into a text field.
- `Guides/Cowork Build Environment/8.1`: pass `timeout_ms` for a loop of slow scripts; a Dropbox (File Provider) folder may fail to mount in `device_bash`. `8.2`: for a verbatim import, a script copies and reports a diff. `11.0`: account skills are synced read-only in the cloud container. `4.0`: the 45000 `timeout_ms` cap is the sandbox's `bash`, not `device_bash`.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.6

**Patch release (2026-11-14): a new continuation of the Device Bridge guide, with the 503 outage behavior.** Docs only; no script changes. Guide 8.0 passed the 30 KB soft size, so a continuation was started and nothing was cut. Shipped in the Seed:

- `Guides/Cowork Build Environment/8.3 Device Bridge - Outages and Recovery.md` (new): when every `remote-devices` call returns 503 "Service Unavailable" (other connectors too; `get_device_info` may still answer), it is neither the full-disk fault nor a bridge drop. How to tell the three apart by what still works, the after-check (`df` about 1% used), that it cleared on its own after about five hours, and the caution that a sub-agent's saved output must be checked and hashed by the lead before the commit. Links to the existing outage bullets in 8.0, 8.1 and MCP Reliability.
- `Guides/MCP Reliability and Write Verification/3.0 Bridge Drops and Hangs (Remote Transport).md`: one pointer paragraph to 8.3.
- `Guides/Cowork Build Environment.md`: embed line for 8.3 after 8.2. `Guides/Cowork Build Environment/8.0 Device Bridge.md`: the intro line points to 8.3.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## What's New in 1.14.5

**Patch release (2026-11-11): the device-shell session disk has two full forms.** Docs only; no script changes. The session disk inside the shell VM can fill by inodes (seen 2026-10) or by space (seen 2026-11: 22 MB free of 9.8 GB, inodes at 39%). Both stop the device shell; the fix is the same swap of `sessiondata.img`. Shipped in the Seed:

- `Guides/Cowork Build Environment/8.0 Device Bridge.md`: the session-disk bullet names both forms; the watch runs `df -h /sessions; df -i /sessions` and plans the swap when either passes 80% (it was `df -i` only, at 100%).
- `Guides/Cowork Build Environment/8.1 Device Bridge - Staging, Commits and Transport.md`: new bullet - the space-full form (low space was seen twice and only worked around before the shell failed; a low-space sighting needs a swap date); after the swap only chats started after it get a device shell - a pre-swap chat keeps only the MCP tools, so verify in a new chat with a folder connected.

**Propagation:** `update_seed.sh`. No Project Instructions change and no re-paste. (DataWizard, 2026-11)

## Older releases

The What's New entries for 1.14.0 to 1.14.4 are in `VERSION History - 1.14.0 to 1.14.4.md`, 1.11.16 to 1.13.5 are in `VERSION History - 1.11.16 to 1.13.5.md`, 1.11.4 to 1.11.15 are in `VERSION History.md`, 1.10.0 to 1.11.3 are in `VERSION History - 1.10.0 to 1.11.3.md`, and 1.0.0 to 1.9.5 are in `VERSION History - 1.0.0 to 1.9.5.md` (moved there word for word, 2026-10 and 2026-11). Expired notices (the 2026-06-10 git history rewrite) are in `VERSION History.md`, section "Retired notices".

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
