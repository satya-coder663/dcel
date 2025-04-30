# pydcel: A Data Structure for Doubly-Connected Edge List (DCEL)

## Project Overview

`pydcel` is a Python library that provides an implementation of the Doubly-Connected Edge List (DCEL) data structure. The doubly connected edge list (DCEL), also known as the half-edge data structure, is a data structure to represent an embedding of a planar graph in the plane, and polytopes in 3D [[1]](https://en.wikipedia.org/wiki/Doubly_connected_edge_list).

`pydcel` allows for efficient traversal and modification of the graph, making it ideal for applications such as geometric modeling, mesh processing, and algorithms related to computational geometry. By maintaining connectivity information for vertices, edges, and faces, the DCEL facilitates operations like edge flipping, face traversal, and vertex splitting, among others. This structure is particularly valuable in areas such as computer graphics, geographic information systems (GIS), and 3D modeling, where efficient representation and manipulation of geometric data are crucial.

## Features

* **DCEL Data Structure:**  A complete and efficient implementation of the DCEL data structure.
* **Point and Vertex Handling:**  Functions for creating, manipulating, and managing points and vertices within the DCEL.
* **Edge and Face Operations:**  Support for edge insertion, deletion, traversal, and finding twins, along with face manipulation.

## Installation

To install the library, using `pip`, run the following command:

```bash
pip install pydcel
```

If you prefer using `pipenv`, you can install the library using the following command:

```bash
pipenv install pydcel
```

## Usage

The library provides classes for `Point`, `Vertex`, and `Edge` which can be used to construct a `DCEL`. 

The `Dcel` takes 2 arguments:
- list containing tuples of points as input. 
- list containing tuples of edges as input.

```python 
from dcel import Dcel

# Define vertices for the polygon as a list of tuples
vertex_coords = [
    (0, 0), (2, 2), (4, 0),
    (3, -2), (1, -2)
]

# Define edges connecting the vertices
edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0)
]

# Create DCEL from vertices and edges
dcel = Dcel(vertex_coords, edges)

# Print DCEL Statistics
print(dcel.statistics)
```

More detailed usage examples can be found in the [examples](./examples/) directory.


## Acknowledgments

`pydcel` builds upon the theoretical insights provided by [Dr. Sanjoy Pratihar](https://sites.google.com/site/sanjoypratihar/home) and takes inspiration from the work of [Angel Yanguas-Gil](https://scholar.google.com/citations?user=HKXeJ9cAAAAJ&hl=en) on the [DCEL](https://pypi.org/project/dcel/) data structure.

## Contributing

To contribute to `pydcel`, please follow the guidelines mentioned in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

`pydcel` is distributed under the BSD 3-Clause License. For more information, please refer to the [LICENSE](LICENSE) file.
