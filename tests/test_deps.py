import pytest
from atopile.deps import DependencySolver
from atopile.model2.errors import AtoCircularDependencyError


def test_check_for_cycles():
    dep_manager = DependencySolver()
    dep_manager._dependency_tree = {
        "a": {"b"},
        "b": {"c"},
        "c": {"a"},
    }
    with pytest.raises(AtoCircularDependencyError):
        dep_manager.check_for_cycles()


def test_check_for_cycles_no_cycles():
    dep_manager = DependencySolver()
    dep_manager._dependency_tree = {
        "a": {"b"},
        "b": {"c"},
        "c": set(),
    }
    dep_manager.check_for_cycles()


def test_buildable():
    dep_manager = DependencySolver()
    dep_manager._dependency_tree = {
        "a": {"b"},
        "b": {"c"},
        "c": set(),
        "d": {"c"},
    }
    assert set(dep_manager.buildable(set())) == {"c"}
    assert set(dep_manager.buildable({"c"})) == {"b", "d"}
    assert set(dep_manager.buildable({"b", "c"})) == {"a", "d"}
    assert set(dep_manager.buildable({"a", "b", "c", "d"})) == set()
