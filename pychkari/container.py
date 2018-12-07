import inspect
from inspect import Parameter


class Container:

    def __init__(self):
        self.__registry = {}
        self.__values = {}

    def register_class(self, clazz):
        if not inspect.isclass(clazz):
            raise ValueError("Only classes can be registered without explicit service name")
        class_name = clazz.__name__
        self.register(class_name, clazz)

    def register(self, name: str, thing):
        if name in self.__registry:
            raise ValueError("Service {0} is already registered".format(name))
        self.__registry[name] = thing

    def is_registered(self, name: str) -> bool:
        return name in self.__registry

    def get(self, service_name: str):
        if not self.is_registered(service_name):
            raise ValueError("Service {0} is not registered".format(service_name))
        value = self.__get_value(service_name)
        return value

    def __get_value(self, name: str):
        if name not in self.__values:
            thing = self.__registry[name]
            if inspect.isclass(thing):
                self.__values[name] = self.__instance_from_class(thing)
            if inspect.isfunction(thing):
                self.__values[name] = self.__instance_from_function(thing)

        return self.__values[name]

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
                raise ValueError("Service {0} is not registered and arg {1} doesn't have a default value".
                                 format(service_name, param_name))
            args.append(value)

        return c(*args)

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
