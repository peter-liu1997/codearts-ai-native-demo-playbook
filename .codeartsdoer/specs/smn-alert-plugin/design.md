# DolphinScheduler SMN 告警插件 - 技术设计

- `SmnConfig` 负责安全配置与格式校验。
- `SmnAlertPlugin` 负责统一发送链路与平台结果映射。
- `MockSmnClient` 负责下载即演示的确定性边界。
- 真实华为云 Java SDK 适配器在客户环境中注入，不在仓库保存任何密钥。
- `send(test=True)` 与 `send(test=False)` 共享实现，避免测试路径与生产路径漂移。

