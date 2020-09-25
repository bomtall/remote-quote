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


class PaintingSurface:
    def __init__(self, surface, paint):
        self.surface = surface
        self.paint = paint

    def get_units_of_paint(self):
        units_of_paint = math.ceil(self.surface.area / self.paint.coverage)
        return units_of_paint

    def get_paint_price(self):
        paint_price = self.get_units_of_paint() * self.paint.price
        return paint_price

