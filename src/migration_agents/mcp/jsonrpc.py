from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class JsonRpcRequest:
    id: Any
    method: str
    params: dict[str, Any] | None


def parse_request(line: str) -> JsonRpcRequest | None:
    if not line.strip():
        return None
    data = json.loads(line)
    return JsonRpcRequest(
        id=data.get("id"),
        method=data.get("method", ""),
        params=data.get("params"),
    )


def write_result(request_id: Any, result: Any) -> None:
    payload = {"jsonrpc": "2.0", "id": request_id, "result": result}
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def write_error(request_id: Any, code: int, message: str) -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def run_stdio(handler: Callable[[JsonRpcRequest], None]) -> None:
    for line in sys.stdin:
        request = parse_request(line)
        if not request:
            continue
        handler(request)
