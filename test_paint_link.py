import paint_link
import pytest
import core


#def test_get_price():
    #price = paint_link.get_price("https://www.duluxdecoratorcentre.co.uk/dulux-trade-vinyl-matt", 19)
    #assert price == 31.56

@pytest.mark.parametrize(
    'args, kwargs, paint_class, expected',
    [
        #Testing instantiation of defaults
        ([], dict(), paint_link.MattEmulsionPaint, 37.87),
        ([], dict(), paint_link.SilkEmulsionPaint, 46.27),
        ([], dict(), paint_link.DiamondMattEmulsion, 50.03),
        ([], dict(), paint_link.OilEggshell, 32.07),
        ([], dict(), paint_link.OilGloss, 19.00),
        ([], dict(), paint_link.OilSatin, 37.20),
        ([], dict(), paint_link.Primer, 31.15),
        ([], dict(price=20.00, unit=5, coverage=17), paint_link.EmulsionPaint, 20.00),
        ([], dict(price=20.00, unit=5, coverage=17), paint_link.OilPaint, 20.00),
        ([], dict(price=20.00, unit=5, coverage=17), core.Paint, 20.00),


    ],
)
def test_paint_classes(args, kwargs, paint_class, expected):
    s = paint_class(*args, **kwargs)
    assert s.price == expected



