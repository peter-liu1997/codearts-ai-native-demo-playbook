# 案例 10：公网资产 TCP 连通性扫描

[返回 20 案例截图索引](../UI-IDE-CASE-SCREENSHOTS.md)

本页截图来自本案例独立启动的 CodeArts Agent IDE 操作。主文件：`playbook/core.py`。

## 步骤 1：打开主文件

定位 TcpScanner。

![案例 10 打开主文件](./case-10-01-source.jpg)

## 步骤 2：码道案例卡

确认只扫描本机授权端口。

![案例 10 码道案例卡](./case-10-02-card.jpg)

## 步骤 3：实际运行

观察本地开端口与闭端口结果。

![案例 10 实际运行](./case-10-03-run.jpg)

## 步骤 4：独立验收

确认案例级验收 PASS。

![案例 10 独立验收](./case-10-04-verify.jpg)

完成后确认没有遗留案例服务器；Web 案例必须先 `Ctrl+C`，再执行独立验收。

