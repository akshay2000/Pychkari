from .errors import CyclicDependencyError, MissingDependencyError


class Node:
    def __init__(self, name: str, dependencies: list = None):
        self.name = name
        self.dependencies = dependencies
        self.is_okay = None


def check_graph(all_nodes: dict, node: Node, current_chain: list = None):
    chain = current_chain or []
    indent = "  " * len(chain)
    print(indent + "Node: {0} Chain: {1}".format(node.name, chain))
    if node.name in chain:
        return False

    if node.is_okay:
        print(indent + " Node was already evaluated")
        return True

    if not node.dependencies:
        print(indent + " Leaf node")
        return True

    print(indent + " Evaluating dependencies")
    chain.append(node.name)

    for d in node.dependencies:
        current_node = all_nodes.get(d)
        if not current_node:
            raise MissingDependencyError("Dependency {0} is missing".format(d), d)

        is_okay = check_graph(all_nodes, current_node, chain)
        if not is_okay:
            dep_chain = chain + [d]
            raise CyclicDependencyError("Node {0} has a cyclic dependency".format(d), d, dep_chain)
        current_node.is_okay = is_okay

    chain.pop()
    return True
