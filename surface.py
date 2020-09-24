from numbers import Number


class SurfaceWithOnlyArea:
    def __init__(self, area):
        assert isinstance(area, Number), 'Input "area" needs to be numeric.'
        self.area = area


class Surface(SurfaceWithOnlyArea):
    def __init__(self, area=None, length=None, width=None):
        if area is None:
            assert length is not None and width is not None, 'Input either "area" or "length" and "width".'
            assert isinstance(length, Number), 'Input "length" needs to be numeric.'
            assert isinstance(width, Number), 'Input "width" needs to be numeric.'
            area = length * width
        else:
            assert length is None and width is None, 'Input either "area" or "length" and "width".'
        super().__init__(area)
        self.length = length
        self.width = width