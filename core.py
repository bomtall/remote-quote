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
            coverage_adjustment=None,
    ):
        print('Hello')
        if area is None:
            assert length is not None and width is not None, 'Input either "area" or "length" and "width".'
            assert isinstance(length, Number), 'Input "length" needs to be numeric.'
            assert isinstance(width, Number), 'Input "width" needs to be numeric.'
            area = length * width
        else:
            assert length is None and width is None, 'Input either "area" or "length" and "width".'
            assert isinstance(area, Number), 'Input "area" needs to be numeric.'

        if coverage_adjustment is None:
            coverage_adjustment = 1
        else:
            assert isinstance(coverage_adjustment, Number), 'Input "coverage_adjustment" needs to be numeric.'

        self.area = area
        self.length = length
        self.width = width
        self.coverage_adjustment = coverage_adjustment


class Wall(Surface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ceiling(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)


class Door(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class Doorframe(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class Skirtingboard(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class Window(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class Windowsill(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class Spindle(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class ElaborateCornice(Surface):
    def __init__(self, *args, coverage_adjustment=None, **kwargs):
        if coverage_adjustment is None:
            coverage_adjustment = 1.1
        super().__init__(*args, **kwargs, coverage_adjustment=coverage_adjustment)

class Substrate:
    def __init__(
            self,
            num_coats=None,
            porosity=None,
            condition=None,

    ):
        self.num_coats = num_coats
        self.porosity = porosity
        self.condition = condition

class Plaster(Substrate):
    def __init__(self, *args, num_coats=None, **kwargs):
        if num_coats is None:
            num_coats = 2

        super().__init__(*args, **kwargs, num_coats=num_coats)





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
    def __init__(self, price, unit, coverage):

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
        units_of_paint = math.ceil(self.surface.area / self.paint.coverage)
        return units_of_paint

    def get_paint_price(self):
        paint_price = self.get_units_of_paint() * self.paint.price
        return paint_price

    def get_labour_price(self):
        labour_price = self.surface.area * self.labour_price_msq * self.surface.coverage_adjustment
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


class Job:
     def __init__(self, painting_surfaces):
         self.painting_surfaces = painting_surfaces

     def get_paint_price(self):
         job_paint_price = 0
         for painting_surface in self.painting_surfaces:
             job_paint_price += painting_surface.get_paint_price()
         return job_paint_price

     def get_labour_price(self):
         job_labour_price = 0
         for painting_surface in self.painting_surfaces:
             job_labour_price += painting_surface.get_labour_price()
         return job_labour_price

     def get_total_price(self):
         job_total_price = 0
         for painting_surface in self.painting_surfaces:
             job_total_price += painting_surface.get_total_price()
         return job_total_price

#TODO worry about units of paint and paint price when adding up for same paint