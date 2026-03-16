from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict


def HttpGet2Obj(url: str, header: Dict[str, str], v: Dict[str, Any]) -> None:
    response = HttpGet(url, header)
    v.clear()
    v.update(response)


def HttpGet(url: str, header: Dict[str, str]) -> Dict[str, Any]:
    req = urllib.request.Request(url=url, method="GET")
    req.add_header("Content-Type", "application/json")
    for k, val in header.items():
        req.add_header(k, val)

    with urllib.request.urlopen(req, timeout=600) as resp:
        if resp.status != 200:
            raise RuntimeError(f"wrong http code{resp.status}")
        body = resp.read()
        return json.loads(body.decode("utf-8"))


def HttpPost(url: str, header: Dict[str, str]) -> Dict[str, Any]:
    req = urllib.request.Request(url=url, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, val in header.items():
        req.add_header(k, val)

    with urllib.request.urlopen(req, timeout=600) as resp:
        if resp.status != 200:
            raise RuntimeError(f"wrong http code{resp.status}")
        body = resp.read()
        return json.loads(body.decode("utf-8"))
