# Mob Write

**Write with purpose, for your reader.**

A lightweight writing skill for messages, social replies, articles, and technical explanations. Decide what the reader needs, preserve the facts, and produce copy they can understand, judge, act on, or naturally respond to.

先看目的、读者与事实，再决定写什么、怎样写；中文审稿与收件人语言分别判断。

**Project:** Mob Write · **Call:** `$mob-write` · **Repository:** [`hotmob/mob-write`](https://github.com/hotmob/mob-write)

Mob Write helps with the decisions behind the wording: whether an update adds useful information, whether a claim is supported, which language reaches the recipient, and how much detail they need. A thank-you can be enough. A technical conclusion may need its limitations. Shorter is not always better.

## What changes in a draft

These are **synthetic teaching examples**, not measured outputs or private conversations.

| Supplied facts and purpose | Problematic draft | Useful draft |
| --- | --- | --- |
| Someone explained a configuration option. You understand but have not run it; thank them in English. | “Worked perfectly, thanks!” | “Thanks, that clears it up!” |
| Export tests passed; delivery has not happened. Tell a teammate the actual status. | “导出功能已完成交付。” | “导出功能测试已通过，尚未交付。” |
| On one 16 GB machine, eight serial tests of a 100,000-row CSV had median times of 70 ms in the old version and 52 ms in the new version. Concurrency and production were not tested. | “新版在所有场景都更快。” | “在这台 16 GB 机器上，对同一份 10 万行 CSV 做八次串行测试，中位耗时从 70 ms 降至 52 ms；并发和生产环境尚未测。” |

The first preserves the difference between understanding and verifying. The second reports a result without upgrading it to delivery. The third keeps the evidence beside the conclusion, even though it takes more words. Other tasks may call for a different tone, length, or result.

There are **12 synthetic worked examples**, each with a problem, an improved draft, an explanation, and a boundary:

- [Work communication](examples/work.md): four examples covering updates, requests, evidence, and commitments.
- [Social writing](examples/social.md): two examples of natural replies without invented experience or forced questions.
- [Documents and explanations](examples/documents.md): six examples covering reader needs, factual limits, language, and editing scope.

Scene guidance and teaching explanations are mainly in Chinese; this does not restrict the draft’s delivery language. The examples teach decisions, not sentences to imitate. For a no-change update with no reporting requirement, the useful result may be a recommendation to wait. An explicit reporting requirement still matters. Chinese instructions do not make an English recipient's draft Chinese. Exact-format work and specialized translation keep their own contracts.

## When to use it

| Request | Fit |
| --- | --- |
| Draft, revise, or review a message, email, post, reply, article, or technical explanation | Use `$mob-write` with the recipient, purpose, and source material. |
| Review an English recipient draft in Chinese | Keep the Chinese review gloss separate from the English copy. |
| Adapt writing to a project's industry or document requirements | Keep the project's evidence and workflow rules; Mob Write supplies expression guidance alongside them. |
| Ask a general question, query a file, or run a command | A Chinese prompt alone does not call for the writing method. |
| Translate under a specialized terminology or fidelity contract | Follow that contract; apply wording guidance only within the permitted scope. |
| Send or publish the draft | Use an independently authorized tool or workflow. This skill drafts and reviews text. |

## Install the candidate

This branch is **0.4.0-rc.5**, a review candidate in [draft PR #2](https://github.com/hotmob/mob-write/pull/2). The published **v0.2.0** release contains the earlier social-writing method. Cloning main or downloading v0.2.0 does not install this candidate. Merge and formal release are separate decisions.

Python 3.10+ is needed for installation and packaging. The writing instructions are Markdown; the optional Python tools make no model or social-account calls.

```sh
git clone --branch feat/unified-writing https://github.com/hotmob/mob-write.git mob-write-source
cd mob-write-source
git rev-parse HEAD
python3 scripts/install.py --skills-dir /path/to/test-project/.agents/skills
```

For a first trial, choose an empty, project-local skills directory your client actually discovers. The path above is suitable for a Codex project; other clients have their own discovery locations. Opening the source checkout alone does not register a skill.

The installer writes only `mob-write/`, with a receipt recording the version and public file hashes. In a **fresh client session**, confirm Mob Write appears and that the host reads this installed version. A successful installation does not prove automatic discovery; an already running session may retain its earlier catalog.

**Old names have been retired:** `$wordaim`, `$chinese-writing`, and `$mob-social-writing` have no forwarding entries or packages in this candidate. Older installations enabled elsewhere can still be discovered. For upgrades, recoverable backups, manual clones, symlinks, and host-managed plugins, follow [migration](docs/migration.md). The installer has no global target default, preserves private and unknown files, and refuses unknown or edited installations. Historical releases remain available.

## Call it

Give the intended reader, what the draft should accomplish, and the facts or original text:

> Use $mob-write to reply to this English comment. We haven't met. A brief thank-you is enough: “That option only applies to the CLI; for the API, set it in the request body.” I understand, but haven't tested it.

> 使用 $mob-write 给英文收件人写邮件，先给中文释义，再给英文正文。接口核对计划周四完成；安全审查需等同事下周一回来。请对方确认周五截止是否只指接口核对，不新增交付承诺。

> 使用 $mob-write 判断这条群进度是否值得发：今天没有新文档、测试、决定或协作需求，与昨天相同，也没有例行汇报要求。如果没有信息增量，说明即可。

Usually one usable draft is enough. A review can explain material changes briefly. For a combined request, each deliverable keeps its own purpose, recipient, facts, and communication decision.

## Small core, guidance on demand

`SKILL.md` is the single entry and owns purpose, reader language, factual boundaries, and routing. For each deliverable, select a scene when it fits the purpose; otherwise the core is enough. Add only necessary guidance:

```text
SKILL.md                  purpose, reader, facts, routing
references/               work, social, documents; Chinese and optional overlays
examples/                 worked cases, opened when calibration is useful
assets/                   blank profile and sample templates
scripts/                  explicit-target installer, public packaging, local corpus tools
tests/                    structural checks, writing fixtures, recorded behavior results
docs/                     design, migration, evaluation, project principles
```

A work email does not need social rules just because it is friendly. A short English reply does not need Chinese expression rules unless Chinese prose is also requested. Examples and local learning tools are optional; the method does not load the entire directory for every task. See [design](docs/design.md) for source ownership and routing.

The public default has no private personal voice. A [blank profile template](assets/voice-profile.example.md) is available; a personal profile applies only when selected or accurately scoped. Your samples and feedback stay local. Profile preferences cannot change facts, recipient language, or authorization.

## Packages and ChatGPT

Build both public packages from the same checkout, **offline by default**, into an empty output directory:

```sh
python3 scripts/build_chatgpt.py --output dist
```

- `mob-write-chatgpt-skill.zip`: for a host that supports skill-file upload.
- `mob-write-plugin.zip`: for a host that supports skills-only plugin import; identity `mob-write`.

`package-manifest.json` records the version and SHA-256 values. These are the only generated ZIPs. [ChatGPT notes](chatgpt/START-HERE.md) cover host access and persistence limits; a built ZIP does not establish account installation or directory publication.

The builder uses a public allowlist and excludes private profiles, drafts, feedback, credentials, and private paths. Four attributed external snippets and their licenses remain included. The separate pinned 40-text public corpus is optional with `--with-reference`, or `--reference-file FILE` for an exact downloaded copy; it is not the synthetic teaching library. See [sources](references/sources.md) and [optional local learning](references/learning.md).

## Verify and contribute

```sh
python3 -m unittest discover -s tests -v
```

All **48 structural checks** pass. They cover public package boundaries, source/package identity, and isolated installation and upgrade. **Passing them does not establish writing quality.** Model trials separately record actual outputs and source reads. [rc.4 validation](docs/rc4-validation.md) preserves the initial ten-case comparison, targeted confirmations, and observed risks; its results were not rerun or rewritten as rc.5 results.

The [bounded rc.5 fidelity check](docs/rc5-validation.md) compares the two earlier ambiguous requests and four new explicit-boundary requests. The candidate retained the broader “interface” wording in one work run, but its date wording remained ambiguous. Both methods met the four new requests' criteria. The clearer rules therefore do not establish repeatable improvement or resolution of either risk. No trial opened the teaching library, so an example-library benefit remains unmeasured. Small synthetic trials do not prove reliable behavior, general improvement, reader understanding, or real-task usefulness.

Contributions should show the original request, scene, observed problem, public-safe example, and applicable boundary. Use synthetic or authorized public material; keep private writing, profiles, and conversations out of issues and patches. Project principles are in the [constitution](docs/constitution.md); planned work is in the [roadmap](docs/roadmap.md).

Stars show interest; download counts include possible repeats. Neither measures installed or active users. The project adds no telemetry and promises no engagement growth or AI-detection result.

## Acknowledgements / 参考来源

These Skills informed the writing method:

| Skill and GitHub repository | What we borrowed | Use in Mob Write |
| --- | --- | --- |
| Meng To's **write-like-meng-on-x** — [MengTo/Skills](https://github.com/MengTo/Skills) | Distinguish replies from standalone posts, learn from authored examples, preserve current wording, and treat generated drafts as weak voice evidence. | Adapted methods; four attributed short excerpts and an optional pinned public corpus, under MIT. |
| Siqi Chen's **Humanizer** — [blader/humanizer](https://github.com/blader/humanizer) | Preserve facts and the author's voice, notice repetitive structures, and make a light final edit. | Adapted editing guidance, under MIT. |
| rabden's **X Social Media Manager** — [rabden/X-twitter-social-manager-skill](https://github.com/rabden/X-twitter-social-manager-skill) | Preserve exact replies as records for later review. | Reference only; no upstream text is bundled. Its reviewed reply archive was an empty template. |

For structure, we consulted the locally installed Codex **skill-creator** and its UI-metadata reference: a small entry, supporting resources loaded as needed, and `agents/openai.yaml`. Its [public counterpart in openai/skills](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) documents these conventions; the consulted local copy was not pinned to an upstream revision. This was an authoring reference, not a source of writing examples or bundled code.

The historical **chinese-writing** Skill came from a user-supplied local guide and was added to [this repository's history](https://github.com/hotmob/mob-write/tree/f878474706754aed0878efc562d3a93c9557a919/chinese-writing); no separate public upstream was established. **mob-social-writing** is this project's former name, not an independent upstream. Private profiles, drafts, and conversations are excluded.

Reviewed versions and adaptation limits are in [source notes](references/sources.md); copied material retains [third-party attribution and licenses](THIRD_PARTY_NOTICES.md). Projects considered only for naming are not content sources. No upstream endorsement is implied.

## License

[MIT](LICENSE). Meng To's public examples and Siqi Chen's editing guidance retain [their notices and licenses](THIRD_PARTY_NOTICES.md). External samples show expression; they do not supply your experiences or endorsements. Added third-party material needs its own authorization.
