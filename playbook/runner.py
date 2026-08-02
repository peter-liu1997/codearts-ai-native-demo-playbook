"""Per-case command dispatcher used by ``demo.py case``."""

from __future__ import annotations

import json
import shutil
import socket
import subprocess
import threading
from pathlib import Path

from .core import (
    CodebaseIndex,
    LogConverter,
    MockSmnClient,
    OidcProviderService,
    SmnAlertPlugin,
    SmnConfig,
    TcpScanner,
    assemble_auth_debug_context,
)
from .server import make_server

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
WEB_PATHS = {
    "07": "/demo/meeting-room",
    "08": "/demo/openai-mock",
    "09": "/demo/dashboard",
    "11": "/demo/api-hub",
    "12": "/demo/ecommerce",
    "16": "/demo/agent-portal",
    "18": "/demo/harmony",
    "19": "/demo/metrics",
    "20": "/demo/roi",
}


def _compile_java() -> Path:
    javac = shutil.which("javac")
    if not javac:
        raise SystemExit("案例 01-04 需要 JDK 17+；未找到 javac")
    target = BUILD / "java"
    target.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "java").glob("*.java"))
    subprocess.run([javac, "-encoding", "UTF-8", "-d", str(target), *map(str, sources)], check=True)
    return target


def _run_java(class_name: str) -> None:
    target = _compile_java()
    java = shutil.which("java")
    subprocess.run([java, "-cp", str(target), class_name], check=True)


def _run_web(case_id: str, port: int) -> None:
    server = make_server("127.0.0.1", port, verbose=True)
    actual = server.server_address[1]
    url = f"http://127.0.0.1:{actual}{WEB_PATHS[case_id]}"
    print(f"CASE {case_id} 已启动：{url}")
    print("请在浏览器打开以上地址；按 Ctrl+C 停止。")
    try:
        server.serve_forever()
    finally:
        server.server_close()


def _run_scanner() -> None:
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    open_port = listener.getsockname()[1]
    thread = threading.Thread(target=lambda: listener.accept()[0].close(), daemon=True)
    thread.start()
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    closed_port = probe.getsockname()[1]
    probe.close()
    results = TcpScanner(timeout=0.25).scan_many([("127.0.0.1", open_port), ("127.0.0.1", closed_port)])
    listener.close()
    for row in results:
        print(json.dumps(vars(row), ensure_ascii=False))
    if [row.reachable for row in results] != [True, False]:
        raise SystemExit("TCP 扫描结果不符合预期")
    print("PASS case 10: 并发、超时和开闭端口识别正常")


def _run_c() -> None:
    compiler = shutil.which("cc") or shutil.which("gcc")
    if not compiler:
        raise SystemExit("案例 17 需要 C11 编译器；未找到 cc/gcc")
    target = BUILD / "device-memory-test"
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        compiler,
        "-std=c11",
        "-Wall",
        "-Wextra",
        "-Werror",
        str(ROOT / "device/device_memory.c"),
        str(ROOT / "device/device_memory_test.c"),
        "-o",
        str(target),
    ], check=True)
    subprocess.run([str(target)], check=True)


def run_case(case_id: str, port: int = 8000) -> None:
    if case_id in WEB_PATHS:
        _run_web(case_id, port)
    elif case_id == "01":
        _run_java("UserGroupingDemo")
    elif case_id == "02":
        _run_java("InventoryRefactorDemo")
    elif case_id == "03":
        _run_java("ProductManagementDemo")
    elif case_id == "04":
        _run_java("ProductControllerTest")
    elif case_id == "05":
        index = CodebaseIndex([ROOT / "java"])
        count = index.build()
        print(f"已索引 {count} 个 Java 符号")
        for question in [
            "请解释 ProductService.createProduct 的执行流程",
            "参照 ProductController 的风格定位 CRUD 接口",
        ]:
            print(json.dumps(index.answer(question), ensure_ascii=False, indent=2))
    elif case_id == "06":
        print(json.dumps(assemble_auth_debug_context(), ensure_ascii=False, indent=2))
    elif case_id == "10":
        _run_scanner()
    elif case_id == "13":
        target = BUILD / "sample-trace.json"
        result = LogConverter(debug=True).convert_file(ROOT / "data/sample.log", target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"输出：{target}")
    elif case_id == "14":
        client = MockSmnClient()
        plugin = SmnAlertPlugin(SmnConfig("https://smn.demo.local", "demo-project", "urn:smn:cn-north-4:demo:alerts"), client)
        print(json.dumps(plugin.send("Test Send", "DolphinScheduler SMN 插件连通", test=True), ensure_ascii=False, indent=2))
        print(json.dumps(plugin.send("Workflow Failed", "workflow=customer-demo"), ensure_ascii=False, indent=2))
    elif case_id == "15":
        service = OidcProviderService()
        provider = service.create_provider({"issuer": "https://idp.demo.local", "clientIds": ["workload-demo"]})
        credential = service.exchange(provider["id"], "workload-demo", "demo.signed.subject")
        print(json.dumps({"provider": provider, "temporaryCredential": credential}, ensure_ascii=False, indent=2))
    elif case_id == "17":
        _run_c()
    else:
        raise SystemExit(f"案例 {case_id} 尚未配置运行入口")

