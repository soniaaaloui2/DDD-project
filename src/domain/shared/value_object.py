"""Classe de base pour tout les value objects"""

from abc import ABC, abstractmethod
from typing import Any


class ValueObject(ABC):

    __slots__ = ()

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Cannot modify attribute '{name}' - ValueObject is immutable")

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"Cannot delete attribute '{name}' - ValueObject is immutable")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        for slot in self.__slots__:
            try:
                if getattr(self, slot) != getattr(other, slot):
                    return False
            except AttributeError:
                return False
        return True

    def __hash__(self) -> int:
        values = []
        for slot in self.__slots__:
            try:
                values.append(getattr(self, slot))
            except AttributeError:
                pass
        return hash(frozenset((id(v), v) if hasattr(v, '__hash__') else (id(v),) for v in values))

    def __repr__(self) -> str:
        attrs = []
        for slot in self.__slots__:
            try:
                attrs.append(f"{slot}={getattr(self, slot)!r}")
            except AttributeError:
                pass
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    @abstractmethod
    def __str__(self) -> str:
        pass
