from numbers import Number


class SurfaceArea:
    def __init__(self, area):
        assert isinstance(area, Number), 'Input "area" needs to be numeric.'
        self.area = area

