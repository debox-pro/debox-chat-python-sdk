from __future__ import annotations

import json
from typing import Any, Dict


class Params(dict):
    def AddNonEmpty(self, key: str, value: str) -> None:
        if value != "":
            self[key] = value

    def AddNonZero(self, key: str, value: int) -> None:
        if value != 0:
            self[key] = str(value)

    def AddNonZero64(self, key: str, value: str) -> None:
        if value != "":
            self[key] = value

    def AddBool(self, key: str, value: bool) -> None:
        if value:
            self[key] = "true"

    def AddNonZeroFloat(self, key: str, value: float) -> None:
        if value != 0:
            self[key] = f"{value:.6f}"

    def AddInterface(self, key: str, value: Any) -> None:
        if value is None:
            return
        self[key] = json.dumps(_to_json_compatible(value), ensure_ascii=False, separators=(",", ":"))

    def AddFirstValid(self, key: str, *args: Any) -> None:
        for arg in args:
            if isinstance(arg, bool):
                if arg:
                    self[key] = "true"
                    return
            elif isinstance(arg, int):
                if arg != 0:
                    self[key] = str(arg)
                    return
            elif isinstance(arg, str):
                if arg != "":
                    self[key] = arg
                    return
            elif arg is None:
                continue
            else:
                self[key] = json.dumps(_to_json_compatible(arg), ensure_ascii=False, separators=(",", ":"))
                return


def _to_json_compatible(value: Any) -> Any:
    if hasattr(value, "__dict__"):
        return {
            _camel_to_snake(k): _to_json_compatible(v)
            for k, v in value.__dict__.items()
            if v is not None and v != "" and v != [] and v is not False
        }
    if isinstance(value, dict):
        return {k: _to_json_compatible(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_to_json_compatible(v) for v in value]
    return value


def _camel_to_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


ParamsType = Dict[str, str]
