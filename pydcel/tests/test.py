import pytest
from math import sqrt, pi, isclose
from typing import List

from ..dcel.point import Point
from ..dcel.vertex import Vertex

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

if __name__ == "__main__":
    pytest.main([__file__])
