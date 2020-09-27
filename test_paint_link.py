import paint_link

def test_get_price():
    price = paint_link.get_price("https://www.duluxdecoratorcentre.co.uk/dulux-trade-vinyl-matt", 19)
    assert price == 31.56