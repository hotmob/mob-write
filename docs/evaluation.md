# Writing comparison for 0.4.0-rc.1

> Historical WordAim candidate evidence. Names, outputs and fingerprints below are preserved as recorded; they are not a rerun under Mob Write. See [Mob Write validation](mob-write-validation.md) for the current candidate.

Most drafts produced without the additional writing skill already preserved the checked language and factual boundaries. The clearest observed change was the progress-update case: WordAim recommended skipping a routine group message with no new information or coordination need. The other cases mainly showed preserved behavior or wording differences.

This is one manual comparison of eight synthetic requests, with one recorded output per request in each arm. It does not establish a causal effect, general improvement, repeated-run reliability, or performance for real users.

The complete requests, verbatim outputs, case criteria, review observations, read manifest, and exact-text checks are in [writing-comparison.json](../tests/results/writing-comparison.json). The shared requests are in [writing-cases.json](../tests/fixtures/writing-cases.json). All people, exchanges, products, and numbers in those requests are fictional.

## What was compared

The control loaded no additional writing skill. It still had host, system, and developer instructions and the model's existing capabilities. Calling it an instruction-free baseline would be inaccurate.

The WordAim trial manually opened the isolated installed entry and applicable references. Its entry fingerprint was SHA-256 `28a6c658b224e5b4308b37178e681a56274ee878efc70d3cd9c9010a69fce809`, matching the requested `0.4.0-rc.1` entry. The fixture fingerprint was `f35f5ba408c80d017290ffffef4a7aca57d1d5e0d79ce86a0aafe81be4109493`.

Neither arm sent or published any text. The recorded outputs are drafts or recommendations, copied without editorial repair. The review checked the supplied text against each request; no recipient response, delivery, command execution, or product-performance test was measured. Exact model identifiers and sampling settings were not recorded in the public trial records, so this comparison cannot rule out model or context effects.

## Observations

| Case | Checked behavior | Without an additional writing skill | With WordAim |
| --- | --- | --- | --- |
| 1 | Chinese review notes, English recipient, deadlines and commitments | Preserves the language separation and schedule boundaries | Preserves the same boundaries; moves the scope question earlier |
| 2 | No invented progress; decide whether an unchanged routine update is useful | Produces an accurate message repeating the unchanged status | Recommends skipping the update because nothing changed and no coordination is needed |
| 3 | Small informal trial does not prove universal approval or efficiency | Keeps three friends, mixed feedback, and no efficiency test | Keeps the same evidence scale and limitation |
| 4 | Technical result stays within the tested conditions | Keeps conditions, median times, and all four untested areas | Keeps the same scope and limitations, with different unit spacing |
| 5 | Natural English gratitude without a question or execution claim | Gives a short thank-you for clarification | Gives a shorter thank-you with the same boundaries |
| 6 | Current formal request overrides an inline fictional profile | Keeps the conditional test date and avoids jokes | Keeps the same condition and test-versus-release distinction |
| 7 | Only paragraph separators may change | Preserves the supplied quotes and command exactly | Produces the identical permitted transformation |
| 8 | Stars and downloads do not establish users or product value | Keeps the metrics separate from unknown use | Preserves the same distinction and uncertainty |

Case 2 provides a concrete difference in the communication decision. The control output was:

> 今天继续思考方案，状态与昨日一致。没有新增文档、测试或决策，暂无需要大家配合的事项。

The WordAim output was:

> 建议今天暂不发送日进展：与昨天相比没有变化，也没有需要群内协调的事项。

Both avoid invented progress. Only the second output advises against this routine broadcast. The fixture does not establish a mandatory reporting policy, and this trial does not cover a user who explicitly insists on sending. Skipping a message remains advice; the record does not prove that a message was actually withheld.

The other cases should not be presented as eight newly acquired abilities. For example, both arms kept the final email in English, preserved the limited technical result, and avoided turning downloads into active users. Both exact-quotation outputs were identical.

Two checks can be reproduced directly from the stored text:

- Case 4 contains 51 Han characters in the control output and 45 in the WordAim output; total character counts are 76 and 83 respectively. Both meet the request for at most 100 Chinese characters, without needing to equate shorter text with better text.
- Case 7 equals the supplied text after replacing only the two inter-item separators with paragraph breaks in both arms. Quote marks, `...`, English case, `--dry-run=false`, and `./out_v1.csv` remain unchanged.

## Actual reading scope

The manifest normalizes installed paths to `skills/wordaim/...`; this identifies the installed skill without exposing a machine path. In the repository, that prefix corresponds to the project root. Fixture paths remain source-relative.

Every WordAim case used `skills/wordaim/SKILL.md` and the request fixture. The reported case-specific references were:

| Cases | References applied |
| --- | --- |
| 1, 2 | `chinese.md`, `work.md` |
| 3, 8 | `chinese.md`, `social.md` |
| 4, 7 | `chinese.md`, `technical-document.md` |
| 5 | `social.md`, `reply-moves.md` |
| 6 | `chinese.md`, `work.md`, `profile.md` |

These are recorded applied sources, not a claim that each file was newly opened for every case. The trial notes state that each source was opened and hashed before drafting, then reused when applicable. The JSON contains the normalized fingerprints.

The trial did not load sample-learning, ChatGPT-access, provenance, or licensing guidance for these supplied writing requests. It did not quote external examples. No personal profile file was loaded: case 6 provides its fictional profile inline. No extra reading, external actions, installed-file changes, memory changes, or global changes were reported. This limited trial does not test those unloaded workflows or replace the separate licensing review.

## Host discovery

Host discovery was checked separately from this writing comparison. [host-discovery.json](../tests/results/host-discovery.json) records two fresh, read-only sessions using Codex CLI 0.145.0 and a project-local isolated installation. WordAim was found in the catalog and its entry was read in both sessions. Both drafts kept the synthetic recipient's text in English and did not claim the setting had been tested.

The first session also read an enabled legacy global Chinese skill. In the second, command-scoped `skills.config` overrides disabled the legacy paths without changing global configuration or installations. That session avoided the old writing rules but still read `work.md` in addition to the social references for a short reply. The observed routing therefore does not guarantee the minimum possible context.

This supports discovery and actual reads in the tested CLI configurations. It does not establish automatic triggering in every client or account, or successful coexistence with all older installations. The host record has one synthetic reply per configuration and no exact served-model identification. See [migration guidance](migration.md) for handling existing discovery paths. Raw host logs are not part of the public report.

## Limits of this evidence

The inputs are synthetic, the review is manual, and each arm has only one output per case. There is no measured recipient understanding, decision quality, real action, long-term use, or statistically supported quality gain. The control's host instructions may already encourage several of the checked behaviors.

No stars, downloads, installations, active users, retention, or real user counts were measured. No telemetry or third-party promotion was added. Case 8 tests how to describe fictional metrics; its numbers are not project-growth evidence.

Package construction and isolated installation checks are separate evidence. They can show that a bundle installs or that expected files are present; they cannot substitute for writing-value evaluation. This report covers only the drafts and recommendations stored in the public comparison record.
