import core
import requests
from bs4 import BeautifulSoup
import json

def get_price(url, index):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all(name='script', attrs={"type": "text/javascript"})
    paint_data = json.loads(scripts[0].contents[0].split('function')[0].split('=')[-1].rstrip(',];\r\n ') + ']')
    price = float(paint_data[index]['price_ex_vat'])
    return price


class Matt(core.Paint):
    def __init__(self,):
        coverage = 17
        unit = 5
        price = get_price("https://www.duluxdecoratorcentre.co.uk/dulux-trade-vinyl-matt", 19)
        super().__init__(price, unit, coverage)



class Diamond(core.Paint):
    def __init__(self):
        coverage = 17
        unit = 5
        price = get_price("https://www.duluxdecoratorcentre.co.uk/dulux-trade-diamond-matt", 6)
        super().__init__(price, unit, coverage)
