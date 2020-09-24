import pytest
import surface


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([1], dict(), 1),
        ([1.0], dict(), 1),
        ([1/2], dict(), 0.5),
        ([], {'area': 1}, 1),
        ([1], dict(), 1),
        ([None, 2, 2], dict(), 4),
        ([], {'length': 2, 'width' : 2},  4),
    ],
)
def test_surface(args, kwargs, expected):
    s = surface.Surface(*args, **kwargs)
    assert s.area == expected


@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        (['a'], dict(), AssertionError, 'Input "area" needs to be numeric.'),
        ([], dict(area='a'), AssertionError, 'Input "area" needs to be numeric.'),
        ([1,2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([1, None, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([1, 3, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([None, None, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([None, 2, None], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([None, '2', 2], dict(), AssertionError, 'Input "length" needs to be numeric.'),
        ([None, 2, '2'], dict(), AssertionError, 'Input "width" needs to be numeric.'),

    ]
)
def test_surface_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        surface.Surface(*args, **kwargs)
    assert e.value.args[0] == error_message