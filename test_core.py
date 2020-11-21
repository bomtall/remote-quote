import pytest
import core


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing different numeric inputs
        ([1], dict(), 1),
        ([1.0], dict(), 1),
        ([1/2], dict(), 0.5),
        # Testing keyword arguments
        ([], {'area': 1}, 1),
        # Testing giving length and width
        ([None, 2, 2], dict(), 4),
        ([], {'length': 2, 'width': 2},  4),
        ([None, 2], {'width' : 2}, 4),
        # Testing initialisation with substrate
        ([1], dict(labour_adjustment=1.5, substrate=core.Plaster()), 1)

    ],
)
def test_surface_area(args, kwargs, expected):
    s = core.Surface(*args, **kwargs)
    assert s.area == expected


@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        # Testing non numeric inputs
        (['a'], dict(), AssertionError, 'Input "area" needs to be numeric.'),
        ([None, '2', 2], dict(), AssertionError, 'Input "length" needs to be numeric.'),
        ([None, 2, '2'], dict(), AssertionError, 'Input "width" needs to be numeric.'),
        ([], dict(area=1, labour_adjustment='a'), AssertionError, 'Input "labour_adjustment" needs to be numeric.'),
        # Testing when user only inputs two arguments but has to be one or three
        ([1, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([1, None, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        # Testing if there are three inputs that the first is None
        ([1, 3, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        # Testing for no inputs
        ([], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        # Testing if only one input that it has to be area
        ([None, None, 2], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
        ([None, 2, None], dict(), AssertionError, 'Input either "area" or "length" and "width".'),
    ]
)
def test_surface_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Surface(*args, **kwargs)
    assert e.value.args[0] == error_message


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([], dict(area=1, labour_adjustment=1), 1),
        ([], dict(area=1), 1),
    ],
)
def test_surface_labour_adjustment(args, kwargs, expected):
    s = core.Surface(*args, **kwargs)
    assert s.labour_adjustment == expected

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing substrate within the surface class
        ([1], dict(labour_adjustment=1.5, substrate=core.Plaster()), core.Plaster),
        ([1], dict(substrate=core.NewWood()), core.NewWood),
        ([1], dict(), core.PrePaintedEmulsion)

    ],
)
def test_surface_substrate(args, kwargs, expected):
    s = core.Surface(*args, **kwargs)
    assert isinstance(s.substrate, expected)



@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing design property in surface
        ([1], dict(design='panelled'), 'panelled'),

    ],
)
def test_surface_design(args, kwargs, expected):
    s = core.Surface(*args, **kwargs)
    assert s.design == expected



# TODO write tests for wall and ceiling(done)

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing different numeric inputs
        ([1], dict(), 1),
        ([1.0], dict(), 1),
        ([1/2], dict(), 0.5),
        # Testing keyword arguments
        ([], {'area': 1}, 1),
        # Testing giving length and width
        ([None, 2, 2], dict(), 4),
        ([], {'length': 2, 'width': 2},  4),
        ([None, 2], {'width' : 2}, 4),
    ],
)
def test_wall(args, kwargs, expected):
    w = core.Wall(*args, **kwargs)
    assert w.area == expected


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing different numeric inputs
        ([1], dict(), 1),
        ([1.0], dict(), 1),
        ([1/2], dict(), 0.5),
        # Testing keyword arguments
        ([], {'area': 1}, 1),
        # Testing giving length and width
        ([None, 2, 2], dict(), 4),
        ([], {'length': 2, 'width': 2},  4),
        ([None, 2], {'width' : 2}, 4),
    ],
)

def test_ceiling(args, kwargs, expected):
    c = core.Ceiling(*args, **kwargs)
    assert c.area == expected

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing design property in door class
        ([1], dict(design='panelled'), 'panelled'),
        ([1], dict(), 'flat door'),
        ([1], dict(design='cutting in'), 'cutting in')

    ],
)
def test_door_design(args, kwargs, expected):
    s = core.Door(*args, **kwargs)
    assert s.design == expected



    # TODO ADD IN TEST FOR LABOUR ADJUSTMENT BASED ON DESIGN PROPERTIES

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        #testing passing in list and dictionary
        ([[core.Wall(10)]], dict(), 10),
        ([[core.Wall(20), core.Wall(40)]], dict(), 60),
        ([[core.Ceiling(10)]], dict(), 10),
        ([[core.Wall(15), core.Ceiling(15)]], dict(), 30),
        ([], {'surfaces' : [core.Wall(10), core.Ceiling(15)]}, 25),
        ([[core.Wall(20), core.Ceiling(40), core.Wall(20), core.Wall(10), core.Wall(10), core.Ceiling(10),]],
         dict(), 110)
    ]
)

def test_get_total_surface_area(args, kwargs, expected):
    sa = core.get_total_surface_area(*args, **kwargs)
    assert sa == expected


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing substrate
        ([1], dict(), 1),
        ([1], dict(condition='poor'), 1.1),
        ([1], dict(condition='okay'), 1.05)
    ],
)
def test_substrate(args, kwargs, expected):
    s = core.Substrate(*args, **kwargs)
    assert s.preparation_factor == expected

@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        # Testing Input validation
        ([], dict(condition='excellent'), AssertionError, 'Input "condition" needs to be "poor", "okay", "good" or None' ),
        ([], dict(num_coats='10'), AssertionError, 'Input "num_coats" needs to be an integer or None'),
        ([], dict(num_coats=2.5), AssertionError, 'Input "num_coats" needs to be an integer or None')
    ]
)
def test_substrate_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Substrate(*args, **kwargs)
    assert e.value.args[0] == error_message

#TODO write tests for paint class

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([30,5,17], dict(), {'price' : 30, 'unit' : 5, 'coverage' : 17})

    ]
)
def test_paint_class(args, kwargs, expected):
    properties = core.Paint(*args, **kwargs)
    assert properties.price == expected['price']
    assert properties.unit == expected['unit']
    assert properties.coverage == expected['coverage']

@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        # Testing non numeric inputs
        (['a', 5, 17], dict(), AssertionError, 'Input "price" needs to be numeric.'),
        ([30, 'a', 2], dict(), AssertionError, 'Input "unit" needs to be numeric.'),
        ([30, 2, '2'], dict(), AssertionError, 'Input "coverage" needs to be numeric.'),

    ]
)
def test_paintclass_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Paint(*args, **kwargs)
    assert e.value.args[0] == error_message


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([core.Wall(10), core.Paint(30, 5, 17)], dict(), 70),
        ([], {'surface' : core.Wall(50), 'paint' : core.Paint(30, 5, 17)}, 290),
        ([], {'surface' : core.Wall(50, substrate=core.Plaster()), 'paint' : core.Paint(30, 5, 17)}, 580),
        ([], {'surface' : core.Skirtingboard(50, substrate=core.NewWood()), 'paint' : core.Paint(30, 5, 17)}, 930)

    ]
)

def test_painting_surface_class(args, kwargs, expected):
    total = core.PaintingSurface(*args, **kwargs)
    assert total.get_total_price() == pytest.approx(expected, 0.001)


def test_painting_surface():
    wall = core.Wall(20)
    paint = core.Paint(30, 5, 17)

    job = core.PaintingSurface(wall, paint)

    units_of_paint = job.get_units_of_paint()
    assert units_of_paint == 2

    paint_price = job.get_paint_price()
    assert paint_price == 60

    labour_price = job.get_labour_price()
    assert labour_price == 80
    total_price = job.get_total_price()
    assert total_price == 140




#TODO parameterise and separate tests for each function

def test_job():

    painting_surface_1 = core.PaintingSurface(core.Wall(8), core.Paint(30, 5, 17))
    painting_surface_2 = core.PaintingSurface(core.Wall(10), core.Paint(30, 5, 17))
    painting_surface_3 = core.PaintingSurface(core.Ceiling(20), core.Paint(30, 5, 17))

    job_1 = core.Job([painting_surface_1, painting_surface_2, painting_surface_3])
    assert job_1.get_paint_price() == 120

    assert job_1.get_labour_price() == 160

    assert job_1.get_total_price() == 280

    ...
