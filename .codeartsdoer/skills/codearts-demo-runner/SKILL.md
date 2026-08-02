---
name: codearts-demo-runner
description: 在本仓库选择、运行和验收 20 个 CodeArts 客户演示案例；当用户提到案例编号、客户演示、功能验证、Vibe Coding 或 SDD 时使用。
---

# CodeArts 客户演示执行技能

1. 运行 `python3 demo.py codearts list`，确认案例编号和推荐模式。
2. 运行 `python3 demo.py codearts show <ID>`，读取上下文、提示词和验收口径。
3. 按案例卡添加 `#File`、`#Symbol`、`#Git`、`#TerminalLastCommand` 上下文；只引用仓库中真实存在的文件与符号。
4. 案例 13、14、15、17 使用 Spec-Driven，按 spec → design → tasks → implementation 顺序检查；其他案例使用 Vibe-Coding 小步迭代。
5. 修改前说明目标和边界；修改后运行 `python3 demo.py codearts verify <ID>`。
6. 客户演示结束前运行 `python3 demo.py verify --verbose`，保留终端结果作为证据。
7. 如果工具链、登录或真实云资源缺失，清楚标注“本地 Mock 已验证”与“云上联调未验证”，不得混淆。

案例的唯一结构化清单是 `codearts/cases.json`，逐步操作指导见 `docs/CODEARTS-DEMO-GUIDE.md`。
