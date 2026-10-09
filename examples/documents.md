# Document examples / 文档与语言边界正反例

All cases below are synthetic. Numbers, dates, products, domain instructions, and drafts are fictional. They illustrate preservation of meaning and editing scope, not domain facts, private business methods, or a replacement for the user's own project rules.

## D1 — Shorter can remove the evidence / 短不必然更好

**Context / materials**

写一段面向同事的技术结论。只在一台 12 GB 内存的机器上，对同一份 8 万行 CSV 做了 6 次串行测试。旧版中位耗时 42 ms，新版 31 ms。并发、其他文件规模与生产环境没有测。没有要求固定字数。

**Bad**

> 新版全面提速，性能显著提升。

**Better**

> 在一台 12 GB 内存的机器上，对同一份 8 万行 CSV 做了 6 次串行测试，新版中位耗时为 31 ms，旧版为 42 ms。并发、其他文件规模与生产环境尚未测试。

**Why**

短稿删掉了支持结论的条件和未测范围，并把一次受限测试扩大到所有场景。改后更长，但读者可以判断结果适用于哪里。没有凭耗时推断内存、吞吐量或生产表现。

**Boundary**

不是每段都要罗列全部实验细节，只保留影响当前判断的条件。若确有篇幅上限，先压缩重复内容；必要限制放不下时指出冲突，不能为达标丢掉条件或强化结论。

## D2 — Review language is separate from delivery language / 审阅与交付语言分开

**Context / materials**

用户要求先给中文审阅说明，再给只读英文的收件人邮件正文。起草者能在 **2026 年 11 月 18 日 10:00 UTC 之前，严格不含该时刻** 完成接口核对。安全审查依赖另一次批准，不在此时间承诺内。邮件需要请收件人确认截止是否只指接口核对。没有给出姓名或署名。

**Bad**

> 我们会按时完成全部审查。
>
> I'll complete the API and security reviews by 10:00 UTC on 18 November 2026.

**Better**

中文审阅说明：

> 英文正文的时间范围只包含接口核对，不包含安全审查；“之前”保留为严格的 before。中文说明不放入收件人的邮件。

English draft:

> I can finish the interface review before 10:00 UTC on 18 November 2026. The security review depends on a separate approval and is not included in that timing. Could you confirm that the deadline covers only the interface review?

**Why**

错误稿混入收件人不读的中文、扩大承诺，并把接口无依据地缩窄成 API。`by` 通常允许在指定时刻完成，不能替代本例明确的严格 `before`。改后把两种语言的用途分开，保留范围、依赖和待确认问题，没有自动补署名。

**Boundary**

普通“周三前”若含义不明，不应机械套用本例的严格时间或自行添加时区。应保留可确认的范围，必要时询问。用户只要英文正文时，不附中文审阅说明；界面语言不能推断收件人语言。

## D3 — Translation preserves negation, degree, and timing / 翻译保留否定、程度与期限

**Context / materials**

只把下面原文忠实翻译成中文，不改成宣传稿：

> The pilot may begin before 09:00 UTC on 2 December 2026 if the data check passes. It is not approved for production, and no reduction in operating costs has been demonstrated.

**Bad**

> 试点将在 2026 年 12 月 2 日 09:00 开始，已具备生产条件，能够显著降低运营成本。

**Better**

> 如果数据核对通过，试点可能在 2026 年 12 月 2 日 09:00 UTC 之前开始。该方案未获准用于生产，且尚未证明它能降低运营成本。

**Why**

错误稿去掉了条件、可能性、时区和否定，新增了效果程度。改后没有用“更肯定、更有力”替换源文含义；“尚未证明”也没有被改成“证明无效”。

**Boundary**

这是忠实翻译任务，不授权改写作者立场或补全缺失事实。用户指定术语表、专业翻译方法或需保持的歧义时，沿用该范围。润色目标不能替代专业核对，也不能把翻译当作事实验证。

## D4 — Writing does not replace the domain method / 行业内容保留业务方法

**Context / materials**

完全虚构的工业设备团队向行业负责人介绍温度巡检原型。给定事实表只有：在实验台接入了 3 个温度传感器，完成读数演示；没有工厂现场试验、可靠性测试、订单或效益数据。

本例另外给定领域要求：沿用已确认的三页顺序“问题—当前演示—待验证项”；逐页写口语讲稿；事实只取自给定表；业务负责人审阅后才可称获准对外交付。当前尚未完成该审阅。

**Bad**

> 我们已进入规模化落地阶段，可靠性得到充分验证，将显著降低工厂巡检成本。这套成熟方案可以直接交付客户。

**Better**

“当前演示”页的口语讲稿：

> 现在完成的是实验台原型：接入了 3 个温度传感器，可以演示读数。尚未做工厂现场试验，也没有可靠性和效益数据。这次演示说明原型能读到数据，还不能说明现场使用已经可行。

给起草者的交付说明：

> 此段用于既定三页中的第二页，仍需业务负责人审阅；不能标为已获准对外交付。

**Why**

错误稿把原型变成成熟方案、把演示变成验证、把未审阅稿变成可交付。改后帮助行业读者判断当前阶段，同时遵守给定事实源、页序、讲稿形式与审阅条件；写作方法没有接管业务批准。

**Boundary**

本例的三页顺序与审阅条件是合成任务输入，不是 Mob Write 对行业分享的通用流程。真实项目应读取自己的业务方法与事实源；不能从本例推断商业阶段、客户需求或试验批准，也不能把私人业务材料放入公共例库。

## D5 — A formatting-only edit keeps the text exact / 纯排版不改引文和术语

**Context / materials**

用户只允许把下列三项分成三个 Markdown 段落，保留每项内部的全部字符、标点、大小写和代码，不补作者、解释或链接：

```text
引文："API_v2 results are preliminary... Do not retry." 命令：`sync run --force=false --output ./Result_A.csv` 注记：QPS 仅指本测试口径。
```

**Bad**

```text
引文：“API V2 results are preliminary…… Do not retry.”

命令：`sync run --force=false --output ./result-a.csv`

注记：每秒查询率（QPS）仅指本测试口径。
```

**Better**

```text
引文："API_v2 results are preliminary... Do not retry."

命令：`sync run --force=false --output ./Result_A.csv`

注记：QPS 仅指本测试口径。
```

**Why**

错误稿为排版习惯改了引号、省略号、标识符、输出路径和术语。改后只把项间的两个空格换成段落分隔，其他字符保持不变；术语解释可能有用，但本次不在授权编辑范围内。

**Boundary**

逐字范围不能反过来变成所有写作都不得解释术语。用户要求面向新手重写时，可以在允许的正文中解释准确术语；引用、命令、路径和标识符仍按各自实际约束处理。

## D6 — A real correction may need negation / 有意纠错不机械禁用否定

**Context / materials**

用户要说清楚自己支持什么、反对什么，允许润色但不改立场：

> 我不是反对先试，而是反对把这次小样本试验说成已经验证。现在只有两次演示，不能据此保证上线后稳定。

**Bad**

> 我支持先上线，两次演示表明方案已经可用，后续会保持稳定。

**Better**

> 我不反对先试；我反对把两次演示称为已经验证。现有材料还不能保证上线后稳定。

**Why**

错误稿为了肯定、简洁，改变了试用与上线的区别，并把不反对试验强化成支持上线。改后保留真正的纠错和必要否定，让读者知道分歧在哪；没有把“两次演示”包装成稳定性证据。

**Boundary**

不是要求每段使用对照句。没有实际纠错内容、只制造气势的对照可以删；原稿有意的否定、条件或立场应保留。若用户要求逐字引用，本例的润色也不适用。
