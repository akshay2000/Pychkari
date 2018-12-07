from datetime import datetime

import pytest

from pychkari.container import Container


class A:
    def __init__(self, depOne, second_dep: "DepTwo", const_dep=3):
        self.dep1 = depOne
        self.dep2 = second_dep
        self.const_d = const_dep


class DepOne:
    def __init__(self):
        self.timestamp = datetime.now()


class DepTwo:
    def __init__(self):
        self.timestamp = datetime.now()


class B:
    def __init__(self, a, dep_one):
        self.a = a
        self.dep1 = dep_one


def test_from_class():
    container = Container()
    container.register("DepOne", DepOne)
    o = container.get("DepOne")
    assert isinstance(o, DepOne)
    o_again = container.get("DepOne")
    assert o == o_again


def test_from_factory():
    container = Container()
    const_dep = 42

    def factory_a():
        return A(DepOne(), DepTwo(), const_dep)

    container.register("AWithFactory", factory_a)
    container.register("AWithoutFactory", A)
    container.register("DepOne", DepOne)
    container.register("DepTwo", DepTwo)

    a_from_factory = container.get("AWithFactory")
    a_without_factory = container.get("AWithoutFactory")

    assert a_from_factory.const_d == const_dep
    assert a_without_factory != a_from_factory


def test_injection():
    container = Container()
    container.register("A", A)
    container.register("DepOne", DepOne)
    container.register("DepTwo", DepTwo)
    a = container.get("A")
    d1 = container.get("DepOne")
    d2 = container.get("DepTwo")
    assert a.dep1 == d1
    assert a.dep2 == d2
    assert a.dep1 != DepOne()


def test_multi_level_injection():
    container = Container()
    container.register_class(B)
    container.register_class(A)
    container.register_class(DepOne)
    container.register_class(DepTwo)

    b = container.get("B")
    a = container.get("A")
    dep1 = container.get("DepOne")

    assert b.a == a
    assert b.dep1 == dep1
    assert a.dep1 == dep1


arg_names = [
    ("underscore_case", "UnderscoreCase"),
    ("long_underscore_case", "LongUnderscoreCase"),
    ("camelCase", "CamelCase"),
    ("PascalCase", "PascalCase"),
    ("long_Ugly_mixed_Case", "LongUglyMixedCase")
]


@pytest.mark.parametrize("arg_name,service_name", arg_names)
def test_arg_name_to_service_name(arg_name, service_name):
    assert Container.arg_name_to_service_name(arg_name) == service_name
