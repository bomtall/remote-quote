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
# Testing the instantiation of the surface class
def test_surface_area(args, kwargs, expected):
    s = core.Surface(*args, **kwargs)
    assert s.area == expected


@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        # Testing non numeric inputs
        (['a'], dict(), AssertionError, 'Input "area" needs to be numeric and > 0.'),
        ([None, '2', 2], dict(), AssertionError, 'Input "length" needs to be numeric and > 0.'),
        ([None, 2, '2'], dict(), AssertionError, 'Input "width" needs to be numeric and > 0.'),
        ([], dict(area=1, labour_adjustment='a'), AssertionError, 'Input "labour_adjustment" '
                                                                  'needs to be numeric and > 0.'),
        #Testing negative and zero number inputs
        ([None, 2, -1], dict(), AssertionError, 'Input "width" needs to be numeric and > 0.'),
        ([0], dict(), AssertionError, 'Input "area" needs to be numeric and > 0.'),
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
# Testing the Surface class validation
def test_surface_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Surface(*args, **kwargs)
    assert e.value.args[0] == error_message


@pytest.mark.parametrize(
    'args, kwargs, surface_class, expected, expected_design',
    [
        # Testing Labour Adjustment and design
        ([1], dict(), core.Surface, 1, None),
        ([1], dict(), core.Wall, 0.9, None),
        ([1], dict(), core.Ceiling, 0.95, None),
        ([1], dict(), core.Door, 1.6, 'Flat door'),
        ([1], dict(labour_adjustment=2.5), core.Door, 2.5, 'Flat door'),
        ([1], dict(design='Flat door'), core.Door, 1.6, 'Flat door'),
        ([1], dict(design='Panelled'), core.Door, 1.65, 'Panelled'),
        ([1], dict(design='Cutting in', num_panes=2), core.Door, 2.7, 'Cutting in'),
        ([1], dict(num_panes=12), core.Door, 5, 'Cutting in'),
        ([1], dict(num_panes=6), core.Door, 2.7, 'Cutting in'),
        ([1], dict(), core.Doorframe, 3.2, 'Standard'),
        ([1], dict(labour_adjustment=2.5), core.Doorframe, 2.5, 'Standard'),
        ([1], dict(design='Standard'), core.Doorframe, 3.2, 'Standard'),
        ([1], dict(design='Victorian'), core.Doorframe, 3.6, 'Victorian'),
        ([1], dict(design='Elaborate'), core.Doorframe, 4.2, 'Elaborate'),
        ([1], dict(), core.Skirtingboard, 2.5, None),
        ([1], dict(), core.Window, 1.325, None),
        ([1], dict(num_panes=4), core.Window, 5.3, None),
        ([1], dict(), core.Windowsill, 8.5, None),
        ([1], dict(), core.Spindle, 0.25, 'Square'),
        ([1], dict(labour_adjustment=3), core.Spindle, 3, 'Square'),
        ([1], dict(design='Square'), core.Spindle, 0.25, 'Square'),
        ([1], dict(design='Shaped'), core.Spindle, 0.5, 'Shaped'),
        ([1], dict(design='Elaborate'), core.Spindle, 0.75, 'Elaborate'),
        ([1], dict(), core.ElaborateCornice, 2, None),
        ([1], dict(), core.Radiator, 3.7, None),


    ]
)
# Testing the labour adjustment and design values for surface sub classes and testing surface class defaults
def test_labour_adjustment_and_design(args, kwargs, surface_class, expected, expected_design):
    s = surface_class(*args, **kwargs)
    assert s.labour_adjustment == pytest.approx(expected, 0.01)
    assert s.design == expected_design

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing substrate within the surface class
        ([1], dict(labour_adjustment=1.5, substrate=core.Plaster()), core.Plaster),
        ([1], dict(substrate=core.NewWood()), core.NewWood),
        ([1], dict(), core.PrePaintedEmulsion)

    ],
)
# Testing the instantiation of the surface class with substrate as a property
def test_surface_substrate(args, kwargs, expected):
    s = core.Surface(*args, **kwargs)
    assert isinstance(s.substrate, expected)

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
# Testing the wall surface sub-class instantiation with area arguments
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
# Testing the ceiling surface sub-class instantiation with area arguments
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
# Testing the design property of the door class arguments and defaults
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
# Testing the assertion statements in surface subclasses
def test_surface_subclass_validation_error(args, kwargs, surface_class, error_type, error_message):

    with pytest.raises(error_type) as e:
        surface_class(*args, **kwargs)
    assert e.value.args[0] == error_message

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing substrate
        ([1], dict(), 1),
        ([1], dict(condition='poor'), 1.05),
        ([1], dict(condition='okay'), 1.025),
        ([1], dict(condition='good'), 1),
    ],
)
# Testing the instantiation of substrate with condition arguments gives the correct preparation factor value
def test_substrate(args, kwargs, expected):
    s = core.Substrate(*args, **kwargs)
    assert s.preparation_factor == expected

@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        # Testing Input validation
        ([], dict(condition='excellent'), AssertionError, 'Input "condition" needs to be "poor", "okay", "good" or None' ),
        ([], dict(num_coats='10'), AssertionError, 'Input "num_coats" needs to be a non-zero integer'),
        ([], dict(num_coats=2.5), AssertionError, 'Input "num_coats" needs to be a non-zero integer'),
        ([], dict(coverage_adjustment=-1), AssertionError, 'Input needs to be numeric and > 0, or None'),
        ([], dict(coverage_adjustment='-1'), AssertionError, 'Input needs to be numeric and > 0, or None'),
        ([], dict(coverage_adjustment=0), AssertionError, 'Input needs to be numeric and > 0, or None'),
    ]
)
# Testing the assertion statements in the substrate class
def test_substrate_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Substrate(*args, **kwargs)
    assert e.value.args[0] == error_message


@pytest.mark.parametrize(
    'args, kwargs, expected_prep_factor, expected_coats, expected_coverage',
    [
        # Testing substrate subclasses
        ([1], dict(), 1, 1, 1),
        ([1], dict(substrate=core.PrePaintedEmulsion()), 1, 1, 1),
        ([1], dict(substrate=core.PrePaintedEmulsion(condition='poor')), 1.05, 2, 1),
        ([1], dict(substrate=core.PrePaintedWood()), 1, 1, 1),
        ([1], dict(substrate=core.PrePaintedWood(condition='poor')), 1.05, 2, 1),
        ([1], dict(substrate=core.NewLiningPaper()), 1, 2, 1.2),
        ([1], dict(substrate=core.Plaster()), 1, 2, 1.2),
        ([1], dict(substrate=core.Mdf(primed=True)), 1, 2, 1.2),
        ([1], dict(substrate=core.Mdf(primed=False)), 1, 3, 1.2),
        ([1], dict(substrate=core.Mdf()), 1, 3, 1.2),
        ([1], dict(substrate=core.NewWood(primed=True)), 1, 2, 1.05),
        ([1], dict(substrate=core.NewWood(primed=False)), 1, 3, 1.05),
        ([1], dict(substrate=core.NewWood()), 1, 3, 1.05),

    ],
)
# Testing the number of coats, preparation factor and coverage adjustment are all correct when instantiating substrate
# subclasses with and without arguments
def test_substrate_subclasses(args, kwargs, expected_prep_factor, expected_coats, expected_coverage):
    s = core.Surface(*args, **kwargs)
    assert s.substrate.preparation_factor == expected_prep_factor
    assert s.substrate.num_coats == expected_coats
    assert s.substrate.coverage_adjustment == expected_coverage






#TODO write tests for paint class

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([30,5,17], dict(), {'price' : 30, 'unit' : 5, 'coverage' : 17})

    ]
)
# Test instantiation of the paint class
def test_paint_class(args, kwargs, expected):
    properties = core.Paint(*args, **kwargs)
    assert properties.price == expected['price']
    assert properties.unit == expected['unit']
    assert properties.coverage == expected['coverage']

@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        # Testing non numeric inputs
        (['a', 5, 17], dict(), AssertionError, 'Input "price" needs to be numeric and greater than or equal to zero.'),
        ([30, 'a', 2], dict(), AssertionError, 'Input "unit" needs to be numeric and greater than 0.'),
        ([30, 2, '2'], dict(), AssertionError, 'Input "coverage" needs to be numeric and greater than 0.'),
        ([30, 2, -1], dict(), AssertionError, 'Input "coverage" needs to be numeric and greater than 0.'),
        ([30, -1, 2], dict(), AssertionError, 'Input "unit" needs to be numeric and greater than 0.'),
        ([-1, 5, 17], dict(), AssertionError, 'Input "price" needs to be numeric and greater than or equal to zero.'),
    ]
)
# Testing the paint class assertion statements
def test_paintclass_error(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Paint(*args, **kwargs)
    assert e.value.args[0] == error_message


@pytest.mark.parametrize(
    'args, kwargs, paint_class, expected',
    [
        #Testing instantiation of defaults
        ([], dict(), core.MattEmulsionPaint, 37.87),
        ([], dict(), core.SilkEmulsionPaint, 46.27),
        ([], dict(), core.DiamondMattEmulsion, 50.03),
        ([], dict(), core.OilEggshell, 32.07),
        ([], dict(), core.OilGloss, 19.00),
        ([], dict(), core.OilSatin, 37.20),
        ([], dict(), core.Primer, 31.15),
        ([], dict(price=20.00, unit=5, coverage=17), core.EmulsionPaint, 20.00),
        ([], dict(price=20.00, unit=5, coverage=17), core.OilPaint, 20.00),
        ([], dict(price=20.00, unit=5, coverage=17), core.Paint, 20.00),
    ],
)
# Testing the correct price is assigned as default and when overwritten by an argument
def test_paint_classes(args, kwargs, paint_class, expected):
    s = paint_class(*args, **kwargs)
    assert s.price == expected




@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([core.Wall(10), core.Paint(30, 5, 17)], dict(), 39.52),
        ([], {'surface' : core.Wall(50), 'paint' : core.Paint(30, 5, 17)}, 197.64),
        ([], {'surface' : core.Wall(50, substrate=core.Plaster(
            coverage_adjustment=1)), 'paint' : core.Paint(30, 5, 17)}, 395.29),
        ([], {'surface' : core.Skirtingboard(50, substrate=core.NewWood(
            coverage_adjustment=1)), 'paint' : core.Paint(30, 5, 17)}, 1552.94),
        ([], {'surface' : core.Wall(50, substrate=core.Plaster()), 'paint' : core.Paint(30, 5, 17)}, 402.35),
        ([], {'surface' : core.Windowsill(0.36, substrate=core.Mdf()), 'paint' : core.Paint(30, 5, 17)}, 37.17),

    ]
)
# Painting surface calculations tested
def test_painting_surface_class(args, kwargs, expected):
    total = core.PaintingSurface(*args, **kwargs)
    assert total.get_total_price() == pytest.approx(expected, 0.01)


@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        ([core.Wall(10), 'paint'], dict(), AssertionError, 'Input needs to be a Paint object'),
        (['wall (10)', core.Paint(30, 5, 17)], dict(), AssertionError, 'Input needs to be a Surface object'),
        ([core.Wall(10), (30, 5, 17)], dict(), AssertionError, 'Input needs to be a Paint object'),
        ([10, core.Paint(30, 5, 17)], dict(), AssertionError, 'Input needs to be a Surface object'),

    ]
)
# Testing the assertions in the painting surface class
def test_painting_surface_assertions(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.PaintingSurface(*args, **kwargs)
    assert e.value.args[0] == error_message


# adding some instantiations of painting surfaces as global variables to use in tests

room_test_painting_surface = core.PaintingSurface(core.Wall(8), core.Paint(30, 5, 17))
room_test_painting_surface_2 = core.PaintingSurface(core.Wall(10), core.MattEmulsionPaint())
room_test_painting_surface_3 = core.PaintingSurface(core.Wall(20, substrate=core.Plaster()), core.DiamondMattEmulsion())
room_test_painting_surface_4 = core.PaintingSurface(core.Skirtingboard(1, substrate=core.Mdf(primed=True)),
                                                    core.OilEggshell())


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [

        ([], dict(painting_surfaces = [room_test_painting_surface]*3), [94.87, 8.47, 86.4]),
        ([[room_test_painting_surface]*3], dict(), [94.87, 8.47, 86.4]),
        ([], dict(painting_surfaces = [room_test_painting_surface_2]), [40.45, 4.45, 36]),
        ([[room_test_painting_surface, room_test_painting_surface_2]], dict(), [72.07, 7.27, 64.8]),
        ([[room_test_painting_surface_3, room_test_painting_surface_4, room_test_painting_surface]], dict(),
         [225.70, 32.9, 192.8])
    ],
)
# Testing instantiation of the room class and the total/paint/labour price functions with the global painting surfaces
def test_room(args, kwargs, expected):
    total = core.Room(*args, **kwargs)
    assert total.get_total_price() == pytest.approx(expected[0], 0.01)
    assert total.get_paint_price() == pytest.approx(expected[1], 0.01)
    assert total.get_labour_price() == pytest.approx(expected[2], 0.01)


@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        ([[1, 2, 3, 4]], dict(), AssertionError, 'Input needs to be a list of painting surface objects'),
    ]
)
# Testing the assertion statement in the room class
def test_room_assertion(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Room(*args, **kwargs)
    assert e.value.args[0] == error_message

# adding some instantiations of the room class as global variables to use for tests in this file

room_1 = core.Room([room_test_painting_surface, room_test_painting_surface_2])
room_2 = core.Room([room_test_painting_surface_3, room_test_painting_surface_4])

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([[room_1, room_2]], dict(), [266.16, 37.36, 228.8]),

    ],
)
# Testing the price calculations in the job class using the global room variables
def test_job(args, kwargs, expected):
    total = core.Job(*args, **kwargs)
    assert total.get_total_price() == pytest.approx(expected[0], 0.01)
    assert total.get_paint_price() == pytest.approx(expected[1], 0.01)
    assert total.get_labour_price() == pytest.approx(expected[2], 0.01)

@pytest.mark.parametrize(
    'args, kwargs, error_type, error_message',
    [
        ([[1, 2, 3, 4]], dict(), AssertionError, 'Input needs to be a list of room objects'),
        ([[1, 2, 3, room_1]], dict(), AssertionError, 'Input needs to be a list of room objects'),
    ]
)
# Testing the assertion statements in the job class
def test_job_assertion(args, kwargs, error_type, error_message):
    with pytest.raises(error_type) as e:
        core.Job(*args, **kwargs)
    assert e.value.args[0] == error_message


@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([[room_test_painting_surface, room_test_painting_surface_2]], dict(), [
            {'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 31.62,
             'labour_price': 28.8, 'paint_price': 2.82,'units_of_paint': 0.09, 'surface_area': 8},
            {'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 40.46,
             'labour_price': 36, 'paint_price': 4.46, 'units_of_paint': 0.12, 'surface_area': 10}]),

    ],
)
# Testing the breakdown dictionary provided by the get breakdown function in the room class
def test_room_breakdown(args, kwargs, expected):
    room = core.Room(*args, **kwargs)
    breakdown = room.get_breakdown()
    assert breakdown == expected



@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        ([[room_1, room_1]], dict(), [
            [{'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 31.62,
              'labour_price': 28.8, 'paint_price': 2.82, 'units_of_paint': 0.09, 'surface_area': 8},
            {'surface_name': 'Wall', 'room_name': 'my room','total_price': 40.46, 'labour_price': 36,
             'paint_price': 4.46, 'units_of_paint': 0.12, 'surface_area': 10}],
            [{'surface_name': 'Wall', 'room_name': 'my room', 'total_price': 31.62, 'labour_price': 28.8,
              'paint_price': 2.82, 'units_of_paint': 0.09, 'surface_area': 8},
            {'surface_name': 'Wall', 'room_name': 'my room','total_price': 40.46, 'labour_price': 36,
             'paint_price': 4.46, 'units_of_paint': 0.12, 'surface_area': 10}]]),


    ],
)
# Testing the breakdown function in the job class gives the same dictionary as expected
def test_job_breakdown(args, kwargs, expected):
    job = core.Job(*args, **kwargs)
    breakdown = job.get_breakdown()
    assert breakdown == expected

job_1 = core.Job([room_1, room_2])

@pytest.mark.parametrize(
    'job, expected',
    [

        (job_1, [room_test_painting_surface_4, room_test_painting_surface, room_test_painting_surface_2,
                 room_test_painting_surface_3])
    ],
)
# Testing the function which get the lists needed for the optimisation in the job class
def test_get_painting_surface_list(job, expected):
    surface_list = job.get_painting_surface_list()
    assert surface_list == expected

@pytest.mark.parametrize(
    'surface_list, expected_values, expected_costs',
    [

        (job_1.get_painting_surface_list(), [1, 8, 10, 20], [22, 32, 41, 173])

    ],
)
# Testing the area costs lists are prepared correctly in ascending order
def test_get_area_cost_lists(surface_list, expected_values, expected_costs):
    values, costs = core.Job.get_area_cost_lists(surface_list)
    assert values == expected_values
    assert costs == expected_costs


@pytest.mark.parametrize(
    'job, budget, expected_budgeted_list',
    [

        (job_1, 200, [room_test_painting_surface_3, room_test_painting_surface_4])

    ],
)
# Testing the optimisation of a job
def test_get_optimised_job(job, budget, expected_budgeted_list):
    optimised_job = job.get_optimised_job(budget)
    assert optimised_job.budgeted_painting_surface_list == expected_budgeted_list


@pytest.mark.parametrize(
    'optimised_job, expected_summary_dict',
    [

        (job_1.get_optimised_job(200), {
            'budget': 200,
            'total_budgeted_job_price': 194.08,
            'total_surface_area_in_budget': 21,
            'unpainted_surface_area': 18,
            'cost_for_remaining_items': 72.08})

    ],
)
# Testing the summary dictionary function from the optimised job class
def test_get_summary(optimised_job, expected_summary_dict):
    summary = optimised_job.get_summary()
    assert summary == expected_summary_dict

@pytest.mark.parametrize(
    'optimised_job, expected_summary_dict',
    [

        (job_1.get_optimised_rooms_job(350), {
            'budget': 350,
            'total_budgeted_job_price': 250.9,
            'total_surface_area_in_budget': 21,
            'unpainted_surface_area': 18,
            'cost_for_remaining_items': 139.87
        })
    ],
)
# Testing the optimisation by whole rooms summary
def test_room_optimise_get_summary(optimised_job, expected_summary_dict):
    summary = optimised_job.get_summary()
    for key in list(summary.keys()):
        assert summary[key] == pytest.approx(expected_summary_dict[key], 0.01)

# global variables below to use in the test for the optimisation by condition priority

condition_optimisation_test_painting_surface = core.PaintingSurface(core.Wall(8, substrate=core.PrePaintedEmulsion(
    condition='poor')), core.Paint(30, 5, 17))
condition_optimisation_test_painting_surface_2 = core.PaintingSurface(core.Wall(10, substrate=core.PrePaintedEmulsion(
    condition='poor')), core.MattEmulsionPaint())
condition_optimisation_test_painting_surface_3 = core.PaintingSurface(
    core.Wall(20, substrate=core.Plaster()), core.DiamondMattEmulsion())
condition_optimisation_test_painting_surface_4 = core.PaintingSurface(
    core.Skirtingboard(1, substrate=core.Mdf(primed=True)), core.OilEggshell())

room_3 = core.Room([condition_optimisation_test_painting_surface, condition_optimisation_test_painting_surface_2])
room_4 = core.Room([condition_optimisation_test_painting_surface_3, condition_optimisation_test_painting_surface_4])

job_2 = core.Job([room_3, room_4])



@pytest.mark.parametrize(
    'optimised_job, expected_summary_dict',
    [

        (job_2.get_optimised_condition_job(400), {
            'budget': 400,
            'total_budgeted_job_price': 150.64,
            'total_surface_area_in_budget': 18,
            'unpainted_surface_area': 21,
            'cost_for_remaining_items': 194.08,
        })
    ],
)
# Testing the optimisation by condition gives the correct summary dictionary
def test_room_optimise_get_summary(optimised_job, expected_summary_dict):
    summary = optimised_job.get_summary()
    for key in list(summary.keys()):
        assert summary[key] == pytest.approx(expected_summary_dict[key], 0.01)