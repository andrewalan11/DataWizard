
seed: 1.14.6
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

## Older releases

The What's New entries for 1.11.16 to 1.13.5 are in `VERSION History - 1.11.16 to 1.13.5.md`, 1.11.4 to 1.11.15 are in `VERSION History.md`, 1.10.0 to 1.11.3 are in `VERSION History - 1.10.0 to 1.11.3.md`, and 1.0.0 to 1.9.5 are in `VERSION History - 1.0.0 to 1.9.5.md` (moved there word for word, 2026-10 and 2026-11). Expired notices (the 2026-06-10 git history rewrite) are in `VERSION History.md`, section "Retired notices".

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
