# 案例 15：IAM OIDC 信任委托

[返回 20 案例截图索引](../UI-IDE-CASE-SCREENSHOTS.md)

本页截图来自本案例独立启动的 CodeArts Agent IDE 操作。主文件：`contracts/oidc-provider.openapi.yaml`。

## 步骤 1：打开主文件

查看接口契约。

![案例 15 打开主文件](./case-15-01-source.jpg)

## 步骤 2：码道案例卡

核对 Spec-Driven 安全上下文。

![案例 15 码道案例卡](./case-15-02-card.jpg)

## 步骤 3：实际运行

创建 Provider 并交换演示临时凭证。

![案例 15 实际运行](./case-15-03-run.jpg)

## 步骤 4：独立验收

确认 HTTPS、Client ID 和 SSRF 边界。

![案例 15 独立验收](./case-15-04-verify.jpg)

完成后确认没有遗留案例服务器；Web 案例必须先 `Ctrl+C`，再执行独立验收。

