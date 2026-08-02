# 逐例客户演示指导

## 演示前统一检查

在仓库根目录执行：

```bash
python3 demo.py verify
```

看到“全部 20 个案例…均通过冷启动验证”后再开始。Web 案例默认端口为 8000；如端口冲突，使用 `--port 8010`。运行中的 Web 案例用 `Ctrl+C` 停止。浏览器数据需要复位时，清除当前站点的 localStorage，或在开发者工具执行 `localStorage.clear()`。

---

## CASE 01 - 用户按年龄分组

启动：`python3 demo.py case 01`

1. 先展示 `java/UserGroupingDemo.java` 中的方法契约和混合输入：合法用户、`null`、负年龄。
2. 运行命令，观察无效数据被过滤、28 岁用户被合并，程序输出 `PASS case 01`。
3. 向客户强调：演示重点不是几行循环，而是码道能从注释恢复输入/输出契约，并主动补齐空输入、空对象和非法年龄边界。

预期：进程退出码为 0，结果只包含年龄 28 和 35。复位：无状态，无需操作。

## CASE 02 - 库存统计解释、优化与重构

启动：`python3 demo.py case 02`

1. 对比同一文件内的命令式实现和 Stream 实现。
2. 指出优化动作：前置返回消除深嵌套、`entrySet` 避免重复查表、`category.equals` 避免空指针。
3. 运行并确认两个版本都得到 10。

讲解重点：码道先解释现状，再做行为不变的最小优化，最后按明确风格继续重构；“等价验证”比代码变短更重要。复位：无状态。

## CASE 03 - 商品管理项目级生成

启动：`python3 demo.py case 03`

1. 展示 `ProductController → ProductService → ProductRepository → Product` 四层结构。
2. 运行 Java 程序，创建一个商品并列出仓库内容。
3. 如需接口视角，另启 `python3 demo.py serve`，调用 `GET /api/products`、`POST /api/products`、`PUT /api/products/{id}`、`DELETE /api/products/{id}`。

讲解重点：自然语言任务被拆成多文件、分层职责和统一 JSON 契约，体现项目级生成，而非单函数补全。默认仓库内存化，便于演示；每次重启服务自动复位。

## CASE 04 - 商品控制器单元测试生成

启动：`python3 demo.py case 04`

1. 打开 `java/ProductControllerTest.java`，展示新增、列表、存在 ID、不存在 ID、删除、删除后列表六个场景。
2. 运行后确认输出 `PASS case 04: 6 controller scenarios`。
3. 现场可临时把一个期望值改错，让测试失败，再交给码道根据错误恢复；演示结束不要提交临时改动。

讲解重点：码道单元测试智能体覆盖测试设计、生成、编译错误修正和结果验证。当前官方插件文档对 JetBrains/Java 有具体约束，客户现场应按所用客户端版本核对。

## CASE 05 - 代码库上下文问答

启动：`python3 demo.py case 05`

1. 命令先扫描真实 Java 文件并建立符号索引。
2. 第一问命中 `createProduct`，第二问命中 `ProductController`。
3. 输出中的 `matchedSymbols` 展示事实来源；不存在的符号不会被加入结果。

讲解重点：通用问答只能给教科书式回答，Codebase 问答会引用当前仓库的真实类名、方法和位置。可追加一个不存在的类名，证明系统不会编造命中。复位：索引每次重新构建。

## CASE 06 - 认证超时协同排查

启动：`python3 demo.py case 06`

1. 逐项展示文件上下文、Debug Skill、上一轮修改记忆、用户偏好和项目调用链。
2. 观察生成计划：确认应用过期值、PDB 断点、Redis TTL/连接。
3. 最终结论指出“应用令牌 60 秒、Redis 键仍 30 秒”的跨组件不一致。

讲解重点：这是“上下文工程”而不是一次猜答案；码道在正确时间加载正确的信息，并保留人类可审查的任务计划。复位：无状态。

## CASE 07 - 会议室预约原型

启动：`python3 demo.py case 07`，打开终端显示的 URL。

1. 切换城市，观察楼宇选项随城市变化。
2. 展开高级搜索，按人数与会议室类型过滤。
3. 选择会议室和多个半小时时段，点击“确认预约”并完成确认。
4. 缩窄浏览器宽度，展示响应式布局。

讲解重点：产品经理把草图和验收标准直接转成可点击制品，反馈周期从周缩短到小时；Vibe Coding 适合探索，但正式上线仍需进入规范与质量流程。刷新页面即可复位。

## CASE 08 - OpenAI 兼容 Mock 与 SSE

启动：`python3 demo.py case 08`。

1. 左侧输入消息，观察 EventSource 逐字追加和闪烁光标。
2. 右侧点击“运行两阶段调用”：第一次 `finish_reason=tool_calls`，本地执行工具后第二次为 `stop`。
3. 打开浏览器 Network，展示 `Access-Control-Allow-Origin` 与 SSE `text/event-stream`。

讲解重点：前端工程师不等待真实后端即可按生产协议开发；智能体还能从 `Failed to fetch` 追到 CORS，再把普通请求演进为流式接口。Mock 只模拟协议，不声称是真实模型。刷新复位。

## CASE 09 - SaaS 产品分析看板

启动：`python3 demo.py case 09`。

1. 切换时间范围，点击指标卡观察选中状态。
2. 说明双 Y 轴三条趋势线、留存行业基准线和状态提示。
3. 展开默认折叠的功能排行，悬停表格行观察左侧蓝色强调。
4. 点击“昨日 / 今日”展示交互反馈。

讲解重点：设计系统、tokens 和业务规范进入上下文后，码道可按“只改这些、其他不动”做局部迭代，减少样式漂移。刷新复位。

## CASE 10 - 公网资产 TCP 连通性扫描

启动：`python3 demo.py case 10`

1. 程序临时打开一个本地端口，同时准备一个关闭端口。
2. 并发扫描并输出 JSON 结果、状态、耗时和错误。
3. 两个结果应分别为 `reachable=true/false`，最后显示 `PASS case 10`。

讲解重点：模糊的“批量 telnet”诉求被补齐为 CSV、超时、并发、进度/结果结构；完成后可沉淀为 Skill。客户真实公网扫描必须经过书面授权，本演示只访问本机。复位：进程自动关闭监听端口。

## CASE 11 - API Hub

启动：`python3 demo.py case 11`。

1. 搜索接口，切换不同 HTTP 方法并观察颜色编码。
2. 在调试面板增加 Key/Value 参数，发送 Mock 请求，查看 50-300ms 模拟响应。
3. 切换“Mock 服务”，复制地址、编辑合法 JSON；再输入非法 JSON 验证红色错误。
4. 切换深色主题和窄屏目录，执行导出、清空 localStorage 后导入恢复。

讲解重点：六轮 Vibe 采用“骨架→调试→Mock→体验→持久化→质量”增量路线；代码质量轮包含文本安全输出、JSDoc 思路和 CSS 变量。复位：`localStorage.removeItem('api-hub-config')` 后刷新。

## CASE 12 - 电商全栈线性演进

启动：`python3 demo.py case 12`。

1. 把两种商品加入购物车，调整数量并提交订单。
2. 观察订单号和总价，页面重新拉取后端库存。
3. 尝试超库存下单，确认后端拒绝且库存不会部分扣减。
4. 结合页头解释从原型、前端打磨、后端、数据抽象到部署的阶段演进。

讲解重点：Vibe 解决 0→1，质量门与抽象层解决 1→100；每个阶段只解决一个核心问题，避免复杂度爆炸。重启服务复位商品库存和订单。

## CASE 13 - Chrome Tracing 日志转换器

启动：`python3 demo.py case 13`

1. 先打开 `.codeartsdoer/specs/log-converter/spec.md`，展示五类 EARS 与验收条件。
2. 顺序查看 `design.md`、`tasks.md`，说明做什么、怎么做、按什么顺序做。
3. 运行后观察 4 条合法事件、1 条错误记录被隔离，输出写入 `.build/sample-trace.json`。
4. 把 JSON 拖入 Chrome Tracing 兼容查看器可做可视化延伸。

讲解重点：SDD 的价值是把自然语言变成可审查、可测试、可追溯的工程输入；错误行不应使整批任务失败。复位：删除 `.build/sample-trace.json` 非必需，下次运行会覆盖。

## CASE 14 - DolphinScheduler SMN 告警插件

启动：`python3 demo.py case 14`

1. 查看 `smn-alert-plugin` 的 spec/design/tasks，确认插件必须进入实例、Test Send 与真实告警链路。
2. 运行后先看到 `TEST_SEND`，再看到 `ALERT`，二者均返回独立 `messageId`。
3. 强调默认 `MockSmnClient` 不需要 AK/SK；真实 SDK 通过接口注入。
4. 可把 Endpoint 改为 `http://`，展示配置在发送前被拒绝。

讲解重点：码道结合 Codebase 理解成熟插件框架，沿既有扩展点增量实现；SDD 防止代码“能调 SDK”却没有真正进入平台流程。复位：无外部状态。

## CASE 15 - IAM OIDC 信任委托

启动：`python3 demo.py case 15`

1. 查看 `contracts/oidc-provider.openapi.yaml` 与 `iam-oidc` SDD 文档。
2. 程序创建 HTTPS Issuer、Client ID 与自动指纹，再用 demo subject token 换取 900 秒临时凭证。
3. 把 Issuer 改成 HTTP/任意主机或把 Client ID 改错，展示 SSRF/信任边界被拒绝。
4. 强调返回值是演示临时凭证，不连接真实 IAM。

讲解重点：高安全云服务先固定 OpenAPI 与错误语义，再做外部访问、证书指纹和信任映射；效率提升不能牺牲保守边界。复位：内存 Provider 随进程退出清空。

## CASE 16 - 制造企业 AI 智能体门户

启动：`python3 demo.py case 16`。

1. 按制造/质量/运维标签筛选智能体。
2. 新建智能体草稿，填写名称、描述和标签。
3. 把草稿发布、将已发布智能体下线、再重新发布。
4. 展示竞赛入口与 RBAC 说明；非法状态跳转由服务端拒绝。

讲解重点：从零文档口述收敛出字段、状态机、权限和竞赛运营，再由规范驱动前后端；业务人员通过对话参与验收。重启服务复位。

## CASE 17 - 设备管理面内存统计

启动：`python3 demo.py case 17`

1. 查看 `.codeartsdoer/specs/device-memory/` 和 `device_memory.h` 中的领域接口与可靠重试常量。
2. 运行 C11 严格编译：`-Wall -Wextra -Werror`。
3. 测试上报两进程得到 272MB，进程退出后降为 240MB，从进程查询被拒绝。
4. 指出固定 64 槽避免嵌入式动态分配，300 次 × 1 秒满足 5 分钟窗口。

讲解重点：大仓场景不能只喂原始需求，需 Codebase、全局 DESIGN、领域 Skill 和阶段 SubAgent；最终仍需专家 Review。复位：无状态，二进制位于 `.build/device-memory-test`。

## CASE 18 - 鸿蒙云手机电商应用

启动：`python3 demo.py case 18`。

1. 在 Web 云手机模拟器中连续加购，观察购物车状态更新。
2. 打开 `harmony/Index.ets`，展示 `@State`、强类型接口、声明式 `ForEach` 和 ArkUI 组件。
3. 说明真实路径：DevEco 创建项目骨架 → 码道整仓生成 → HDC 隧道连接云手机 → 编译/投屏/测试。
4. 明确 Web 页面是离线替身，真实云手机需要用户自己的华为云资源和授权。

讲解重点：码道减少 ArkTS 语法、API 与跨文件配置错误，端云协同消除实体设备依赖；凭据不进入代码仓。刷新复位模拟器购物车。

## CASE 19 - AI 编码成熟度指标诊断

启动：`python3 demo.py case 19`。

1. 使用预置 68% / 31% / 27%，得到“生成膨胀期”。
2. 改成 45% / 12% / 41%，得到“规范内耗期”。
3. 改成 60% / 10% / 8%，得到“进化成熟期”。
4. 对照表格解释每个阶段的风险和最紧迫动作。

讲解重点：指标用于组织系统调优，不应直接考核个人；双周看趋势、每月联合诊断、每季度归因。刷新恢复预置数据。

## CASE 20 - AI 编程净 ROI

启动：`python3 demo.py case 20`。

1. 使用书中电商团队数据：毛收益 345 万、成本 278 万、生成率 71%、返工率 29%、违反率 19%。
2. 得到 NEC 约 40.8%、净 ROI 约 -49.3%，说明表面高生成率掩盖质量损耗。
3. 点击“应用改进目标”，观察返工与违反率下降后 NEC 和 ROI 改善。
4. 与客户讨论成本是否包含基础设施、集成、审查、返工、合规修正与技术债务。

讲解重点：生成率不能直接等价为收益；码道的价值要通过质量、工程治理和业务交付转化。页面不保存输入，刷新即复位。

---

## 演示结束后的统一复位

1. 停止所有运行中的 `demo.py case` 或 `demo.py serve` 进程。
2. Web 状态异常时清除站点 localStorage。
3. `.build/` 仅包含可再生成的编译物和转换结果；执行 `make clean` 可清理。
4. 再次执行 `python3 demo.py verify`，确认环境恢复到可交付状态。

