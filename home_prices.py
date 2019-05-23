import urllib.request
import datetime
from pyquery import PyQuery

city_codes = {
    'Γουδή': 83040,
    'Κέντρο Αθήνας': 82271,
    'Εξάρχεια': 82399,
    'Περισσός': 83175,
    'Μαρούσι': 82433,
    'Ζωγράφου': 82470
}

city = input('Περιοχή: ')
area_from = input('Τετραγωνικά (από): ')
area_to = input('Τετραγωνικά (έως): ')
response = urllib.request.urlopen("https://www.xe.gr/property/search?Geo.area_id_new__hierarchy={}&System.item_type=re_residence&Transaction.type_channel=117541&Item.area.from={}&Item.area.to={}&page={}".format(city_codes[city], area_from, area_to, 1)).read()
pyquery = PyQuery(response)
page_label = pyquery("#r_paging_label")
print(page_label.html())
number_of_pages = int(page_label.find("strong").eq(1).html())
print("numer of pages: {}".format(number_of_pages))
total_number_of_homes = 0
total_price = 0
for page in range(1, number_of_pages + 1):
    print("page: {}".format(page))
    response = urllib.request.urlopen("https://www.xe.gr/property/search?Geo.area_id_new__hierarchy={}&System.item_type=re_residence&Transaction.type_channel=117541&Item.area.from={}&Item.area.to={}&page={}".format(city_codes[city], area_from, area_to, page)).read()
    pyquery = PyQuery(response)
    homes = pyquery(".r_price")
    number_of_homes = len(list(homes.items()))
    for home in homes.items():
        if (home(".r_price").html() != None):
            try:
                price = int(home(".r_price").html().split(' ')[0].replace('.', ''))
                if price > 20000:
                    raise ValueError
                print(price)
                total_price += price
                total_number_of_homes += 1
            except ValueError as identifier:
                pass
            
d = datetime.datetime.now()
print("date: {}".format(d.strftime("%d/%m/%Y")))
print("found {} homes".format(total_number_of_homes))
print("avg. price: {} €".format(round(total_price / total_number_of_homes, 2)))
