# DolphinScheduler SMN 告警插件 - 需求规格

- 插件应作为独立 `SMN Alert` 类型进入现有告警实例配置。
- 插件应使用 HTTPS Endpoint、Project ID、Topic URN 和 AK/SK 配置。
- `Test Send` 与真实告警应复用同一发送链路，仅标识不同运行模式。
- 配置错误应在发送前失败，不得向外部端点发送半成品请求。
- 默认演示必须使用内存 Mock Client，不依赖真实 AK/SK；真实 SDK 只能通过显式适配器启用。

验收：配置校验、Test Send、真实告警、消息 ID 回传和错误分支均有自动化测试。

