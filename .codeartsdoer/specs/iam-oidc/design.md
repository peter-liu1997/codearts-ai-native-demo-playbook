# IAM OIDC 信任委托 - 技术设计

- 契约：`contracts/oidc-provider.openapi.yaml` 固化请求、响应与错误语义。
- 控制面：`OidcProviderService` 维护 Provider 与 Client ID 映射。
- 出站安全：解析 URL 后强制 HTTPS、无凭据、无 query/fragment、主机白名单。
- 指纹：演示模式基于 Issuer 生成 SHA-256；生产模式应读取并验证 TLS 证书链。
- 交换：演示 Token 使用 `demo.` 前缀，输出短期临时凭证；生产应替换为签名与 claims 校验器。

