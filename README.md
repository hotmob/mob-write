# Mob Social Writing

A portable agent skill for natural social replies, grounded in conversation and real writing samples. 中文说明与英文使用入口如下。

回复可以只是感谢、认同、惊讶或接一句玩笑。这个 skill 帮助代理根据语境选回应方式，用真实样本和明确反馈学习个人语气，避免每条都写成技术提问。

它不运营账号、不抓取私人消息、不自动发帖，也不训练模型。名字来自最初使用者，任何人都可以用自己的本地样本建立口吻。

通用中文方法的源码是 [chinese-writing/SKILL.md](chinese-writing/SKILL.md)，技术排版按需读取其 reference；根 [SKILL.md](SKILL.md) 保留 `mob-social-writing` 兼容入口，只维护社交方法和 personal profile 适配。本人偏好与反馈留在 `.local/`，不进入公共仓库。单纯技术说明调用 `$chinese-writing`，社交接话调用 `$mob-social-writing` 后复用通用层。

## 安装

**在 ChatGPT 使用：**从 [Releases](https://github.com/hotmob/mob-social-writing/releases) 下载技能上传包，按 [ChatGPT 安装说明](chatgpt/START-HERE.md) 使用。另提供完整 skills-only 插件包，以及没有 Skills 入口时的普通聊天用法。不需要服务器或 API Key；可用入口取决于账号和工作空间。

使用支持 Agent Skills 的客户端，将本仓库作为一个技能目录安装。Codex 的手动安装方式：

```sh
git clone https://github.com/hotmob/mob-social-writing.git ~/.codex/skills/mob-social-writing
ln -s "$HOME/.codex/skills/mob-social-writing/chinese-writing" "$HOME/.codex/skills/chinese-writing"
```

两个目标目录必须尚不存在。已有同名技能时先检查来源与改动，备份并更新本任务相关入口，保留 `.local/` 中的个人数据；不要直接覆盖或把私人目录提交。`chinese-writing` 的同级入口应链接到同一份源码，不能另维护一份规则。其他客户端可将根目录的社交 Skill 与 `chinese-writing` 安装到其可发现路径。核心写作只需要 Markdown；语料工具使用 Python 3 标准库。

对话里直接说：

> 使用 $mob-social-writing 回这条。我们不熟，轻松一点，不必提问题：［原帖］

或者：

> 用 $mob-social-writing 学习我提供的这些回复。把亲写、AI 草稿、外部参考分开，再帮我回这条。

## 在本地使用参考语料

进入安装目录后：

```sh
python3 scripts/corpus.py fetch-reference
python3 scripts/corpus.py stats
python3 scripts/corpus.py search --query 'thank' --limit 4
```

下载的是固定版本、校验过哈希的 MengTo 公开语料，共 40 条。数据保存在被 Git 忽略的 `.local/`，不会作为本仓库提交的一部分。它缺少父帖上下文，只能帮助观察表达方式，不能当成完整对话或你的亲身经历。

ChatGPT 发布包则从同一固定公开源构建只读 Markdown 参考，直接附带 40 条及其许可，便于离线读取。社交单技能包含嵌套的 `chinese-writing` 依赖；完整插件只在同级 `skills/chinese-writing/` 放一份，另提供独立 `chinese-writing-chatgpt-skill.zip`。所有副本由同一源码生成，测试比较字节一致性。打包器不读取你的 `.local/`，所以个人资料和本地反馈不会混入发布包。

另外两项参考中，Humanizer 提供编辑方法；rabden 的回复归档是空模板。本项目没有虚构它们的“真实回复数据”。版本、许可和取舍见 [来源说明](references/sources.md)。

## 学成自己的语气

1. 提供自己的回复及父帖，或对当前稿件给出明确语气反馈。
2. 把记录整理成 [JSONL 格式](assets/sample-record.example.jsonl)，然后运行 `python3 scripts/corpus.py add --file /path/to/my-replies.jsonl`。
3. 用户明确评价后，用 `python3 scripts/corpus.py feedback --id 样本ID --status approved --note '实际反馈'` 保存认可，或用 rejected 保存否定。写作时检索同类样本，结合 `.local/profile.md` 和 `.local/voice-notes.md`；发过、被点赞或由 AI 写过都不自动算认可。

“学习”发生在上下文和本地记录中，不会修改模型权重。没有本人样本时，也能按自然对话方式起草，但不能声称已精准复刻个人风格。完整流程见 [本地学习方法](references/learning.md)。

## English quick start

Install this repository as an Agent Skills directory and invoke `$mob-social-writing` with the original post and relationship context. For example: “Reply casually to this launch post. We haven't met. A short reaction is fine.”

Use `python3 scripts/corpus.py fetch-reference` for the pinned external corpus, `add --file` for your own records, `feedback --id ID --status approved --note 'actual feedback'` to record an explicit judgment, and `search --approved` to retrieve approved examples. Keep local profiles and unpublished writing under `.local/`. The corpus tool makes no calls to X or an LLM service; only `fetch-reference` downloads one public GitHub file.

## 开源范围

公共仓库包含技能、接话方式、署名片段、本地导入/检索工具、格式示例与测试。个人资料、未发布稿件、用户反馈、完整本地语料和账号凭据都不随仓库发布。

ChatGPT 发布包另含固定版本的完整公开参考语料；它与个人本地语料是分开的。打包和使用方法见 [ChatGPT 说明](chatgpt/START-HERE.md)。

本项目采用 [MIT](LICENSE)。参考 Meng To 的真实语料学习方法和 Siqi Chen 的编辑方法，保留 [第三方版权与许可](THIRD_PARTY_NOTICES.md)。外部样本不表示作者代言；项目许可不覆盖你之后自行加入的第三方材料。

## 检查

```sh
python3 -m unittest discover -s tests -v
```

测试覆盖语料导入、去重、冲突、来源校验与检索隔离。写作质量还需要用户真实反馈；它不承诺互动增长或规避 AI 检测。
