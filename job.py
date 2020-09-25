import math


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
