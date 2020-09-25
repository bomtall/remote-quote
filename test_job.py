import job
import surface
import paint


def test_painting_surface():
    s = surface.Wall(20)
    p = paint.Paint(30, 5, 17)

    j = job.PaintingSurface(s, p)

    units_of_paint = j.get_units_of_paint()
    assert units_of_paint == 2

    paint_price = j.get_paint_price()
    assert paint_price == 60
