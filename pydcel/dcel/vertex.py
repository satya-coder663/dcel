from typing import List, Tuple, Optional, Iterator

from dcel.point import Point


class Vertex:
    """Represents a vertex in a DCEL with its coordinates and incident half-edges."""
    def __init__(self, x: float, y: float):
        self._point = Point(x, y)
        self.hedgelist = []
        self._index: Optional[int] = None

    @property
    def x(self) -> float:
        return self._point.x

    @property
    def y(self) -> float:
        return self._point.y

    @property
    def coordinates(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property
    def degree(self) -> int:
        """Returns the degree (number of incident edges) of the vertex"""
        return len(self.hedgelist)

    def sortincident(self) -> None:
        """Sorts incident edges counter-clockwise based on their angles."""
        self.hedgelist.sort(key=lambda h: h.angle, reverse=True)

    def __repr__(self) -> str:
        return f"Vertex({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
