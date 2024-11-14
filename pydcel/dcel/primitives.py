from functools import cached_property
import math
from typing import Iterator, Optional, Tuple

from dcel.point import Point
from dcel.utils import signed_area
from dcel.vertex import Vertex


class HalfEdge:
    """Represents a half-edge (directed edge) in the DCEL."""
    def __init__(self, v1: Vertex, v2: Vertex):
        self.origin = v1
        self.twin: Optional[HalfEdge] = None
        self.face: Optional['Face'] = None
        self.nexthedge: Optional[HalfEdge] = None
        self.prevhedge: Optional[HalfEdge] = None
        self._destination = v2

    @property
    def destination(self) -> Vertex:
        """Returns the destination vertex of the half-edge"""
        return self.twin.origin if self.twin else self._destination

    @cached_property
    def length(self) -> float:
        """Computes and caches the length of the edge."""
        return self.origin._point.distance_to(self.destination._point)

    @cached_property
    def angle(self) -> float:
        """Computes and caches the angle of the edge with respect to the x-axis."""
        dx = self.destination.x - self.origin.x
        dy = self.destination.y - self.origin.y
        angle = math.atan2(dy, dx)
        return angle if angle >= 0 else angle + 2 * math.pi

    @property
    def midpoint(self) -> Point:
        """Returns the midpoint of the edge"""
        return Point(
            (self.origin.x + self.destination.x) / 2,
            (self.origin.y + self.destination.y) / 2
        )

    def __repr__(self) -> str:
        return f"HalfEdge({self.origin} -> {self.destination})"
        

class Face:
    """Represents a face (polygon) in the DCEL."""
    def __init__(self):
        self.wedge: Optional[HalfEdge] = None
        self.external: bool = False
        self._cached_properties = {}

    @cached_property
    def area(self) -> float:
        """Calculates the signed area of the polygon."""
        if not self.wedge:
            return 0.0
            
        area = 0.0
        for v1, v2 in self.edge_vertices():
            area += (v1.x * v2.y) - (v2.x * v1.y)
        return abs(area) / 2

    @cached_property
    def perimeter(self) -> float:
        """Calculates the perimeter of the polygon."""
        return sum(edge.length for edge in self.edges())

    @cached_property
    def centroid(self) -> Point:
        """Calculates the centroid (center of mass) of the polygon."""
        if not self.wedge:
            raise ValueError("Face has no edges")
            
        area = self.area
        if area == 0:
            raise ValueError("Face has zero area")

        cx = cy = 0.0
        for v1, v2 in self.edge_vertices():
            factor = (v1.x * v2.y) - (v2.x * v1.y)
            cx += (v1.x + v2.x) * factor
            cy += (v1.y + v2.y) * factor

        factor = 1.0 / (6.0 * area)
        return Point(cx * factor, cy * factor)

    def vertices(self) -> Iterator[Vertex]:
        """Yields vertices of the face in counter-clockwise order."""
        if not self.wedge:
            return
        
        start = self.wedge
        current = start
        while True:
            yield current.origin
            current = current.nexthedge
            if current is start:
                break

    def edges(self) -> Iterator[HalfEdge]:
        """Yields half-edges of the face in counter-clockwise order."""
        if not self.wedge:
            return
            
        start = self.wedge
        current = start
        while True:
            yield current
            current = current.nexthedge
            if current is start:
                break

    def edge_vertices(self) -> Iterator[Tuple[Vertex, Vertex]]:
        """Yields pairs of vertices forming edges."""
        for edge in self.edges():
            yield edge.origin, edge.destination

    def isinside(self, point: Tuple[float, float]) -> bool:
        """Determines if a point is inside the face using the winding number algorithm.
        Also handles points exactly on edges or vertices."""
        
        for edge in self.edges():
            if (point[0] == edge.origin.x and point[1] == edge.origin.y) or \
            (point[0] == edge.destination.x and point[1] == edge.destination.y):
                return True
                
            if self._point_on_edge(point, edge):
                return True
        
        # Not on boundary: use winding number algorithm
        winding_number = 0
        for v1, v2 in self.edge_vertices():
            if v1.y <= point[1]:
                if v2.y > point[1]:
                    if signed_area((v1.x, v1.y), (v2.x, v2.y), point) > 0:
                        winding_number += 1
            else:
                if v2.y <= point[1]:
                    if signed_area((v1.x, v1.y), (v2.x, v2.y), point) < 0:
                        winding_number -= 1
        return winding_number != 0

    def _point_on_edge(self, point: Tuple[float, float], edge: HalfEdge) -> bool:
        """Helper method to determine if a point lies exactly on an edge."""

        x_min = min(edge.origin.x, edge.destination.x)
        x_max = max(edge.origin.x, edge.destination.x)
        y_min = min(edge.origin.y, edge.destination.y)
        y_max = max(edge.origin.y, edge.destination.y)
        
        
        if not (x_min <= point[0] <= x_max and y_min <= point[1] <= y_max):
            return False
        
        if edge.origin.x == edge.destination.x:
            return point[0] == edge.origin.x
            
        if edge.origin.y == edge.destination.y:
            return point[1] == edge.origin.y
        
        slope = (edge.destination.y - edge.origin.y) / (edge.destination.x - edge.origin.x)
        expected_y = edge.origin.y + slope * (point[0] - edge.origin.x)
        return abs(expected_y - point[1]) < 1e-10

    @property
    def vertex_count(self) -> int:
        """Returns the number of vertices in the face."""
        return sum(1 for _ in self.vertices())

    def __repr__(self) -> str:
        return f"Face(external={self.external}, vertices={self.vertex_count})"
