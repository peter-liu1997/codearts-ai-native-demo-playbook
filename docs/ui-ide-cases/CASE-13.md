# 案例 13：Chrome Tracing 日志转换器

[返回 20 案例截图索引](../UI-IDE-CASE-SCREENSHOTS.md)

## 项目背景

- 业务场景：性能分析需要把文本日志转换为 Chrome Tracing 可读取的 JSON，以便在时间轴中定位耗时事件。
- 原始痛点：日志格式、时间单位和错误行处理若未先定义，转换器即使能运行也可能生成无法追溯或误导分析的结果。
- 演示目标与边界：以需求、设计、任务三件套驱动实现；只处理案例定义的日志格式，不宣称兼容所有生产日志。

## 本案例使用的码道能力

| 维度 | 内容 |
|---|---|
| 工作模式 | 规范驱动模式（Spec-Driven），先消除需求歧义，再进入实现。 |
| 关键上下文 | `#File .codeartsdoer/specs/log-converter/spec.md`、`design.md`、`tasks.md`、`#File data/sample.log`、`#Symbol LogConverter`。 |
| 智能工程动作 | 用 EARS 形式明确需求，将设计映射为任务，再按真实符号完成解析和 Chrome Trace 输出。 |
| 验证与治理 | 逐条检查“需求—设计—任务—测试”覆盖关系，使用 4 条合法记录和 1 条错误记录验证结果。 |
| 客户价值 | 展示码道将文本需求转成可追踪、可验收的确定性交付过程。 |

本页截图来自本案例独立启动的 CodeArts Agent IDE 操作。主文件：`.codeartsdoer/specs/log-converter/spec.md`。

## 步骤 1：打开主文件

检查 EARS 需求。

![案例 13 打开主文件](./case-13-01-source.jpg)

## 步骤 2：码道案例卡

核对 Spec-Driven 证据链。

![案例 13 码道案例卡](./case-13-02-card.jpg)

## 步骤 3：实际运行

查看合法事件、隔离错误和 trace JSON。

![案例 13 实际运行](./case-13-03-run.jpg)

## 步骤 4：独立验收

确认案例级验收 PASS。

![案例 13 独立验收](./case-13-04-verify.jpg)

完成后确认没有遗留案例服务器；Web 案例必须先 `Ctrl+C`，再执行独立验收。
