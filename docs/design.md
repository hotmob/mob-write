# Mob Write design

**Mob Write / `mob-write`** is the project and canonical invocation. The existing `hotmob/mob-social-writing` repository was renamed to [`hotmob/mob-write`](https://github.com/hotmob/mob-write) in place. It retains history, PRs and issues; no second canonical repository is created. Mob is the project identity, not an assumed private voice.

The result should be copy suited to a purpose and recipient with accurate facts. Fewer useless updates, correct recipient language and preserved uncertainty are observable criteria. The [constitution](constitution.md) sets the principles; the [four-stage roadmap](roadmap.md) sets the current scope.

## One owner per method

```text
SKILL.md                         mob-write: purpose, recipient, facts, routing
agents/openai.yaml               one recommended implicit writing entry
references/
  chinese.md                     Chinese expression
  social.md + reply-moves.md      social decisions and attributed examples
  work.md                        useful updates, requests and decisions
  technical-document.md          formal structure and formatting
  profile.md                     optional scoped voice; no real profile
  learning.md                     optional local sample tools
  chatgpt.md                      environment limits
  sources.md                      provenance and licensing
scripts/                         corpus, public packaging, explicit-target installer
docs/                            maintainer principles, migration and evidence
tests/                           boundary tests and synthetic writing fixtures
```

The root owns constraints that apply across writing tasks. References add only applicable scene detail. Read applicable sources before drafting and reuse current sources within a task; do not load the whole directory. At task start, scope changes and pre-delivery, check the method, recipient constraints and claim-dependent evidence. These are instructions for judgment, not runtime enforcement.

Private profiles are optional data, not a public default scene or identity. Public builds use an allowlist and reject unsafe paths and symlinks. Generated copies are byte-checked; writing rules and the `mob-write` plugin manifest each have one authored source. The public method does not absorb a project's business process, evidence rules or governance: those remain in the adopting project's instructions and apply alongside writing guidance.

## Names and continuity

The 0.4.0-rc.3 candidate exposes only `$mob-write`. There are no `$wordaim`, `$chinese-writing` or `$mob-social-writing` forwarding entries. Chinese expression and technical-document guidance remain references within the canonical method. Adopting projects must change their active writing routes to `mob-write` while retaining their own business and governance constraints.

The plugin identity is `mob-write`. The builder produces only `mob-write-chatgpt-skill.zip` and `mob-write-plugin.zip` and refuses retired alias archive names in its output directory. Use an empty output directory to keep builds separate. This breaks old invocation and package names. [Migration](migration.md) describes verified public-file backups, retirement of managed old entries, and the separate handling needed for manual clones or host-managed plugins. Historical releases and evaluation records are retained; they describe their own versions, not the current installed method.

The name removes the former social-only scope without adding a `skill-` prefix. The target repository name was checked before renaming; this is not a claim of trademark clearance. WordAim's earlier trial records retain their historical names and hashes.

## Keep it lightweight

No index, daemon, telemetry, cross-project private-data collection or account operator is introduced. New structure or tools need an observed writing or loading problem. Constitution and roadmap are maintainer documents; ordinary writing does not load them as another mandatory rule layer.
