import math
import pytest
from math import sqrt, pi, isclose
from typing import List

from dcel.point import Point
from dcel.vertex import Vertex
from dcel.primitives import Face, HalfEdge

# -------------------- Point Tests --------------------
class TestPoint:
    def test_distance_properties(self):
        """
        Tests the fundamental properties of distance calculations:
        1. Distance to self is 0
        2. Distance is commutative
        3. Triangle inequality [d(a,c) ≤ d(a,b) + d(b,c)]
        """
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        p3 = Point(6, 0)
        
        # Distance to self should be 0
        assert p1.distance_to(p1) == 0
        
        # Distance should be commutative
        assert isclose(p1.distance_to(p2), p2.distance_to(p1))
        
        # Triangle inequality: distance(a,c) ≤ distance(a,b) + distance(b,c)
        dist_direct = p1.distance_to(p3)
        dist_through_p2 = p1.distance_to(p2) + p2.distance_to(p3)
        assert dist_direct <= dist_through_p2

    def test_vector_operations(self):
        """
        Tests vector operations that are essential for geometric calculations:
        1. Vector addition forms parallelogram
        2. Scalar multiplication scales distances proportionally
        3. Vector subtraction gives expected displacement
        """
        p1 = Point(1, 1)
        p2 = Point(4, 5)
        p3 = Point(2, 3)
        
        # Vector addition should be commutative
        sum1 = p1 + p2
        sum2 = p2 + p1
        assert sum1.x == sum2.x and sum1.y == sum2.y
        
        # Scalar multiplication should scale distances proportionally
        original_dist = p1.distance_to(p2)
        scaled = (p2 - p1) * 2
        new_dist = Point(0, 0).distance_to(scaled)
        assert isclose(new_dist, 2 * original_dist)
        
        # Vector subtraction should give correct displacement
        displacement = p2 - p1
        assert isclose(displacement.x, 3)  # 4 - 1
        assert isclose(displacement.y, 4)  # 5 - 1

    @pytest.mark.parametrize("p1,p2,expected_dist", [
        (Point(0, 0), Point(3, 4), 5),  # Pythagorean triple
        (Point(0, 0), Point(0, 5), 5),  # Vertical line
        (Point(0, 0), Point(5, 0), 5),  # Horizontal line
        (Point(1, 1), Point(1, 1), 0),  # Same point
        (Point(-2, -2), Point(2, 2), 4*sqrt(2)),  # Through origin
    ])
    def test_specific_distances(self, p1: Point, p2: Point, expected_dist: float):
        """Tests specific distance calculations with known results."""
        assert isclose(p1.distance_to(p2), expected_dist)

# -------------------- Half Edge Tests --------------------
class TestHalfEdge:
    @pytest.fixture
    def simple_edge(self):
        """Creates a simple edge from (0,0) to (1,1)"""
        v1 = Vertex(0, 0)
        v2 = Vertex(1, 1)
        return HalfEdge(v1, v2)

    @pytest.fixture
    def twin_edges(self):
        """Creates a pair of twin edges"""
        v1 = Vertex(0, 0)
        v2 = Vertex(1, 1)
        he1 = HalfEdge(v1, v2)
        he2 = HalfEdge(v2, v1)
        he1.twin = he2
        he2.twin = he1
        return he1, he2

    def test_basic_properties(self, simple_edge):
        """Test basic properties of a half-edge"""
        assert simple_edge.origin.x == 0
        assert simple_edge.origin.y == 0
        assert simple_edge.destination.x == 1
        assert simple_edge.destination.y == 1
        assert simple_edge.twin is None
        assert simple_edge.face is None
        assert simple_edge.nexthedge is None
        assert simple_edge.prevhedge is None

    def test_twin_properties(self, twin_edges):
        """Test properties of twin edges"""
        he1, he2 = twin_edges
        assert he1.twin is he2
        assert he2.twin is he1
        assert he1.origin is he2.destination
        assert he2.origin is he1.destination

    @pytest.mark.parametrize("start,end,expected_length", [
        ((0, 0), (1, 0), 1.0),  # Horizontal
        ((0, 0), (0, 1), 1.0),  # Vertical
        ((0, 0), (1, 1), 2**0.5),  # Diagonal
        ((2, 2), (2, 2), 0.0),  # Zero length
        ((-1, -1), (1, 1), 2*2**0.5),  # Through origin
    ])
    def test_edge_length(self, start, end, expected_length):
        """Test edge length calculations"""
        v1 = Vertex(*start)
        v2 = Vertex(*end)
        edge = HalfEdge(v1, v2)
        assert isclose(edge.length, expected_length, rel_tol=1e-10)

    @pytest.mark.parametrize("start,end,expected_angle", [
        ((0, 0), (1, 0), 0),  # Horizontal right
        ((0, 0), (0, 1), pi/2),  # Vertical up
        ((0, 0), (-1, 0), pi),  # Horizontal left
        ((0, 0), (0, -1), 3*pi/2),  # Vertical down
        ((0, 0), (1, 1), pi/4),  # 45 degrees
    ])
    def test_edge_angle(self, start, end, expected_angle):
        """Test edge angle calculations"""
        v1 = Vertex(*start)
        v2 = Vertex(*end)
        edge = HalfEdge(v1, v2)
        assert isclose(edge.angle, expected_angle, rel_tol=1e-10)

    def test_midpoint(self, simple_edge):
        """Test midpoint calculation"""
        midpoint = simple_edge.midpoint
        assert isclose(midpoint.x, 0.5, rel_tol=1e-10)
        assert isclose(midpoint.y, 0.5, rel_tol=1e-10)

# -------------------- Face Tests --------------------
class TestFace:
    @pytest.fixture
    def square_face(self):
        """Creates a square face with vertices at (0,0), (1,0), (1,1), (0,1)"""
        vertices = [
            Vertex(0, 0), Vertex(1, 0),
            Vertex(1, 1), Vertex(0, 1)
        ]
        edges = [
            HalfEdge(vertices[i], vertices[(i+1)%4])
            for i in range(4)
        ]
        # Set next and prev pointers
        for i in range(4):
            edges[i].nexthedge = edges[(i+1)%4]
            edges[i].prevhedge = edges[(i-1)%4]
        
        face = Face()
        face.wedge = edges[0]
        for edge in edges:
            edge.face = face
        return face

    @pytest.fixture
    def triangle_face(self):
        """Creates a triangle face with vertices at (0,0), (1,0), (0,1)"""
        vertices = [Vertex(0, 0), Vertex(1, 0), Vertex(0, 1)]
        edges = [
            HalfEdge(vertices[i], vertices[(i+1)%3])
            for i in range(3)
        ]
        # Set next and prev pointers
        for i in range(3):
            edges[i].nexthedge = edges[(i+1)%3]
            edges[i].prevhedge = edges[(i-1)%3]
        
        face = Face()
        face.wedge = edges[0]
        for edge in edges:
            edge.face = face
        return face

    def test_empty_face(self):
        """Test properties of an empty face"""
        face = Face()
        assert face.wedge is None
        assert face.external is False
        assert face.area == 0.0
        assert face.vertex_count == 0
        with pytest.raises(ValueError):
            _ = face.centroid

    def test_square_properties(self, square_face):
        """Test properties of a square face"""
        assert isclose(square_face.area, 1.0, rel_tol=1e-10)
        assert isclose(square_face.perimeter, 4.0, rel_tol=1e-10)
        assert square_face.vertex_count == 4
        
        # Test centroid
        centroid = square_face.centroid
        assert isclose(centroid.x, 0.5, rel_tol=1e-10)
        assert isclose(centroid.y, 0.5, rel_tol=1e-10)

    def test_triangle_properties(self, triangle_face):
        """Test properties of a triangle face"""
        assert isclose(triangle_face.area, 0.5, rel_tol=1e-10)
        assert isclose(triangle_face.perimeter, 2 + 2**0.5, rel_tol=1e-10)
        assert triangle_face.vertex_count == 3

    @pytest.mark.parametrize("point,expected_inside", [
        ((0.5, 0.5), True),   # Center
        ((0, 0), True),       # Vertex
        ((0.5, 0), True),     # Edge midpoint
        ((2, 2), False),      # Outside
        ((0.5, -0.1), False), # Just outside
        ((1, 1), True),       # Corner
    ])
    def test_point_inside(self, square_face, point, expected_inside):
        """Test point-in-polygon tests"""
        assert square_face.isinside(point) == expected_inside

    def test_vertex_iteration(self, square_face):
        """Test vertex iteration"""
        vertices = list(square_face.vertices())
        assert len(vertices) == 4
        # Check if vertices form a square
        assert vertices[0].coordinates == (0, 0)
        assert vertices[1].coordinates == (1, 0)
        assert vertices[2].coordinates == (1, 1)
        assert vertices[3].coordinates == (0, 1)

    def test_edge_iteration(self, square_face):
        """Test edge iteration"""
        edges = list(square_face.edges())
        assert len(edges) == 4
        # Verify edge connectivity
        for i in range(4):
            assert edges[i].nexthedge is edges[(i+1)%4]
            assert edges[i].prevhedge is edges[(i-1)%4]

    def test_edge_vertices_iteration(self, square_face):
        """Test edge vertices iteration"""
        edge_vertices = list(square_face.edge_vertices())
        assert len(edge_vertices) == 4
        # Check if pairs form valid edges
        expected_pairs = [
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 1)),
            ((0, 1), (0, 0))
        ]
        for (v1, v2), (exp1, exp2) in zip(edge_vertices, expected_pairs):
            assert v1.coordinates == exp1
            assert v2.coordinates == exp2


if __name__ == "__main__":
    pytest.main([__file__])
