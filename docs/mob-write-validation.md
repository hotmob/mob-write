# Mob Write candidate validation

The current **0.4.0-rc.4** candidate has its own [validation record](rc4-validation.md), including revised writing rules, twelve synthetic teaching cases, independent behavior trials, remaining failures, and source/package/install verification. The evidence below is preserved for its original versions.

## Preserved single-entry candidate: 0.4.0-rc.3

The rc.3 candidate installed only `mob-write` and produced only `mob-write-chatgpt-skill.zip` and `mob-write-plugin.zip`. The three former entrypoint sources and alias packages were removed from that candidate; historical commits, releases and evaluations were retained. Its canonical writing bytes and entry hash were unchanged from rc.2, so the earlier writing comparisons remain evidence for that method, rather than a new writing trial of the packaging change.

All **48 automated checks** passed locally. The checks cover one entry in every package and fresh install, private-path protection, old receipt verification and public backups, changes made during backup, and a late first-install failure that removes only this attempt's unchanged public files. Retired-entry `.gitignore` files remain to protect private data at its original path. Fresh failure cleanup does not read or remove private or unknown data. Updating an existing canonical installation is not a full transaction; keep its prior public version for recovery.

Separate isolated trials exported the actual rc.1 commit `7a1f8b47052639b03a0261c5e68c685a48f2b86a` and rc.2 commit `46a741c6d0651486e308a83851c6fa4570514dba`, installed each with its original installer, and upgraded each to rc.3. Both ended with one active `mob-write` entry. All retired public files and receipts matched their backups byte for byte, a synthetic private marker stayed at its old path, and a second installation succeeded without creating aliases. These trials inspected no real profile and made no external delivery. [Single-entry results](../tests/results/mob-write-single-entry.json) record the scope and limitations.

## Preserved 0.4.0-rc.2 evidence

Candidate version: **0.4.0-rc.2**. The entry SHA-256 is `1af74beb06b7717b20e4df23867f65a93989c059021cbab8220d98a59f473635`; offline canonical content hash is `bd097c9b594ee6b306ac9b49b0868d7d74482a434bffd52f28a2f59eab79ec92`. Source, package files, fresh installation and the upgraded installation were compared separately and agree. This is a review candidate, not a formal release.

## Installation and naming

All **42 automated checks** passed locally. They cover four entry layouts, the known technical pointer, current and legacy plugin identities, deterministic packages, isolated fresh installation and explicit old-receipt migration, refusal of unknown/edited/conflicting installs, and private-path protection. Both legacy plugin ZIP names contain identical bytes; their generated manifest retains `mob-social-writing`, while the new plugin uses `mob-write`.

A frozen export of the actual prior commit `7a1f8b47052639b03a0261c5e68c685a48f2b86a` and its original installer created an rc.1 managed installation. The current installer upgraded it to rc.2, verified the former public hashes and handed over receipts. A deliberately synthetic private marker remained under `wordaim/.local`, and no private directory was moved to the new canonical. This is separate from synthetic receipt unit tests; neither test inspected an actual personal profile.

The default offline build bundles no full reference corpus. The optional full build was also executed and hash-verified: it includes the same 40 pinned licensed public records. Skill structure validation passed for the four source entries and four isolated installed entries. These results do not establish ChatGPT account upload or plugin-directory publication.

[Repository rename evidence](../tests/results/repository-rename.json) records the same repository ID before and after renaming, retained PR 2, old repository/PR/CI web redirects and successful resolution of the old git URL. The repository remains public, with its history and MIT license.

## Actual writing and reads

[The final-name eight-request suite](../tests/results/mob-write-writing.json) contains unchanged synthetic inputs, verbatim outputs, per-case applied references and file hashes. Applicable sources were opened before drafting and reused within the suite; the listed paths do not mean every source was reopened for every case. The independent writer checked the entry fingerprint; the parent verification separately matched the package and installation version.

This suite separated Chinese review from English delivery, kept technical limits and profile scope, advised omission of the no-change update, preserved the exact supplied command and quotations, and kept stars/downloads distinct from unknown use. Case 4 contains 84 total Unicode characters; case 7 changes only paragraph separators. The email uses “by Thursday” for the supplied Chinese deadline, which can include Thursday rather than strictly precede it. That nuance requires review before an actual send.

[Fresh host probes](../tests/results/mob-write-host.json) record both successful loading and failures:

- An implicit work-task request located and read `mob-write` without a supplied skill-file path. The draft used English for the recipient and Chinese for review. It nevertheless drafted the unchanged progress update and also read social references. The email narrowed interface review to API review.
- Explicit `$wordaim` opened the compatibility entry, then the new canonical and relevant social references.
- Selecting the retained old test directory first opened only its old references; this did not verify the entry. A follow-up explicitly read and hashed the old entry, confirming rc.1 without overwriting either installation. This is a directory/session return, not a supported in-place downgrade.

The observed no-change behavior differs between the suite and the host batch. Minimum-context loading, precise deadline translation and consistent use of the communication decision therefore remain work to improve. Discovery and file identity passing are not evidence that every writing rule was followed.

## What this evidence cannot show

The preserved [WordAim comparison](evaluation.md) remains historical; its names, hashes and outputs were not rewritten as a Mob Write rerun. Current checks are synthetic, small and model/context-dependent, with no new control arm or statistical quality measure. They do not prove general improvement, reliable triggering across clients, recipient understanding, real action or adoption.

There was no message sending, global skill change, private sample publication, telemetry, account migration or formal release. The [roadmap](roadmap.md) leaves real-task feedback, repeated and other-host testing, and the observed execution gaps open. CI and its downloadable candidate are verified separately on the pushed commit.
