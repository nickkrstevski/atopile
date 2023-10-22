import pytest

from atopile.model2.errors import AtoSyntaxError

from .utils import parse


def test_util_parse():
    parse(
        """
        component Foo:
            pin 1

        module Bar:
            foo = new Foo
        """
    )


def test_util_parse_error():
    try:
        parse(
            """
            flooptidoo
            """
        )
    except* AtoSyntaxError as exs:
        pass
    else:
        pytest.fail("Expected an exception")
