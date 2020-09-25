from numbers import Number


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