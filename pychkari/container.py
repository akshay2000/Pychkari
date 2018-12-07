import inspect
from inspect import Parameter

__registry = {}


def register(name: str, thing):
    if name in __registry:
        raise ValueError("Service {0} is already registered".format(name))
    __registry[name] = thing


def is_registered(name: str) -> bool:
    return name in __registry


def get(service_name: str):
    if not is_registered(service_name):
        raise ValueError("Service {0} is not registered".format(service_name))
    value = __get_value(service_name)
    return value


__values = {}


def __get_value(name: str):
    if name not in __values:
        thing = __registry[name]
        if inspect.isclass(thing):
            __values[name] = __instance_from_class(thing)

    return __values[name]


def __instance_from_class(clazz):
    signature = inspect.signature(clazz)
    params = signature.parameters
    args = []
    for param_name, param in params.items():
        annotation = param.annotation
        service_name = annotation
        if annotation == Parameter.empty:
            service_name = __arg_name_to_service_name(param.name)

        if is_registered(service_name):
            value = get(service_name)
        elif param.default != Parameter.empty:
            value = param.default
        else:
            raise ValueError("Service {0} is not registered and arg {1} doesn't have a default value".
                             format(service_name, param_name))
        args.append(value)

    return clazz(*args)


def __arg_name_to_service_name(arg_name: str) -> str:
    tokens = arg_name.split("_")

    def cap_first(word):
        return word[:1].upper() + word[1:]

    capitalized_tokens = list(map(cap_first, tokens))
    return "".join(capitalized_tokens)
