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
