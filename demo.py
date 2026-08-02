#!/usr/bin/env python3
"""Unified, dependency-free launcher for all customer demos."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_cases():
    return json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))


def print_cases():
    cases = load_cases()
    print("ID  案例                                形式                 码道能力")
    print("--  ----------------------------------  -------------------  ------------------------------")
    for case in cases:
        print(f"{case['id']}  {case['name']:<34}  {case['type']:<19}  {case['capability']}")


def run_case(case_id, port):
    from playbook.runner import run_case as dispatch

    known = {case["id"] for case in load_cases()}
    normalized = str(case_id).zfill(2)
    if normalized not in known:
        raise SystemExit(f"未知案例 {case_id}；请先运行 python3 demo.py list")
    dispatch(normalized, port=port)


def main():
    parser = argparse.ArgumentParser(description="CodeArts AI-Native 客户演示案例集")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="列出 20 个案例")
    verify = sub.add_parser("verify", help="执行全量冷启动验证")
    verify.add_argument("--verbose", action="store_true")
    serve = sub.add_parser("serve", help="启动统一 Web 演示门户")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--host", default="127.0.0.1")
    case = sub.add_parser("case", help="运行指定案例")
    case.add_argument("id")
    case.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.command == "list":
        print_cases()
    elif args.command == "verify":
        from playbook.verify import verify_all

        raise SystemExit(0 if verify_all(verbose=args.verbose) else 1)
    elif args.command == "serve":
        from playbook.server import serve

        serve(args.host, args.port)
    elif args.command == "case":
        run_case(args.id, args.port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n演示已停止。")
        sys.exit(130)

