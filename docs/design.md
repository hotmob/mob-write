# Design and name

WordAim combines the existing Chinese writing method and social adapter without making a new knowledge platform. The useful outcome is copy suited to a purpose and recipient with accurate facts. Fewer useless updates, correct recipient language, and preserved uncertainty are observable criteria; an attractive folder tree is not.

## One owner per method

```text
SKILL.md                         wordaim: discovery, purpose, factual boundaries, routing
agents/openai.yaml               one implicit writing entry
references/
  chinese.md                     Chinese expression
  social.md + reply-moves.md      social decisions and attributed examples
  work.md                        updates, requests, recipient needs
  technical-document.md          formal structure and formatting
  profile.md                     optional voice selection; no real profile included
  learning.md                    optional local sample tools
  chatgpt.md                     environment limits
  sources.md                     provenance and license decisions
chinese-writing/                 thin explicit compatibility entry
compat/mob-social-writing/       thin explicit compatibility entry
scripts/                        corpus, public packaging, explicit-target installer
tests/                          boundary tests and synthetic writing fixtures
```

The root carries constraints that matter in every relevant writing task. References carry only scene-specific detail. Trigger descriptions tell an agent what to read before drafting; they are method instructions, not runtime enforcement. Current user requirements and applicable host constraints precede personal preferences. Supplied project state or evidence is loaded only when a claim depends on it.

Private profiles are optional data under a private local path, not a public scene or assumed author identity. Public construction uses an allowlist with symlink checks. Generated package copies are byte-checked; no second authored rule set is maintained.

## Discovery failure criteria

Test whether the right source was actually read, whether required constraints were omitted, and how much unrelated material was loaded. At task start, scope change, and pre-delivery, recheck the applicable scene, recipient language, and evidence. Missing files and conflicting versions are visible limitations. A host catalog that omits a readable skill must be reported separately from source routing.

No global index, daemon, telemetry, or cross-project private-data collection is introduced. Other projects can reuse these principles without adopting this directory tree. This repository contains no private cross-project design report or user cases.

## Name and continuity

Recommended name: **WordAim**, seven letters, word + aim. Folder/frontmatter/invocation are `wordaim`. The repository address remains `hotmob/mob-social-writing`, and the old explicit names remain compatibility entries. A later rename or removal needs a concrete migration decision.

Independent name search on 2026-10-05 found no exact GitHub repository name `wordaim`; one near-match was [wordaiml.com](https://github.com/johnnypeck/wordaiml.com). The author's namespace had no match. This supports the candidate, not trademark clearance or universal uniqueness.

Alternatives: DraftAim had no GitHub name result but search may autocorrect it; Write Usefully also had no GitHub name result but overlaps [Paul Graham's article title](https://paulgraham.com/useful.html). Reader-first and useful-writing already have related repositories, so they were not selected. No `skill-` prefix is necessary.
