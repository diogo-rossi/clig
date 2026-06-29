from typing import Protocol


class OutErr(Protocol):
    out: str
    err: str


class CapSys(Protocol):
    def readouterr(self) -> OutErr: ...


def deindent(text: str) -> str:
    return "\n".join(
        [s[4:].rstrip() if s.startswith("    ") else s.rstrip() for s in text.strip().split("\n")]
    )
