"""CodeArts-native case cards and per-case acceptance verification."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple
from urllib.request import Request, urlopen

from .server import make_server

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "codearts" / "cases.json"
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


def load_matrix() -> list[Dict[str, Any]]:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def get_case(case_id: str) -> Dict[str, Any]:
    normalized = str(case_id).zfill(2)
    for case in load_matrix():
        if case["id"] == normalized:
            return case
    raise SystemExit(f"未知 CodeArts 案例 {case_id}；请先运行 python3 demo.py codearts list")


def print_matrix() -> None:
    print("ID  模式          场景                         验收命令")
    print("--  ------------  ---------------------------  --------------------------------------")
    for case in load_matrix():
        print(f"{case['id']}  {case['mode']:<12}  {case['scene']:<27}  {case['acceptance']}")


def show_case(case_id: str, prompt_only: bool = False) -> None:
    case = get_case(case_id)
    if prompt_only:
        print(case["prompt"])
        return
    print(f"CASE {case['id']} · {case['scene']}")
    print(f"码道模式：{case['mode']}")
    print("上下文：")
    for context in case["context"]:
        print(f"  - {context}")
    if case.get("specDir"):
        print(f"SDD 证据链：{case['specDir']}")
    print("演示提示词：")
    print(case["prompt"])
    print(f"验收：{case['acceptance']}")


def _request(base: str, path: str, method: str = "GET", payload: Any = None) -> Tuple[int, Any, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(base + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=3) as response:
        raw = response.read().decode("utf-8")
        content_type = response.headers.get("Content-Type", "")
        body = json.loads(raw) if "application/json" in content_type else raw
        return response.status, response.headers, body


def _assert_contains(text: str, values: Iterable[str]) -> None:
    for value in values:
        if value not in text:
            raise AssertionError(f"页面缺少关键功能标识：{value}")


def _verify_web(case_id: str) -> None:
    server = make_server("127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, _, page = _request(base, WEB_PATHS[case_id])
        if status != 200 or "<!doctype html>" not in page.lower():
            raise AssertionError("演示页面未正常加载")

        if case_id == "07":
            _assert_contains(page, ['id="city"', 'id="rooms"', 'id="slots"', 'id="modal"'])
        elif case_id == "08":
            tools = [{"type": "function", "function": {"name": "get_weather"}}]
            _, headers, first = _request(base, "/v1/chat/completions", "POST", {
                "messages": [{"role": "user", "content": "weather"}], "tools": tools,
            })
            if headers.get("Access-Control-Allow-Origin") != "*":
                raise AssertionError("CORS 响应头缺失")
            call = first["choices"][0]["message"]["tool_calls"][0]
            messages = [
                {"role": "user", "content": "weather"},
                first["choices"][0]["message"],
                {"role": "tool", "tool_call_id": call["id"], "content": "sunny"},
            ]
            _, _, second = _request(base, "/v1/chat/completions", "POST", {"messages": messages, "tools": tools})
            if (first["choices"][0]["finish_reason"], second["choices"][0]["finish_reason"]) != ("tool_calls", "stop"):
                raise AssertionError("Tool Calling 两阶段闭环失败")
            _, headers, stream = _request(base, "/api/chat/stream?message=CodeArts&fast=1")
            if "text/event-stream" not in headers.get("Content-Type", "") or "event: done" not in stream:
                raise AssertionError("SSE 流式闭环失败")
        elif case_id == "09":
            _assert_contains(page, ['id="metrics"', 'id="compare"', 'id="toggle-table"'])
        elif case_id == "11":
            _assert_contains(page, ["localStorage", 'id="json-editor"', 'id="save-mock"', 'id="json-error"'])
        elif case_id == "12":
            _, _, products = _request(base, "/api/ecommerce/products")
            product = products["data"][0]
            _, _, order = _request(base, "/api/ecommerce/orders", "POST", {
                "items": [{"productId": product["id"], "quantity": 1}],
            })
            if order["data"]["total"] <= 0:
                raise AssertionError("下单或库存扣减失败")
        elif case_id == "16":
            _, _, created = _request(base, "/api/agents", "POST", {"name": "CodeArts Demo", "tags": ["制造"]})
            agent_id = created["data"]["id"]
            _, _, published = _request(base, f"/api/agents/{agent_id}/transition", "POST", {"target": "PUBLISHED"})
            if published["data"]["state"] != "PUBLISHED":
                raise AssertionError("智能体生命周期流转失败")
        elif case_id == "18":
            _assert_contains(page, ["ArkTS", "data-buy", 'id="phone-cart"'])
            for source in [ROOT / "harmony" / "EntryAbility.ets", ROOT / "harmony" / "Index.ets"]:
                if source.stat().st_size < 100:
                    raise AssertionError(f"ArkTS 源码不完整：{source}")
        elif case_id == "19":
            _, _, result = _request(base, "/api/metrics/diagnose", "POST", {
                "generationRate": .60, "reworkRate": .10, "violationRate": .08,
            })
            if result["data"]["stage"] != "进化成熟期":
                raise AssertionError("成熟度联合诊断失败")
        elif case_id == "20":
            _, _, result = _request(base, "/api/roi/calculate", "POST", {
                "grossBenefit": 345, "totalCost": 278,
                "generationRate": .71, "reworkRate": .29, "violationRate": .19,
            })
            if round(result["data"]["nec"], 4) != .4083 or round(result["data"]["netRoi"], 4) != -.4933:
                raise AssertionError("NEC 或净 ROI 计算不符合书中样例")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def verify_case(case_id: str) -> bool:
    normalized = get_case(case_id)["id"]
    try:
        if normalized in WEB_PATHS:
            _verify_web(normalized)
        else:
            result = subprocess.run(
                [sys.executable, "demo.py", "case", normalized],
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=30,
            )
            if result.returncode != 0:
                detail = (result.stdout + "\n" + result.stderr).strip()
                raise AssertionError(detail or f"exit={result.returncode}")
        print(f"PASS CodeArts case {normalized}: 功能与验收标准一致")
        return True
    except Exception as exc:  # Keep CLI output concise while preserving a non-zero exit.
        print(f"FAIL CodeArts case {normalized}: {exc}", file=sys.stderr)
        return False
