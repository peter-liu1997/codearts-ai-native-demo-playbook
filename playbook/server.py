"""Unified HTTP server for the browser, API, and protocol demonstrations."""

from __future__ import annotations

import json
import mimetypes
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import parse_qs, unquote, urlparse

from .core import AgentPortal, OidcProviderService, ProductCatalog, calculate_roi, diagnose_maturity, json_response

ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = ROOT / "web"


class DemoState:
    def __init__(self):
        self.products = ProductCatalog()
        self.oidc = OidcProviderService()
        self.agents = AgentPortal()
        self.orders = []


class DemoHandler(BaseHTTPRequestHandler):
    state: DemoState
    server_version = "CodeArtsDemo/1.0"

    ROUTES = {
        "/": "portal.html",
        "/demo/meeting-room": "meeting-room.html",
        "/demo/dashboard": "dashboard.html",
        "/demo/openai-mock": "openai-mock.html",
        "/demo/api-hub": "api-hub.html",
        "/demo/ecommerce": "ecommerce.html",
        "/demo/agent-portal": "agent-portal.html",
        "/demo/harmony": "harmony-shop.html",
        "/demo/metrics": "metrics.html",
        "/demo/roi": "roi.html",
    }

    def log_message(self, fmt: str, *args: Any) -> None:
        # Keep demos quiet while retaining explicit application output.
        if getattr(self.server, "verbose", False):
            super().log_message(fmt, *args)

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _json(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, message: str) -> None:
        self._json(status, json_response(False, None, message))

    def _read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 2_000_000:
            raise ValueError("request body is too large")
        raw = self.rfile.read(length) if length else b"{}"
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("JSON object expected")
        return payload

    def _static(self, relative: str) -> None:
        candidate = (WEB_ROOT / relative).resolve()
        if WEB_ROOT.resolve() not in candidate.parents or not candidate.is_file():
            self._error(HTTPStatus.NOT_FOUND, "resource not found")
            return
        content = candidate.read_bytes()
        media_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        if media_type.startswith("text/") or media_type in {"application/javascript", "application/json"}:
            media_type += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", media_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self._cors()
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path, query = unquote(parsed.path), parse_qs(parsed.query)
        if path in self.ROUTES:
            self._static(self.ROUTES[path])
            return
        if path.startswith("/assets/"):
            self._static(path.removeprefix("/"))
            return
        if path == "/api/cases":
            self._json(200, json.loads((ROOT / "cases.json").read_text(encoding="utf-8")))
            return
        if path in {"/api/products", "/api/ecommerce/products"}:
            self._json(200, json_response(True, self.state.products.list()))
            return
        if path.startswith("/api/products/"):
            self._get_product(path)
            return
        if path == "/api/agents":
            tag = query.get("tag", [""])[0]
            self._json(200, json_response(True, self.state.agents.list(tag)))
            return
        if path == "/api/oidc/providers":
            self._json(200, json_response(True, [vars(row) for row in self.state.oidc.providers.values()]))
            return
        if path == "/api/chat/stream":
            self._stream_chat(query)
            return
        if path == "/api/health":
            self._json(200, {"status": "UP", "examples": 20})
            return
        self._error(HTTPStatus.NOT_FOUND, "route not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            payload = self._read_json()
            if path == "/api/products":
                self._json(201, json_response(True, self.state.products.create(payload)))
            elif path == "/api/ecommerce/orders":
                order = self.state.products.reserve(payload.get("items", []))
                self.state.orders.append(order)
                self._json(201, json_response(True, order))
            elif path == "/api/agents":
                self._json(201, json_response(True, self.state.agents.create(payload)))
            elif path.startswith("/api/agents/") and path.endswith("/transition"):
                agent_id = int(path.split("/")[3])
                self._json(200, json_response(True, self.state.agents.transition(agent_id, str(payload.get("target", "")))))
            elif path == "/api/oidc/providers":
                self._json(201, json_response(True, self.state.oidc.create_provider(payload)))
            elif path.startswith("/api/oidc/providers/") and path.endswith("/exchange"):
                provider_id = path.split("/")[4]
                result = self.state.oidc.exchange(provider_id, str(payload.get("clientId", "")), str(payload.get("subjectToken", "")))
                self._json(200, json_response(True, result))
            elif path == "/v1/chat/completions":
                self._chat_completion(payload)
            elif path == "/api/metrics/diagnose":
                result = diagnose_maturity(float(payload["generationRate"]), float(payload["reworkRate"]), float(payload["violationRate"]))
                self._json(200, json_response(True, result))
            elif path == "/api/roi/calculate":
                result = calculate_roi(
                    float(payload["grossBenefit"]),
                    float(payload["totalCost"]),
                    float(payload["generationRate"]),
                    float(payload["reworkRate"]),
                    float(payload["violationRate"]),
                )
                self._json(200, json_response(True, result))
            else:
                self._error(HTTPStatus.NOT_FOUND, "route not found")
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc))
        except PermissionError as exc:
            self._error(HTTPStatus.FORBIDDEN, str(exc))
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._error(HTTPStatus.BAD_REQUEST, str(exc))

    def do_PUT(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            if not path.startswith("/api/products/"):
                self._error(404, "route not found")
                return
            product_id = int(path.rsplit("/", 1)[1])
            item = self.state.products.update(product_id, self._read_json())
            if item is None:
                self._error(404, "product not found")
            else:
                self._json(200, json_response(True, item))
        except (ValueError, json.JSONDecodeError) as exc:
            self._error(400, str(exc))

    def do_DELETE(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if not path.startswith("/api/products/"):
            self._error(404, "route not found")
            return
        try:
            deleted = self.state.products.delete(int(path.rsplit("/", 1)[1]))
            self._json(200 if deleted else 404, json_response(deleted, {"deleted": deleted}, "" if deleted else "product not found"))
        except ValueError as exc:
            self._error(400, str(exc))

    def _get_product(self, path: str) -> None:
        try:
            product_id = int(path.rsplit("/", 1)[1])
        except ValueError:
            self._error(400, "product id must be an integer")
            return
        item = self.state.products.get(product_id)
        if item is None:
            self._error(404, "product not found")
        else:
            self._json(200, json_response(True, item))

    def _chat_completion(self, payload: Dict[str, Any]) -> None:
        messages = payload.get("messages") or []
        tools = payload.get("tools") or []
        last_role = messages[-1].get("role") if messages else ""
        completion_id = f"chatcmpl-demo-{uuid.uuid4().hex[:10]}"
        if tools and last_role != "tool":
            function = tools[0].get("function", {})
            name = function.get("name", "get_demo_data")
            arguments = {"city": "深圳"} if "weather" in name.lower() else {"query": "演示数据"}
            message: Dict[str, Any] = {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": f"call_{uuid.uuid4().hex[:12]}",
                    "type": "function",
                    "function": {"name": name, "arguments": json.dumps(arguments, ensure_ascii=False)},
                }],
            }
            finish_reason = "tool_calls"
        else:
            tool_message = next((row for row in reversed(messages) if row.get("role") == "tool"), None)
            suffix = f"，工具返回：{tool_message.get('content')}" if tool_message else ""
            message = {"role": "assistant", "content": f"本地 Mock 已完成标准对话闭环{suffix}"}
            finish_reason = "stop"
        response = {
            "id": completion_id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": payload.get("model", "codearts-local-mock"),
            "choices": [{"index": 0, "message": message, "finish_reason": finish_reason}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
        self._json(200, response)

    def _stream_chat(self, query: Dict[str, Any]) -> None:
        message = query.get("message", ["你好"])[0]
        reply = f"已收到：{message}。这是逐字发送的本地 SSE 演示。"
        delay = 0.0 if query.get("fast", ["0"])[0] == "1" else 0.08
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self._cors()
        self.end_headers()
        try:
            for character in reply:
                data = json.dumps({"delta": character}, ensure_ascii=False)
                self.wfile.write(f"data: {data}\n\n".encode("utf-8"))
                self.wfile.flush()
                if delay:
                    time.sleep(delay)
            self.wfile.write(b"event: done\ndata: {}\n\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return


def make_server(host: str = "127.0.0.1", port: int = 8000, verbose: bool = False) -> ThreadingHTTPServer:
    state = DemoState()

    class BoundHandler(DemoHandler):
        pass

    BoundHandler.state = state
    server = ThreadingHTTPServer((host, port), BoundHandler)
    server.verbose = verbose  # type: ignore[attr-defined]
    return server


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = make_server(host, port, verbose=True)
    actual_port = server.server_address[1]
    print(f"CodeArts 客户演示门户已启动：http://{host}:{actual_port}")
    print("按 Ctrl+C 停止。")
    try:
        server.serve_forever()
    finally:
        server.server_close()
