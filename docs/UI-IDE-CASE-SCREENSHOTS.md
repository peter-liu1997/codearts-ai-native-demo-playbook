# CodeArts Agent IDE 20 案例逐步截图手册

本册是 [CodeArts Agent IDE UI 客户演示手册](UI-IDE-DEMO.md) 的逐例截图索引。全部 98 张图片来自真实 CodeArts Agent IDE 操作，不是示意图；图片与仓库一起下载，离线也能查看。

为保证 CodeArts IDE 与 CodeArts Repo Markdown 预览稳定，截图按案例分页，并与案例 Markdown 放在同一目录，使用 `./图片名` 引用，避免部分渲染器不支持 `../` 父目录跳转。CLI/SDD 案例每页 4 张，Web 案例每页 6 张。每页均从打开主文件开始，经过码道真实对话与结果、实际运行或内置浏览器交互，最后以独立验收结束。

> 华为云账号套餐已恢复。2026-08-03 已为 20 个案例分别新建码道对话，截图右侧保留真实的文件读取、分析、命令执行与验收结果；程序功能仍以案例级独立验收和全量质量门为最终证据。

## 码道能力口径

为避免演示只展示“生成了代码”，每个案例页都补充了项目背景、演示边界和本案例实际使用的码道能力。能力描述以华为云当前官方文档为口径：

- [探索模式（Vibe-Coding）](https://support.huaweicloud.com/usermanual-codeartssnap/codeartsdoer_ug_0101.html)：用于目标仍需边做边澄清的任务，通过多轮交互快速形成可运行结果。
- 规范驱动模式（Spec-Driven）：用于安全、兼容性或验收要求明确的任务，先形成 `spec.md`、`design.md`、`tasks.md`，再按任务实施和追踪。
- [上下文管理](https://support.huaweicloud.com/usermanual-codeartssnap/codeartsdoer_ug_0009.html)：用 `#File`、`#Folder`、`#Symbol`、`#Git`、`#Terminal Last Command` 等上下文限定证据范围。
- [斜杠命令](https://support.huaweicloud.com/usermanual-codeartssnap/codeartsdoer_ug_0038.html)：本项目用 `/demo-case` 统一 20 个案例的演示提示词、步骤和输出格式。
- [项目 Skill](https://support.huaweicloud.com/usermanual-codeartssnap/codeartsdoer_ug_0024.html)：仓库在 `.codeartsdoer/skills` 中沉淀可复用的排障、验证和交付方法。

每页“客户价值”描述的是该案例能够证明的工程能力。码道对话结果、程序运行结果和独立验收分别截图，避免把 AI 文字结论代替可执行验证。

## 逐例入口

| ID | 案例 | 类型 | 截图 | 分页 |
|---|---|---|---:|---|
| 01 | 用户按年龄分组 | Vibe / Java | 4 | [打开](ui-ide-cases/CASE-01.md) |
| 02 | 库存统计解释、优化与重构 | Vibe / Java | 4 | [打开](ui-ide-cases/CASE-02.md) |
| 03 | 商品管理项目级生成 | Vibe / Java | 4 | [打开](ui-ide-cases/CASE-03.md) |
| 04 | 商品控制器单元测试生成 | Vibe / Java | 4 | [打开](ui-ide-cases/CASE-04.md) |
| 05 | 代码库上下文问答 | Vibe / Python | 4 | [打开](ui-ide-cases/CASE-05.md) |
| 06 | 认证超时协同排查 | Vibe / Python | 4 | [打开](ui-ide-cases/CASE-06.md) |
| 07 | 会议室预约原型 | Vibe / Web | 6 | [打开](ui-ide-cases/CASE-07.md) |
| 08 | OpenAI 兼容 Mock 与 SSE | Vibe / HTTP | 6 | [打开](ui-ide-cases/CASE-08.md) |
| 09 | SaaS 产品分析看板 | Vibe / Web | 6 | [打开](ui-ide-cases/CASE-09.md) |
| 10 | 公网资产 TCP 连通性扫描 | Vibe / Python | 4 | [打开](ui-ide-cases/CASE-10.md) |
| 11 | API Hub 接口管理工具 | Vibe / Web | 6 | [打开](ui-ide-cases/CASE-11.md) |
| 12 | 电商全栈线性演进 | Vibe / Web + API | 6 | [打开](ui-ide-cases/CASE-12.md) |
| 13 | Chrome Tracing 日志转换器 | Spec / Python | 4 | [打开](ui-ide-cases/CASE-13.md) |
| 14 | DolphinScheduler SMN 告警插件 | Spec / Python | 4 | [打开](ui-ide-cases/CASE-14.md) |
| 15 | IAM OIDC 信任委托 | Spec / OpenAPI | 4 | [打开](ui-ide-cases/CASE-15.md) |
| 16 | 制造企业 AI 智能体门户 | Vibe / Web + API | 6 | [打开](ui-ide-cases/CASE-16.md) |
| 17 | 设备管理面内存统计优化 | Spec / C11 | 4 | [打开](ui-ide-cases/CASE-17.md) |
| 18 | 鸿蒙云手机电商应用 | Vibe / ArkTS + Web | 6 | [打开](ui-ide-cases/CASE-18.md) |
| 19 | AI 编码成熟度指标诊断 | Vibe / Web | 6 | [打开](ui-ide-cases/CASE-19.md) |
| 20 | AI 编程净 ROI 测算 | Vibe / Web | 6 | [打开](ui-ide-cases/CASE-20.md) |

## 截图复核清单

- 01–06、10、13–15、17：每例 4 张，共 44 张。
- 07–09、11–12、16、18–20：每例 6 张，共 54 张。
- 总数：98 张。
- 所有服务器均按“单例启动 → 交互 → `Ctrl+C` → 独立验收”执行。
- 20 个案例均已在套餐恢复后重新发起真实码道对话；截图不再使用历史冻结提示。
