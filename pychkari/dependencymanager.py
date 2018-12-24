import logging

from .errors import CyclicDependencyError, MissingDependencyError


class Node:
    """Represents a node in dependency graph"""

    def __init__(self, name: str, dependencies: list = None):
        """
        :param name: Name of this node.
        :param dependencies: Names of the nodes this node depends on.
        """
        self.name = name
        self.dependencies = dependencies
        self.is_okay = None


def check_graph(all_nodes: dict, node: Node):
    """
    Checks the dependency graph for cyclic dependencies
    :param all_nodes: Bag of all the nodes
    :param node: Root node to check for cyclic dependencies
    :return: True if there are no cyclic dependencies for the current node
    """
    return __check_graph(all_nodes, node)


def __check_graph(all_nodes: dict, node: Node, current_chain: list = None):
    chain = current_chain or []
    indent = "  " * len(chain)
    logging.info(indent + "Node: {0} Chain: {1}".format(node.name, chain))
    if node.name in chain:
        return False

    if node.is_okay:
        logging.info(indent + " Node was already evaluated")
        return True

    if not node.dependencies:
        logging.info(indent + " Leaf node")
        return True

    logging.info(indent + " Evaluating dependencies")
    chain.append(node.name)

    for d in node.dependencies:
        current_node = all_nodes.get(d)
        if not current_node:
            raise MissingDependencyError("Dependency {0} is missing".format(d), d)

        is_okay = __check_graph(all_nodes, current_node, chain)
        if not is_okay:
            dep_chain = chain + [d]
            raise CyclicDependencyError("Node {0} has a cyclic dependency".format(d), d, dep_chain)
        current_node.is_okay = is_okay

    chain.pop()
    return True
