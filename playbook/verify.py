"""Cold-start verification across Python, HTTP, Java, C, SDD, and static UI."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"


def _run(label: str, command: List[str], verbose: bool) -> bool:
    print(f"[RUN ] {label}")
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if verbose or result.returncode != 0:
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
    if result.returncode == 0:
        print(f"[PASS] {label}")
        return True
    print(f"[FAIL] {label} (exit={result.returncode})")
    return False


def verify_all(verbose: bool = False) -> bool:
    BUILD.mkdir(parents=True, exist_ok=True)
    checks = []
    checks.append(_run("Python 语法编译", [sys.executable, "-m", "compileall", "-q", "demo.py", "playbook", "tests"], verbose))
    checks.append(_run("Python/HTTP/静态/SDD/CodeArts 测试", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], verbose))

    javac, java = shutil.which("javac"), shutil.which("java")
    if javac and java:
        java_build = BUILD / "java"
        java_build.mkdir(parents=True, exist_ok=True)
        sources = [str(path) for path in sorted((ROOT / "java").glob("*.java"))]
        checks.append(_run("Java 21 编译", [javac, "-encoding", "UTF-8", "-Xlint:all", "-d", str(java_build), *sources], verbose))
        for class_name in ["UserGroupingDemo", "InventoryRefactorDemo", "ProductManagementDemo", "ProductControllerTest"]:
            checks.append(_run(f"Java {class_name}", [java, "-cp", str(java_build), class_name], verbose))
    else:
        print("[FAIL] Java 17+ 工具链缺失（需要 javac/java）")
        checks.append(False)

    compiler = shutil.which("cc") or shutil.which("gcc")
    if compiler:
        binary = BUILD / "device-memory-test"
        checks.append(_run("C11 编译（-Wall -Wextra -Werror）", [
            compiler, "-std=c11", "-Wall", "-Wextra", "-Werror",
            str(ROOT / "device/device_memory.c"), str(ROOT / "device/device_memory_test.c"),
            "-o", str(binary),
        ], verbose))
        checks.append(_run("设备内存 C 单元测试", [str(binary)], verbose))
    else:
        print("[FAIL] C11 工具链缺失（需要 cc/gcc）")
        checks.append(False)

    passed = sum(1 for value in checks if value)
    print(f"\n验收结果：{passed}/{len(checks)} 个验证阶段通过。")
    if all(checks):
        print("全部 20 个案例的共享运行时、原语言样例、交互页面与证据链均通过冷启动验证。")
    return all(checks)
