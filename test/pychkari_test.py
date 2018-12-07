from datetime import datetime

import pytest

from pychkari import container


class A:
    def __init__(self, depOne, dep_two: "DepTwo", const_dep=3):
        self.dep1 = depOne
        self.dep2 = dep_two
        self.const_d = const_dep


class DepOne:
    def __init__(self):
        self.timestamp = datetime.now()


class DepTwo:
    def __init__(self):
        self.timestamp = datetime.now()


def test_class_instance():
    container.register("A", A)
    container.register("DepOne", DepOne)
    container.register("DepTwo", DepTwo)
    a = container.get("A")
    d1 = container.get("DepOne")
    d2 = container.get("DepTwo")
    assert a.dep1 == d1
    assert a.dep2 == d2
    assert a.dep1 != DepOne()


arg_names = [
    ("underscore_case", "UnderscoreCase"),
    ("long_underscore_case", "LongUnderscoreCase"),
    ("camelCase", "CamelCase"),
    ("PascalCase", "PascalCase"),
    ("long_Ugly_mixed_Case", "LongUglyMixedCase")
]


@pytest.mark.parametrize("arg_name,service_name", arg_names)
def test_arg_name_to_service_name(arg_name, service_name):
    assert container.__arg_name_to_service_name(arg_name) == service_name
