# 设备管理面内存统计优化 - 增量设计

- 使用固定容量 64 的进程表，避免嵌入式场景动态分配。
- `EXPT_ReportProcessMemory` 采用 upsert 语义，先更新再寻找空槽。
- `EXPT_RemoveProcessMemory` 清空活动标记。
- `EXPT_GetAmountOfMemUseInCpu` 前置检查主进程、空指针和 32 位溢出。
- 重试间隔与次数以常量表达，测试验证窗口为 300 秒。

