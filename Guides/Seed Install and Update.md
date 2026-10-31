---
audience: Claude instances helping DataWizard users
created: 2026-06-11
edit_log:
  - DW-S168 2026-06-11
  - DW-S189 2026-06-18
  - "DW-S227 2026-08-01 - Jay FR batch item b: zip-as-canon distribution note;
    Windows update_seed.ps1 manual-update instructions + Task Scheduler
    auto-sync section"
  - "DW-S227 2026-08-01 - Jay FR batch item d: announcement norm added to
    Upstream Operator Note; note de-personalized (maintainer name removed)"
  - DW-S270 2026-08-15 - one-command auto-sync installers (--install-autosync /
    -InstallAutosync) replace the manual plist and Task Scheduler recipes;
    sleep/wake catch-up semantics documented; upstream seed_role guard;
    git-clone-aware sync
  - "WV_2026-09-07_AA_03 2026-09-09 - Upstream Operator Note: diagnostic corollary (missing sync log on an upstream clone is expected; check seed_role first)"
  - 'DW-S400 2026-10-12 - distribution model: Seed-embedded-in-shared-vault-repo shape (update path, social pinning, onboarding presence check)'
  - 'DW-S447 2026-10-31 - new section: Claude Code and Obsidian sidebar plugins (per-person PI pointer, PI.md, import facts, external-import dialog, checks)'
operator: Andrew
purpose: Canonical guide for installing, manually updating, and auto-syncing the
  DataWizard Seed
title: Seed Install and Update
type: guide
updated: 2026-10-31
---
# Seed Install and Update

*For Claude instances helping DataWizard users install or update their Seed. Covers fresh install, manual updates, and automated sync setup.*

## Distribution model: zip is canonical

The **zip download is the canonical install and update path for every operator, on every platform.** All install/update commands and both update scripts (`update_seed.sh`, `update_seed.ps1`) pull the GitHub zip, not a git clone.

Git clones of the Seed are for **contributors only**. The Seed's history can be rewritten (for example, to purge an accidentally committed secret), which breaks a downstream clone's next `git pull` with an unrelated-histories error -- while the zip is unaffected. So: **operator path = zip** (the scripts below), **contributor path = git clone** (only if you intend to push changes back upstream). `update_seed.sh` recognizes a cloned Seed and syncs it with `git fetch` + fast-forward merge instead of the zip, refusing to touch local edits or local commits; `update_seed.ps1` skips clones and tells you to sync with git.

**A third shape: the Seed embedded in a shared vault repo.** A team can run one shared vault as a single git repo with `_DataWizard/Seed/` committed inside it, so every collaborator gets the Seed when they clone the vault. The embedded copy has no `Seed/.git`, so both update scripts treat it as a zip install. The update runs once for the whole team: one person runs the update script against the embedded copy, then commits and pushes the vault repo, and everyone else gets the new Seed through their normal vault sync. Name one updater and leave auto-sync off on the other machines, or several machines will rewrite the same tracked folder. Version pinning is social, not mechanical: the team works from whatever Seed the vault repo last carried. A machine-onboarding step that checks the cloned vault actually contains the Seed, and flags it when missing, keeps everyone on one pinned protocol version. (Field deployment, 2026-09.)

---

## Step 1: Find the vault path

Run `obsidian:get_vault_stats` to confirm MCP is connected. Then run `obsidian:list_directory` with path `_DataWizard/Seed` to confirm the Seed exists.

If the Seed folder doesn't exist at all, skip to the Fresh Install section below.

## Step 2: Determine the platform

Ask your human: "Are you on Mac or Windows?" (Or check if you already know from context.)

---

## Fresh Install

If `_DataWizard/Seed` doesn't exist, the Seed was never installed.

Claude Code users: after the install, see the "Claude Code and Obsidian sidebar plugins" section below for how to load the Project Instructions.

### Mac

```bash
cd "/path/to/vault" && \
curl -sL https://github.com/andrewalan11/DataWizard/archive/refs/heads/main.zip -o /tmp/dw-seed.zip && \
unzip -qo /tmp/dw-seed.zip -d /tmp/dw-seed && \
mkdir -p _DataWizard/Seed && \
cp -R /tmp/dw-seed/DataWizard-main/* _DataWizard/Seed/ && \
rm -rf /tmp/dw-seed /tmp/dw-seed.zip && \
echo "DataWizard Seed installed."
```

Replace `/path/to/vault/` with the actual vault path. If you have filesystem access, you can find it by checking where Obsidian MCP points.

### Windows (PowerShell)

```powershell
cd "C:\path\to\vault"
Invoke-WebRequest -Uri "https://github.com/andrewalan11/DataWizard/archive/refs/heads/main.zip" -OutFile "$env:TEMP\dw-seed.zip"
Expand-Archive -Path "$env:TEMP\dw-seed.zip" -DestinationPath "$env:TEMP\dw-seed" -Force
if (!(Test-Path "_DataWizard\Seed")) { New-Item -ItemType Directory -Path "_DataWizard\Seed" -Force }
Copy-Item -Path "$env:TEMP\dw-seed\DataWizard-main\*" -Destination "_DataWizard\Seed\" -Recurse -Force
Remove-Item -Path "$env:TEMP\dw-seed.zip", "$env:TEMP\dw-seed" -Recurse -Force
Write-Host "DataWizard Seed installed."
```

After installing, the human also needs to paste Project Instructions into a Claude Project. Read `_DataWizard/Seed/DataWizard Project Instructions.md` and help them set it up. Without this step, the Seed files exist but Claude won't know the protocol.

For full setup (MCP connection, Weave repo access, etc.), see the `DataWizard Setup and Sync Checklist` in the Weave Workflows folder.

---

## Manual Update

If the Seed already exists, use `update_seed.sh`:

```bash
bash "/path/to/vault/_DataWizard/Seed/update_seed.sh"
```

The script auto-detects the vault path if run from within the Seed folder. It compares versions and only downloads if there's a newer version available.

If `update_seed.sh` doesn't exist (older install), use the curl command from the Fresh Install section above -- it handles both fresh installs and updates.

On Windows, use the PowerShell twin `update_seed.ps1` (same version-compare, sync-log, and PI-change behavior, same exit codes):

```powershell
powershell -ExecutionPolicy Bypass -File "C:\path\to\vault\_DataWizard\Seed\update_seed.ps1"
```

Like the bash script, it auto-detects the vault root when run from inside the Seed folder, and only downloads when a newer version is available. If `update_seed.ps1` doesn't exist (older install), use the PowerShell command from the Fresh Install section -- it handles both fresh installs and updates.

---

## Automated Sync

Once manual updates work, turn on daily automatic syncing so the Seed stays current without human intervention. Both installers are built into the update scripts -- one command, no hand-edited config.

**The machine does not need to be awake at the scheduled hour.** On Mac, launchd runs a missed calendar job once when the machine wakes from sleep, and the login trigger covers a machine that was powered off. On Windows, Task Scheduler's `StartWhenAvailable` fires a missed run as soon as the machine is next available. The only way to never sync is to never turn the computer on.

### Path A: Already running datawizard-sync.sh (Mac)

If the user already has a launchd agent running `datawizard-sync.sh` for git repo syncing, the Seed just needs to be included in their sync config.

1. Check if `~/.datawizard-sync.conf` exists. Ask the user to run:
   ```bash
   cat ~/.datawizard-sync.conf
   ```
2. Look for a line pointing to their `_DataWizard/Seed` folder (e.g. `/Users/username/Vaults/MyVault/_DataWizard/Seed`).
3. If the Seed path is missing, add it. Ask the user to run:
   ```bash
   echo "/path/to/vault/_DataWizard/Seed" >> ~/.datawizard-sync.conf
   ```
   Replace with their actual vault path.
4. Verify the launchd agent is loaded:
   ```bash
   launchctl list | grep datawizard
   ```
   Should show `com.datawizard.sync`. If not, they need to reload it.

Done. Their existing sync schedule now covers the Seed. They do NOT also need Path B -- that would be two agents syncing the same folder.

### Path B: Seed-only sync (Mac)

One command:

```bash
bash "/path/to/vault/_DataWizard/Seed/update_seed.sh" --install-autosync
```

This writes the launchd agent (`com.datawizard.seed-update`) with the vault path filled in automatically, loads it, verifies it registered, and writes an "Auto-sync installed" entry to the Seed Sync Log. Schedule: daily at 6:00 plus at every login, with catch-up on wake. Options:

- `--hour N` -- sync at a different hour (0-23), e.g. `--hour 9`
- `--uninstall-autosync` -- remove the agent

`RunAtLoad` means the first sync fires immediately on install -- that's expected.

Verify:
```bash
launchctl list | grep datawizard.seed
```
Should show `com.datawizard.seed-update`, and the Seed Sync Log should have the install entry.

### Windows (Task Scheduler)

One command (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File "C:\path\to\vault\_DataWizard\Seed\update_seed.ps1" -InstallAutosync
```

This registers a Scheduled Task named "DataWizard Seed Update": daily at 6:00 plus at every logon, with `StartWhenAvailable` catch-up for runs missed while the machine was asleep or off. No admin rights required. Options:

- `-Hour N` -- sync at a different hour (0-23)
- `-UninstallAutosync` -- remove the task

Verify:
```powershell
Get-ScheduledTask -TaskName "DataWizard Seed Update"
```

Optionally run it once on demand to confirm end to end:
```powershell
Start-ScheduledTask -TaskName "DataWizard Seed Update"
```

Results log to `_DataWizard\Seed Sync Log.md`, the same log the Mac path writes.

> Note: the Windows installer has not yet been validated on a live Windows machine -- confirm the first run against the Seed Sync Log before relying on the schedule.

---

## Verify

After any install or update, read `_DataWizard/Seed/VERSION.md` using `obsidian:read_note`. It contains the current `seed:`, `protocol:`, and `project_instructions:` versions. Tell the human what you see.

To check if automated sync is working over time, look for `_DataWizard/Seed Sync Log.md` in Obsidian. Each sync writes a timestamped entry. If the log exists and has recent entries, sync is running.

Claude instances now report `seed_version` in session log frontmatter (protocol 1.8). When scanning session logs, a stale `seed_version` value means that operator's Seed isn't current.

## Check Project Instructions

While verifying, check whether the human's Project Instructions version matches. The PI version is in the header of whatever instructions are pasted into their Claude Project settings (e.g. "DW Project Instructions v4.3"). If their running PI is older than what VERSION.md says, tell them:

> "Your Project Instructions are out of date. Copy the updated version from `_DataWizard/Seed/DataWizard Project Instructions.md` into your Claude Project settings."

---

## Claude Code and Obsidian sidebar plugins

*For people who run Claude Code in a terminal, or inside Obsidian through a sidebar plugin. Cowork users paste the Project Instructions (PI) into Project settings instead; see "Cowork users" below.*

### Where your pointer goes

Claude Code loads the PI through an import line, the pointer. The pointer holds your own path to the Seed, so it is personal. Put it in a CLAUDE file that you own and that git does not track:

- **Your vault holds the repo:** use the vault-root `CLAUDE.md`.
- **The repo is your vault, or you start Claude Code in the repo:** use a `CLAUDE.local.md` at the repo root, and list it in the repo `.gitignore`.

A shared repo's tracked `CLAUDE.md` holds only repo-relative, team-wide lines. It never holds a Seed path. Each person's Seed path is different, so a path in a tracked file breaks for the others at the next pull. Canonical rule: D96 in the Conventions Registry (33.0 Operational one-liners).

### Import facts

- A relative path is read from the file that holds the import, not from the folder where you start Claude Code.
- Put a backslash before every space in the path.
- Never put quotes around the path. A quoted path is not imported.
- An import inside backticks or a code block does not fire.
- Imports chain at most 4 hops.

### Point at PI.md

The Seed root holds `PI.md`. Its only line imports the Project Instructions from its own folder, so it works in the nested and the flat Seed layout. Point your import at `PI.md`. Then you escape spaces only in your own path to the Seed. Your pointer plus `PI.md` uses 2 of the 4 hops.

Example pointer lines follow. They are in a code block, so they do not fire here. Copy one line, without quotes, into your own CLAUDE file. Then change the path to match your machine.

```
@../_DataWizard/Seed/PI.md
@_DataWizard/PI.md
@../Shared\ Vault/_DataWizard/Seed/PI.md
```

- Line 1: the Seed is nested (`_DataWizard/Seed/`) and sits beside the repo.
- Line 2: the Seed is a flat clone (no `Seed/` level) inside the repo.
- Line 3: Windows (not yet tested on a Windows machine). Use forward slashes, not backslashes. The example also shows an escaped space.

### The external-import dialog

Claude Code asks before it loads an import that points outside the folder where you start it. This can also happen when you start in a repo subfolder and the vault-root `CLAUDE.md` holds an import that points outside that subfolder (untested). On a first launch in a new folder, a folder-trust dialog comes first.

The dialog title is "Allow external CLAUDE.md file imports?". It has two options:

- "No, disable external imports" - selected by default.
- "Yes, allow external imports".

Do not press Enter straight away. Press the down arrow to select "Yes, allow external imports". Then press Enter.

A decline is silent and permanent for that folder. The dialog does not come back, and nothing warns you that the PI did not load. The answer is stored per project, and the Claude Code docs give no reset step. To see the dialog again, start Claude Code from a fresh copy of the folder (tested). Advanced, untested: the answer is held in Claude Code's own file `~/.claude.json`, in that project's entry, as `hasClaudeMdExternalIncludesApproved` and `hasClaudeMdExternalIncludesWarningShown`; set both to `false` to be asked again. Close Claude Code first, and keep a copy of the file.

### Check that the PI loaded

1. Run `/context`. Under the memory files, look for `PI.md` and the Project Instructions file, not only your own CLAUDE file. (Untested: whether imported files are listed there. Step 2 is the sure check.)
2. Ask: "Which DataWizard Project Instructions version are you running, and from which file did you load it?" A good answer names the version in `VERSION.md` and a real file path.

Do this check after every new setup. A declined dialog shows up only here.

### Cowork users

Cowork loads the PI from Project settings, where you paste it. Do not put the pointer in `~/.claude/CLAUDE.md`. Cowork skips a user-scope import that points outside the session folder. Whether the pasted PI plus an import in the same folder loads the PI twice is untested.

### AGENTS.md repos

In a repo that uses only `AGENTS.md`, a new `CLAUDE.local.md` stops `AGENTS.md` from loading. The exception: the Claude Code "Project instructions" setting loads both. Check this before you add `CLAUDE.local.md` to such a repo. A repo with its own `AGENTS.md` is outside DataWizard; see the Scope section of the PI.

### Two home-folder lines

A vault-root `CLAUDE.md` and a repo `CLAUDE.md` can both declare a home folder. The file closer to the launch folder is read last. The repo template from the project-guidelines skill says "home folder for this repo", so the reader can see which line applies.

### Obsidian sidebar plugins

Obsidian sidebar plugins (which run Claude Code inside Obsidian) usually start Claude Code at the vault root (untested). Use the vault-root `CLAUDE.md` route for them. Whether they read `CLAUDE.local.md` is untested.

### Several worktrees

A gitignored `CLAUDE.local.md` exists only in the worktree where you made it. Make one in each worktree. The Claude Code docs suggest an import from `~/.claude/` for people with several worktrees. Do not use that route if you also use Cowork (see "Cowork users").

---

## Upstream Operator Note

The Seed maintainer (whoever publishes the Seed to GitHub) does NOT run auto-sync. Their local Seed is the upstream source -- running `update_seed.sh` / `update_seed.ps1` would overwrite local edits with the last push to GitHub. This guide's install/update automation is for downstream operators only.

**The scripts enforce this.** A `seed_role` row containing `upstream` in the vault's `Vault Config.md` (untracked, user-specific) makes both scripts refuse to sync or install auto-sync on that machine (exit 3, logged). The maintainer should carry that row; downstream operators should not.

**Diagnostic corollary.** On an upstream machine there is no launchd/Task Scheduler job and no `Seed Sync Log.md` - by design, not by defect. The clone stays current by *pushing* (`git log` shows push-side auto-sync commits). Before reading a missing sync log as "auto-sync never ran," check `seed_role` in `Vault Config.md`; a Weave review note recommended installing auto-sync on the maintainer's own machine before this was caught (Weave, 2026-09).

**Announcement norm.** After each Seed push, the maintainer posts a one-line announcement to the operator/team channel: the new `seed:` / `project_instructions:` versions and whether operators must re-paste Project Instructions. This is the push-side counterpart to the local-only version check instances run at orientation -- without it, operators have no signal that a new Seed shipped (both the zip and npx caches update silently). With auto-sync installed, downstream Seeds pick up a push within a day on their own -- the announcement still matters for PI re-pastes, which no script can do for the user.
