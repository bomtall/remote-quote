from numbers import Number
import math
import knapsack


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Global variables ----------------------------------------------------------

CONDITION_OPTIONS = ['good', 'okay', 'poor']


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Surface class -------------------------------------------------------------
class Surface:
    def __init__(
            self,
            area=None,
            length=None,
            width=None,
            labour_adjustment=None,
            substrate=None,
            design=None,
            design_options=None,
            description=None,
            name=None,
            num_panes=None,
            room_name=None

    ):


        if area is None:
            assert length is not None and width is not None, 'Input either "area" or "length" and "width".'
            assert isinstance(length, Number), 'Input "length" needs to be numeric.'
            assert isinstance(width, Number), 'Input "width" needs to be numeric.'
            area = length * width
        else:
            assert length is None and width is None, 'Input either "area" or "length" and "width".'
            assert isinstance(area, Number), 'Input "area" needs to be numeric.'

        if labour_adjustment is None:
            labour_adjustment = 1
        else:
            assert isinstance(labour_adjustment, Number), 'Input "labour_adjustment" needs to be numeric.'

        if substrate is None:
            substrate = PrePaintedEmulsion()

        self.area = area
        self.length = length
        self.width = width
        self.labour_adjustment = labour_adjustment
        self.substrate = substrate
        self.design = design
        self.design_options = design_options
        self.description = description
        self.name = name
        self.num_panes = num_panes
        self.room_name = room_name




# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Surface subclasses --------------------------------------------------------
class Wall(Surface):
    def __init__(self, *args, **kwargs):
        description = 'An interior wall'
        name = 'Wall'
        super().__init__(*args, **kwargs, description=description, name=name)


class Ceiling(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        description = 'An interior ceiling'
        name = 'Ceiling'
        if labour_adjustment is None:
            labour_adjustment = 1.1

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Door(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, num_panes=None, **kwargs):
        description = 'One side of an interior door'
        name = 'Door'
        design_options = ['Panelled', 'Flat door', 'Cutting in']

        if design == 'Cutting in' and num_panes is None:
            num_panes = 1
        elif num_panes is None:
            num_panes = 0

        assert design in (design_options + [None]), 'input needs to be "Panelled", "Flat door", "Cutting in" or None'
        assert isinstance(num_panes, int) and num_panes >= 0, 'Input "num_panes" needs to be a non-negative integer'

        if num_panes > 0 and design is None:
            design = 'Cutting in'
        if design is None:
            design = 'Flat door'

        assert (num_panes > 0 and design == 'Cutting in') or \
               (num_panes == 0 and design in ['Panelled', 'Flat door', None]), 'Only "Cutting in" doors have panes > 0'

        if labour_adjustment is None:
            labour_adjustment = 2
            if design == 'Panelled':
                labour_adjustment = 2.1
            elif design == 'Cutting in':
                if num_panes < 3:
                    labour_adjustment = 2.5
                else:
                    labour_adjustment = min(3/2 * (num_panes + 1), 15)

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design,
                         design_options=design_options, description=description, name=name, num_panes=num_panes)


class Doorframe(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, **kwargs):
        description = 'Room side of door frame'
        name = 'Door Frame'
        design_options = ['Standard', 'Victorian', 'Elaborate']

        if design is None:
            design = design_options[0]
        else:
            assert design in design_options,\
                'input needs to be "Standard", "Victorian", "Elaborate" or None'

        if labour_adjustment is None:
            labour_adjustment = 2
            if design == 'Victorian':
                labour_adjustment = 2.1
            elif design == 'Elaborate':
                labour_adjustment = 2.2

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design,
                         design_options=design_options, description=description, name=name)


class Skirtingboard(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        description = 'Skirting board along the bottom of a wall'
        name = 'Skirting board'
        if labour_adjustment is None:
            labour_adjustment = 1.1
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Window(Surface):
    def __init__(self, *args, labour_adjustment=None, num_panes=1, **kwargs):
        description = 'Interior side of a window, frame included'
        name = 'Window'
        assert isinstance(num_panes, int) and num_panes >= 1, '"num_panes" needs to be an integer and >= 1'
        if labour_adjustment is None:
            labour_adjustment = (2 * num_panes)

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description,
                         name=name, num_panes=num_panes)


class Windowsill(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        description = 'The interior horizontal sill beneath a window'
        name = 'Windowsill'
        if labour_adjustment is None:
            labour_adjustment = 1.1
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Spindle(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, **kwargs):
        description = 'Vertical bars underneath a handrail'
        name = 'Spindle'
        design_options = ['Square', 'Shaped', 'Elaborate']

        if design is None:
            design = design_options[0]
        else:
            assert design in design_options, \
                'input needs to be "Square", "Shaped", "Elaborate" or None'

        if labour_adjustment is None:
            labour_adjustment = 2
            if design == 'Shaped':
                labour_adjustment = 2.1
            elif design == 'Elaborate':
                labour_adjustment = 2.2

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design,
                         design_options=design_options, description=description, name=name)


class ElaborateCornice(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        description = 'Large ornate plaster cornice, ceiling roses or corbels'
        name = 'Decorative plaster'
        if labour_adjustment is None:
            labour_adjustment = 2
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Radiator(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        description = 'Enamelled modern radiator'
        name = 'Radiator'
        if labour_adjustment is None:
            labour_adjustment = 2
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Substrate class -----------------------------------------------------------
class Substrate:
    def __init__(
            self,
            num_coats=1,
            porosity=None,
            condition=None,
            coverage_adjustment=1,
            condition_assumption=None,
            primed=False

    ):
        self.condition_options = CONDITION_OPTIONS

        assert condition in self.condition_options + [None], \
            'Input "condition" needs to be "poor", "okay", "good" or None'

        if condition is None:
            condition = 'good'
        assert isinstance(num_coats, int) or num_coats is None, 'Input "num_coats" needs to be an integer or None'
        assert (isinstance(coverage_adjustment, Number) and coverage_adjustment > 0.0) \
               or (coverage_adjustment is None), 'Input needs to be numeric and > 0, or None'

        if coverage_adjustment is None:
            coverage_adjustment = 1

        if condition_assumption is None:
            condition_assumption = ConditionAssumptions()

        # TODO add in validation for porosity

        self.num_coats = num_coats
        self.porosity = porosity
        self.condition = condition
        self.preparation_factor = self.get_preparation_factor()
        self.coverage_adjustment = coverage_adjustment
        self.condition_assumption = condition_assumption
        self.primed = False

    def get_preparation_factor(self):
        if self.condition == 'poor':
            preparation_factor = 1.05
        elif self.condition == 'okay':
            preparation_factor = 1.025
        else:
            preparation_factor = 1

        return preparation_factor


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Substrate subclasses-------------------------------------------------------
class Plaster(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, **kwargs):
        if num_coats is None:
            num_coats = 2
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)
        self.preparation_factor = self.get_preparation_factor()


class PrePaintedEmulsion(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        if num_coats is None and condition == 'poor':
            num_coats = 2
        elif num_coats is None:
            num_coats = 1
        if coverage_adjustment is None:
            coverage_adjustment = 1
        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition,
                         coverage_adjustment=coverage_adjustment)
        self.preparation_factor = self.get_preparation_factor()


class PrePaintedWood(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        if num_coats is None and condition == 'poor':
            num_coats = 2
        elif num_coats is None:
            num_coats = 1
        if coverage_adjustment is None:
            coverage_adjustment = 1
        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition,
                         coverage_adjustment=coverage_adjustment)
        self.preparation_factor = self.get_preparation_factor()


class NewLiningPaper(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, **kwargs):
        if num_coats is None:
            num_coats = 2
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)

        self.preparation_factor = self.get_preparation_factor()


class Mdf(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, primed=False, **kwargs):
        if num_coats is None:
            num_coats = 3
        if primed is True:
            num_coats = 2

        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment, primed=primed)

        self.preparation_factor = self.get_preparation_factor()


class NewWood(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, **kwargs):
        if num_coats is None:
            num_coats = 3
        if coverage_adjustment is None:
            coverage_adjustment = 1.05

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)
        self.preparation_factor = self.get_preparation_factor()


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Paint ---------------------------------------------------------
class Paint:
    def __init__(self, price, unit, coverage,):

        assert isinstance(price, Number), 'Input "price" needs to be numeric.'
        assert isinstance(unit, Number), 'Input "unit" needs to be numeric.'
        assert isinstance(coverage, Number), 'Input "coverage" needs to be numeric.'

        self.price = price
        self.unit = unit
        self.coverage = coverage


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------- Painting Surface -----------------------------------------------------
# TODO add validation for inputs to painting surface
class PaintingSurface:
    def __init__(self, surface, paint, labour_price_msq=None):
        if labour_price_msq is None:
            labour_price_msq = 4

        self.surface = surface
        self.paint = paint
        self.labour_price_msq = labour_price_msq

# TODO make calculation reflect unit and coverage properly
        # if surface.substrate in [NewWood, MDF, ]

    def get_units_of_paint(self):
        units_of_paint = math.ceil(
            (self.surface.area / (self.paint.coverage / self.surface.substrate.coverage_adjustment))
            * self.surface.substrate.num_coats)
        return units_of_paint

    def get_paint_price(self):
        paint_price = self.get_units_of_paint() * self.paint.price
        return paint_price

    def get_labour_price(self):
        labour_price = self.surface.area * self.labour_price_msq * self.surface.labour_adjustment * \
            self.surface.substrate.num_coats * self.surface.substrate.preparation_factor
        return labour_price

    def get_total_price(self):
        total_price = self.get_labour_price() + self.get_paint_price()
        return total_price

    def get_breakdown(self):
        breakdown = dict(
            room_name=self.surface.room_name,
            surface_name=self.surface.name,
            total_price=self.get_total_price(),
            labour_price=self.get_labour_price(),
            paint_price=self.get_paint_price(),
            units_of_paint=self.get_units_of_paint(),
            surface_area=self.surface.area,
        )
        return breakdown


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Room --------------------------------------------------------------
class Room:
    def __init__(self, painting_surfaces, name=None):
        if name is None:
            name = 'my room'

        self.painting_surfaces = painting_surfaces
        self.name = name

        # adding the room name to the surface name
        for painting_surface in self.painting_surfaces:
            painting_surface.surface.room_name = self.name

    def get_paint_price(self):
        room_paint_price = 0
        for painting_surface in self.painting_surfaces:
            room_paint_price += painting_surface.get_paint_price()
        return room_paint_price

    def get_labour_price(self):
        room_labour_price = 0
        for painting_surface in self.painting_surfaces:
            room_labour_price += painting_surface.get_labour_price()
        return room_labour_price

    def get_total_price(self):
        room_total_price = 0
        for painting_surface in self.painting_surfaces:
            room_total_price += painting_surface.get_total_price()
        return room_total_price

    def get_total_surface_area(self):
        room_surface_area = 0
        for painting_surface in self.painting_surfaces:
            room_surface_area += painting_surface.surface.area
        return room_surface_area

    def get_total_surface_area_by_condition(self, condition_list):
        total_surface_area_by_condition = 0
        for painting_surface in self.painting_surfaces:
            if painting_surface.surface.substrate.condition in condition_list:
                total_surface_area_by_condition += painting_surface.surface.area
        return total_surface_area_by_condition

    def get_breakdown(self):
        breakdown_list = []

        for painting_surface in self.painting_surfaces:
            breakdown_dict = painting_surface.get_breakdown()
            breakdown_list.append(breakdown_dict)

        return breakdown_list


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Job ---------------------------------------------------------------
class Job:
    def __init__(self, rooms, name=None):
        self.rooms = rooms

        if name is None:
            name = 'my job'

        self.name = name

    def get_total_price(self):
        total_job_price = 0
        for room in self.rooms:
            total_job_price += room.get_total_price()
        return total_job_price

    def get_breakdown(self):
        breakdown_list = []
        for room in self.rooms:
            breakdown_list.append(room.get_breakdown())
        return breakdown_list

    def get_painting_surface_list(self):
        rooms = self.rooms
        return self.get_painting_surface_list_from_room_list(rooms)

    @staticmethod
    def get_painting_surface_list_from_room_list(rooms):
        painting_surface_list = []
        for room in rooms:
            for painting_surface in room.painting_surfaces:
                painting_surface_list.append(painting_surface)

        # sorting list in preparation for knapsack algorithm which needs ascending order of cost
        painting_surface_list.sort(key=lambda x: x.get_total_price())

        return painting_surface_list

    @staticmethod
    def get_area_cost_lists(painting_surface_list):

        surface_area_list = []
        painting_price_list = []

        # creating value and cost lists for knapsack
        for painting_surface in painting_surface_list:
            surface_area_list.append(painting_surface.surface.area)
            painting_price_list.append(math.ceil(painting_surface.get_total_price()))

        return surface_area_list, painting_price_list

    def get_optimised_job(self, budget):

        surface_list = self.get_painting_surface_list()
        values, costs = self.get_area_cost_lists(surface_list)
        optimal_index_list = knapsack.optimal_knapsack(budget, values, costs)
        optimal_surface_list = [surface_list[i] for i in optimal_index_list]
        return OptimisedJob(optimal_surface_list, surface_list, budget)

    def get_sorted_room_list(self):
        sorted_room_list = []
        for room in self.rooms:
            sorted_room_list.append(room)
            sorted_room_list.sort(key=lambda x: x.get_total_price())
        return sorted_room_list

    def get_room_surface_area_list(self, sorted_room_list):
        room_surface_area_list = []
        for room in sorted_room_list:
            room_surface_area_list.append(room.get_total_surface_area())
        return room_surface_area_list

    def get_room_price_list(self, sorted_room_list):
        room_price_list = []
        for room in sorted_room_list:
            room_price_list.append(math.ceil(room.get_total_price()))
        return room_price_list

    def get_optimised_rooms_job(self, budget):
        sorted_room_list = self.get_sorted_room_list()
        room_surface_area_list = self.get_room_surface_area_list(sorted_room_list)
        room_price_list = self.get_room_price_list(sorted_room_list)
        optimal_room_index_list = knapsack.optimal_knapsack(budget, room_surface_area_list, room_price_list)
        optimal_room_list = [sorted_room_list[i] for i in optimal_room_index_list]
        budgeted_painting_surface_list = self.get_painting_surface_list_from_room_list(optimal_room_list)
        original_painting_surface_list = self.get_painting_surface_list_from_room_list(sorted_room_list)
        return OptimisedJob(budgeted_painting_surface_list, original_painting_surface_list, budget)

    def get_room_surface_area_by_condition_list(self, sorted_room_list, condition_list):
        room_surface_area_by_condition_list = []
        for room in sorted_room_list:
            room_surface_area_by_condition_list.append(room.get_total_surface_area_by_condition(condition_list))
        return room_surface_area_by_condition_list

    def get_optimised_condition_job(self, budget):
        sorted_room_list = self.get_sorted_room_list()
        condition_list = ['poor']
        room_surface_area_by_condition_list = self.get_room_surface_area_by_condition_list(sorted_room_list,
                                                                                           condition_list)
        room_price_list = self.get_room_price_list(sorted_room_list)
        optimal_room_index_list = knapsack.optimal_knapsack(budget, room_surface_area_by_condition_list,
                                                            room_price_list)
        optimal_room_list = [sorted_room_list[i] for i in optimal_room_index_list]
        budgeted_painting_surface_list = self.get_painting_surface_list_from_room_list(optimal_room_list)
        original_painting_surface_list = self.get_painting_surface_list_from_room_list(sorted_room_list)
        return OptimisedJob(budgeted_painting_surface_list, original_painting_surface_list, budget)


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Optimised Job -----------------------------------------------------
class OptimisedJob:
    def __init__(self, budgeted_painting_surface_list, original_painting_surface_list, budget):
        self.budgeted_painting_surface_list = sorted(budgeted_painting_surface_list, key=lambda x: x.surface.room_name)
        self.original_painting_surface_list = original_painting_surface_list
        self.budget = budget

    def get_breakdown(self):
        breakdown_list = []
        for painting_surface in self.budgeted_painting_surface_list:
            breakdown_dict = painting_surface.get_breakdown()
            breakdown_list.append(breakdown_dict)

        return breakdown_list

    def get_summary(self):
        summary_dict_original_job = self.get_surface_list_summary_statistics(self.original_painting_surface_list)
        summary_dict_budgeted_job = self.get_surface_list_summary_statistics(self.budgeted_painting_surface_list)

        final_summary_dict = dict(
            budget=self.budget,
            total_budgeted_job_price=summary_dict_budgeted_job['total_price'],
            total_surface_area_in_budget=summary_dict_budgeted_job['total_surface_area'],
            unpainted_surface_area=
            summary_dict_original_job['total_surface_area']-summary_dict_budgeted_job['total_surface_area'],
            cost_for_remaining_items=summary_dict_original_job['total_price']-summary_dict_budgeted_job['total_price'],
        )
        return final_summary_dict

    @staticmethod
    def get_surface_list_summary_statistics(surface_list):
        total_price = 0
        total_surface_area = 0
        for painting_surface in surface_list:
            total_price += painting_surface.get_total_price()
            total_surface_area += painting_surface.surface.area
        return dict(
            total_price=total_price,
            total_surface_area=total_surface_area,
        )



# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Other things ------------------------------------------------------
def get_total_surface_area(surfaces):
    total_surface_area = 0
    for surface in surfaces:
        total_surface_area += surface.area
    return total_surface_area


class ConditionAssumptions():
    def __init__(self):
        poor = '''Poor condition is where lots of preparation is required. Surfaces exhibit cracking, gaps not filled,
        previously poorly painted with drips and fibres in the surface paint.'''
        okay = '''Okay condition is where some small amount of preparation is needed, 
        there is very little filling and sanding required'''
        good = '''Good condition is where there is almost no preparation required'''

        self.poor = poor
        self.okay = okay
        self.good = good

    @staticmethod
    def get_condition_assumption(condition):
        if condition == 'poor':
            return 'poor_example.jpg'
        else:
            return 'poor_example.jpg'

# optional stuff

# add tooltips
# add assumptions - including brand of defaults
# add instructions (text box) maybe download complete instruction file
# headings widgets.HTML

# extend optimiser to rooms

# bring primer in to bare wood and mdf
# option to apply trade discount to materials price get paint price discount in painting surface
# flexible unit sizes or option to not round up units to get around multiple uses of same paints
# options to combine same paint type and colour used on multiple surfaces to avoid buying more paint that needed
