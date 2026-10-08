# 本地学习：用参考和反馈，不训练模型

这里的“学习”是检索少量相关样本并放入写作上下文，结合用户反馈持续修订本地口吻说明。它不微调模型，也不会修改模型权重。

## 数据放在哪里

建议将个人数据放在技能安装目录之外的一个私有资料包，升级公共方法时保持资料独立。空白目录结构见[私有资料包模板](../assets/private-bundle-template/README.md)：

- `profile.md`：称呼、使用语言、表达偏好，按需读取。
- `voice-notes.md`：用户明确的语气反馈及适用范围。
- `corpus.jsonl`：本人样本、明确认可或否定的稿件。
- `reference-corpus.jsonl`：下载的外部作者样本，始终保留外部身份。
- `bundle.json`：`schema: 1`、owner 和 scope。owner 只标记资料归属；scope 说明适用语言、平台、关系和例外，不替代收件人语言。

通过 `scripts/private_data.py` 初始化并显式连接自己的目录。连接记录只写到安装目录被 Git 忽略的 `.local/config.json`，内容为 `schema: 1` 和绝对 `data_dir`；公共源码、安装收据与发布包不包含私人路径或资料。切换开发者时连接另一目录，不合并不同作者的数据。

```sh
python3 scripts/private_data.py init --data-dir /path/to/private-writing-bundle --owner 'Your name' --scope 'English replies to developer peers; formal work messages excluded'
# 在私有目录填写 profile.md 与 voice-notes.md，再连接。
python3 scripts/private_data.py connect --data-dir /path/to/private-writing-bundle
python3 scripts/private_data.py show
```

`connect` 和 `show` 默认针对脚本所属的技能目录；需要指定实际安装时使用 `--skill-dir /path/to/skills/mob-write`。初始化保留空语料，不导入虚构模板，不伪造认可。连接只确认显式目录与清单格式、profile 文件存在，不读取私人正文；命令成功不能证明写作时已加载或效果符合本人语气。

语料命令的 `--data-dir` 可以显式指定资料包；不传时采用已连接目录，没有连接则沿用技能目录下 `.local/`。这个旧的本地数据位置不表示已自动选择个人口吻。读取 profile 前仍要核对资料归属和范围。资料缺失或宿主不能访问时，保持通用起草，不声称已学习或应用口吻。

公开仓库源码只包含方法、少量署名片段和空白/合成模板；完整参考语料在本地按需下载。ChatGPT 发布包可选附带固定公开源生成的只读 `references/external-examples.md`，不读取或打包个人 `.local/` 或已连接目录。`.gitignore` 不是访问控制，分享文件前仍要检查实际打包内容。

## 下载已有参考语料

在技能目录运行；需要选择特定资料包时，在子命令前加 `--data-dir /path/to/private-writing-bundle`：

```sh
python3 scripts/corpus.py fetch-reference
python3 scripts/corpus.py stats
python3 scripts/corpus.py search --query 'thank' --limit 4
```

`fetch-reference` 只向 GitHub 的公开原始文件地址请求固定版本的 MengTo 语料，不需要令牌。先校验 SHA-256，再将 40 条记录转为本地格式；不安装依赖、不执行来源脚本、不访问 X 账号。它固定使用已审核的 commit，不会自动跟随 main 更新。

原始样本包含 34 条回复、5 条引用、1 条原创，集中在 2026-07-11 至 07-17，其中多条是生日感谢。所有父帖上下文都缺失；适合观察表达，不代表所有 X 场景，也不是关于用户本人的事实。

Humanizer 提供编辑规则；rabden 的回复归档在核验版本中是空白模板。不能把三者都说成已下载的真实对话语料库。

## 加入自己的真实样本

每行一个 JSON 对象，字段示例见 [示例记录](../assets/sample-record.example.jsonl)。该文件是虚构的格式演示，不是已认可语料，请填入自己的内容后再导入。

```sh
python3 scripts/corpus.py add --file /path/to/my-reviewed-replies.jsonl
python3 scripts/corpus.py feedback --id my-reply-001 --status approved --note '用户明确说这句像自己的语气'
python3 scripts/corpus.py search --approved --intent gratitude --limit 4
python3 scripts/corpus.py search --rejected --limit 4
```

记录字段：

| 字段 | 含义 |
|---|---|
| `id` | 稳定的唯一标识；同 ID 不同内容会报冲突 |
| `platform` / `format` | 平台；format 为 reply、post 或 quote |
| `intent` | 如 gratitude、reaction、agreement、banter、question；不确定就 unknown |
| `author` | 实际作者，不默认写成用户 |
| `origin` | human_authored、ai_draft 或 external_reference |
| `feedback` | unreviewed、approved 或 rejected |
| `feedback_note` | approved/rejected 时必须写清用户反馈；不能伪造认可 |
| `text` | 回复原文，保留有意义的口语特点 |
| `parent_text` | 父帖原文；无法核验就 null，不自行补造 |
| `source_url` | 可核验来源；未公开稿件可以为 null |
| `source_revision` | 可选，外部样本所在源码版本 |

脚本检查格式、去重和反馈备注，但无法判断用户是否真的认可；输入者负责保持真实性。导入会先检查全部记录，再一次写入；冲突时保留原文件。更新已有记录的判断使用 `feedback` 命令，只改反馈及说明，保留作者、来源和文本。

对外部样本的反馈以本地覆盖记录保存，再次下载固定参考语料也不会冲掉它。任何时候 `origin` 都不随认可状态改变：认可某句外部表达，并不会把它变成本人的经历。

默认检索排除被否定的稿件和未认可的 AI 草稿，优先返回已认可样本。即便外部样本被用户认可，`origin` 仍是 external_reference。

## 提炼口吻

读与当前任务同平台、同类型的少量样本，观察用户通常如何表达感谢、惊讶、认同、分歧或提问。注意双方关系和父帖语境，不仅看标点。

将有重复证据或明确用户反馈的结论写进所选私有资料包的 `voice-notes.md`，注明适用范围和来源。少量例子先作为倾向，不扩成“永远不问问题”“每句必须小写”等规则。没有反馈就保留未确认状态。

新的草稿正常交给用户。用户明确认可或纠正语气时，在已获授权维护语料的任务里记录反馈；不要每次都发起问卷。
