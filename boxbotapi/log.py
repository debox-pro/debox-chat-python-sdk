from __future__ import annotations

from typing import Protocol


class BotLogger(Protocol):
    def Println(self, *v: object) -> None:
        ...

    def Printf(self, format_str: str, *v: object) -> None:
        ...


def SetLogger(logger: BotLogger) -> None:
    if logger is None:
        raise ValueError("logger is nil")
