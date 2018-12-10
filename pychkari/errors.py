class PychkariError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)


class CyclicDependencyError(PychkariError):
    def __init__(self, message: str, cycled_node_name: str, chain: list):
        PychkariError.__init__(self, message)
        self.cycled_node_name = cycled_node_name
        self.chain = chain


class MissingDependencyError(PychkariError):
    def __init__(self, message: str, missing_node_name: str):
        PychkariError.__init__(self, message)
        self.missing_node_name = missing_node_name


class RegistrationError(PychkariError):
    def __init__(self, message: str, service_name: str):
        PychkariError.__init__(self, message)
        self.service_name = service_name
