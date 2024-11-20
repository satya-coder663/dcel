from typing import List, Tuple

from dcel.primitives import Face, HalfEdge
from dcel.vertex import Vertex


class Dcel:
    """Represents a Doubly Connected Edge List (DCEL)."""
    def __init__(self, vertices: List[Tuple[float, float]] = None, edges: List[Tuple[int, int]] = None):
        self.vertices: List[Vertex] = []
        self.hedges: List[HalfEdge] = []
        self.faces: List[Face] = []
        
        if vertices and edges:
            self.build_dcel(vertices, edges)

    def add_vertex(self, x: float, y: float) -> Vertex:
        """Adds a new vertex to the DCEL."""
        vertex = Vertex(x, y)
        vertex._index = len(self.vertices)
        self.vertices.append(vertex)
        return vertex

    def add_edge(self, v1_idx: int, v2_idx: int) -> Tuple[HalfEdge, HalfEdge]:
        """Adds a new edge between two vertices.""" 
        if v1_idx >= len(self.vertices) or v2_idx >= len(self.vertices):
            raise ValueError("Vertex index out of range")

        v1, v2 = self.vertices[v1_idx], self.vertices[v2_idx]
        h1 = HalfEdge(v1, v2)
        h2 = HalfEdge(v2, v1)
        
        h1.twin = h2
        h2.twin = h1
        
        self.hedges.extend([h1, h2])
        v1.hedgelist.append(h1)
        v2.hedgelist.append(h2)
        
        return h1, h2

    def build_dcel(self, vertices: List[Tuple[float, float]], edges: List[Tuple[int, int]]) -> None:
        """Constructs the DCEL from vertices and edges."""
        for x, y in vertices:
            self.add_vertex(x, y)

        for v1_idx, v2_idx in edges:
            self.add_edge(v1_idx, v2_idx)

        # Sort incident edges and set next/prev pointers
        for vertex in self.vertices:
            vertex.sortincident()
            for i, hedge in enumerate(vertex.hedgelist):
                next_idx = (i + 1) % len(vertex.hedgelist)
                hedge.nexthedge = vertex.hedgelist[next_idx].twin
                hedge.prevhedge = vertex.hedgelist[i - 1]

        self._create_faces()

    def _create_faces(self) -> None:
        """Creates faces from the DCEL structure."""
        unprocessed = set(self.hedges)
        
        while unprocessed:
            hedge = unprocessed.pop()
            if hedge.face is None:
                face = Face()
                face.wedge = hedge
                self.faces.append(face)
                
                # Traverse face boundary
                current = hedge
                while True:
                    current.face = face
                    unprocessed.discard(current)
                    current = current.nexthedge
                    if current is hedge:
                        break

        # Mark external faces using negative area test
        for face in self.faces:
            if face.area < 0:
                face.external = True

    @property
    def statistics(self) -> dict:
        """Returns basic statistics about the DCEL."""
        return {
            'vertices': len(self.vertices),
            'edges': len(self.hedges) // 2,
            'faces': len(self.faces),
            'internal_faces': sum(1 for f in self.faces if not f.external),
            'total_perimeter': sum(f.perimeter for f in self.faces if not f.external),
            'total_area': sum(f.area for f in self.faces if not f.external)
        }

    def __repr__(self) -> str:
        stats = self.statistics
        return f"DCEL(vertices={stats['vertices']}, edges={stats['edges']}, faces={stats['faces']})"
