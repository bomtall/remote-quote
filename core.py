from numbers import Number
import math

# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# surface


class Surface:
    def __init__(
            self,
            area=None,
            length=None,
            width=None,
            labour_adjustment=None,
            substrate=None,
            design=None,
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


class Wall(Surface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ceiling(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        if labour_adjustment is None:
            labour_adjustment = 1.1
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment)


class Door(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, num_panes=0, **kwargs):

        assert design in ['panelled', 'flat door',
                          'cutting in', None], 'input needs to be "panelled", "flat door", "cutting in" or None'
        assert isinstance(num_panes, int) and num_panes >= 0, 'Input "num_panes" needs to be a non-negative integer'
        assert (num_panes > 0 and design == 'cutting in') or \
               (num_panes == 0 and design in ['panelled', 'flat door', None]), 'Only "cutting in" doors have panes > 0'

        if num_panes > 0:
            design = 'cutting in'
        if design is None:
            design = 'flat door'


        if labour_adjustment is None:
            labour_adjustment = 2
            if design == 'panelled':
                labour_adjustment = 2.1
            elif design == 'cutting in':
                if num_panes < 3:
                    labour_adjustment = 2.5
                else:
                    labour_adjustment = min(3/2 * (num_panes + 1), 15)

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design)
        self.num_panes = num_panes

class Doorframe(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, **kwargs):

        if design is None:
            design = 'standard'
        else:
            assert design in ['standard', 'victorian', 'elaborate'],\
                'input needs to be "standard", "victorian", "elaborate" or None'

        if labour_adjustment is None:
            labour_adjustment = 2
            if design == 'victorian':
                labour_adjustment = 2.1
            elif design == 'elaborate':
                labour_adjustment = 2.2
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design)

class Skirtingboard(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        if labour_adjustment is None:
            labour_adjustment = 1.1
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment)

class Window(Surface):
    def __init__(self, *args, labour_adjustment=None, num_panes=1, **kwargs):
        assert isinstance(num_panes, int) and num_panes >= 1, '"num_panes" needs to be an integer and >= 1'
        if labour_adjustment is None:
            labour_adjustment = (2 * num_panes)



        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment)
        self.num_panes = num_panes

class Windowsill(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        if labour_adjustment is None:
            labour_adjustment = 1.1
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment)

class Spindle(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, **kwargs):
        if design is None:
            design = 'square'
        else:
            assert design in ['square', 'shaped', 'elaborate'], \
                'input needs to be "square", "shaped", "elaborate" or None'

        if labour_adjustment is None:
            labour_adjustment = 2
            if design == 'shaped':
                labour_adjustment = 2.1
            elif design == 'elaborate':
                labour_adjustment = 2.2
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design)

class ElaborateCornice(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        if labour_adjustment is None:
            labour_adjustment = 2
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment)

class Substrate:
    def __init__(
            self,
            num_coats=None,
            porosity=None,
            condition=None,
            coverage_adjustment=None,

    ):
        assert condition in [None, 'poor', 'okay', 'good'], 'Input "condition" needs to be "poor", "okay", "good" or None'
        if condition is None:
            condition = 'good'
        assert isinstance(num_coats, int) or num_coats is None, 'Input "num_coats" needs to be an integer or None'
        assert (isinstance(coverage_adjustment, Number) and coverage_adjustment > 0.0) or (coverage_adjustment is None),\
            'Input needs to be numeric and > 0, or None'

        if coverage_adjustment is None:
            coverage_adjustment = 1

        ##TODO add in validation for porosity

        self.num_coats = num_coats
        self.porosity = porosity
        self.condition = condition
        self.preparation_factor = self.get_preparation_factor()
        self.coverage_adjustment = coverage_adjustment

    def get_preparation_factor(self):
        if self.condition == 'poor':
            preparation_factor = 1.1
        elif self.condition == 'okay':
            preparation_factor = 1.05
        else:
            preparation_factor = 1

        return preparation_factor


class Plaster(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, **kwargs):
        if num_coats is None:
            num_coats = 2
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)


class PrePaintedEmulsion(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        if num_coats is None and condition == 'poor':
            num_coats = 2
        elif num_coats is None:
            num_coats = 1
        if coverage_adjustment is None:
            coverage_adjustment = 1
        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition, coverage_adjustment=coverage_adjustment)


class PrePaintedWood(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        if num_coats is None and condition == 'poor':
            num_coats = 2
        elif num_coats is None:
            num_coats = 1
        if coverage_adjustment is None:
            coverage_adjustment = 1
        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition, coverage_adjustment=coverage_adjustment)


class NewLiningPaper(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        if num_coats is None:
            num_coats = 2
        if condition is None:
            condition = 'good'
        if coverage_adjustment is None:
                coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment, condition=condition)
        self.preparation_factor = self.get_preparation_factor()


class Mdf(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, primed=False, **kwargs):
        if num_coats is None:
            num_coats = 3
        if primed:
            num_coats = 2

        if condition is None:
            condition = 'good'
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition, coverage_adjustment=coverage_adjustment)
        self.preparation_factor = self.get_preparation_factor()

        self.primed = primed


class NewWood(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        if num_coats is None:
            num_coats = 3
        if condition is None:
            condition = 'good'
        if coverage_adjustment is None:
            coverage_adjustment = 1.05

        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition, coverage_adjustment=coverage_adjustment)





def get_total_surface_area(surfaces):
    total_surface_area = 0
    for surface in surfaces:
        total_surface_area += surface.area
    return total_surface_area


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# PAINT

class Paint:
    def __init__(self, price, unit, coverage,):

        assert isinstance(price, Number), 'Input "price" needs to be numeric.'
        assert isinstance(unit, Number), 'Input "unit" needs to be numeric.'
        assert isinstance(coverage, Number), 'Input "coverage" needs to be numeric.'

        self.price = price
        self.unit = unit
        self.coverage = coverage



# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# JOB

#TODO add validation for inputs to painting surface

class PaintingSurface:
    def __init__(self, surface, paint, labour_price_msq=None):
        if labour_price_msq is None:
            labour_price_msq = 4

        self.surface = surface
        self.paint = paint
        self.labour_price_msq = labour_price_msq

#TODO make calculation reflect unit and coverage properly
    def get_units_of_paint(self):
        units_of_paint = math.ceil((self.surface.area /
            (self.paint.coverage/self.surface.substrate.coverage_adjustment)) * self.surface.substrate.num_coats)
        return units_of_paint

    def get_paint_price(self):
        paint_price = self.get_units_of_paint() * self.paint.price
        return paint_price

    def get_labour_price(self):
        labour_price = self.surface.area * self.labour_price_msq * self.surface.labour_adjustment * \
            self.surface.substrate.num_coats
        return labour_price

    def get_total_price(self):
        total_price = self.get_labour_price() + self.get_paint_price()
        return total_price


    def get_breakdown(self):

        breakdown = dict(
            total_price = self.get_total_price(),
            labour_price = self.get_labour_price(),
            paint_price = self.get_paint_price(),
            units_of_paint = self.get_units_of_paint(),
        )
        return breakdown


class Room:
     def __init__(self, painting_surfaces):
         self.painting_surfaces = painting_surfaces

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

class Job:
    def __init__(self, rooms):
        self.rooms = rooms

    def get_total_job_price(self):
        total_job_price = 0
        for room in self.rooms:
            total_job_price += room.get_total_price()
        return total_job_price




#TODO worry about units of paint and paint price when adding up for same paint