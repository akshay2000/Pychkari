import inspect
from inspect import Parameter

from .dependencymanager import Node, check_graph
from .errors import RegistrationError, MissingDependencyError


class Container:

    def __init__(self):
        self.__registry = {}
        self.__values = {}
        self.__dependency_nodes = {}

    def register_class(self, clazz):
        if not inspect.isclass(clazz):
            raise RegistrationError("Only classes can be registered without explicit service name", clazz.__name__)
        class_name = clazz.__name__
        self.register(class_name, clazz)

    def register(self, service_name: str, thing):
        if service_name in self.__registry:
            raise RegistrationError("Service {0} is already registered".format(service_name), service_name)
        self.__registry[service_name] = thing
        dependencies = Container.__extract_dependencies(thing)
        self.__dependency_nodes[service_name] = Node(service_name, dependencies)

    def is_registered(self, name: str) -> bool:
        return name in self.__registry

    def get(self, service_name: str):
        if not self.is_registered(service_name):
            raise MissingDependencyError("Service {0} is not registered".format(service_name), service_name)
        value = self.__get_value(service_name)
        return value

    def __get_value(self, name: str):
        if name not in self.__values:
            self.__check_dependency_graph(name)
            thing = self.__registry[name]
            if inspect.isclass(thing):
                self.__values[name] = self.__instance_from_class(thing)
            if inspect.isfunction(thing):
                self.__values[name] = self.__instance_from_function(thing)

        return self.__values[name]

    def __check_dependency_graph(self, service_name):
        check_graph(self.__dependency_nodes, self.__dependency_nodes[service_name])

    # region Instance Creation

    def __instance_from_class(self, clazz):
        return self.__instance_from_callable(clazz)

    def __instance_from_function(self, f):
        return self.__instance_from_callable(f)

    def __instance_from_callable(self, c):
        if not callable(c):
            raise ValueError("Given thing {0} is not callable".format(c))

        signature = inspect.signature(c)
        params = signature.parameters
        args = []
        for param_name, param in params.items():
            annotation = param.annotation
            service_name = annotation
            if annotation == Parameter.empty:
                service_name = Container.arg_name_to_service_name(param.name)

            if self.is_registered(service_name):
                value = self.get(service_name)
            elif param.default != Parameter.empty:
                value = param.default
            else:
                raise MissingDependencyError("Service {0} is not registered and arg {1} doesn't have a default value".
                                             format(service_name, param_name), service_name)
            args.append(value)

        return c(*args)

    # endregion

    @staticmethod
    def arg_name_to_service_name(arg_name: str) -> str:
        tokens = arg_name.split("_")

        def cap_first(word):
            return word[:1].upper() + word[1:]

        capitalized_tokens = list(map(cap_first, tokens))
        return "".join(capitalized_tokens)

    __instance = None

    @staticmethod
    def instance():
        if Container.__instance is None:
            Container.__instance = Container()
        return Container.__instance

    @staticmethod
    def __extract_dependencies(service):
        signature = inspect.signature(service)
        params = signature.parameters
        dependencies = []
        for param_name, param in params.items():
            annotation = param.annotation
            service_name = annotation
            if annotation == Parameter.empty:
                service_name = Container.arg_name_to_service_name(param.name)

            if param.default == Parameter.empty:
                dependencies.append(service_name)

        return dependencies
