# Mob Write 0.4.0-rc.5 fidelity validation

This bounded candidate clarifies two existing core passages: preserve the source's level of specificity, and distinguish a gap in supplied information from an absent or undecided state in the world. It adds no worked examples and does not change the scene methods. Both methods passed all four new diagnostic/control cases. The candidate used more conservative terminology in one known probe, but the ambiguous date phrase remained. **The results do not establish stable improvement or resolution of both risks.**

The evaluation examines evidence boundaries in context. “API” is not automatically an incorrect translation of “接口,” and “尚未明确” is not automatically a false claim about the world's schedule. An unsupported increase in specificity or a claim beyond the writer's evidence is the risk to examine. The earlier ambiguous requests are not benchmarks with a uniquely established technical meaning or planning state.

The [rc.4 record](rc4-validation.md), its original requests, and its raw outputs remain intact. This document does not overwrite those results or retrospectively score them using new diagnostic facts. Public rc.5 records contain the [requests and constraints](../tests/fixtures/rc5-fidelity-cases.json) and [outputs, source identities, observed reads, and independent review](../tests/results/mob-write-rc5-fidelity.json).

## Bounded method change

The two revised passages ask the writer to:

- Use supplied definitions and terminology, preserving their specificity. Familiar associations alone do not justify selecting a narrower technical meaning.
- Separate missing source information from an actual absent or undecided state. Omit immaterial gaps from the copy, flag material gaps in review or ask, and preserve uncertainty explicitly supplied by the source.

These constraints still permit a specific API definition and an explicitly confirmed unknown completion date. The reverse controls test those possibilities so that caution does not erase facts, approved states, or useful technical detail. No new diagnostic or regression case is added to the teaching library.

## What the earlier observations establish

The original work request used “接口” without defining its implementation type. In a software context, an API interpretation can be plausible. The concern is that the English draft selected a more specific term without establishing that meaning in the supplied or authorized context. Treat this as a specificity risk; the word choice by itself does not prove an erroneous translation.

The original mandatory check-in gave no completion date in the material. “尚未明确” can be read as the sender having no clear date to report, or as a claim that the real schedule is undecided. Independent review treated it as a minor, ambiguous fidelity risk. It did not establish the actual schedule or make one interpretation the only permissible truth.

Fresh rc.4 known-case runs produced different observations:

| Known request | Fresh baseline observation | Interpretation |
| --- | --- | --- |
| Compound work email and unchanged update | The draft again used “API portion” and “API review,” while retaining “before Wednesday” and recommending no group update without a fallback. | The unverified-specificity risk recurred. The earlier communication-decision fix remained present in this run. |
| Mandatory unchanged check-in with no supplied completion date | The draft said “审核完成日期尚未给出.” | The earlier “尚未明确” wording did not recur. This wording is closer to the supplied-information boundary, although its meaning still needs the full context. |

These are known-prompt reproductions. They are not newly unseen confirmation, and one different output does not establish that the earlier minor risk is reliably absent. The old raw outputs stay in the record.

## Method identity

| Arm | Frozen method |
| --- | --- |
| Baseline | **0.4.0-rc.4**, commit `034ab3d0e0adc1bd127d893f508376acded72152`; entry SHA-256 `fd7b18ba5e861c8377bb3ef192a1c59d0d7b4c67178616b18d0f8954b8c9d328`; offline public-content SHA-256 `52a39fca80f12fc9879e206bcb51d331bfad8cd95153048baa035ad0138415c3` |
| Candidate | **0.4.0-rc.5**; entry SHA-256 `9f70d982e1480572652cf27c356bcb78e5d017d72e2bdb0d4ee02c5ca117b9cf`; offline public-content SHA-256 `531fe70fe9886475463a55907f3e8586e893374856a446224a023d9cb11b7aed` |

The frozen public-file records show only `SKILL.md` changed among the installed writing files. All twelve worked examples retain their rc.4 bytes. Frozen method hashes identify the instructions tested independently of later documentation changes. Use the matching [draft PR #2 head and checks](https://github.com/hotmob/mob-write/pull/2/checks) for the source commit and CI status; building or reviewing this candidate does not establish a merge or formal release.

## Trial design

Each arm uses the same native-host protocol in an isolated project-local installation, with four fresh, read-only sessions. The baseline is the previous installed skill, not a model without a skill.

| Session | Requests | Purpose |
| --- | --- | --- |
| Known work reproduction | One earlier compound work request | Observe the ambiguous terminology risk and retain the useful no-update decision. |
| Known date reproduction | One earlier mandatory check-in request | Observe whether missing source information becomes a planning-state assertion. |
| Diagnostic batch | Two new explicit evidence-gap variants | Distinguish a generic interaction boundary from an unestablished implementation, and a missing date in the writer's material from an unknown real schedule. |
| Reverse-control batch | Two new requests with explicit facts | Preserve a defined API-verification scope and approved date; preserve an explicitly confirmed in-progress review and genuinely undetermined completion date. |

That is six request outputs across four sessions per arm. The two requests in each batch share context. The two diagnostic variants and two reverse controls are separately authored synthetic inputs; neither group is the original known request with a new name. Their additional facts must not be imported into the earlier ambiguous requests to prove a retrospective error.

Review should judge actual meaning against each request's evidence layers. A lexical check for “API” or “未定” would not establish fidelity. It must also examine retained scope, completed or approved status, explicit uncertainty, editing limits, recipient language, actual method reads, and whether useful outputs were omitted through excessive caution.

## Independently reviewed results

| Evidence group | Baseline | Candidate | Independent assessment |
| --- | --- | --- | --- |
| Known work reproduction | Used “API portion/API review”; no-update decision retained | Used “interface-related items/interface verification”; timing, dependency, and no-update decision retained | More conservative in this run; no other material failure identified. The original technical referent remains ambiguous. |
| Known date reproduction | Provided the mandatory check-in and used “尚未给出” | Provided the mandatory check-in and used “尚未明确”; its limitation said the date was not supplied | No invented date or result commitment. Minor ambiguity persisted; no stable improvement shown. |
| Two explicit diagnostic variants | 0 of 2 material failures | 0 of 2 material failures | Both preserved the established interface-boundary scope and the writer's information gap without asserting unestablished implementation or real scheduling state. |
| Two reverse controls | 0 of 2 material failures | 0 of 2 material failures | Both retained defined API verification, completed/approved states and exact time zone, plus explicitly confirmed in-progress review and genuinely undecided completion date. |

Both arms passed the four clear diagnostic/control cases, so this comparison shows no pass-rate advantage for rc.5. These cases provide bounded evidence that the clarification retained useful specifics and explicit uncertainty without an observed reverse-risk regression. They do not retroactively establish a unique truth for the two original prompts.

## Actual reads and source verification

Independent review inspected completed tool events separately from model-reported references. All eight sessions opened and hashed their selected installed core before substantive drafts; all entry hashes matched the corresponding freeze. Each arm's 22 installed public files also matched its frozen public-file record.

| Session | Baseline opened | Candidate opened |
| --- | --- | --- |
| Known work reproduction | `SKILL.md`, `work.md`, `chinese.md` | Same three method files |
| Known date reproduction | `SKILL.md`, `work.md`, `chinese.md` | Same three method files |
| Diagnostic batch | `SKILL.md`, `work.md`, `technical-document.md`, `chinese.md` | `SKILL.md`, `work.md`, `chinese.md` |
| Reverse-control batch | `SKILL.md`, `technical-document.md`, `work.md`, `chinese.md` | Same four method files |

Reference filenames in the table are under `references/`. The candidate diagnostic session omitted one reference; the other sessions opened the same method-file sets. No session opened worked examples, so the results cannot be credited to the unchanged teaching library.

The observed traces showed no private-profile, credential, other-project, neighboring-fixture/result, network, or browser reads, and no sending, deployment, test execution, or file mutation inside the writing sessions. These observations are limited to completed tool events. They do not prove per-case cognitive application, runtime enforcement, complete host-catalog enumeration, or unobserved behavior. The batch cases shared context.

Do not count six outputs as six independent sessions or merge these counts into rc.4's ten-case comparison. This bounded round ends here; it does not continue revising prompts or rules until known requests produce preferred wording.

## Distribution and final checks

| Check | Status |
| --- | --- |
| Final structural test count and result | **48 checks passed** locally |
| Source, package, and isolated-install identity | Frozen behavior installation and both ZIPs match all 22 public source files |
| Same-project upgrade and repeated installation | Actual rc.4 installation upgraded to rc.5 with matching public files; a synthetic private marker was preserved, and repeat installation succeeded |
| Public evidence export and privacy review | Separate public fixtures/results preserve synthetic requests, outputs, relative reads, and independent assessment; no private profile or business source is included |
| Pushed source commit and matching CI | Inspect the matching [PR #2 checks](https://github.com/hotmob/mob-write/pull/2/checks), comparing the installed entry fingerprint with the tested candidate above |

Structural checks and package identity establish implementation properties, not writing quality or reliable application of the revised guidance. No global skill, second-brain route, WorkOS installation, real private profile, or external account is changed by these trials. No real message is sent.

[Distribution evidence](../tests/results/mob-write-rc5-distribution.json) records the exact method and package fingerprints and the isolated upgrade checks.

## Limits

- This is a small, targeted comparison of two existing risks and possible overcorrection. It does not repeat the full rc.4 suite or establish broader quality improvement.
- The original requests leave context unresolved. Plausible interpretations must be recorded instead of presenting one invented ground truth as the benchmark.
- The explicit diagnostic variants deliberately make evidence gaps clearer. A successful diagnostic output would not settle the meaning of every ambiguous real request.
- One run per session and shared batch contexts do not establish statistical reliability, a failure rate, or consistent behavior across models and hosts. The harness did not explicitly pin a model version or fixed random seed; there was no no-skill control or repeated matched sampling.
- The candidate's more conservative terminology is one paired observation. Its date wording still carries the earlier ambiguity; the rule edit has not demonstrated stable resolution of either risk.
- Real recipient comprehension, action, adoption, account installation, and updates to already running sessions are outside this bounded evaluation.
