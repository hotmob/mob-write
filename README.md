<h1 align="center">Mob Write</h1>

<p align="center"><strong>Write with purpose, for your reader.</strong><br>A writing skill in the Mob Skills series.</p>

<p align="center">
  <a href="https://github.com/hotmob/mob-write/releases/latest"><img src="https://img.shields.io/github/v/release/hotmob/mob-write" alt="Latest GitHub release"></a>
  <a href="https://github.com/hotmob/mob-write/actions/workflows/check.yml"><img src="https://github.com/hotmob/mob-write/actions/workflows/check.yml/badge.svg?branch=main&amp;event=push" alt="Tests and package build on main"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/hotmob/mob-write" alt="MIT license"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

Draft and review messages, social replies, articles, and technical explanations. Start with what the recipient needs, preserve the supplied facts, and load only the guidance the task needs. Chinese review notes and the recipient's delivery language are separate decisions.

**Series:** Mob Skills · **Project:** Mob Write · **Call:** `$mob-write` · **Repository:** [`hotmob/mob-write`](https://github.com/hotmob/mob-write)

[Examples](#what-changes-in-a-draft) · [Install](#install-v040) · [Usage](#use-it) · [Private voice](#optional-private-voice) · [Validation](#validation-and-contributions) · [Sources](#sources-and-license)

## What changes in a draft

These are **synthetic teaching examples**, not measured model outputs or private conversations.

| Supplied facts and purpose | Problematic draft | Useful draft |
| --- | --- | --- |
| Someone explained a configuration option. You understand but have not run it; thank them in English. | “Worked perfectly, thanks!” | “Thanks, that clears it up!” |
| Export tests passed; delivery has not happened. Tell a teammate the actual status. | “The export feature has been delivered.” | “Export tests passed; it hasn't been delivered yet.” |
| On one 16 GB machine, eight serial tests of a 100,000-row CSV had median times of 70 ms in the old version and 52 ms in the new version. Concurrency and production were not tested. | “The new version is faster in every scenario.” | “On this 16 GB machine, eight serial tests of the same 100,000-row CSV reduced median time from 70 ms to 52 ms. Concurrency and production remain untested.” |

A thank-you can be enough. A technical conclusion may need its evidence and limitations. Shorter is useful only when the necessary meaning survives.

There are **12 synthetic worked examples**: [work communication](examples/work.md) (4), [social writing](examples/social.md) (2), and [documents and explanations](examples/documents.md) (6). Each includes the problem, an improved draft, a reason, and a boundary. Scene guidance and teaching explanations are mainly in Chinese; drafts can use the recipient's language. Examples teach decisions, not sentences to imitate.

## Install v0.4.0

Use the pinned [v0.4.0 release](https://github.com/hotmob/mob-write/releases/tag/v0.4.0). **Python 3.10+** is needed for installation and packaging. The writing instructions are Markdown; the optional tools make no model or social-account calls.

```sh
git clone --branch v0.4.0 --depth 1 https://github.com/hotmob/mob-write.git mob-write-source
cd mob-write-source
git rev-parse HEAD
python3 scripts/install.py --skills-dir /path/to/test-project/.agents/skills
```

Choose an empty, project-local skills directory your client actually discovers for the first trial. The example path is suitable for a Codex project; other clients have their own discovery locations. Opening the checkout alone does not register a skill.

A fresh installation writes only `mob-write/`, including a receipt with the version and public file hashes. In a **fresh client session**, confirm the host discovers Mob Write and reads the installed version. Installation success does not prove discovery; a running session can retain an earlier catalog.

**Upgrading an older installation?** Read [migration and recovery](docs/migration.md). Managed, unchanged same-source installs can upgrade. The installer has no global default, preserves private and unknown files, and refuses unknown installations, edited public files, and symlinked installation targets or managed public paths. Retiring verified managed legacy entries also writes an explicitly chosen backup and removes their managed public files. Existing canonical upgrades are not full I/O transactions; keep a recoverable backup. Manual clones and host-managed plugins need their own migration procedure.

`$wordaim`, `$chinese-writing`, and `$mob-social-writing` have no forwarding entries or packages in v0.4.0; older entries enabled elsewhere may still be discovered. Historical releases remain available. **v0.2.0** contains the earlier social-writing method, without the unified entry or private bundle tools.

## Use it

Give the intended reader, purpose, and source facts or original text:

> Use $mob-write to reply to this English comment. We haven't met. A brief thank-you is enough: “That option only applies to the CLI; for the API, set it in the request body.” I understand, but haven't tested it.

> Use $mob-write to draft an email for an English recipient, with a separate Chinese review gloss. The interface check is planned to finish on Thursday; security review must wait until a colleague returns next Monday. Ask whether Friday's deadline covers only the interface check. Add no delivery commitment.

> Use $mob-write to judge whether this group update is useful: today has no new documents, tests, decisions, or coordination needs compared with yesterday, and no routine reporting requirement. If it adds nothing, explain that.

Usually one usable draft is enough. A review can briefly explain material changes. Evaluate each part of a combined request separately; each keeps its own facts, recipient, and communication decision.

| Request | How to use the skill |
| --- | --- |
| Draft, revise, or review a message, post, article, or explanation | Supply the recipient, purpose, and source material. |
| Review an English draft in Chinese | Keep review notes separate from English copy for the recipient. |
| Judge an unchanged routine update | Recommend waiting when it adds nothing and no reporting requirement is supplied; preserve a supplied obligation to report. |
| Adapt writing to an industry or project | Keep that project's evidence, terminology, and workflow rules. |
| Translate with specified specialist requirements, preserve an exact quotation, or change only layout | Follow the requested fidelity and edit scope. |
| Ask a general question, query a file, or run a command | A Chinese prompt alone does not call for this writing method. |
| Send or publish copy | Use a separately authorized tool or workflow; drafting grants no sending permission. |

## Small core, guidance on demand

[`SKILL.md`](SKILL.md) is the sole entry. It owns purpose, recipient language, factual boundaries, and routing. Select a scene by purpose; use the core alone when no scene fits. Load Chinese expression or optional voice only when relevant.

```text
SKILL.md       purpose, reader, facts, routing
references/    work, social, documents; Chinese and optional overlays
examples/      worked cases for optional calibration
assets/        blank profile and synthetic sample templates
scripts/       explicit-target installation, packaging, local corpus tools
tests/         structural checks, fixtures, recorded behavior results
docs/          design, migration, evaluation, project principles
```

A friendly work email still uses work guidance. A short English reply needs Chinese expression rules only if Chinese prose is also requested. The skill does not load the entire directory for every task. See [design](docs/design.md) for source ownership and routing.

## Optional private voice

The public default has no private personal voice. Keep a replaceable [private bundle](assets/private-bundle-template/README.md) **outside the installation**, with its owner and scope, profile, feedback notes, and corpus. For an installed skill:

```sh
python3 /path/to/skills/mob-write/scripts/private_data.py init --data-dir /path/to/private/my-writing --owner 'Your name' --scope 'Personal developer replies; formal reports excluded'
# Fill profile.md and import your samples with corpus.py --data-dir DIR add --file FILE.
python3 /path/to/skills/mob-write/scripts/private_data.py connect --data-dir /path/to/private/my-writing
python3 /path/to/skills/mob-write/scripts/private_data.py show
```

`connect` writes only the ignored `.local/config.json` pointer. To switch authors, initialize another private directory and connect it; data are not merged. The installed corpus tool selects the connection unless `--data-dir` is explicit. Public upgrades preserve the connection without reading private data.

Before loading voice material, a writing task checks the bundle's scope. Without a connection, generic writing works normally. Preferences cannot change facts, recipient language, or authorization. Connection, host discovery, source loading, and writing effect need separate checks; connecting data does not prove the model learned your voice. See [personal voice guidance](references/profile.md).

## Packages and ChatGPT

Download packages from the [release](https://github.com/hotmob/mob-write/releases/tag/v0.4.0), or build both from the same checkout **offline by default** into an empty directory:

```sh
python3 scripts/build_chatgpt.py --output dist
```

| Artifact | Intended use |
| --- | --- |
| `mob-write-chatgpt-skill.zip` | A host that supports skill-file upload. |
| `mob-write-plugin.zip` | A host that supports skills-only plugin import; identity `mob-write`. |
| `package-manifest.json` | Version, public file identities, and SHA-256 values. |

These are the only generated ZIPs. [ChatGPT notes](chatgpt/START-HERE.md) explain file access and persistence limits; a built package does not establish account installation or directory publication.

The builder's public path allowlist excludes private directories, drafts, feedback, credentials, and personal paths. Four attributed external snippets and their licenses are included. Keep private material out of public source files too: the allowlist is not a private-text detector. The separate pinned 40-text public corpus is optional with `--with-reference`, or `--reference-file FILE` for an exact downloaded copy. It is external reference material, separate from the synthetic teaching library; it does not supply your experiences. See [sources](references/sources.md) and [local learning](references/learning.md).

## Validation and contributions

```sh
python3 -m unittest discover -s tests -v
```

**v0.4.0 passed 55 structural checks** covering package boundaries, source/package identity, isolated installation and upgrade, bundle selection, author switching, and connected-data preservation. The badge above reports the current main workflow. Structural checks do not establish writing quality; behavior trials separately record actual outputs and source reads.

| Behavior evidence | What it establishes and what remains limited |
| --- | --- |
| [rc.4 comparison](docs/rc4-validation.md) | Initial ten-case comparison and targeted confirmations, with observed risks. These results were not rerun or relabeled as rc.5. |
| [rc.5 fidelity check](docs/rc5-validation.md) | Two earlier ambiguous requests and four new explicit-boundary requests. One candidate run retained broader “interface” wording, but date wording stayed ambiguous. Both methods met the four new requests' criteria; repeatable improvement and risk resolution remain unproven. |
| [rc.6 bundle check](docs/rc6-validation.md) | Three fresh isolated sessions, generic writing, two fictional profiles, and a formal-report scope exclusion. Reads matched installed sources and drafts showed limited profile differences. One draft omitted an explicit status; another inferred ongoing progress from an incomplete state. No corpus or feedback notes were read, so this proves neither sample learning nor complete factual fidelity. |

No behavior trial opened the teaching library, so its benefit remains unmeasured. Small synthetic trials do not establish reliable behavior, general improvement, reader understanding, real-task usefulness, or compatibility across every model and host.

Contributions should include the original request, scene, observed problem, public-safe example, and boundary. Use synthetic or authorized public material; keep private writing, profiles, and conversations out of issues and patches. See the [constitution](docs/constitution.md), [evaluation](docs/evaluation.md), and [roadmap](docs/roadmap.md).

Stars show interest; download counts can include repeats. Neither measures installed or active users. The project adds no telemetry and promises no engagement growth or AI-detection result.

## Sources and license

| Skill and repository | What informed Mob Write | Bundled material |
| --- | --- | --- |
| Meng To's [write-like-meng-on-x](https://github.com/MengTo/Skills/blob/321c769739b823de5eb94eb3a52aa1974fe783a2/agent-skills/codex/write-like-meng-on-x/SKILL.md) · [MengTo/Skills](https://github.com/MengTo/Skills) | Replies versus posts, authored examples, current wording, and generated drafts as weak voice evidence. | Adapted methods, four attributed excerpts, and an optional pinned public corpus, under MIT. |
| Siqi Chen's [Humanizer](https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md) · [blader/humanizer](https://github.com/blader/humanizer) | Preserve facts and voice, notice repetitive structures, and make a light final edit. | Adapted editing guidance, under MIT. |
| rabden's [X Social Media Manager](https://github.com/rabden/X-twitter-social-manager-skill) | Preserve exact replies for later review. | Method reference only; no upstream text is bundled. The reviewed reply archive was an empty template. |

For structure, we consulted the locally installed Codex **skill-creator** and its UI-metadata reference: a small entry, on-demand resources, and `agents/openai.yaml`. The consulted local copy was not pinned to an upstream revision. This was an authoring reference, not a source of writing examples or bundled code. The historical [openai/skills catalog](https://github.com/openai/skills) now directs authors to [OpenAI Plugins](https://github.com/openai/plugins).

The historical **chinese-writing** Skill came from a user-supplied local guide and entered [this repository's history](https://github.com/hotmob/mob-write/tree/f878474706754aed0878efc562d3a93c9557a919/chinese-writing); no separate public upstream was established. **mob-social-writing** is this project's former name. Private profiles, drafts, and conversations are excluded.

Reviewed revisions and adaptation limits are in [source notes](references/sources.md). Copied material retains [third-party notices and licenses](THIRD_PARTY_NOTICES.md). Projects considered only for naming are not content sources. No upstream endorsement is implied.

**License:** [MIT](LICENSE), with full notices for Meng To's public examples and Siqi Chen's editing guidance. External samples supply wording evidence, not your biography or endorsements. Added third-party material needs its own authorization.
