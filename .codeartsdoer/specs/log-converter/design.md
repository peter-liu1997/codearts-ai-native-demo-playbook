# Chrome Tracing 日志转换器 - 技术设计

- 输入层逐行读取 UTF-8 文本，忽略空行与 `#` 注释。
- 解析层按 `timestamp|name|phase|pid|tid|duration` 拆分，并对 `B/E/X/i` 做白名单校验。
- 模型层输出 Chrome Trace Event；`X` 阶段映射 `dur`。
- 错误层将异常隔离到 `errors`，不污染合法事件。
- 输出层采用 `ensure_ascii=False`，方便客户查看中文事件名。
- 测试覆盖正常、异常、空输入和文件写入。

