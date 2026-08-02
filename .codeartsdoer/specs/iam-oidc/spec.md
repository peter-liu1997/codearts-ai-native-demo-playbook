# IAM OIDC 信任委托 - 需求规格

- 控制面应允许创建 OIDC Provider，并限定 HTTPS Issuer、Client ID 和证书指纹。
- 外部元数据获取只能访问显式允许的 IdP 主机，禁止用户信息、查询串与任意跳转。
- 公共 IdP 可自动生成演示指纹；企业自建 CA 可提交 SHA-1/SHA-256 手工指纹。
- 令牌交换应验证 Provider、Client ID 与 Subject Token，成功后只返回 15 分钟临时凭证。
- 失败响应应可诊断但不泄露内部堆栈、密钥或网络拓扑。

