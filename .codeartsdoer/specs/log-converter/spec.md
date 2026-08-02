# Chrome Tracing 日志转换器 - 需求规格

## 目标

把本地管道分隔日志转换为 `chrome://tracing` 可加载的 JSON，并使异常行不会中断整批转换。

## EARS 需求

- UBIQUITOUS: 日志转换器应输出包含 `traceEvents` 的 Chrome Tracing JSON。
- EVENT-DRIVEN: 当读取到合法日志行时，系统应将时间戳、名称、阶段、进程与线程转换为标准事件。
- UNWANTED: 若日志行字段缺失、类型错误或阶段非法，系统应跳过该行并记录行号和原因。
- STATE-DRIVEN: 当调试模式开启时，系统应逐行输出转换结果。
- OPTIONAL: 在指定输出文件时，系统应以 UTF-8 写入可复现的 JSON。

## 验收标准

1. 示例文件产出 4 条合法事件并跳过 1 条错误记录。
2. 完整事件 `X` 包含 `dur`；开始/结束/瞬时事件不强制包含 `dur`。
3. 空文件生成合法的空 `traceEvents` 数组。

