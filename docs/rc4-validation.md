# Mob Write 0.4.0-rc.4 validation

The first comparison found **no material failure in either method across ten synthetic cases**. A simple social probe read three files with rc.3 and two with the initial rc.4 candidate. The compound work probe improved the main communication decision but still generated an unnecessary conditional update. These observations do not establish a better pass rate, universal fidelity, or reliable elimination of empty broadcasts.

This document separates the original held-out comparison from later targeted confirmation after a rule revision. Independent review found no listed material failure in the three new confirmation cases, with one minor fidelity note. The repeated work probe still narrowed “interface” to “API.” A review candidate is not a merge or formal release.

Public records: [requests and constraints](../tests/fixtures/rc4-writing-cases.json) and [outputs, reads, review, and version evidence](../tests/results/mob-write-rc4.json). The worked examples in `examples/` are teaching material; these evaluation requests are not part of that library or the installed writing context.

## What was compared

| Arm | Method identity |
| --- | --- |
| Baseline | Previous installed method, **0.4.0-rc.3**, commit `1fcffc78edd73305899f926b1f74626e94988ef5`; entry SHA-256 `1af74beb06b7717b20e4df23867f65a93989c059021cbab8220d98a59f473635` |
| Initial candidate | Frozen public **0.4.0-rc.4** files; entry SHA-256 `26b6910beeb79a65255e05ef84276e0b1ac2d67d23834153b27df31e0929ee5a`; offline public-content SHA-256 `61913b4107c74ce8dbdb0c4f42f8f95dc7f8ff49294af58a1a8a7da5d3f92bfe` |
| Revised final candidate | Entry SHA-256 `fd7b18ba5e861c8377bb3ef192a1c59d0d7b4c67178616b18d0f8954b8c9d328`; offline public-content SHA-256 `52a39fca80f12fc9879e206bcb51d331bfad8cd95153048baa035ad0138415c3`. Published rc.4 source: [commit 034ab3d](https://github.com/hotmob/mob-write/commit/034ab3d0e0adc1bd127d893f508376acded72152). Later results identify this method separately from the initial freeze. |

Both arms ran through the native Codex host in isolated project-local installations and fresh ephemeral, read-only sessions. The baseline is a previous skill, **not a model without writing guidance**. Each arm had two five-case batches and two routing probes: four sessions per arm. Cases within a batch share context; they are not ten independent repeated experiments.

The independent case author prepared synthetic requests without reading the evolving public examples or sharing case text with the implementation and example authors. Independent review examined source, actual outputs, and completed tool events. It evaluated material constraints rather than matching an expected sentence. People, organizations, dates, and business situations in the fixtures are synthetic; no private profile, real customer fact, or conversation was used.

## Original held-out comparison

| Set | Coverage | Baseline material failures | Initial candidate material failures |
| --- | --- | --- | --- |
| Batch A: h01–h05 | Social reply plus empty update; English delivery with Chinese review; complete technical conditions; the same facts for different readers; faithful translation | 0 of 5 | 0 of 5 |
| Batch B: h06–h10 | Natural social assent; industry prototype boundaries; localization with intact product behavior; exact text plus empty update; useful update with a real decision need | 0 of 5 | 0 of 5 |

Both methods preserved the supplied factual and editing constraints in these ten cases, including recipient language, uncertainty, conditions, negation, exact text, and the distinction between a prototype and demonstrated gains. Both omitted the empty updates when those case requests explicitly required a communication judgment.

Passing the material criteria does not make all drafts equally useful. In h04, the candidate's manager conclusion was less concrete than the baseline's reminder about classification errors and missing timing evidence. In h10, the candidate preserved the dependency between deciding to extend access and filing an application more explicitly. These differences support reviewing individual drafts, not a claim of uniform improvement.

Batch B was reserved until the implementation and teaching examples were fixed for the initial freeze. It remains part of this original comparison. It is **not** the later three-session confirmation of revised rules.

## Routing probes and actual reads

Completed command events were reviewed separately from the model's self-reported `applied_references`. Paths below are relative to each isolated installed method.

| Trial | Baseline opened | Initial candidate opened |
| --- | --- | --- |
| Batch A | `SKILL.md`, `chinese.md`, `social.md`, `work.md`, `technical-document.md`, `reply-moves.md` | `SKILL.md`, `work.md`, `social.md`, `technical-document.md`, `chinese.md` |
| Batch B | `SKILL.md`, `chinese.md`, `social.md`, `work.md`, `reply-moves.md` | `SKILL.md`, `social.md`, `work.md`, `chinese.md` |
| Compound work probe | `SKILL.md`, `chinese.md`, `work.md` | `SKILL.md`, `work.md`, `chinese.md` |
| Simple social probe | `SKILL.md`, `social.md`, `reply-moves.md` | `SKILL.md`, `social.md` |

All reference filenames in this table are under `references/`. The simple English thank-you was identical in both arms: “Thanks, that makes sense!” The candidate opened two files rather than three, omitting the optional `reply-moves.md`. This is an observed reduction in one supplemental read, not a measured latency or quality improvement.

The candidate opened **none of the worked-example files in any of its four initial sessions**. The trials therefore cannot attribute any behavioral difference to the added example library. They also do not show that an agent will open an example when calibration is needed.

The compound work probe was only **partially improved**:

- The baseline narrowed “interface” to “API,” rendered “before Wednesday” as “by Wednesday” without clarification, and supplied a sendable no-change group update. A later limitation recommending omission did not undo that generated draft.
- The candidate preserved “interface” and “before Wednesday” and recommended not posting. It nevertheless supplied a fallback group draft for a reporting obligation absent from the request. The fallback was conditional and did not invent progress; it remains unnecessary content rather than complete suppression of the empty update.

The observed traces show rule reads before substantive drafts and no reads of another project's files, private profiles, credentials, neighboring fixtures or results, or network/browser content. They show no sending, publishing, deployment, or file mutation within the writing sessions. These are trace observations for these runs, not runtime enforcement guarantees. Catalog fields are model reports; opening and hashing the selected entry does not independently enumerate the host's entire skill catalog.

## Rule revision and targeted confirmation

After the original probe exposed the conditional fallback, a small rule revision was checked with **three new independent follow-up sessions**. This is targeted confirmation, not a rerun of the ten-case comparison, and does not replace the original work-probe result.

A separate development regression reused the original work-probe prompt with the revised rules. It omitted the fallback update and retained “before Wednesday,” but again narrowed “interface” to “API.” This known-prompt regression is not an unseen confirmation case. It leaves term-scope fidelity unresolved even though the communication decision improved.

| Follow-up | Status |
| --- | --- |
| c01: useful email plus unchanged group update | No listed material failure: useful email supplied; empty group update omitted without a hypothetical fallback |
| c02: explicitly mandatory check-in despite unchanged state | No listed material failure: mandatory check-in supplied; one minor inference described below |
| c03: English delivery, Chinese review, approved deadline and exact timezone | No listed material failure: already-approved status, English delivery and exact UTC+03:00 preserved |

Independent review checked outputs and completed tool events. All four final sessions opened `SKILL.md`, `references/work.md`, and `references/chinese.md` before drafting; none opened worked examples or showed private-source reads or real delivery. The targeted fallback was absent in the new compound request and repeated probe. These observations do not establish reliable suppression or example calibration. Confirmations use their own fresh contexts; their counts are separate from the original ten cases and two probes. The earlier ten-case results are not a rerun of the final source, so a final-source “13/13” claim would be unsupported.

The c02 draft turned a completion date absent from the supplied material into a statement that the date was not yet clear. That is a minor fidelity risk: missing source information does not prove the underlying date is unsettled. Keep this nuance visible rather than treating a lack of material failure as perfect fidelity.

## Final candidate and structural verification

| Check | Status |
| --- | --- |
| Final rc.4 source commit | [034ab3d](https://github.com/hotmob/mob-write/commit/034ab3d0e0adc1bd127d893f508376acded72152); later PR heads may contain newer versions |
| Revised entry and offline public-content SHA-256 | Recorded above and in [distribution evidence](../tests/results/mob-write-rc4-distribution.json) |
| Final structural test count and result | **48 checks passed** locally |
| Source/package/install identity and isolated upgrade | Source, both ZIPs, fresh isolated installation, actual rc.3-to-rc.4 upgrade, and repeated installation match; a synthetic private marker remained unchanged |
| CI on the pushed rc.4 commit | [Successful matching Check](https://github.com/hotmob/mob-write/actions/runs/37502184430); downloaded packages matched the local and fresh remote builds |

Structural checks cover package boundaries, relative references, single-entry generation, public-file identity, private-path protection, and recoverable managed installation/upgrade. These properties are different evidence from the writing trials. A package or installation passing does not establish automatic discovery, actual rule application, recipient comprehension, or writing quality.

## Limits

- There was one run per arm for each initial session. The harness did not explicitly pin a model version or random seed; no statistical reliability or significance claim is supported.
- The synthetic requests state constraints unusually clearly. Ambiguous real requests may still prompt unnecessary text, altered nuance, or the wrong amount of detail.
- Deadline preservation in these examples does not settle every translation ambiguity. User-supplied terminology, fidelity requirements, and domain instructions still govern the task.
- The initial work probe retained a conditional empty-update draft. Its result stays in the record even if the separate follow-up succeeds.
- The revised development regression still narrowed “interface” to “API.” The mandatory-check-in confirmation also made a minor inference from a missing completion date. Do not describe term scope or factual nuance as fully resolved.
- Trial-level file opens do not prove per-case application, minimal routing across all hosts, or future example use. No examples were opened in the initial candidate trials.
- Real reader understanding, action, adoption, global installation, and hot updates to already running sessions were not measured. No real external message was sent.

Present the result as a small public review candidate with clearer source organization, explicit synthetic teaching material, and bounded observations. Keep remaining failures and nuance visible; stars, downloads, passing package tests, and this small comparison do not measure actual users or universal writing improvement.
