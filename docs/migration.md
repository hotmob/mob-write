# Installation and migration

The source root is the canonical `wordaim` skill. `chinese-writing/` and `compat/mob-social-writing/` contain only compatibility entries. Generated standalone alias archives include one nested WordAim; plugin and directory installations use one sibling WordAim.

## First installation

Choose the host's real skills path. For an isolated project-local Codex test:

```sh
python3 scripts/install.py --skills-dir /path/to/test-project/.agents/skills
```

The explicit path is required. There is no default that silently changes a global installation. Restart/refresh the client if it snapshots skills, then check its catalog and perform an actual read. A receipt confirms files and version, not host discovery.

## Upgrade an installer-managed copy

Keep the source checkout on this candidate branch until a release/merge is separately decided:

```sh
git pull --ff-only
python3 scripts/install.py --skills-dir /path/to/client/skills
```

The installer verifies its previous source identity and public file hashes before replacing anything. It preserves local private directories without reading them. If a public file was changed or a target is not recognized as its own installation, it stops with the affected path. Review those edits before updating; do not bypass the check by copying over the old directory.

## Existing manual clone or another source

The old README recommended cloning the repository into `mob-social-writing` and linking `chinese-writing`. Those directories may contain edits and private profiles. They are not treated as managed copies automatically.

1. Keep the existing directories intact. Back them up using your normal private backup process.
2. Install the candidate into an empty isolated directory and verify its version and behavior.
3. Select any legacy private profile explicitly when testing personal voice. Do not automatically copy, inspect, upload, or commit it.
4. After reviewing client discovery paths and old references, choose which installation should serve future calls. Replace an old installation only under your own migration decision.

The candidate does not remove global old skills or edit account-operation skills. Existing filesystem references continue to point to their original installations until that separate migration is performed.

## Compatibility and source links

Both old explicit invocation names route to `wordaim`. Compatibility entries are excluded from implicit invocation so discovery has one recommended writing method. A missing canonical entry is reported, rather than recreating old rules. Conflicting candidates must be compared and reported.

The old source path `chinese-writing/references/technical-document.md` is a pointer to the new canonical technical reference. It contains no duplicate formatting rules. The repository and plugin identity stay `mob-social-writing`; the recommended display/invocation is WordAim/`wordaim`.

## Coexisting legacy skills

Installing the candidate does not disable an older skill in another discovery directory. In a fresh Codex CLI 0.145.0 trial, the project-local WordAim was discovered, but an enabled global legacy Chinese skill was also read. A second read-only trial used command-scoped `skills.config` overrides to disable the discovered legacy paths and read only the new writing method. No global configuration or installation was changed. It still loaded one additional work reference for a short social reply; routing does not guarantee the minimum possible context.

Codex documents per-skill `enabled = false` entries under `skills.config` and command-line `-c key=value` overrides. Use the actual legacy skill path from your host's catalog when testing, rather than copying another machine's path. Other clients may handle coexistence differently. Verify their actual reads before switching an active installation. See [OpenAI's skill configuration](https://developers.openai.com/codex/skills) and [the configuration reference](https://developers.openai.com/codex/config-reference).

## Version evidence

Keep four distinct checks: source revision, package hashes, installation receipt, and actual host read. Do not call a release tag, build success, or saved directory a verified host install. New-session automatic discovery may be unavailable to a test host; report that limit rather than assuming it.
