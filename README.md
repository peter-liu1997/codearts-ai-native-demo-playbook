# CodeArts AI-Native 客户演示案例集

本仓库把《The CodeArts Playbook for AI-Native Development》中可转化为程序的显式实践案例，整理成 20 个可重复、可验证、适合客户演示的单元。它既是下载后即可运行的演示资产，也是可直接由华为云 CodeArts Agent IDE 识别的项目：包含项目规则、Project Skill、自定义命令、Vibe/Spec 模式卡和逐案例功能验收。

## 在 CodeArts Agent IDE 中演示

打开仓库根目录后，保持左侧资源管理器、中央编辑器、右侧 AI 对话和底部终端可见：

1. `⌘P` 打开 `codearts/cases.json`。
2. 右侧新建对话，选择 Vibe-Coding 或 Spec-Driven。
3. 在输入框键入 `#`，从 UI 添加当前文件、Git、Terminal、Rules 等上下文。
4. 在码道对话中使用：

```text
/demo-list
/demo-case 案例 07
/demo-verify
```

5. Web 案例通过 `⇧⌘P` → `Simple Browser: Show` 在 IDE 内置浏览器中展示。

项目级规则位于 `AGENTS.md`，Skill 位于 `.codeartsdoer/skills/`，自定义命令位于 `.codeartsdoer/commands/`；20 个场景的模式、上下文、提示词和验收命令位于 `codearts/cases.json`。逐点击操作见 [IDE UI 客户演示手册](docs/UI-IDE-DEMO.md)，完整方法见 [码道运行与客户演示指导](docs/CODEARTS-DEMO-GUIDE.md)。

## IDE 底部终端验收

```bash
python3 demo.py list
python3 demo.py codearts list
python3 demo.py verify
python3 demo.py serve --port 8000
```

这些命令应从 CodeArts Agent IDE 的底部终端执行。统一门户启动后，使用 IDE 的 `Simple Browser: Show` 打开 `http://127.0.0.1:8000`。也可以运行单个案例：

```bash
python3 demo.py case 01
python3 demo.py case 13
python3 demo.py case 20

# 查看码道案例卡并做独立功能验收
python3 demo.py codearts show 13
python3 demo.py codearts verify 13
```

## 环境要求

- Python 3.9+：统一启动器、HTTP 服务、测试和多数案例；只使用标准库。
- JDK 17+：案例 01-04 的 Java 原语言程序。已在 JDK 21 验证。
- C11 编译器：案例 17 的设备内存统计。macOS Command Line Tools 或 Linux GCC 均可。
- 现代浏览器：交互原型、看板、API Hub、鸿蒙模拟器、指标与 ROI 页面。

不要求 Docker、Node.js、数据库、云账号或第三方 Python 包。SMN、OIDC 和鸿蒙云手机案例默认使用安全 Mock / Web 模拟器；真实 SDK、AK/SK 和云资源只在客户环境中显式接入，仓库不会保存凭据。

## 交付内容

- [示例总览与能力映射](docs/CASE-INVENTORY.md)：20 个案例、来源页、演示形态和码道能力。
- [逐例客户演示指导](docs/DEMO-GUIDE.md)：每例的启动、讲解、操作、预期结果和复位方法。
- [码道原生演示指导](docs/CODEARTS-DEMO-GUIDE.md)：在 CodeArts Agent IDE 中选择模式、加载上下文、使用 Skill/命令和逐例验收。
- [IDE UI 客户演示手册](docs/UI-IDE-DEMO.md)：图形界面布局、逐点击流程、Vibe/Spec 样板和 20 个案例 UI 索引。
- [功能验证报告](docs/VALIDATION-REPORT.md)：20/20 案例、9/9 全量质量门、CodeArts IDE 与 GitHub 冷启动证据。
- [原书提示词提炼](docs/PROMPTS.md)：把书中关键指令整理成可在码道中复用的提示词卡。
- [提取范围与页码证据](docs/PDF-EXTRACTION-MAP.md)：说明什么被纳入、什么属于理论举例。
- `AGENTS.md`、`.codeartsdoer/skills/`、`.codeartsdoer/commands/`：码道项目规则、项目级 Skill 和客户演示命令。
- `.codeartsdoer/specs/`：日志转换、SMN 插件、IAM OIDC、设备内存四组 `spec.md → design.md → tasks.md` 证据链。
- `.cloudbuild/build.yml`：CodeArts Repo 场景的代码化全量构建验证。
- `contracts/`：IAM OIDC 控制面 OpenAPI 契约。
- `java/`、`device/`、`harmony/`：Java、C、ArkTS 原语言样例。
- `web/`：无需构建工具的客户交互页面。
- `.github/workflows/verify.yml`：每次推送自动执行全量验证。

## 验收口径

`python3 demo.py verify` 会同时检查：

1. Python 语法与单元/集成测试。
2. 20 条案例清单、页码映射和入口完整性。
3. 10 个 Web 页面不引用外部运行时或 CDN。
4. OpenAI 兼容 Tool Calling 两阶段闭环、SSE 与 CORS。
5. 商品 CRUD、库存原子扣减、智能体生命周期、OIDC 临时凭证。
6. Java 4 个程序编译执行。
7. C11 在 `-Wall -Wextra -Werror` 下编译并通过测试。
8. 四组 SDD `spec/design/tasks` 完整性。
9. CodeArts 项目规则、Skill、自定义命令、20 张模式/上下文/提示词/验收案例卡。

## 与码道当前产品能力的对应

仓库结构已按 2026 年 7 月官方文档校准：项目规则采用 `AGENTS.md`，项目 Skill 采用 `.codeartsdoer/skills/`，自定义命令采用 `.codeartsdoer/commands/`；规范开发采用 `.codeartsdoer/specs/`，并映射 `/sdd-new`、`/sdd-design`、`/sdd-tasks`、`/sdd-apply` 四阶段。官方参考：

- [智能体对话与 Vibe / Spec-Driven 模式](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0005.html)
- [项目级 Skills](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0024.html)
- [项目规则与 AGENTS.md](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0019.html)
- [自定义命令](https://support.huaweicloud.com/usermanual-cli/codeartsagent_cli_0010.html)
- [SDD 标准工作流与斜杠命令](https://support.huaweicloud.com/bestpractice-codeartssnap/codeartsdoer_bp_0011.html)
- [代码库索引](https://support.huaweicloud.com/usermanual-cli/codeartsagent_cli_0002.html)
- [单元测试智能体](https://support.huaweicloud.com/usermanual-plugin/codeartsagent_plugin_0005.html)
- [CodeArts 代码智能体产品功能](https://support.huaweicloud.com/productdesc-codeartssnap/codeartsdoer_pd_0004.html)

## 建议的客户演示路线

- 15 分钟高层版：案例 07 → 13 → 19 → 20。
- 30 分钟研发版：案例 01 → 03 → 05 → 08 → 13 → 14。
- 45 分钟企业架构版：案例 06 → 11 → 13 → 15 → 17 → 19 → 20。
- 行业专项：制造选 16/17，云服务选 14/15，鸿蒙生态选 18。

## 许可与说明

仓库代码采用 MIT License。案例是根据用户提供的书稿重建的教学演示，不包含书中原始截图、客户源代码、真实密钥或专有数据；其中云服务与企业案例是最小可运行复现，不宣称替代生产实现。
