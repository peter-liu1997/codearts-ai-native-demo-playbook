---
description: 执行案例级和全量功能验证并报告证据
---

若用户给出了案例编号，先运行 `python3 demo.py codearts verify <ID>`；随后运行 `python3 demo.py verify --verbose`。报告命令、退出码、关键行为与边界。任何失败都必须如实列出，不得宣称通过。
