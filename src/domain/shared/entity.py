"""Entity - Base class for all Entities"""

from typing import TypeVar, Generic

ID = TypeVar('ID')


class Entity(Generic[ID]):
    def __init__(self, entity_id: ID):
        self._id = entity_id

    @property
    def id(self) -> ID:
        return self._id

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id!r})"
