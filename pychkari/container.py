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
        """
        Registers a class with its own name as service name. This is shorthand for register("MyClass", MyClass).
        :param clazz: Class to be registered
        """
        if not inspect.isclass(clazz):
            raise RegistrationError("Only classes can be registered without explicit service name", clazz.__name__)
        class_name = clazz.__name__
        self.register(class_name, clazz)

    def register(self, service_name: str, thing):
        """
        Registers a service with the given name and factory.
        :param service_name: Name of the service to be registered
        :param thing: Thing can be either the class of the service to be returned or
            a factory function that returns an instance.
        Dependencies will be resolved within container. In case dependency is not registered, default value will be used
        if provided. Otherwise, error will be raised.
        :raises: RegistrationError if service_name is already registered.
        """
        if service_name in self.__registry:
            raise RegistrationError("Service {0} is already registered".format(service_name), service_name)
        self.__registry[service_name] = thing
        dependencies = Container.__extract_dependencies(thing)
        self.__dependency_nodes[service_name] = Node(service_name, dependencies)

    def is_registered(self, name: str) -> bool:
        """
        Checks if the service is registered with this container.
        :param name: Name of the service to check.
        :return: True if the service is registered in this container
        """
        return name in self.__registry

    def get(self, service_name: str):
        """
        Returns an instance of the service. New instance is created if instance doesn't already exist.
        :param service_name: Name of the service of which instance is to be retrieved.
        :return: A singleton instance of the given service name.
        """
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
            if annotation == Parameter.empty:
                service_name = Container.arg_name_to_service_name(param.name)
            elif inspect.isclass(annotation):
                service_name = annotation.__name__
            else:
                service_name = annotation

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
        """
        Converts a function argument name to service name. All the cases are eventually converted into Pascal case.
        For example:
            camelCase -> CamelCase
            underscore_case -> UnderscoreCase
            PascalCase -> PascalCase
            Weird_mixed_Case -> WeirdMixedCase
        :param arg_name: text to be converted to Pascal case
        :return: Pascal cased text
        """
        tokens = arg_name.split("_")

        def cap_first(word):
            return word[:1].upper() + word[1:]

        capitalized_tokens = list(map(cap_first, tokens))
        return "".join(capitalized_tokens)

    __instance = None

    @staticmethod
    def instance():
        """
        Maintains singleton instance of the container
        :return: Singleton instance of the container
        """
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
            if annotation == Parameter.empty:
                service_name = Container.arg_name_to_service_name(param.name)
            elif inspect.isclass(annotation):
                service_name = annotation.__name__
            else:
                service_name = annotation

            if param.default == Parameter.empty:
                dependencies.append(service_name)

        return dependencies
