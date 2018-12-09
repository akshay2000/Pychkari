import pytest

import dependencymanager
from dependencymanager import Node
from errors import CyclicDependencyError


def test_tree():
    a = Node("A", ["A1", "B1", "C1"])
    a1 = Node("A1", ["A2", "B2"])
    b1 = Node("B1", ["A2", "C2"])
    c1 = Node("C1")
    a2 = Node("A2", ["B2"])
    b2 = Node("B2")
    c2 = Node("C2")

    all_nodes = {}
    for node in [a, a1, b1, c1, a2, b2, c2]:
        all_nodes[node.name] = node

    assert dependencymanager.check_graph(all_nodes, a) is True


def test_cycle():
    a = Node("A", ["A1", "B1", "C1"])
    a1 = Node("A1", ["A2", "B2"])
    b1 = Node("B1", ["A2", "C2"])
    c1 = Node("C1")
    a2 = Node("A2", ["B2"])
    b2 = Node("B2")
    c2 = Node("C2", ["A"])

    all_nodes = {}
    for node in [a, a1, b1, c1, a2, b2, c2]:
        all_nodes[node.name] = node

    with pytest.raises(CyclicDependencyError) as exec_info:
        dependencymanager.check_graph(all_nodes, a)
    assert exec_info.value.cycled_node_name == "A"
