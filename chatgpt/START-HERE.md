# 在 ChatGPT 用 Mob Social Writing

你可以在 ChatGPT 中直接使用这套写作规则和有来源的样本，无需部署服务器或配置 API Key。本仓库的包分别用于社交 Skill、独立中文 Skill 和完整插件。

## 个人使用：技能上传包

从 [GitHub Releases](https://github.com/hotmob/mob-social-writing/releases) 下载 `mob-social-writing-chatgpt-skill.zip`。

在支持该功能的 ChatGPT 中：

1. 打开侧栏 **Plugins → Skills → Create → Upload from your computer**。
2. 选择 `mob-social-writing-chatgpt-skill.zip`，按页面提示完成扫描与安装。
3. 在可使用该技能的对话里说：“用 Mob Social Writing 帮我回这条。我们不熟，轻松一点：［原帖］”。

社交技能包包含接话方法、40 条公开参考、来源与许可、可选语料工具，以及 `chinese-writing/` 中的中文通用依赖。独立 `chinese-writing-chatgpt-skill.zip` 只有通用方法与技术参考。写作时直接读 Markdown 即可，不依赖脚本执行或再次下载语料。**不要把完整插件 ZIP 上传到单技能入口。**

截至 2026-09-16，官方列出的个人 Skills 可用账户为符合条件的 Business、Enterprise、Healthcare、Edu，且受工作空间设置和产品开放情况影响。入口不存在不一定是安装包问题；个人 Plus/Pro 不能假设有相同上传入口。官方说明：[Skills in ChatGPT](https://help.openai.com/en/articles/20001066)。

## 完整插件：本地插件来源与后续分发

`mob-social-writing-plugin.zip` 包含 `.codex-plugin/plugin.json`、`skills/mob-social-writing/` 和 `skills/chinese-writing/`。通用层在完整插件中只保留一份；社交入口按同级依赖读取。它可交给支持本地插件的客户端或管理员导入，也可用于后续目录投稿。

ChatGPT 桌面端的 Work/Codex 本地插件来源，与网页版个人 Skills 上传是不同入口；不是任意网页账号都能直接上传完整插件 ZIP。需要在支持的宿主里配置本地 marketplace 并安装时，可解压完整包，再让 `plugin-creator` 将其加入个人插件来源。

这里的 GitHub 发布**不等于**上架 ChatGPT 公共插件目录。目录投稿和工作空间发布是独立操作，需要相应身份、权限和审核。本项目不含 MCP、外部账号连接或服务端。打包规范见 [Package your plugin](https://developers.openai.com/plugins/build/plugins)。

## 没有 Skills 入口也可以用

在普通 ChatGPT 新对话中，粘贴 [chat-starter.md](chat-starter.md) 的内容，再贴原帖。将社交技能 ZIP 解压，把根 `SKILL.md` 与 `chinese-writing/SKILL.md` 附到同一对话；中文通用规则以该文件为准，未附上时不能声称已应用。需要样本时再附 `references/reply-moves.md` 和 `references/external-examples.md`。技术排版任务再附 `chinese-writing/references/technical-document.md`。也可在可用的项目中放入这些资料，并将起始说明放入项目指令。

这是当前对话/项目中的使用方式，不代表插件已安装。不会自动读取你电脑上的技能或私人反馈。

## 让它逐步像你

直接说“这句太正式”“这里道谢就够了”“这种玩笑像我”。同一对话中会按反馈修订。想留到以后，可以说：

> 把我明确说过的语气偏好整理成口吻卡。区分本人样本、AI 草稿和外部参考，没有确认的别当结论。

保存口吻卡，之后在新对话附上，或更新你自己的项目资料/私人技能副本。本包没有自动同步或跨会话存储服务，不会将这些反馈提交到公开 GitHub。

## 安装后试这几类请求

- “对方回答了我的问题，帮我简单道谢。”应能自然结束，不强加问题。
- “对方发了自己做的作品，我们不熟，回一句。”不应变成技术验收，也不应冒称用过。
- “这句不像我，少一点工作汇报感。”应直接改稿，不要求填写校准问卷。
- “把这个外部作者的经历改成我的。”应保留事实边界，不冒用经历。
- “替我发出去。”本包本身没有发送工具，不能报告已发送。

包结构、引用完整性和测试在仓库中验证；账户内的实际安装、扫描结果与调用需要在对应 ChatGPT 环境里确认。

## 从源码重新打包

在仓库根目录运行：

```sh
python3 scripts/build_chatgpt.py
```

仅下载已固定版本和 SHA-256 的公开 Meng To 语料，并从明确文件清单构建三个 ZIP 和校验清单，输出到 `dist/`。不读取 `.local/`，不包含私人资料。离线构建可用 `--reference-file /path/to/original-tweet-corpus.jsonl` 提供**同一哈希**的上游原始文件；不是导入私人语料的入口。
