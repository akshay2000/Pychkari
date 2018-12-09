class PychkariError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)


class CyclicDependencyError(PychkariError):
    def __init__(self, cycled_node_name: str, chain: list):
        PychkariError.__init__(self, cycled_node_name)
        self.cycled_node_name = cycled_node_name
        self.chain = chain
