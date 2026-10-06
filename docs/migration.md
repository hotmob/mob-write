# Installation and migration

The root is canonical `mob-write`. Three explicit aliases preserve `wordaim`, `chinese-writing` and `mob-social-writing` calls. New work uses `$mob-write`.

## New isolated installation

```sh
git clone --branch feat/unified-writing https://github.com/hotmob/mob-write.git mob-write-source
cd mob-write-source
git rev-parse HEAD
python3 scripts/install.py --skills-dir /path/to/test-project/.agents/skills
```

The target is explicit; no global installation is selected. Use a host-discoverable directory and a fresh session. A receipt proves file identity, not discovery. Current main and release v0.2.0 retain earlier behavior until a separate merge/release decision.

## Upgrade the earlier managed WordAim candidate

The installer recognizes only its current Mob Write receipt or the explicitly supported earlier WordAim receipt from this same renamed project. It verifies every managed public file and all targets before writing. An unrelated source, unknown clone, changed public file, unsafe path or conflicting receipts causes refusal.

For an unchanged installer-managed candidate, pull this branch and run the same explicit-target installer. The old `wordaim/` public method becomes a thin alias, and `mob-write/` contains the canonical rules. New receipts use `.mob-write-install.json`; supported old receipts use `.wordaim-install.json`. Receipts record public identities and version, not private content or machine paths.

Only previously managed, verified public files are retired. Unknown files and private `.local/` remain at their old paths, without reading or migration. A profile at `wordaim/.local/` is not moved to `mob-write/.local/`; select its original path explicitly if it is authorized and applicable. Compatibility covers calls, archive names, legacy plugin identity and the known Chinese technical pointer, rather than every old internal reference or corpus-tool path.

## Manual clones and private data

Old manually cloned or symlinked installations are not silently adopted as managed copies. Keep them intact and test in an empty isolated directory. Review their public edits and discovery paths before choosing a migration. The installer does not inspect private profiles, change global skills or modify account-operation skills.

## Return to a known version

Keep an older isolated test installation intact before trying an upgrade. Return by selecting that older directory in a test session, then verify the method actually read. Checking out an old commit and running its old installer over a newer target is not a supported automatic downgrade: it may reject the newer receipt or leave another canonical skill enabled. Do not delete receipts or overwrite private data to force it.

## Repository and plugin continuity

The repository was renamed in place; update clones with:

```sh
git remote set-url origin https://github.com/hotmob/mob-write.git
```

Old repository and PR links and old git fetch paths are checked separately. Do not reuse `hotmob/mob-social-writing` for another repository, because that would remove its redirects. GitHub documents rename exceptions for project sites and repository-hosted Actions; this repository had neither when checked. See [GitHub rename guidance](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

The new plugin uses identity `mob-write`. The two legacy plugin archive names preserve identity `mob-social-writing`, using a generated manifest and identical writing content. A host may treat plugin identities as separate installs; choose one and verify its catalog rather than assuming installing the new identity upgrades the old host entry.

## Coexisting legacy skills

A project-local install does not disable old global methods. The historical WordAim host trial read an enabled old Chinese skill too. Command-scoped `skills.config` overrides removed that overlap without editing global configuration; that trial still loaded an extra work reference for a social reply. The current Mob Write trial is recorded separately in [validation](mob-write-validation.md). Other clients may handle coexistence differently.

For Codex, use the actual discovered legacy path with a per-skill `enabled = false` override in a test session; do not copy machine paths from someone else. See [OpenAI's skills documentation](https://developers.openai.com/codex/skills) and [configuration reference](https://developers.openai.com/codex/config-reference).

## Four separate version checks

Verify source commit, package manifest and hashes, installation receipt, and actual host reads. A successful build, saved directory or release label alone does not establish a usable host installation. Report missing discovery, conflicting sources, omitted guidance and excess reads.
