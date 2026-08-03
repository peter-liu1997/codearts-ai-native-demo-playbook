# 功能验证报告

验证日期：2026-08-03（Asia/Shanghai）  
验证范围：套餐恢复后的当前工作树；推送后由 GitHub Actions 从远端冷启动复验

## 结论

- 20/20 个案例的独立验收命令全部通过。
- 全量冷启动质量门 9/9 阶段通过。
- 23 项 Python 单元/HTTP/静态/SDD/CodeArts/UI 文档与截图契约测试通过。
- 4 个 Java 程序完成编译和执行。
- C11 设备内存案例在 `-Wall -Wextra -Werror` 下编译并通过测试。
- 项目已在本机 CodeArts Agent IDE 中打开；20 个案例均分别新建真实码道对话，并完成文件读取、分析、命令执行和验收结果截取。
- IDE 的 `#` 上下文菜单已显示当前文件、File、Folder、Git、Terminal、Problems、Knowledge Bases 和 Rules。
- IDE 内置简单浏览器完成案例 07 的会议室、09:30–10:00 时段、二次确认和预约成功交互。
- 20 个案例均从打开主文件开始重新操作并截图：CLI/SDD 每例 4 张、Web 每例 6 张，共 98 张真实 IDE 截图；全部图片随仓库离线交付。
- GitHub Actions 从远端全新检出后复验：[verify-all-demos 工作流](https://github.com/peter-liu1997/codearts-ai-native-demo-playbook/actions/workflows/verify.yml)。

## 验证环境

- macOS arm64
- Python 3.9.6
- Eclipse Temurin OpenJDK 21.0.11 LTS
- Apple clang 21.0.0
- CodeArts Agent 桌面客户端

## 执行命令

逐案例验收：

```bash
for case_id in $(seq -w 1 20); do
  python3 demo.py codearts verify "$case_id" || exit 1
done
```

全量质量门：

```bash
python3 demo.py verify --verbose
```

CodeArts Agent IDE 集成终端抽检：

```bash
python3 demo.py codearts list
python3 demo.py codearts verify 13
```

## 覆盖范围

| 范围 | 结果 | 主要证据 |
|---|---:|---|
| 案例卡完整性 | 20/20 | ID、模式、上下文、提示词、验收命令 |
| Python 与 HTTP | 通过 | CRUD、库存原子扣减、Tool Calling、SSE、CORS、OIDC、生命周期、指标、ROI |
| 静态 Web | 通过 | 10 个页面自包含、关键交互结构存在、无外部 CDN |
| Java | 4/4 | 用户分组、库存重构、商品管理、控制器测试 |
| C11 | 通过 | 严格编译、进程 upsert/退出、主进程保护 |
| SDD | 4/4 | 日志转换、SMN、IAM OIDC、设备内存的 spec/design/tasks |
| CodeArts 项目资产 | 通过 | `AGENTS.md`、Project Skill、自定义命令、`.cloudbuild/build.yml` |
| CodeArts IDE UI | 通过 | 20 个独立码道对话、项目浏览、上下文读取、命令执行、集成终端和内置浏览器交互 |
| 逐例截图证据 | 20/20 | 98 张 IDE 截图，覆盖主文件、码道对话与结果、运行、Web 交互和独立验收 |
| GitHub 冷启动 | 通过 | Ubuntu Runner 全量验证成功 |

## 尚未宣称通过的边界

- 码道对话与本地功能验收已通过；CodeArts Repo 导入、CodeArts Build 及真实云服务资源仍需在客户授权环境单独验证。
- CodeArts Repo 导入和 CodeArts Build 云上任务需要登录后创建项目资源；仓库已提供 `.cloudbuild/build.yml`，但在实际云上执行前不宣称流水线已通过。
- SMN、OIDC、鸿蒙云手机默认使用安全 Mock 或本地替身；真实云资源联调需在客户授权环境另行验证。
