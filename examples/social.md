# Social examples / 社交表达正反例

All cases below are synthetic. They are not copied conversations, real product claims, or approved personal-voice samples. A useful social response can be brief; the purpose and relationship determine how brief.

## S1 — Gratitude can finish the exchange / 感谢可以自然结束

**Context / materials**

一位不熟悉的网友用英文解释设置：“The toggle only affects preview; export uses its own setting.” 用户看懂了，尚未试过。当前只想简短道谢，不要再问问题。

**Bad**

> Amazing, it works perfectly now! What other powerful features should I explore next?

**Better**

> Thanks, that clears it up!

**Why**

错误稿虚构了运行结果，并新增了对方需要回答的问题。改后只完成本次感谢，不把每次接话改成追问、验收或推广。

**Boundary**

这不是“回复必须短”或“禁止提问”。确有未理解的点、对方邀请反馈，或已经实际测试时，可以按那些事实回应。不能从这个例子学出固定口头禅或默认个人风格。

## S2 — A professional reply needs its conditions / 专业回复需要必要信息

**Context / materials**

虚构的支持工程师要在英文技术社区回复用户。用户问：返回 `task_key` 后是否可以下载文件，能否同时导出多个文件。已知：返回 key 仅表示请求已接受；`phase=ready` 才可下载；当前仅支持串行导出；重试行为未验证。

**Bad**

> Yep, you're good to go!

**Better**

> A `task_key` means the export request was accepted; it does not mean the file is ready. Wait for `phase=ready` before downloading. Only serial exports are supported, and retry behavior has not been verified.

**Why**

错误稿很短，却可能让读者过早下载或开始并发导出。改后回答了两个实际问题，保留未验证范围，读者能据此选择操作。自然语气不等于省略条件。

**Boundary**

这些字段和能力只属于本例，不能用于别的产品。若用户只问一句感谢，不需要加载这类技术说明节奏；若读者还需要排错步骤，应从实际产品资料补充，不能从例子猜。

## S3 — A short post names the subject and skips a headline / 短帖写出对象，不另加标题

**Context / materials**

面向不熟悉内部代号的普通读者，写一条中文短帖，不要标题。虚构事实只有这些：虚构公司“北风软件 Northwind Software”发布了虚构工具“北风对账 Northwind Reconcile”。它只在演示环境把一份 40 行的样例收据导出成一个 CSV，少了一次手工复制。没有客户，没有生产部署，没有测量节省的时间。

**Bad**

> 三个影响维度
>
> 北风对账改变了一切。我更在意开发者。不是工具，而是变革。大多数人还在复制，高手已经自动化。

**Better**

> 北风软件的北风对账，在演示环境里把一份 40 行样例收据导出成一个 CSV，少了一次手工复制。还没有客户，也没有生产部署，所以这还不能当成已经省下的工作时间。

**Why**

短帖不另加标题，也不把分析标题当成正文。前两行写出可辨认的公司名、工具名和具体变化，正文没有把演示说成普遍收益。

**Boundary**

名称和数字只属于本例。读者已经知道全称以后，后文可以简称。Article 或用户明确要求标题时，仍另拟标题。

## S4 — Commentary keeps supported dimensions / 评论只保留有支持的维度

**Context / materials**

写一条给开发者看的中文短评。虚构组织“灯塔实验室 Lighthouse Lab”声称，其虚构组件“灯塔缓存 Lighthouse Cache”在一台演示机上，把一家虚构试点商店的夜间库存查询从 800 ms 降到 200 ms。没有对照说明，也没有第二家商店。行业分工和社会影响都没有材料。不要写成三段。

**Bad**

> 对开发者：查询变快了。
>
> 对 AI 行业：竞争门槛已经改写。
>
> 对社会：这将重塑就业。
>
> 灯塔缓存让所有查询快四倍。我更在意真正的变化。

**Better**

> 灯塔实验室声称，灯塔缓存在一台演示机上把一家试点商店的夜间库存查询从 800 ms 降到 200 ms。这是厂商的单次演示，没有对照，也不能说明别的商店或生产环境会同样变快。对要接入库存查询的开发者，眼下能确认的只是有一个可试用的缓存组件，省下的延迟还没在自己的环境里测过。

**Why**

起草时检查了开发者、行业和社会，成稿只留下有材料支持的开发者含义，不写成三段。厂商声称和尚未验证的推断分开，演示时间没有被说成生产收益。

**Boundary**

毫秒数和机构名只属于本例，不能用于真实产品。只要求忠实转述时，不加载这套评论。

