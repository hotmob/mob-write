# Mob Write

Write with purpose, for your reader.

先看目的和读者，让文字帮助理解、判断与行动。适用于消息、邮件、社交回复、文章和技术说明，支持中文表达与英文文案的中文审稿。

**Project:** Mob Write · **Invocation:** `$mob-write` · **Repository:** [`hotmob/mob-write`](https://github.com/hotmob/mob-write). The existing repository was renamed in place, retaining its history and PRs. Former calls `$wordaim`, `$chinese-writing`, and `$mob-social-writing` remain explicit compatibility aliases. Mob Write is a project name, not a default personal voice.

Read the [project constitution](docs/constitution.md) and [four-stage roadmap](docs/roadmap.md) for the purpose, scope, acceptance criteria, and remaining work.

## Install the candidate

This branch is **0.4.0-rc.2**, a review candidate. The latest published release, **v0.2.0**, has the earlier social-writing behavior. Downloading that release or cloning main before this change is merged does not install Mob Write.

Python 3.10+ is needed for packaging and installation; writing itself uses Markdown only.

```sh
git clone --branch feat/unified-writing https://github.com/hotmob/mob-write.git mob-write-source
cd mob-write-source
git rev-parse HEAD
python3 scripts/install.py --skills-dir /path/to/client/skills
```

Use an **empty target directory** for the first trial. For a Codex project, `--skills-dir /path/to/project/.agents/skills` is a suitable project-local location. Choose the actual discoverable skill directory of your client; opening a source checkout alone does not register a skill.

The installer writes `mob-write/` plus the three compatibility directories `wordaim/`, `chinese-writing/`, and `mob-social-writing/`. Within this installed set, only Mob Write has implicit invocation enabled. The others contain thin forwarding instructions; rules live once in Mob Write. Older skills enabled elsewhere can still be loaded by the host; see [coexistence](docs/migration.md#coexisting-legacy-skills). Installation receipts record version and public file hashes. Read the result in a fresh client session and confirm that Mob Write appears; filesystem installation and automatic discovery are different checks.

For an existing installation or an upgrade, read [migration](docs/migration.md). The installer updates its own unchanged files, preserves `.local/` without reading it, and refuses unknown installations or edited public files. It has no global target default. Do not overwrite an old clone or private profile.

## Use it

Give the intended recipient, purpose, and material you already have:

> Use $mob-write to reply to this English comment. We haven't met. A brief thank-you is enough: “That option only applies to the CLI; for the API, set it in the request body.” I understand, but haven't tested it.

Example draft: **“Thanks, that clears it up!”** It does not claim the fix worked.

> 使用 $mob-write 帮我给英文收件人写邮件。请先给中文释义，再给英文正文。接口部分周四前能核对；安全审查需等同事下周一回来。请对方确认周五截止是否只指接口核对。

Mob Write separates the Chinese review gloss from the English recipient draft. User interface language alone does not establish recipient language.

> 使用 $mob-write 改这条群进度：今天没有新文档、测试、决定或协作需求，与昨天相同。

Mob Write can recommend waiting instead of polishing a message with no new information. If you still need wording, it follows that scope and keeps the facts accurate.

At task start, a scope change, and before externally addressed copy is handed off, the method checks applicable guidance and recipient constraints. These Markdown instructions help judgment; they are not an enforced sending gate and do not grant account permissions.

## What loads

`SKILL.md` owns purpose, recipient language, factual boundaries, and routing. The agent then reads only applicable references:

- `references/chinese.md`: Chinese wording and rhythm.
- `references/social.md` and reply examples: natural social responses.
- `references/work.md`: useful updates, requests, and decisions.
- `references/technical-document.md`: formal structure and formatting.
- `references/profile.md`: optional, narrowly scoped personal voice.
- Learning and ChatGPT environment notes only when those tasks need them.

The public default assumes no personal identity. A private profile is used only when explicitly selected or when a user-provided profile's stated scope applies. A blank [profile template](assets/voice-profile.example.md) is supplied; your own writing and feedback stay local. [Architecture and naming](docs/design.md) explains the source ownership and name search.

## Packages and ChatGPT

Build from this same checkout, **offline by default**:

```sh
python3 scripts/build_chatgpt.py --output dist
```

Use `mob-write-chatgpt-skill.zip` for a supported skill-file upload and `mob-write-plugin.zip` for a supported skills-only plugin import. Old standalone archive names contain a thin alias and nested Mob Write. `wordaim-plugin.zip` and `mob-social-writing-plugin.zip` retain the actual old plugin identity `mob-social-writing`; their generated manifest differs from the new plugin's `mob-write` identity. Every package uses the same public writing source, and `package-manifest.json` lists version, file identities, and SHA-256 values.

The package builder reads a public allowlist. It excludes personal profiles, drafts, feedback, credentials, and private paths. The four existing attributed snippets and licenses remain included. The full pinned 40-text public reference corpus is optional:

```sh
python3 scripts/build_chatgpt.py --output dist --with-reference
```

That explicit option downloads a hash-verified public file. `--reference-file FILE` accepts an already downloaded copy of exactly that pinned source. Core drafting does not need it. [ChatGPT notes](chatgpt/START-HERE.md) explain file access and persistence limits. Upload availability depends on the host and workspace; a ZIP build does not prove account installation or directory publication.

For optional local corpus commands, read [learning](references/learning.md). The tools use Python standard library and make no model or social-account calls.

## Verify and contribute

```sh
python3 -m unittest discover -s tests -v
```

CI tests the public package boundary and isolated installation/upgrade and supplies candidate artifacts. Writing checks use [eight synthetic requests](tests/fixtures/writing-cases.json) with independently recorded outputs. See [final-name validation](docs/mob-write-validation.md) and the preserved [WordAim baseline evaluation](docs/evaluation.md). Package tests do not establish writing usefulness. Real adoption still needs feedback from people using it on their own tasks.

Stars show interest; release download counts show downloads, including possible repeats; neither measures installed or active users. This project adds no telemetry and promises no engagement growth or AI-detection result.

Contributions should show the original request, applicable scene, observed problem, and a public-safe example. Keep private writing, profiles, and conversations out of issues and patches. This is a drafting method, not a social-account operator.

## License

[MIT](LICENSE). Meng To's public examples and Siqi Chen's editing guidance retain [their notices and licenses](THIRD_PARTY_NOTICES.md). External samples are expression references, not your experiences or endorsements. Your added third-party material requires its own authorization.
