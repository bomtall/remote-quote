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
