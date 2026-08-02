# CodeArts Agent 项目规则

本仓库用于客户演示华为云码道（CodeArts Agent）的 AI 原生开发能力。回答和修改必须可验证、可复现，并严格限定在当前案例范围内。

## 工作约定

- 开始前先确认案例 ID，并运行 `python3 demo.py codearts show <ID>` 读取模式、上下文、提示词和验收命令。
- 案例 13、14、15、17 使用 Spec-Driven；先核对 `.codeartsdoer/specs/<name>/spec.md`、`design.md`、`tasks.md`，再改代码。
- 其他案例使用 Vibe-Coding，小步修改、即时运行，避免无关重构。
- 优先引用项目内真实上下文：`#File`、`#Symbol`、`#Git`、`#TerminalLastCommand`。找不到符号时明确说明，不得臆造代码、日志、客户数据或云资源状态。
- 默认使用本地 Mock；不得提交 AK/SK、Token、Cookie、真实客户数据或未经授权的公网扫描目标。
- 保持 Python 标准库、Java 17+、C11 和无构建 Web 页面可冷启动。引入外部依赖前必须说明理由和演示影响。
- 修改后先执行案例验收 `python3 demo.py codearts verify <ID>`；交付前执行 `python3 demo.py verify --verbose`。
- 只有命令退出码为 0 且预期行为得到验证，才能声明“已完成”或“已通过”。

## 输出格式

用中文先给结论，再列出修改文件、验证命令、结果和仍存在的真实环境边界。涉及安全、成本、商业指标时，显式区分事实、演示假设与推断。
