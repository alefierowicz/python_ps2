from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Serializable: ...
