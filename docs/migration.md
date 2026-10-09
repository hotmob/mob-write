# Installation and migration

Version 0.4.0 installs only canonical `mob-write`. Former `$wordaim`, `$chinese-writing` and `$mob-social-writing` calls no longer have forwarding entries. Update active writing routes to `$mob-write`; preserve the adopting project's business, source, audience and governance constraints separately.

## New isolated installation

```sh
git clone --branch v0.4.0 --depth 1 https://github.com/hotmob/mob-write.git mob-write-source
cd mob-write-source
git rev-parse HEAD
python3 scripts/install.py --skills-dir /path/to/test-project/.agents/skills
```

The target is explicit; no global installation is selected. Use an empty host-discoverable directory and a fresh session. A receipt proves file identity, not discovery. Release v0.4.0 provides this unified entry; historical v0.2.0 retains the earlier social-writing method. Building a checkout alone does not establish release publication or host discovery.

## Upgrade a supported managed candidate

The installer recognizes supported receipts from this same project, including the earlier WordAim candidate and Mob Write 0.4.0-rc.2, as well as its current receipt. Recognition checks the source identity, canonical name, receipt schema and recorded public file hashes; a version string alone is not proof. It verifies every managed public file and all targets before writing. An unrelated source, unknown clone, changed public file, unsafe path or conflicting receipts causes refusal.

When a supported receipt manages old active entries, provide an explicit backup directory outside the skills directory and outside any host discovery path:

```sh
python3 scripts/install.py \
  --skills-dir /path/to/client/skills \
  --backup-dir /path/to/migration-backups
```

The installer backs up the verified receipt-managed public files and receipt, retires those old public paths, and writes only `mob-write/` with `.mob-write-install.json`. It does not leave an old-name wrapper. An unchanged installation already containing only `mob-write` can be updated using the same explicit target without retiring old entries.

Unknown files and private `.local/` stay at their original paths without reading or migration. An old directory may remain to hold those files, but its retired `SKILL.md` must no longer be discoverable. Its existing `.gitignore` stays to protect private data at that path. A private profile at an old path is not moved into `mob-write/.local/`; select its original path explicitly only when authorized and applicable. Backups describe the retired public installation, not a complete private-data backup.

Public files and receipts are rechecked after backup and immediately before replacement or retirement. A failed first installation removes only public files successfully written by that attempt whose bytes are still unchanged, leaving private and unknown files intact. Updating an existing canonical installation is not a full transaction; a write failure may leave partial public updates. When retirement has begun, the failure report includes the verified legacy public backup path. Preserve the failed state and the previous canonical version before recovery.

## Manual clones, symlinks and host-managed plugins

The installer refuses unmanaged clones and symlinked installations. Review public edits and discovery paths, then move the old active entries to a recoverable backup outside host discovery before installing into an empty target. Keep private data intact; do not delete it or assume the installer will relocate it. Check every applicable discovery root, since a project-local installation does not disable a global skill.

For a host-managed plugin, use that host's supported uninstall/import mechanism. Importing a plugin with identity `mob-write` does not establish removal of an older plugin with identity `mob-social-writing`. Verify the host catalog in a new session. Do not edit a generated plugin cache as though it were its source.

## Return to a known version

Keep the public backup outside discovery. It contains retired entries, not a snapshot of the updated `mob-write/` directory; retain the earlier canonical public version or its exact source commit separately if a complete return is needed. To return, first move the new active entry out of discovery, then restore a complete selected older public installation and verify what the host actually reads. Restoring only old forwarders without their matching canonical method leaves unresolved routes. A complete return intentionally restores the older method and names.

There is no supported automatic downgrade by running an old installer over a newer target; it may reject the newer receipt or leave another method enabled. Do not delete receipts or overwrite private data to force it.

## Repository and packages

The repository was renamed in place; update clones with:

```sh
git remote set-url origin https://github.com/hotmob/mob-write.git
```

Old repository and PR links and old git fetch paths are checked separately. Do not reuse `hotmob/mob-social-writing` for another repository, because that would remove its redirects. GitHub documents rename exceptions for project sites and repository-hosted Actions; this repository had neither when checked. See [GitHub rename guidance](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

Current builds produce only `mob-write-chatgpt-skill.zip` and `mob-write-plugin.zip`; the plugin identity is `mob-write`. Old package names are no longer generated. The builder refuses retired alias archive names in its output directory. Move retained earlier builds to an archive location and use an empty output directory to avoid mixing versions. Old releases, source history and evaluation records are not deleted by this migration.

## Legacy discovery paths

After migration, use a fresh session and check that `mob-write` appears, that the three old names are absent from the active catalog, and that project writing routes resolve to the new method. Already running sessions may retain a prior catalog or loaded instructions; this migration does not promise a hot update.

The historical WordAim trial loaded an enabled old Chinese skill as well. Its command-scoped disabling experiment is recorded as historical evidence, not the current retirement procedure. The earlier Mob Write trial is recorded separately in [validation](mob-write-validation.md). Clients may discover skills from different locations; a successful install into one directory is not proof that no old entry exists elsewhere.

## Four separate version checks

Verify the source commit, package manifest and hashes, installation receipt, and actual host catalog and reads. A successful build, saved directory or release label alone does not establish a usable host installation. Report missing discovery, conflicting sources, omitted guidance and excess reads. Writing checks should also exercise recipient language, factual uncertainty and the adopting project's constraints; package checks alone do not establish writing value.

## Replaceable private bundle

Install the public release first. Keep a complete recoverable copy of legacy entries, including private files and symlink identities, outside host discovery before retirement. The public installer deliberately does not migrate private data. For an authorized personal migration, copy the selected legacy private directory to an independently owned private bundle outside the installation; preserve profile, notes, corpus, reference provenance, and history byte-for-byte. Add only `bundle.json` with schema=1, owner and applicable scope, then use the installed `scripts/private_data.py connect --data-dir DIR`. Do not infer approved feedback or convert external reference samples into authored samples. No missing corpus or history should be manufactured.

The binding lives in `mob-write/.local/config.json`, excluded from public hashes and packages. A public upgrade preserves it. `private_data.py init` refuses existing directories; `connect` checks metadata and file presence without reading private prose. `show` reveals local path/owner/scope, so do not paste its output into public issues. To switch authors, connect a different validated bundle; retain the previous one unchanged.

Verify private byte identities, the connected corpus selection, and a scoped writing task. Do not publish real migration records or host paths in this repository. A route in an expected file is only a proposal until the actual target is written and a fresh host discovers/loads it.
