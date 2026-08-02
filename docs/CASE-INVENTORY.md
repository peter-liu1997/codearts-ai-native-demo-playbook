# 示例总览与码道能力映射

| ID | 示例 | 来源 | 可演示制品 | 体现的码道能力 |
|---|---|---|---|---|
| 01 | 用户按年龄分组 | PDF 70-72 | Java CLI | 根据注释续写、过滤边界补全、可维护实现 |
| 02 | 库存统计解释、优化与重构 | PDF 72-75 | Java CLI | 代码解释、最小化优化、等价 Stream 重构 |
| 03 | 商品管理项目级生成 | PDF 75-77 | Java 分层程序 + HTTP API | 跨文件生成、Controller/Service/Repository 分层、CRUD |
| 04 | 商品控制器单元测试 | PDF 77-80 | Java 测试程序 | 测试场景设计、正常/异常/边界覆盖、失败自修复 |
| 05 | 代码库上下文问答 | PDF 80-81 | Java 符号索引 + Python CLI | Codebase 索引、真实符号召回、抑制不存在类名幻觉 |
| 06 | 认证超时协同排查 | PDF 95-96 | 上下文组装 CLI | 文件引用、Skill、历史记忆、用户偏好、调用链联合推理 |
| 07 | 会议室预约原型 | PDF 112-115 | 交互 Web | Vibe Coding、多模态草图理解、小时级反馈闭环 |
| 08 | OpenAI 兼容 Mock 与 SSE | PDF 116-120 | HTTP + Web | 协议实现、Tool Calling、CORS 定位、流式改造 |
| 09 | SaaS 产品分析看板 | PDF 121-124 | 交互 Web | 设计规范作为上下文、局部约束修改、图表与交互生成 |
| 10 | 公网资产 TCP 扫描 | PDF 125-127 | Python CLI | 工具脚本、并发与超时补全、成果沉淀为 Skill |
| 11 | API Hub | PDF 127-137 | 交互 Web | 六轮增量 Vibe、Mock、localStorage、导入导出、XSS 防护 |
| 12 | 电商全栈线性演进 | PDF 138-141 | Web + API | 原型到全栈、最小变更、质量门、库存与订单闭环 |
| 13 | Chrome Tracing 日志转换器 | PDF 143-151 | Python CLI + SDD | EARS、Spec/Design/Tasks、编码—测试—修复闭环 |
| 14 | DolphinScheduler SMN 告警插件 | PDF 153-157 | Python插件模型 + SDD | 遗留代码理解、插件式增量、SDK 隔离、Test Send |
| 15 | IAM OIDC 信任委托 | PDF 169-172 | OpenAPI + HTTP + SDD | 高约束需求、接口契约、外部元数据、安全边界、短期凭证 |
| 16 | 制造企业 AI 智能体门户 | PDF 172-176 | Web + API | 零文档意图收敛、文档驱动生成、生命周期、权限与运营 |
| 17 | 设备管理面内存统计 | PDF 176-180 | C11 + SDD | 大仓 Codebase、领域 Skill、阶段 SubAgent、编译自修复 |
| 18 | 鸿蒙云手机电商应用 | PDF 181-194 | ArkTS + Web 模拟器 | ArkTS 生成、声明式 UI、静态检查、端云调试 |
| 19 | AI 编码成熟度指标 | PDF 241-243 | Web + API | 生成率/返工率/违反率联合诊断、组织工程治理 |
| 20 | AI 编程净 ROI | PDF 249, 252-253 | Web + API | NEC 质量修正、全口径成本、情景模拟、商业决策 |

## 能力覆盖矩阵

- 个人效率：01-05。
- 上下文与智能体协作：05-06。
- Vibe Coding 与快速制品：07-12。
- SDD 与确定性交付：13-15、17。
- 行业/生态落地：14-18。
- 组织效能与商业价值：19-20。

原书第 6 章的“电商全栈项目”小节编号重复写成 `6.2`，本仓库按出现顺序将其识别为独立案例 12，不修改原书事实但避免目录冲突。

