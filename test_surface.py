import pytest
import surface


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([1], dict(), 1),
        ([1.0], dict(), 1),
        ([1/2], dict(), 0.5),
        ([], {'area': 1}, 1),
    ],
)
def test_surface(args, kwargs, expected):
    s = surface.SurfaceArea(*args, **kwargs)
    assert s.area == expected


@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        (['a'], dict(), AssertionError, 'Input "area" needs to be numeric.'),
        ([], dict(area='a'), AssertionError, 'Input "area" needs to be numeric.'),
    ]
)
def test_surface_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        surface.SurfaceArea(*args, **kwargs)
    assert e.value.args[0] == error_message
