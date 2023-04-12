import pytest

from .pin import pin_defintion


@pytest.mark.parametrize(
    ('test_str',                                  'expected_connections'), [
    ('pin test_id',                               []),
    ('pin test_id ~ test_id2',                    ['test_id']),
    ('pin test_id ~ test_id2, test_id3',          ['test_id2', 'test_id3']),
    ('pin test_id ~ test_id2.test_id4, test_id3', ['test_id2', 'test_id3']),]
)
def test_valid_pin_definition(test_str, expected_connections):
    # valid pin definitions
    assert pin_defintion.parseString(test_str).as_dict() == {
        'type': 'pin',
        'name': 'test_id',
        'connections': expected_connections,
        'locn_start': 0,
        'locn_end': len(test_str)
    }
