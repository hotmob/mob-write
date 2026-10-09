<h1 align="center">Mob Write</h1>

<p align="center"><strong>先看目的与读者，再写出有用的话。</strong><br>Mob Skills 系列的写作 Skill。</p>

<p align="center">
  <a href="https://github.com/hotmob/mob-write/releases/latest"><img src="https://img.shields.io/github/v/release/hotmob/mob-write" alt="最新 GitHub Release"></a>
  <a href="https://github.com/hotmob/mob-write/actions/workflows/check.yml"><img src="https://github.com/hotmob/mob-write/actions/workflows/check.yml/badge.svg?branch=main&amp;event=push" alt="main 分支测试与打包状态"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/hotmob/mob-write" alt="MIT 许可证"></a>
</p>

<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>

用于起草和审阅消息、社交回复、文章与技术说明。先判断接收者需要什么，保留已有事实，再按需加载指导。中文审稿与收件人的交付语言分别判断。

**系列：** Mob Skills · **项目：** Mob Write · **调用：** `$mob-write` · **仓库：** [`hotmob/mob-write`](https://github.com/hotmob/mob-write)

[写作对照](#写作对照) · [安装](#安装-v040) · [使用](#使用) · [私密口吻](#可选的私密个人口吻) · [验证](#验证与贡献) · [来源](#来源与许可证)

## 写作对照

以下是**合成教学示例**，不是模型实测输出或私人对话。

| 已知事实与目的 | 有问题的稿子 | 有用的稿子 |
| --- | --- | --- |
| 对方解释了一个配置选项。你理解了，但没有运行验证；用英文致谢。 | “Worked perfectly, thanks!” | “Thanks, that clears it up!” |
| 导出测试已通过，尚未交付；告诉同事真实状态。 | “导出功能已完成交付。” | “导出功能测试已通过，尚未交付。” |
| 在一台 16 GB 机器上，对同一份 10 万行 CSV 做八次串行测试，旧版中位耗时 70 ms，新版 52 ms。未测并发和生产环境。 | “新版在所有场景都更快。” | “在这台 16 GB 机器上，对同一份 10 万行 CSV 做八次串行测试，中位耗时从 70 ms 降至 52 ms；并发和生产环境尚未测。” |

一句感谢可以足够。技术结论可能需要附上依据和限制。精简表达的前提是保留必要含义。

完整例库有 **12 个合成案例**：[工作沟通](examples/work.md) 4 个、[社交写作](examples/social.md) 2 个、[文档与说明](examples/documents.md) 6 个。每个案例包含问题、改稿、理由和适用边界。场景指导与教学说明主要使用中文，正文可以按收件人的语言交付。示例帮助判断，不提供固定套句。

## 安装 v0.4.0

使用固定版本 [v0.4.0](https://github.com/hotmob/mob-write/releases/tag/v0.4.0)。安装与打包需要 **Python 3.10+**。写作规则是 Markdown；可选工具不调用模型或社交账号。

```sh
git clone --branch v0.4.0 --depth 1 https://github.com/hotmob/mob-write.git mob-write-source
cd mob-write-source
git rev-parse HEAD
python3 scripts/install.py --skills-dir /path/to/test-project/.agents/skills
```

首次试用时，选择空的、客户端实际发现的项目级 skills 目录。示例路径适用于 Codex 项目；其他客户端有各自的发现位置。仅打开源码目录不会注册 Skill。

首次安装只写入 `mob-write/`，其中包含记录版本及公共文件哈希的凭据。在**新的客户端会话**中，确认宿主发现了 Mob Write，并读取当前安装版本。安装成功不代表发现成功；正在运行的会话可能保留旧目录信息。

**升级旧安装？** 先读[迁移与恢复](docs/migration.md)。来源相同、受管理且公共文件未改动的安装可以升级。安装器没有默认全局目标，保留私密文件和未知文件，拒绝未知安装、修改过的公共文件，以及含符号链接的安装目标或受管理公共路径。退役已验证的受管理旧入口时，还会向显式指定的位置写入备份，并删除其受管理公共文件。已有 canonical 安装的升级不具备完整 I/O 事务性，应保留可恢复备份。手工 clone 和宿主管理的插件需要分别迁移。

`$wordaim`、`$chinese-writing`、`$mob-social-writing` 在 v0.4.0 中没有转发入口或安装包；其他位置仍启用的旧入口可能继续被发现。历史 release 保留。**v0.2.0** 是较早的社交写作版本，没有统一入口和私密 bundle 工具。

## 使用

提供目标读者、写作目的，以及已有事实或原文：

> 使用 $mob-write 回复这条英文评论。我们没有见过面，一句感谢就够：“That option only applies to the CLI; for the API, set it in the request body.” 我理解了，但还没有验证。

> 使用 $mob-write 给英文收件人写邮件，另附中文审稿释义。接口核对计划周四完成；安全审查需等同事下周一回来。请对方确认周五截止是否只指接口核对，不新增交付承诺。

> 使用 $mob-write 判断这条群进度是否值得发：今天没有新文档、测试、决定或协作需求，与昨天相同，也没有例行汇报要求。如果没有信息增量，说明即可。

通常给出一份可用稿即可。审稿时可以简要解释有实际影响的修改。组合请求逐项判断，每项都保留各自的事实、接收者和沟通决定。

| 请求 | 使用方式 |
| --- | --- |
| 起草、改写或审阅消息、帖子、文章、说明 | 提供接收者、目的和来源材料。 |
| 用中文审阅英文稿 | 中文释义与供收件人使用的英文正文分开。 |
| 判断没有变化的例行进度 | 没有信息增量且无汇报要求时，建议暂缓；已有汇报义务则忠实报告。 |
| 适配行业或项目写作 | 保留项目的证据、术语和工作流规则。 |
| 按指定的专业要求翻译、保留精确引文，或只改排版 | 遵守指定的保真要求和编辑范围。 |
| 一般提问、文件查询或执行命令 | 仅使用中文提问不会调用这套写作方法。 |
| 发送或发布正文 | 使用另行授权的工具或工作流；起草不授予发送权限。 |

## 小入口，按需加载

[`SKILL.md`](SKILL.md) 是唯一入口，维护目的、收件人语言、事实边界和路由。按目的选择场景；没有合适场景时，只用通用规则。中文表达与个人口吻仅在相关时加载。

```text
SKILL.md       目的、读者、事实、路由
references/    工作、社交、文档；中文表达及可选补充
examples/      按需对照的教学案例
assets/        空白 profile 与合成样本模板
scripts/       显式目标安装、打包、本地语料工具
tests/         结构检查、测试输入、已记录的行为结果
docs/          设计、迁移、评估、项目原则
```

友好的工作邮件仍按工作场景处理。简短英文回复只有同时需要中文正文时，才加载中文表达规则。Skill 不会在每项任务中加载整个目录。来源归属与路由见[设计说明](docs/design.md)。

## 可选的私密个人口吻

公共默认不含私密个人口吻。把可替换的[私密 bundle](assets/private-bundle-template/README.md) 放在**安装目录之外**，分别保存归属与适用范围、profile、反馈笔记和语料。对于已安装的 Skill：

```sh
python3 /path/to/skills/mob-write/scripts/private_data.py init --data-dir /path/to/private/my-writing --owner 'Your name' --scope 'Personal developer replies; formal reports excluded'
# Fill profile.md and import your samples with corpus.py --data-dir DIR add --file FILE.
python3 /path/to/skills/mob-write/scripts/private_data.py connect --data-dir /path/to/private/my-writing
python3 /path/to/skills/mob-write/scripts/private_data.py show
```

`connect` 只写入被忽略的 `.local/config.json` 指针。切换作者时，初始化另一个私密目录并连接，数据不会合并。已安装的语料工具默认使用连接目录；显式 `--data-dir` 优先。公共升级保留连接，不读取私密数据。

写作任务在加载口吻材料前检查 bundle 的适用范围。没有连接时，通用写作照常工作。个人偏好不能改动事实、收件人语言或授权。连接、宿主发现、来源读取和写作效果需分别验证；连接数据不代表模型已学会你的口吻。另见[个人口吻规则](references/profile.md)。

## 安装包与 ChatGPT

从 [release](https://github.com/hotmob/mob-write/releases/tag/v0.4.0) 下载，或从同一份源码构建两个公共安装包。**默认离线构建**，输出目录应为空：

```sh
python3 scripts/build_chatgpt.py --output dist
```

| 文件 | 用途 |
| --- | --- |
| `mob-write-chatgpt-skill.zip` | 支持上传 Skill 文件的宿主。 |
| `mob-write-plugin.zip` | 支持导入仅含 Skills 插件的宿主；插件标识为 `mob-write`。 |
| `package-manifest.json` | 版本、公共文件身份与 SHA-256。 |

只生成这两个 ZIP。[ChatGPT 说明](chatgpt/START-HERE.md)记录文件读取和持久化限制；打包成功不代表已安装到账号或发布到目录。

构建器的公共路径白名单排除私密目录、草稿、反馈、凭据和个人路径。安装包保留四段已署名的外部片段与许可证。公共源文件中也不得写入私人材料；白名单不是私人文字检测器。另有固定版本的 40 条公共参考语料，可通过 `--with-reference` 加入，或以 `--reference-file FILE` 指定完全匹配的下载文件。它们是外部参考，与合成教学例库分开，不提供你的经历。详见[来源](references/sources.md)与[本地学习](references/learning.md)。

## 验证与贡献

```sh
python3 -m unittest discover -s tests -v
```

**v0.4.0 已通过 55 项结构检查**，覆盖打包边界、源码与安装包身份、隔离安装及升级、bundle 选择、作者切换、已连接数据保留。顶部徽章显示当前 main 工作流状态。结构检查不证明写作质量；行为试验另行记录实际输出与来源读取。

| 行为证据 | 已支持的结论与限制 |
| --- | --- |
| [rc.4 对照](docs/rc4-validation.md) | 最初十案例对照、定向确认及已观察风险。没有将这些结果重跑或改标为 rc.5。 |
| [rc.5 保真检查](docs/rc5-validation.md) | 两个此前有歧义的请求和四个新增明确边界请求。一次候选输出保留了较宽泛的“接口”用词，日期仍有歧义。两套方法都满足新增四项标准，尚未证明可重复改善或风险已解决。 |
| [rc.6 bundle 检查](docs/rc6-validation.md) | 三个新的隔离会话，涵盖通用写作、两个虚构 profile、排除个人口吻的正式报告。实际读取与安装源一致，稿子呈现有限的口吻差异。一份稿子遗漏明确状态，另一份把“未完成”推断为“正在推进”。没有读取语料或反馈笔记，不能据此证明样本学习或完整事实保真。 |

没有行为试验打开教学例库，其收益仍未测量。少量合成试验不能证明可靠行为、普遍改善、读者理解、真实任务价值或所有模型与宿主的兼容性。

贡献应附原始请求、场景、观察到的问题、可公开的示例与适用边界。使用合成或获准公开的材料，私密写作、profile 和对话不要放入 issue 或补丁。另见[项目原则](docs/constitution.md)、[评估](docs/evaluation.md)与[路线图](docs/roadmap.md)。

Star 表示关注，下载次数可能包含重复下载，都不代表已安装或活跃用户人数。项目不新增遥测，不承诺互动增长或 AI 检测结果。

## 来源与许可证

| Skill 与仓库 | 对 Mob Write 的参考 | 打包内容 |
| --- | --- | --- |
| Meng To 的 [write-like-meng-on-x](https://github.com/MengTo/Skills/blob/321c769739b823de5eb94eb3a52aa1974fe783a2/agent-skills/codex/write-like-meng-on-x/SKILL.md) · [MengTo/Skills](https://github.com/MengTo/Skills) | 区分回复与独立帖子、参考作者样本、保留当前措辞、把生成稿视为较弱口吻证据。 | 改编方法、四段署名片段及可选的固定公共语料，采用 MIT。 |
| Siqi Chen 的 [Humanizer](https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md) · [blader/humanizer](https://github.com/blader/humanizer) | 保留事实与作者口吻、检查重复结构、做轻量终稿编辑。 | 改编编辑指导，采用 MIT。 |
| rabden 的 [X Social Media Manager](https://github.com/rabden/X-twitter-social-manager-skill) | 保留精确回复供后续审阅。 | 仅参考方法，不打包上游文字；当时审阅的回复档案是空模板。 |

结构上参考了本机 Codex **skill-creator** 及其 UI 元数据说明：小入口、按需加载资源、`agents/openai.yaml`。当时读取的本机版本未固定到上游 revision；这是编写方式参考，没有提供写作示例或打包代码。历史 [openai/skills 目录](https://github.com/openai/skills)目前指向 [OpenAI Plugins](https://github.com/openai/plugins)。

历史 **chinese-writing** Skill 来自用户提供的本地指南，已进入[本仓库历史](https://github.com/hotmob/mob-write/tree/f878474706754aed0878efc562d3a93c9557a919/chinese-writing)，未建立独立公共上游。**mob-social-writing** 是本项目旧名。私密 profile、草稿和对话不公开。

已审阅 revision 与改编边界见[来源记录](references/sources.md)，复制材料保留[第三方声明与许可证](THIRD_PARTY_NOTICES.md)。仅为命名查阅的项目不是内容来源，不暗示上游作者背书。

**许可证：** [MIT](LICENSE)。Meng To 公共样本与 Siqi Chen 编辑指导保留完整声明。外部样本提供措辞参考，不提供你的生平或背书；新增第三方材料需另行获得授权。
