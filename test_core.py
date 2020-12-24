import pytest
import core
import paint_link


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
    'args, kwargs, surface_class, expected',
    [
        # Testing Labour Adjustment
        ([1], dict(), core.Surface, 1),
        ([1], dict(), core.Wall, 1),
        ([1], dict(), core.Ceiling, 1.1),
        ([1], dict(), core.Door, 2),
        ([1], dict(labour_adjustment=2.5), core.Door, 2.5),
        ([1], dict(design='Flat door'), core.Door, 2),
        ([1], dict(design='Panelled'), core.Door, 2.1),
        ([1], dict(design='Cutting in', num_panes=2), core.Door, 2.5),
        ([1], dict(num_panes=12), core.Door, 15),
        ([1], dict(num_panes=6), core.Door, 10.5),
        ([1], dict(), core.Doorframe, 2),
        ([1], dict(labour_adjustment=2.5), core.Doorframe, 2.5),
        ([1], dict(design='Standard'), core.Doorframe, 2),
        ([1], dict(design='Victorian'), core.Doorframe, 2.1),
        ([1], dict(design='Elaborate'), core.Doorframe, 2.2),
        ([1], dict(), core.Skirtingboard, 1.1),
        ([1], dict(), core.Window, 2),
        ([1], dict(num_panes=4), core.Window, 8),
        ([1], dict(), core.Windowsill, 1.1),
        ([1], dict(), core.Spindle, 2),
        ([1], dict(labour_adjustment=3), core.Spindle, 3),
        ([1], dict(design='Square'), core.Spindle, 2),
        ([1], dict(design='Shaped'), core.Spindle, 2.1),
        ([1], dict(design='Elaborate'), core.Spindle, 2.2),
        ([1], dict(), core.ElaborateCornice, 2),
        ([1], dict(), core.Radiator, 2),


    ]
)
def test_labour_adjustment(args, kwargs, surface_class, expected):
    s = surface_class(*args, **kwargs)
    assert s.labour_adjustment == pytest.approx(expected, 0.01)

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
    'args, kwargs, surface_class, expected',
    [
        # Testing design property in surface subclasses
        ([1], dict(design='Panelled'), core.Door, 'Panelled'),
        ([1], dict(), core.Door, 'Flat door'),
        ([1], dict(design='Cutting in'), core.Door, 'Cutting in'),
        ([1], dict(), core.Doorframe, 'Standard'),
        ([1], dict(design='Standard'), core.Doorframe, 'Standard'),
        ([1], dict(design='Victorian'), core.Doorframe, 'Victorian'),
        ([1], dict(design='Elaborate'), core.Doorframe, 'Elaborate'),
        ([1], dict(), core.Spindle, 'Square'),
        ([1], dict(design='Square'), core.Spindle, 'Square'),
        ([1], dict(design='Shaped'), core.Spindle, 'Shaped'),
        ([1], dict(design='Elaborate'), core.Spindle, 'Elaborate'),
    ],
)
def test_door_design(args, kwargs, surface_class, expected):
    s = surface_class(*args, **kwargs)
    assert s.design == expected

@pytest.mark.parametrize(
    'args, kwargs, surface_class, error_type, error_message',
    [
        # Testing class validations
        ([1], dict(design='fancy'), core.Door, AssertionError, 'input needs to be "Panelled", "Flat door", "Cutting in" or None'),
        ([1], dict(design='fancy'), core.Doorframe, AssertionError, 'input needs to be "Standard", "Victorian", "Elaborate" or None'),
        ([1], dict(design='fancy'), core.Spindle, AssertionError, 'input needs to be "Square", "Shaped", "Elaborate" or None'),
        ([1], dict(num_panes='10'), core.Door, AssertionError, 'Input "num_panes" needs to be a non-negative integer'),
        ([1], dict(num_panes=-5), core.Door, AssertionError, 'Input "num_panes" needs to be a non-negative integer'),
        ([1], dict(num_panes=2.4), core.Door, AssertionError, 'Input "num_panes" needs to be a non-negative integer'),
        ([1], dict(num_panes=2, design='Flat door'), core.Door, AssertionError, 'Only "Cutting in" doors have panes > 0'),
        ([1], dict(num_panes=0, design='Cutting in'), core.Door, AssertionError, 'Only "Cutting in" doors have panes > 0'),
        ([1], dict(num_panes=0), core.Window, AssertionError, '"num_panes" needs to be an integer and >= 1'),
        ([1], dict(num_panes=2.4), core.Window, AssertionError, '"num_panes" needs to be an integer and >= 1'),
        ([1], dict(num_panes=-5), core.Window, AssertionError, '"num_panes" needs to be an integer and >= 1'),
        ([1], dict(num_panes='6'), core.Window, AssertionError, '"num_panes" needs to be an integer and >= 1'),
    ]
)
def test_surface_subclass_validation_error(args, kwargs, surface_class, error_type, error_message):

    with pytest.raises(error_type) as e:
        surface_class(*args, **kwargs)
    assert e.value.args[0] == error_message



    # TODO ADD IN TEST FOR VALIDATION OF NUMBER OF PANES IN WINDOW AND CUTTING IN DOOR

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
        ([], dict(num_coats=2.5), AssertionError, 'Input "num_coats" needs to be an integer or None'),
        ([], dict(coverage_adjustment=-1), AssertionError, 'Input needs to be numeric and > 0, or None'),
        ([], dict(coverage_adjustment='-1'), AssertionError, 'Input needs to be numeric and > 0, or None'),
        ([], dict(coverage_adjustment=0), AssertionError, 'Input needs to be numeric and > 0, or None'),
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
        ([], {'surface' : core.Wall(50, substrate=core.Plaster(coverage_adjustment=1)), 'paint' : core.Paint(30, 5, 17)}, 580),
        ([], {'surface' : core.Skirtingboard(50, substrate=core.NewWood(coverage_adjustment=1)), 'paint' : core.Paint(30, 5, 17)}, 930),
        ([], {'surface' : core.Wall(50, substrate=core.Plaster()), 'paint' : core.Paint(30, 5, 17)}, 640),
        ([], {'surface' : core.Windowsill(0.36, substrate=core.Mdf()), 'paint' : core.Paint(30, 5, 17)}, 34.752),

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

room_test_painting_surface = core.PaintingSurface(core.Wall(8), core.Paint(30, 5, 17))
room_test_painting_surface_2 = core.PaintingSurface(core.Wall(10), paint_link.MattEmulsionPaint())
room_test_painting_surface_3 = core.PaintingSurface(core.Wall(20, substrate=core.Plaster()), paint_link.DiamondMattEmulsion())
room_test_painting_surface_4 = core.PaintingSurface(core.Skirtingboard(1, substrate=core.Mdf(primed=True)), paint_link.OilEggshell())


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [

        ([], dict(painting_surfaces = [room_test_painting_surface]*3), [186, 90, 96]),
        ([[room_test_painting_surface]*3], dict(), [186, 90, 96]),
        ([], dict(painting_surfaces = [room_test_painting_surface_2]), [77.87, 37.87, 40]),
        ([[room_test_painting_surface, room_test_painting_surface_2]], dict(), [139.87, 67.87, 72]),
        ([[room_test_painting_surface_3, room_test_painting_surface_4, room_test_painting_surface]], dict(), [312.9, 112.1, 200.8])


   ],
)

def test_room(args, kwargs, expected):
    total = core.Room(*args, **kwargs)
    assert total.get_total_price() == expected[0]
    assert total.get_paint_price() == expected[1]
    assert total.get_labour_price() == expected[2]

room_1 = core.Room([room_test_painting_surface, room_test_painting_surface_2])
room_2 = core.Room([room_test_painting_surface_3, room_test_painting_surface_4])

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([[room_1, room_2]], dict(), 390.77),

    ],
)
def test_job(args, kwargs, expected):
    total = core.Job(*args, **kwargs)
    assert total.get_total_price() == expected


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([[room_test_painting_surface, room_test_painting_surface_2]], dict(), [
            {'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 62, 'labour_price': 32, 'paint_price': 30,
             'units_of_paint': 1, 'surface_area': 8},
            {'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 77.87, 'labour_price': 40, 'paint_price': 37.87,
             'units_of_paint': 1, 'surface_area': 10}]),

    ],
)
def test_room_breakdown(args, kwargs, expected):
    room = core.Room(*args, **kwargs)
    breakdown = room.get_breakdown()
    assert breakdown == expected



@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([[room_1, room_1]], dict(), [
            [{'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 62, 'labour_price': 32, 'paint_price': 30, 'units_of_paint': 1, 'surface_area': 8},
            {'surface_name': 'Wall', 'room_name': 'my room','total_price': 77.87, 'labour_price': 40, 'paint_price': 37.87, 'units_of_paint': 1, 'surface_area': 10}],
            [{'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 62, 'labour_price': 32, 'paint_price': 30, 'units_of_paint': 1, 'surface_area': 8},
            {'surface_name': 'Wall', 'room_name': 'my room','total_price': 77.87, 'labour_price': 40, 'paint_price': 37.87, 'units_of_paint': 1, 'surface_area': 10}]]),


    ],
)
def test_job_breakdown(args, kwargs, expected):
    job = core.Job(*args, **kwargs)
    breakdown = job.get_breakdown()
    assert breakdown == expected

job_1 = core.Job([room_1, room_2])

@pytest.mark.parametrize(
    'job, expected',
    [
        #total prices surface1=62 surface2=77.87 surface3=210.03 surface4=40.87 approx 8 10 20 1
        (job_1, [room_test_painting_surface_4, room_test_painting_surface, room_test_painting_surface_2, room_test_painting_surface_3])

    ],
)
def test_get_painting_surface_list(job, expected):
    surface_list = job.get_painting_surface_list()
    assert surface_list == expected

@pytest.mark.parametrize(
    'surface_list, expected_values, expected_costs',
    [
        # total prices surface1=62 surface2=77.87 surface3=210.03 surface4=40.87 approx
        # areas of surfaces 1,2,3,4 respectively 8 10 20 1
        (job_1.get_painting_surface_list(), [1, 8, 10, 20], [41, 62, 78, 211])

    ],
)
def test_get_area_cost_lists(surface_list, expected_values, expected_costs):
    values, costs = core.Job.get_area_cost_lists(surface_list)
    assert values == expected_values
    assert costs == expected_costs


@pytest.mark.parametrize(
    'job, budget, expected_budgeted_list',
    [

        (job_1, 300, [room_test_painting_surface_3, room_test_painting_surface_2])

    ],
)
def test_get_optimised_job(job, budget, expected_budgeted_list):
    optimised_job = job.get_optimised_job(budget)
    assert optimised_job.budgeted_painting_surface_list == expected_budgeted_list


@pytest.mark.parametrize(
    'optimised_job, expected_summary_dict',
    [

        (job_1.get_optimised_job(300), {
            'budget': 300,
            'total_budgeted_job_price': 287.9,
            'total_surface_area_in_budget': 30,
            'unpainted_surface_area': 9,
            'cost_for_remaining_items': 102.87})

    ],
)
def test_get_summary(optimised_job, expected_summary_dict):
    summary = optimised_job.get_summary()
    assert summary == expected_summary_dict

