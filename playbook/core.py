"""Business logic shared by the CLI, HTTP server, and verification suite.

The module intentionally uses only Python's standard library. The demo package can
therefore be cloned and exercised without package installation or cloud credentials.
Cloud-facing examples expose a deterministic mock boundary plus an optional real
adapter point, so the customer demonstration is repeatable and safe.
"""

from __future__ import annotations

import concurrent.futures
import csv
import hashlib
import json
import re
import socket
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
from urllib.parse import urlparse


# Cases 01-02: local code generation and refactoring -------------------------


@dataclass(frozen=True)
class User:
    name: str
    age: Optional[int]


def group_users_by_age(users: Optional[Iterable[Optional[User]]]) -> Dict[int, List[User]]:
    """Group valid users by non-negative age and never return ``None``."""

    result: Dict[int, List[User]] = {}
    for user in users or []:
        if user is None or user.age is None or user.age < 0:
            continue
        result.setdefault(user.age, []).append(user)
    return result


def calculate_category_inventory(
    inventory: Optional[Mapping[str, Optional[int]]],
    categories: Optional[Mapping[str, Optional[str]]],
    category: Optional[str],
) -> int:
    """Refactored single-pass implementation of the deeply nested book sample."""

    if inventory is None or categories is None or category is None:
        return 0
    return sum(
        count
        for product_id, count in inventory.items()
        if count is not None and categories.get(product_id) == category
    )


# Cases 03-05: project-level CRUD, tests, and repository context -------------


@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], product_id: int) -> "Product":
        name = str(payload.get("name", "")).strip()
        if not name:
            raise ValueError("name is required")
        price = float(payload.get("price", 0))
        stock = int(payload.get("stock", 0))
        if price < 0 or stock < 0:
            raise ValueError("price and stock must be non-negative")
        return cls(product_id, name, price, stock)


class ProductCatalog:
    """Thread-safe in-memory repository used by generated REST examples."""

    def __init__(self):
        self._lock = threading.RLock()
        self._next_id = 3
        self._products: Dict[int, Product] = {
            1: Product(1, "AI 开发套件", 299.0, 12),
            2: Product(2, "企业云沙箱", 599.0, 8),
        }

    def list(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [asdict(item) for item in sorted(self._products.values(), key=lambda x: x.id)]

    def get(self, product_id: int) -> Optional[Dict[str, Any]]:
        with self._lock:
            item = self._products.get(product_id)
            return asdict(item) if item else None

    def create(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        with self._lock:
            item = Product.from_payload(payload, self._next_id)
            self._products[item.id] = item
            self._next_id += 1
            return asdict(item)

    def update(self, product_id: int, payload: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        with self._lock:
            if product_id not in self._products:
                return None
            item = Product.from_payload(payload, product_id)
            self._products[product_id] = item
            return asdict(item)

    def delete(self, product_id: int) -> bool:
        with self._lock:
            return self._products.pop(product_id, None) is not None

    def reserve(self, items: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
        """Atomically reserve inventory for the e-commerce checkout demo."""

        with self._lock:
            requested: List[Tuple[Product, int]] = []
            for row in items:
                product_id, quantity = int(row["productId"]), int(row["quantity"])
                product = self._products.get(product_id)
                if product is None:
                    raise ValueError(f"product {product_id} not found")
                if quantity <= 0 or product.stock < quantity:
                    raise ValueError(f"insufficient stock for product {product_id}")
                requested.append((product, quantity))
            total = 0.0
            for product, quantity in requested:
                product.stock -= quantity
                total += product.price * quantity
            return {"orderId": f"ORD-{uuid.uuid4().hex[:8].upper()}", "total": round(total, 2)}


JAVA_SYMBOL = re.compile(
    r"\b(?:public|protected|private)?\s*(?:static\s+)?(?:[A-Za-z_$][\w$<>?,\[\]. ]*\s+)?"
    r"(?P<name>[A-Za-z_$][\w$]*)\s*\([^;{}]*\)\s*\{"
)


class CodebaseIndex:
    """Small deterministic symbol index that makes the context demo observable."""

    def __init__(self, roots: Sequence[Path]):
        self.roots = list(roots)
        self.symbols: Dict[str, List[str]] = {}

    def build(self) -> int:
        self.symbols.clear()
        for root in self.roots:
            for path in root.rglob("*.java"):
                text = path.read_text(encoding="utf-8")
                for match in JAVA_SYMBOL.finditer(text):
                    self.symbols.setdefault(match.group("name"), []).append(str(path))
        return sum(len(paths) for paths in self.symbols.values())

    def answer(self, question: str) -> Dict[str, Any]:
        tokens = re.findall(r"[A-Za-z_$][\w$]*", question)
        matched = {token: self.symbols[token] for token in tokens if token in self.symbols}
        if "createProduct" in matched:
            answer = "createProduct 校验名称、价格和库存后写入线程安全的内存仓库，并返回统一 JSON 数据。"
        elif "ProductController" in matched:
            answer = "ProductController 暴露列表、按 ID 查询、新增、修改和删除接口；业务状态统一转换为 JSON/HTTP 状态。"
        else:
            answer = "已依据真实符号索引定位相关文件；未命中的类或方法不会被编造。"
        return {"question": question, "matchedSymbols": matched, "answer": answer}


# Case 06: context assembly and repeat debugging -----------------------------


def assemble_auth_debug_context() -> Dict[str, Any]:
    """Expose each context contribution from the book's auth timeout example."""

    sources = [
        {"kind": "file", "content": "src/auth/oauth.py: EXPIRY_DELTA = 60"},
        {"kind": "skill", "content": "Debug: reproduce -> inspect state -> isolate dependency -> verify"},
        {"kind": "memory", "content": "上一轮已将 EXPIRY_DELTA 从 30 调整为 60，超时仍存在"},
        {"kind": "preference", "content": "使用 pdb 调试"},
        {"kind": "project", "content": "refresh_token 调用链: jwt.decode -> redis.get"},
    ]
    plan = ["确认 EXPIRY_DELTA 当前值", "在 refresh_token 路径增加 pdb 断点", "检查 Redis TTL 与连接状态"]
    conclusion = "应用令牌期限已延长，但 Redis 键 TTL 仍为 30 秒；应统一两处过期策略并补充回归测试。"
    return {"sources": sources, "plan": plan, "conclusion": conclusion}


# Case 10: security asset scanning -------------------------------------------


@dataclass
class ScanResult:
    ip_address: str
    port: int
    reachable: bool
    elapsed_ms: int
    error: str = ""


class TcpScanner:
    def __init__(self, timeout: float = 0.4, workers: int = 16):
        self.timeout = timeout
        self.workers = workers

    def scan_one(self, host: str, port: int) -> ScanResult:
        started = time.perf_counter()
        try:
            with socket.create_connection((host, int(port)), timeout=self.timeout):
                reachable, error = True, ""
        except OSError as exc:
            reachable, error = False, str(exc)
        elapsed = int((time.perf_counter() - started) * 1000)
        return ScanResult(host, int(port), reachable, elapsed, error)

    def scan_many(self, targets: Sequence[Tuple[str, int]]) -> List[ScanResult]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = [pool.submit(self.scan_one, host, port) for host, port in targets]
            return [future.result() for future in futures]

    @staticmethod
    def load_csv(path: Path) -> List[Tuple[str, int]]:
        with path.open(encoding="utf-8", newline="") as stream:
            return [(row["ip_address"], int(row["port"])) for row in csv.DictReader(stream)]


# Case 13: EARS-driven log conversion ----------------------------------------


class LogConverter:
    """Convert pipe-delimited events to Chrome Tracing JSON."""

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.errors: List[str] = []

    def convert_lines(self, lines: Iterable[str]) -> Dict[str, Any]:
        events: List[Dict[str, Any]] = []
        self.errors.clear()
        for line_number, raw in enumerate(lines, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                timestamp, name, phase, pid, tid, duration = [part.strip() for part in line.split("|")]
                if phase not in {"B", "E", "X", "i"}:
                    raise ValueError("phase must be B, E, X, or i")
                event: Dict[str, Any] = {
                    "name": name,
                    "ph": phase,
                    "ts": int(timestamp),
                    "pid": int(pid),
                    "tid": int(tid),
                }
                if phase == "X":
                    event["dur"] = int(duration)
                elif duration not in {"", "0"}:
                    event["args"] = {"duration_hint_us": int(duration)}
                events.append(event)
                if self.debug:
                    print(f"line {line_number}: accepted {name}")
            except (TypeError, ValueError) as exc:
                self.errors.append(f"line {line_number}: {exc}")
        return {"traceEvents": events, "displayTimeUnit": "ms", "metadata": {"skippedLines": len(self.errors)}}

    def convert_file(self, source: Path, target: Path) -> Dict[str, Any]:
        result = self.convert_lines(source.read_text(encoding="utf-8").splitlines())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result


# Case 14: DolphinScheduler-style SMN plugin boundary ------------------------


@dataclass(frozen=True)
class SmnConfig:
    endpoint: str
    project_id: str
    topic_urn: str
    access_key: str = "DEMO_AK"
    secret_key: str = "DEMO_SK"

    def validate(self) -> None:
        if not self.endpoint.startswith("https://"):
            raise ValueError("SMN endpoint must use HTTPS")
        if not self.project_id or not self.topic_urn.startswith("urn:smn:"):
            raise ValueError("project_id and a valid topic_urn are required")


class MockSmnClient:
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []

    def publish(self, topic_urn: str, subject: str, message: str) -> str:
        message_id = f"smn-{uuid.uuid4().hex[:12]}"
        self.messages.append({"id": message_id, "topic": topic_urn, "subject": subject, "message": message})
        return message_id


class SmnAlertPlugin:
    """A portable reproduction of plugin configuration, Test Send, and alert reuse."""

    def __init__(self, config: SmnConfig, client: Optional[MockSmnClient] = None):
        config.validate()
        self.config = config
        self.client = client or MockSmnClient()

    def send(self, subject: str, body: str, test: bool = False) -> Dict[str, Any]:
        message_id = self.client.publish(self.config.topic_urn, subject, body)
        return {"success": True, "mode": "TEST_SEND" if test else "ALERT", "messageId": message_id}


# Case 15: OIDC trust delegation ---------------------------------------------


@dataclass
class OidcProvider:
    id: str
    issuer: str
    client_ids: List[str]
    fingerprint: str
    fingerprint_source: str


class OidcProviderService:
    """Contract-first provider registry with conservative outbound URL controls."""

    def __init__(self, allowed_hosts: Optional[Sequence[str]] = None):
        self.allowed_hosts = set(allowed_hosts or ["idp.demo.local", "accounts.example.com"])
        self.providers: Dict[str, OidcProvider] = {}

    def _validate_issuer(self, issuer: str) -> None:
        parsed = urlparse(issuer)
        if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("issuer must be a clean HTTPS URL")
        if parsed.hostname not in self.allowed_hosts:
            raise ValueError("issuer host is not on the outbound allowlist")

    def create_provider(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        issuer = str(payload.get("issuer", "")).rstrip("/")
        self._validate_issuer(issuer)
        clients = sorted({str(value).strip() for value in payload.get("clientIds", []) if str(value).strip()})
        if not clients:
            raise ValueError("at least one clientId is required")
        manual = str(payload.get("fingerprint", "")).replace(":", "").upper()
        if manual:
            if not re.fullmatch(r"[0-9A-F]{40,64}", manual):
                raise ValueError("fingerprint must be a SHA-1/SHA-256 hex digest")
            fingerprint, source = manual, "manual"
        else:
            # In production this digest is derived from the TLS certificate chain.
            fingerprint = hashlib.sha256(issuer.encode("utf-8")).hexdigest().upper()
            source = "auto-demo"
        provider_id = f"oidc-{uuid.uuid4().hex[:10]}"
        provider = OidcProvider(provider_id, issuer, clients, fingerprint, source)
        self.providers[provider_id] = provider
        return asdict(provider)

    def exchange(self, provider_id: str, client_id: str, subject_token: str) -> Dict[str, Any]:
        provider = self.providers.get(provider_id)
        if provider is None:
            raise KeyError("provider not found")
        if client_id not in provider.client_ids:
            raise PermissionError("clientId is not trusted by this provider")
        if not subject_token.startswith("demo."):
            raise PermissionError("subject token validation failed")
        digest = hashlib.sha256(f"{provider_id}:{client_id}:{subject_token}".encode()).hexdigest()
        return {
            "accessKeyId": f"TMP{digest[:14].upper()}",
            "secretAccessKey": f"demo-{digest[14:42]}",
            "securityToken": digest[42:],
            "expiresIn": 900,
        }


# Case 16: enterprise agent portal -------------------------------------------


@dataclass
class AgentRecord:
    id: int
    name: str
    description: str
    tags: List[str]
    state: str = "DRAFT"


class AgentPortal:
    TRANSITIONS = {"DRAFT": {"PUBLISHED"}, "PUBLISHED": {"OFFLINE"}, "OFFLINE": {"PUBLISHED"}}

    def __init__(self):
        self._lock = threading.RLock()
        self._next_id = 3
        self._agents: Dict[int, AgentRecord] = {
            1: AgentRecord(1, "设备故障诊断", "根据日志给出排障顺序", ["制造", "运维"], "PUBLISHED"),
            2: AgentRecord(2, "质量报告助手", "汇总产线质量指标", ["质量", "分析"], "DRAFT"),
        }

    def list(self, tag: str = "") -> List[Dict[str, Any]]:
        with self._lock:
            rows = self._agents.values()
            if tag:
                rows = [row for row in rows if tag in row.tags]
            return [asdict(row) for row in rows]

    def create(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        name = str(payload.get("name", "")).strip()
        if not name:
            raise ValueError("name is required")
        with self._lock:
            row = AgentRecord(
                self._next_id,
                name,
                str(payload.get("description", "")).strip(),
                [str(tag) for tag in payload.get("tags", [])],
            )
            self._agents[row.id] = row
            self._next_id += 1
            return asdict(row)

    def transition(self, agent_id: int, target: str) -> Dict[str, Any]:
        target = target.upper()
        with self._lock:
            row = self._agents.get(agent_id)
            if row is None:
                raise KeyError("agent not found")
            if target not in self.TRANSITIONS[row.state]:
                raise ValueError(f"illegal transition {row.state} -> {target}")
            row.state = target
            return asdict(row)


# Case 17: embedded device memory accounting ---------------------------------


class DeviceMemoryTracker:
    """Reference model for primary-process-only memory accounting."""

    def __init__(self, rtos_base_mb: int, service_base_mb: int, is_primary: bool = True):
        self.rtos_base_mb = rtos_base_mb
        self.service_base_mb = service_base_mb
        self.is_primary = is_primary
        self._processes: Dict[int, int] = {}

    def report(self, process_id: int, memory_mb: int) -> None:
        if memory_mb < 0:
            raise ValueError("memory must be non-negative")
        self._processes[process_id] = memory_mb

    def process_exit(self, process_id: int) -> None:
        self._processes.pop(process_id, None)

    def total(self) -> int:
        if not self.is_primary:
            raise PermissionError("memory total is only available in the primary process")
        return self.rtos_base_mb + self.service_base_mb + sum(self._processes.values())

    @staticmethod
    def retry_schedule(max_retries: int = 300, interval_seconds: int = 1) -> Dict[str, int]:
        return {"maxRetries": max_retries, "intervalSeconds": interval_seconds, "windowSeconds": max_retries * interval_seconds}


# Cases 19-20: maturity and ROI ----------------------------------------------


def diagnose_maturity(generation_rate: float, rework_rate: float, violation_rate: float) -> Dict[str, str]:
    for value in (generation_rate, rework_rate, violation_rate):
        if not 0 <= value <= 1:
            raise ValueError("rates must be between 0 and 1")
    high_generation = generation_rate >= 0.55
    high_rework = rework_rate >= 0.20
    high_violation = violation_rate >= 0.20
    if high_generation and high_rework and high_violation:
        return {"stage": "生成膨胀期", "risk": "技术债务加速累积", "action": "重建 Code Review 质量门并前移规范预检"}
    if generation_rate >= 0.35 and not high_rework and high_violation:
        return {"stage": "规范内耗期", "risk": "合规修正成本高", "action": "结构化企业规范并注入知识库"}
    if not high_generation:
        return {"stage": "工具观望期", "risk": "ROI 低与上下文不匹配", "action": "改善集成、构建代码库索引并建立信任"}
    return {"stage": "进化成熟期", "risk": "状态漂移", "action": "持续监控、季度归因与模型对比"}


def calculate_roi(gross_benefit: float, total_cost: float, generation_rate: float, rework_rate: float, violation_rate: float) -> Dict[str, float]:
    if gross_benefit < 0 or total_cost <= 0:
        raise ValueError("gross benefit must be non-negative and total cost must be positive")
    for value in (generation_rate, rework_rate, violation_rate):
        if not 0 <= value <= 1:
            raise ValueError("rates must be between 0 and 1")
    nec = generation_rate * (1 - rework_rate) * (1 - violation_rate)
    net_benefit = gross_benefit * nec
    roi = (net_benefit - total_cost) / total_cost
    return {"nec": round(nec, 4), "netBenefit": round(net_benefit, 2), "netRoi": round(roi, 4)}


def json_response(ok: bool, data: Any = None, message: str = "") -> Dict[str, Any]:
    return {"success": ok, "data": data, "message": message}

