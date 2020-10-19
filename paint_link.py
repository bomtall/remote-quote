import core
import requests
from bs4 import BeautifulSoup
import json

#TODO create better tests

def get_price(url, index):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all(name='script', attrs={"type": "text/javascript"})
    paint_data = json.loads(scripts[0].contents[0].split('function')[0].split('=')[-1].rstrip(',];\r\n ') + ']')
    price = float(paint_data[index]['price_ex_vat'])
    return price


class Matt(core.Paint):
    def __init__(self,):
        coverage = 50
        unit = 5
        #price = get_price("https://www.duluxdecoratorcentre.co.uk/dulux-trade-vinyl-matt", 19)
        price = 37.87
        super().__init__(price, unit, coverage)



class Diamond(core.Paint):
    def __init__(self):
        coverage = 50
        unit = 5
        #price = get_price("https://www.duluxdecoratorcentre.co.uk/dulux-trade-diamond-matt", 6)
        price = 50.03
        super().__init__(price, unit, coverage)
