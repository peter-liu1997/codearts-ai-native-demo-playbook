# CodeArts Agent IDE UI 客户演示手册

本手册规定：客户演示以 CodeArts Agent IDE 图形界面为主，外部终端不是主入口。命令仅在 IDE 底部集成终端中作为可审计验收证据执行。20 个案例从打开文件到运行、交互和验收的 98 张真实 IDE 截图见 [20 案例逐步截图手册](UI-IDE-CASE-SCREENSHOTS.md)。

截图版统一要求：CLI/SDD 案例每例保留“主文件、码道对话与结果、实际运行、独立验收”4 张图；Web 案例额外保留“专用服务启动、内置浏览器初始页面、交互结果”，每例共 6 张图。截图必须来自本例重新启动的对话、终端和服务，不复用上一个案例状态。

## 1. 演示前检查

1. 将 CodeArts Agent 安装到 macOS“应用程序”目录，避免应用转置导致更新服务失败。
2. 登录华为云账号，确认右上角显示账号而不是 `Sign In`。
3. 确认账号套餐可用。若右侧提示“套餐已被冻结”或“尚未获得此功能的访问权限”，AI 对话无法演示；文件、终端和内置浏览器仍可使用，但不能宣称码道 AI 对话已通过。
4. 选择“文件 → 打开文件夹”，打开仓库根目录。
5. 在左侧资源管理器确认能看到 `AGENTS.md`、`.codeartsdoer`、`codearts`、`web`、`java`、`device`。
6. 保持五个区域可见：左侧资源管理器、中央编辑器、右侧 AI 对话、底部终端、按需打开的内置简单浏览器。

## 2. 标准 UI 操作闭环

| 阶段 | IDE UI 操作 | 客户看到的证据 |
|---|---|---|
| 选案例 | `⌘P` 快速打开 `codearts/cases.json` | 20 个场景的模式、上下文、提示词和验收命令 |
| 选模式 | 右侧新建对话，点击 Vibe-Coding 或 Spec-Driven 卡片 | 快速迭代与规范交付两种工作方式 |
| 加上下文 | 在对话输入框键入 `#`，选择当前文件、File、Folder、Git、Terminal、Problems、Rules | 码道使用真实项目证据而非孤立提示词 |
| 调项目命令 | 输入 `/demo-case 案例 <ID>` | 项目级自定义命令和 Skill 被调用 |
| 审计划 | 在对话区审查码道的目标、影响文件和验证计划 | 先计划、后修改，范围可控 |
| 看变更 | 在中央编辑器和源代码管理视图审查差异 | 多文件修改、最小变更和可回退性 |
| 做验收 | 打开底部“终端”，执行案例卡中的验收命令 | `PASS CodeArts case <ID>` |
| 看页面 | `⇧⌘P` → `Simple Browser: Show` → 输入本地 URL | 页面与交互在 IDE 内完成，不切换外部应用 |
| 做复盘 | 输入 `/demo-verify`，查看终端和问题面板 | 案例级与全量质量门闭环 |

## 3. Vibe-Coding 完整演示：案例 07

目标是把“对话—代码—运行—交互—验收”全部放在 CodeArts Agent IDE 内。

1. 左侧资源管理器打开 `web/meeting-room.html`，再打开 `web/assets/styles.css`。
2. 右侧点击“+”新建对话，选择 Vibe-Coding 卡片。
3. 在输入框键入 `#`，加入当前 HTML、公共样式和 Rules；需要运行证据时再加入 Terminal。
4. 输入 `/demo-case 案例 07`，要求保留城市、楼宇、会议室、连续时段和二次确认交互。
5. 审查码道计划和差异；只批准案例相关文件，不接受无关重构。
6. 在底部终端执行：

   ```bash
   python3 demo.py codearts verify 07
   ```

   预期显示 `PASS CodeArts case 07`。

7. 新建一个 IDE 终端并启动案例：

   ```bash
   python3 demo.py case 07 --port 8000
   ```

8. 使用 `⇧⌘P` 打开命令面板，选择 `Simple Browser: Show`，输入：

   ```text
   http://127.0.0.1:8000/demo/meeting-room
   ```

9. 在 IDE 内置浏览器选择“启航”、09:30 和 10:00，点击“确认预约”，在二次确认框再次点击“确认”。
10. 预期页面显示“预约成功，反馈闭环已完成”。演示结束后回到底部服务器终端按 `Ctrl+C`。

## 4. Spec-Driven 完整演示：案例 13

1. 右侧新建对话，选择 Spec-Driven 卡片。
2. 左侧依次打开：
   - `.codeartsdoer/specs/log-converter/spec.md`
   - `.codeartsdoer/specs/log-converter/design.md`
   - `.codeartsdoer/specs/log-converter/tasks.md`
   - `data/sample.log`
   - `playbook/core.py`
3. 在输入框键入 `#`，把以上文件、Rules 和 Terminal 加入上下文。
4. 输入 `/demo-case 案例 13`，要求先核对 EARS 需求，再审查设计、任务和实现覆盖关系。
5. 在编辑器中展示 `spec → design → tasks → LogConverter` 的可追溯链路。
6. 在 IDE 底部终端运行：

   ```bash
   python3 demo.py codearts verify 13
   ```

7. 预期显示 `PASS CodeArts case 13`，并在 `.build/sample-trace.json` 看到转换结果。

## 5. 20 个案例 UI 操作索引

| ID | 模式 | `⌘P` 打开的主文件 | `#` 上下文重点 | IDE 中的演示动作 |
|---|---|---|---|---|
| 01 | Vibe | `java/UserGroupingDemo.java` | 当前文件、测试、Rules | 审查 null/负年龄，终端验收分组结果 |
| 02 | Vibe | `java/InventoryRefactorDemo.java` | 当前文件、目标符号 | 对比循环与 Stream，确认行为等价 |
| 03 | Vibe | `java/ProductManagementDemo.java` | 实现、测试、Git | 在编辑器定位 Controller/Service/Repository |
| 04 | Vibe | `java/ProductControllerTest.java` | 实现、测试、Terminal | 从失败输出生成并修复测试 |
| 05 | Vibe | `java/ProductManagementDemo.java` | Folder、Git、Rules | 询问真实调用链并验证不存在符号不被臆造 |
| 06 | Vibe | `playbook/core.py` | File、Git、Terminal、Rules | 把认证超时证据拆成事实/推断/待验证项 |
| 07 | Vibe | `web/meeting-room.html` | HTML、样式、Rules | 内置浏览器完成会议室预约闭环 |
| 08 | Vibe | `playbook/server.py` | 服务端、页面、测试 | 终端验证 Tool Calling、SSE、CORS |
| 09 | Vibe | `web/dashboard.html` | 页面、样式、公共脚本 | 内置浏览器切换对比和折叠排行 |
| 10 | Vibe | `playbook/core.py` | 扫描器、CSV、测试、Rules | 仅扫描本地授权端口并观察开/闭结果 |
| 11 | Vibe | `web/api-hub.html` | 页面、样式、Rules | 内置浏览器演示搜索、Mock、非法 JSON、持久化 |
| 12 | Vibe | `web/ecommerce.html` | 页面、服务端、测试 | 内置浏览器加购下单，终端验证原子扣减 |
| 13 | Spec | `specs/log-converter/spec.md` | Spec、Design、Tasks、日志、实现 | 展示 SDD 证据链并生成 trace JSON |
| 14 | Spec | `specs/smn-alert-plugin/spec.md` | Spec、Design、Tasks、实现、Rules | 终端展示 Test Send 与告警复用路径 |
| 15 | Spec | `specs/iam-oidc/spec.md` | Spec、OpenAPI、实现、Rules | 展示 HTTPS/Client ID/SSRF 安全失败分支 |
| 16 | Vibe | `web/agent-portal.html` | 页面、服务端、测试 | 内置浏览器创建、筛选、发布和非法回退 |
| 17 | Spec | `specs/device-memory/spec.md` | Spec、Design、C 实现、测试 | 终端展示严格编译、upsert 和主进程保护 |
| 18 | Vibe | `harmony/Index.ets` | ArkTS、Ability、Web 替身 | 内置浏览器加购，编辑器对照 `@State` |
| 19 | Vibe | `web/metrics.html` | 页面、诊断符号、测试 | 内置浏览器调节三指标并观察联合诊断 |
| 20 | Vibe | `web/roi.html` | 页面、ROI 符号、测试 | 内置浏览器复算 NEC 与净 ROI |

表中 `specs/...` 均位于 `.codeartsdoer/specs/`。所有案例在右侧输入 `/demo-case 案例 <ID>`，在底部终端执行 `python3 demo.py codearts verify <ID>`。

逐例执行时不要只读上表：按 [20 案例逐步截图手册](UI-IDE-CASE-SCREENSHOTS.md) 从案例 01 开始依次操作。截图卷同时是现场讲师的复位检查表和客户下载后的离线证据。

## 6. UI 演示异常处理

- **套餐冻结/无访问权限**：停止 AI 对话演示，联系管理员恢复套餐；可以继续展示代码、终端和内置浏览器，但必须明确 AI 对话未验证。
- **macOS 提示应用被隔离**：把 CodeArts Agent 移入“应用程序”目录后重新启动。
- **项目命令未出现**：检查 `.codeartsdoer/commands/` 是否存在，并新建对话重试。
- **Skill 未加载**：检查 `.codeartsdoer/skills/ProjectSkillStatus.txt` 是否包含 `codearts-demo-runner=true`。
- **页面打不开**：确认服务器终端仍在运行、端口未冲突，并在内置浏览器点击刷新。
- **终端环境过时**：新建终端后重试，或通过命令面板执行 `Terminal: Create New Terminal`。
- **演示结束**：服务器终端按 `Ctrl+C`；确认源代码管理视图没有非预期修改。

## 7. 已实测 UI 证据

2026-08-03 在 CodeArts Agent IDE 中完成：

- 图形界面打开本仓库和 `codearts/cases.json`。
- Vibe-Coding/Spec-Driven 模式卡可见。
- `#` 上下文菜单显示当前文件、File、Folder、Git、Terminal、Problems、Knowledge Bases 和 Rules。
- IDE 集成终端执行案例 07，返回 `PASS CodeArts case 07`。
- IDE 简单浏览器加载会议室页面，完成“启航 → 09:30–10:00 → 二次确认”，显示“预约成功，反馈闭环已完成”。
- 华为云账号套餐已恢复；20 个案例均分别新建码道对话，并保留真实的上下文读取、分析、命令执行与验收结论。
- 98 张截图已全部刷新：CLI/SDD 案例覆盖主文件、真实对话、运行和验收，Web 案例额外覆盖初始页面与操作结果。
