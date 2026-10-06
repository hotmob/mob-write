# Mob Write design

**Mob Write / `mob-write`** is the project and single invocation. The existing repository was renamed in place to [`hotmob/mob-write`](https://github.com/hotmob/mob-write), retaining its history, PRs, and issues. Mob is the project name; it does not establish a default private voice.

The method helps decide what deserves to be communicated and how a reader can use it. Observable criteria include supported claims, useful information, appropriate recipient language, and enough detail for the intended purpose. The [constitution](constitution.md) sets the principles; the [roadmap](roadmap.md) distinguishes completed work from open evidence.

## One method, one entry

```text
SKILL.md                         purpose, recipient, facts, per-deliverable routing
agents/openai.yaml               one discoverable writing entry
references/
  work.md                        emails, requests, updates, decisions
  social.md                      replies, posts, ordinary social exchange
  technical-document.md          explanations, formal documents, formatting
  chinese.md                     Chinese prose and Chinese review glosses
  profile.md                     optional scoped voice, without a real profile
  learning.md                     optional local sample tools
  chatgpt.md                      optional host access and persistence guidance
  reply-moves.md                  attributed social snippets
  sources.md                     provenance and licensing
examples/
  work.md                        four synthetic worked cases
  social.md                      two synthetic worked cases
  documents.md                   six synthetic worked cases
assets/                          blank local-data templates
scripts/                         installer, public packaging, corpus tools
tests/                           structural checks, fixtures, behavior evidence
docs/                            design, migration, evaluation, project principles
```

The root owns the shared decisions and routing. Scene references add the relevant methods without duplicating the root. Each deliverable selects a fitting scene, or uses only the core if none fits; Chinese expression, a supplied profile, or host-specific file handling are added only when they apply. A combined task evaluates each output separately: a useful email does not make a no-change progress post useful, and a friendly work message does not automatically become a social reply.

Read applicable rules before drafting and reuse current sources within the task. Worked examples are opened when a relevant judgment needs calibration, not as a default reading list. They illustrate an error, a useful revision, its reason, and a boundary. Their sentences are not templates or the user's biography. No folder of examples should be loaded just because it exists.

Instructions can guide an agent's choices, but this Markdown architecture does not enforce source loading, communication decisions, or a sending gate at runtime. Discovery, actual reads, and resulting drafts need separate verification.

## Preserve the adopting project's constraints

Recipient language and review language are separate. The method preserves supplied facts, conditions, uncertainty, exact text, and commitment strength. Technical and translation contracts still govern edits within their scope. Brevity is useful only when the recipient retains the information needed to understand, judge, or act.

An adopting project's business process, authoritative sources, audience, acceptance steps, confidentiality rules, and governance remain in that project's instructions. They apply alongside expression guidance; Mob Write does not publish or absorb those private workflows. Drafting does not authorize sending, publishing, changing accounts, or writing personal memory.

Private profiles are optional local data. Public builds use an allowlist, reject unsafe paths and symlinks, and byte-check generated copies. Writing rules and the `mob-write` plugin manifest each have one authored source. Installed and packaged copies are outputs, not additional places to edit the method.

## Examples and tests serve different purposes

The 12 worked examples are synthetic public teaching material. Attributed external snippets remain separate, with their source and license limits. Neither kind establishes the author's experiences or measured effectiveness.

Structural tests check package and installation properties: one entry, valid references, public-file identity, private-path boundaries, refusal of unknown edits, and recoverable managed retirement. Model trials inspect actual outputs and source reads, including held-out variants outside the teaching library. Fixtures, expected judgments, and recorded results do not belong in the default writing context.

The initial ten-case rc.3/rc.4 comparison found no material failures in either arm. A simple social probe omitted an extra reference with the same suitable output. Three new follow-up requests respected their supplied constraints after a targeted rule revision; a repeated work probe still narrowed “interface” to “API”. No trial read the teaching examples. [rc.4 validation](rc4-validation.md) separates these observations, source fingerprints, and limits from [preserved earlier evidence](mob-write-validation.md); it does not claim reliable enforcement or an example-library benefit.

## Names, installation, and continuity

The **0.4.0-rc.4** candidate exposes only `$mob-write`. There are no `$wordaim`, `$chinese-writing`, or `$mob-social-writing` forwarders or alias packages. Chinese expression remains an internal reference; historical releases and evaluation records retain their original names. This change breaks old calls. Adopting projects need to update their active routes while keeping their own business and governance constraints.

The builder produces only `mob-write-chatgpt-skill.zip` and `mob-write-plugin.zip`, with plugin identity `mob-write`. Both derive from the same public source; manifests and receipts record version and file hashes. The builder refuses retired alias archive names in its output directory. Use an empty build directory to keep versions distinct.

The installer has an explicit target and no global default. It supports same-source, receipt-managed upgrades, with recoverable public-file backups for retired entries. Manual clones, symlinks, and host-managed plugins require their appropriate migration path. Preserve private data at its original location, and verify catalog and reads in a fresh session. [Migration](migration.md) describes the boundaries; no package build establishes a host installation or a formal release.

The repository and invocation names match without a `skill-` prefix. The target repository name was checked before renaming; this is not trademark clearance. Old repository redirects depend on leaving the old repository name unused.

## Keep it lightweight

No daemon, telemetry, knowledge platform, account operator, or cross-project private-data collection is introduced. New files or tools need an observed writing or loading problem. Constitution, roadmap, evaluations, and tests are maintainer material; they are not another mandatory rule layer for ordinary drafting.
