from atopile.model2 import types
import pytest

def test_object_type():
    iface = types.INTERFACE.make_instance()
    assert isinstance(iface, types.InterfaceObject)
