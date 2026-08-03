# 基于华为云码道的运行与客户演示指导

这份指导把 20 个可运行成品变成 CodeArts Agent IDE 内可重复执行的演示流程。客户演示以 IDE 图形界面为主：左侧选文件、中央看代码、右侧与码道对话、底部看验收、内置浏览器做页面交互。完整逐点击手册见 [CodeArts Agent IDE UI 客户演示手册](UI-IDE-DEMO.md)。

## 1. 首次准备

1. 将 CodeArts Agent 安装到“应用程序”目录，登录并确认套餐状态正常；出现“套餐已被冻结”或“尚未获得此功能的访问权限”时，不进入 AI 对话演示。
2. 选择“文件 → 打开文件夹”，打开本仓库根目录。
3. 在左侧资源管理器确认项目内存在 `AGENTS.md`、`.codeartsdoer/skills/codearts-demo-runner/SKILL.md` 和 `.codeartsdoer/commands/`。
4. 在右侧新建对话，按案例选择 Vibe-Coding 或 Spec-Driven；在输入框键入 `#` 添加 File、Folder、Git、Terminal 和 Rules 上下文。
5. 在码道对话框输入 `/demo-list`。演示指定案例时输入 `/demo-case 案例 07`，完成后输入 `/demo-verify`。
6. 只在 IDE 底部集成终端执行验收：

   ```bash
   python3 demo.py codearts list
   python3 demo.py verify --verbose
   ```

项目级 Skill 位于 `.codeartsdoer/skills/`，项目规则由根目录 `AGENTS.md` 自动提供；项目级自定义命令位于 `.codeartsdoer/commands/`。这些目录遵循当前 CodeArts Agent 官方约定。

## 2. 演示闭环

每个案例都按同一节奏执行：

1. **选场景**：按 `⌘P` 打开 `codearts/cases.json`，在中央编辑器找到案例 ID。
2. **选模式**：右侧新建对话；01-12、16、18-20 选择 Vibe-Coding，13-15、17 选择 Spec-Driven。
3. **加上下文**：在输入框键入 `#`，从 UI 选择当前文件、File、Folder、Git、Terminal、Problems 或 Rules。
4. **让码道行动**：输入 `/demo-case 案例 <ID>`，先审查计划，再批准相关修改。
5. **看差异**：在中央编辑器和源代码管理视图查看多文件差异、最小变更和安全边界。
6. **做验收**：在 IDE 底部终端执行 `python3 demo.py codearts verify <ID>`。
7. **看页面**：按 `⇧⌘P`，选择 `Simple Browser: Show`，在 IDE 内置浏览器完成交互。
8. **做总验收**：在 IDE 终端执行 `python3 demo.py verify --verbose`。

CodeArts Agent 的 Vibe-Coding 适合快速迭代原型，Spec-Driven 适合需求、设计、任务与实现可追溯的复杂交付。四个 SDD 案例已有 `.codeartsdoer/specs/` 证据链，演示时不要跳过规格审查直接改代码。

## 3. 20 个案例逐例指导

### 01 用户按年龄分组 — Vibe-Coding

- 码道操作：`/demo-case 案例 01`，附加 `java/UserGroupingDemo.java`。
- 演示动作：让码道识别 `null`、负年龄、稳定顺序三个边界，做最小补全。
- 客户价值：代码续写不是拼文本，而是理解意图并补齐健壮性。
- 功能验收：`python3 demo.py codearts verify 01`，应输出分组结果并以 PASS 结束。

### 02 库存统计解释与重构 — Vibe-Coding

- 码道操作：引用 `InventoryRefactorDemo.java` 和目标符号，先解释再优化。
- 演示动作：对比普通循环与 Stream 版本，确认 null 语义未改变。
- 客户价值：解释、优化、重构在同一上下文连续完成，减少行为漂移。
- 功能验收：`python3 demo.py codearts verify 02`。

### 03 商品管理项目级生成 — Vibe-Coding

- 码道操作：同时引用商品实现与测试文件，要求梳理 Controller/Service/Repository。
- 演示动作：让码道定位 CRUD、校验和分层职责，观察跨符号理解。
- 客户价值：从单函数生成升级到项目级、多角色代码协作。
- 功能验收：`python3 demo.py codearts verify 03`。

### 04 商品控制器测试 — Vibe-Coding

- 码道操作：引用实现、测试和最后一次终端输出。
- 演示动作：让码道先列风险，再补正常、非法、缺货和不存在分支，运行测试后修复。
- 客户价值：体现测试设计与基于真实失败的自修复，而非只生成样板。
- 功能验收：`python3 demo.py codearts verify 04`。

### 05 代码库上下文问答 — Vibe-Coding

- 码道操作：引用 Java 代码和 Git 上下文，询问真实调用链并混入一个不存在符号。
- 演示动作：检查回答是否给出文件/符号定位，并明确拒绝臆造缺失符号。
- 客户价值：Codebase 索引、符号检索和可信问答。
- 功能验收：`python3 demo.py codearts verify 05`。

### 06 认证超时协同排查 — Vibe-Coding

- 码道操作：加入 `playbook/core.py`、`AGENTS.md`、Git 与终端上下文。
- 演示动作：要求码道把事实、推断、待验证项拆开，给出最小排查顺序。
- 客户价值：文件、规则、版本和运行证据的上下文编排。
- 功能验收：`python3 demo.py codearts verify 06`。

### 07 会议室预约原型 — Vibe-Coding

- 码道操作：引用页面和公共样式，要求局部迭代而非重写。
- 演示动作：在浏览器完成城市/楼宇筛选、会议室选择、连续时段和二次确认。
- 客户价值：自然语言快速原型、多轮 UI 迭代和响应式交付。
- 功能验收：`python3 demo.py codearts verify 07`；展示时另运行 `python3 demo.py case 07`。

### 08 OpenAI 兼容 Mock 与 SSE — Vibe-Coding

- 码道操作：引用服务端、页面和测试，要求对照协议找缺口。
- 演示动作：展示 `tool_calls → tool → stop`、CORS 响应头和 SSE done 事件。
- 客户价值：协议理解、后端调试、流式接口改造与自动回归。
- 功能验收：`python3 demo.py codearts verify 08`。

### 09 SaaS 产品分析看板 — Vibe-Coding

- 码道操作：引用 Dashboard、设计样式和公共脚本。
- 演示动作：切换日期对比、折叠排行、调整窗口宽度。
- 客户价值：设计规范注入和多轮局部 UI 修改。
- 功能验收：`python3 demo.py codearts verify 09`；展示时运行 `python3 demo.py case 09`。

### 10 TCP 连通性扫描 — Vibe-Coding

- 码道操作：引用扫描器、样例 CSV 和测试；明确只测本地授权端口。
- 演示动作：同时构造一个开放端口和一个关闭端口，观察并发、超时与结构化结果。
- 客户价值：轻量脚本生成、安全约束和可沉淀 Skill。
- 功能验收：`python3 demo.py codearts verify 10`。

### 11 API Hub — Vibe-Coding

- 码道操作：引用单页应用和公共样式，要求按六轮小步检查。
- 演示动作：搜索、在线调试、编辑 Mock、刷新验证持久化、输入非法 JSON、导入导出和切换主题。
- 客户价值：长链路增量 Vibe、状态持久化和输入安全治理。
- 功能验收：`python3 demo.py codearts verify 11`；展示时运行 `python3 demo.py case 11`。

### 12 电商全栈线性演进 — Vibe-Coding

- 码道操作：引用页面、服务端、`ProductCatalog` 符号和测试。
- 演示动作：加载商品、加购、下单、观察库存扣减，再制造缺货失败。
- 客户价值：从页面原型到 API 和领域逻辑的端到端最小演进。
- 功能验收：`python3 demo.py codearts verify 12`。

### 13 Chrome Tracing 日志转换器 — Spec-Driven

- 码道操作：切到 Spec-Driven，依次打开 `spec.md`、`design.md`、`tasks.md`、样例日志和 `LogConverter`。
- 演示动作：先让码道核对 EARS 需求覆盖，再转换日志；展示错误行隔离和生成的 trace JSON。
- 客户价值：需求—设计—任务—代码—测试的可追溯闭环。
- 功能验收：`python3 demo.py codearts verify 13`。

### 14 DolphinScheduler SMN 插件 — Spec-Driven

- 码道操作：加载 SMN SDD 文档和插件符号，明确默认 Mock、禁止真实凭据。
- 演示动作：先 Test Send，再模拟真实告警，比较是否复用同一发送链路和消息 ID。
- 客户价值：遗留插件式增量开发、云服务边界和可测试适配器。
- 功能验收：`python3 demo.py codearts verify 14`。

### 15 IAM OIDC 信任委托 — Spec-Driven

- 码道操作：加载 OIDC SDD、OpenAPI 契约和服务符号。
- 演示动作：创建 Provider、交换临时凭证，再演示 HTTP Issuer、错误 Client ID 和 SSRF 地址失败。
- 客户价值：高约束接口生成、契约一致性和安全边界推理。
- 功能验收：`python3 demo.py codearts verify 15`。

### 16 制造企业 AI 智能体门户 — Vibe-Coding

- 码道操作：引用门户、服务端、Agent 生命周期符号和测试。
- 演示动作：创建智能体、按制造标签筛选、发布，再尝试非法回退。
- 客户价值：从模糊需求到领域状态机与前后端一致实现。
- 功能验收：`python3 demo.py codearts verify 16`。

### 17 设备管理面内存统计 — Spec-Driven

- 码道操作：加载设备内存增量规格、设计、C 实现与测试。
- 演示动作：检查 upsert、进程退出、主进程限制、溢出保护与 300 秒窗口；展示严格编译。
- 客户价值：大仓增量修改、领域规则落地和编译反馈自修复。
- 功能验收：`python3 demo.py codearts verify 17`。

### 18 鸿蒙云手机电商 — Vibe-Coding

- 码道操作：引用 `EntryAbility.ets`、`Index.ets` 和 Web 模拟器。
- 演示动作：查看 ArkTS 声明式结构，在模拟器加购并观察状态更新。
- 客户价值：ArkTS 生成、代码库理解与端云协同调试思路。
- 功能验收：`python3 demo.py codearts verify 18`；真实云手机需另行准备 DevEco 与云资源。

### 19 AI 编码成熟度诊断 — Vibe-Coding

- 码道操作：引用指标页面、诊断符号和测试，说明输入仅为演示数据。
- 演示动作：改变生成率、返工率、违规率，展示联合诊断和改进建议变化。
- 客户价值：把码道价值从代码生成提升到工程治理与组织改进。
- 功能验收：`python3 demo.py codearts verify 19`。

### 20 AI 编程净 ROI — Vibe-Coding

- 码道操作：引用 ROI 页面、计算符号和测试，使用书中样例复算。
- 演示动作：先看毛收益，再加入 NEC、返工和治理成本，观察净 ROI 由正转负。
- 客户价值：把生产率口径转为可审计的商业决策口径。
- 功能验收：`python3 demo.py codearts verify 20`，预期 NEC 约 0.4083、净 ROI 约 -0.4933。

## 4. CodeArts Repo 与构建

仓库提供 `.cloudbuild/build.yml`，构建任务会检查 Python、Java、C 工具链并运行全量验证。云端使用步骤：

1. 在 CodeArts 项目中创建 Repo，并从 GitHub 仓库导入。
2. 创建 CodeArts Build 任务，代码源选择该 CodeArts Repo。
3. 选择包含 Python 3、JDK 17+ 和 C 编译器的构建环境。
4. 使用代码化构建文件 `.cloudbuild/build.yml`，执行后确认所有阶段通过。

CodeArts 的代码化构建当前只支持 CodeArts Repo，因此 GitHub 是公开下载源，CodeArts Repo 是客户现场演示和构建入口。未登录华为云或未实际运行构建任务时，只能声明“构建配置已提供、本地已验证”，不能声明“云上流水线已通过”。

## 5. 演示复位与边界

- 停止 Web 案例：终端按 `Ctrl+C`。
- 清除 API Hub 状态：浏览器开发者工具删除 `localStorage` 的 `api-hub-config`。
- 清理本地产物：删除 `.build/`；它已被 Git 忽略。
- SMN、OIDC、鸿蒙云手机默认是安全 Mock/替身，不代表真实云资源已联调。
- 客户现场若接真实云服务，凭据只通过环境变量或密钥管理服务注入，不写入仓库或对话。

## 6. 官方依据

- [CodeArts Agent：Vibe-Coding 与 Spec-Driven 模式](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0005.html)
- [CodeArts Agent：Skills 配置与项目级目录](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0024.html)
- [CodeArts Agent：项目规则与 AGENTS.md](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0019.html)
- [CodeArts CLI：项目级配置与自定义命令](https://support.huaweicloud.com/usermanual-cli/codeartsagent_cli_0010.html)
- [CodeArts Repo：从 GitHub 导入仓库](https://support.huaweicloud.com/usermanual-codeartsrepo/codeartsrepo_03_0053.html)
- [CodeArts Build：代码化构建](https://support.huaweicloud.com/usermanual-codeci/codeci_ug_0058.html)
