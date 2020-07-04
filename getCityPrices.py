import urllib.request
import time
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

def get_stats_for_city(city, area_from, area_to):
    time.sleep(5)
    response = urllib.request.urlopen("https://www.xe.gr/property/search?Geo.area_id_new__hierarchy={}&System.item_type=re_residence&Transaction.type_channel=117541&Item.area.from={}&Item.area.to={}&page={}".format(city_codes[city], area_from, area_to, 1)).read()
    time.sleep(5)
    pyquery = PyQuery(response)
    page_label = pyquery("#r_paging_label")
    print(page_label.html())
    number_of_pages = int(page_label.find("strong").eq(1).html())
    print("numer of pages: {}".format(number_of_pages))
    total_number_of_homes = 0
    total_price = 0
    for page in range(1, number_of_pages + 1):
        print("page: {}".format(page))
        time.sleep(5)
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
    return (total_number_of_homes, total_price)

city_number_of_homes = {}
city_price = {}
for city in ['Γουδή', 'Κέντρο Αθήνας', 'Εξάρχεια', 'Περισσός', 'Μαρούσι', 'Ζωγράφου']:         
    (total_number_of_homes, total_price) = get_stats_for_city(city, 65, 85)
    city_number_of_homes[city] = total_number_of_homes
    city_price[city] = round(total_price / total_number_of_homes, 2)

d = datetime.datetime.now()
print(city_number_of_homes)
print(city_price)

f = open('C:\\Users\\george\\Desktop\\homeAvailability.txt', 'a')
f.write(d.strftime("%d/%m/%Y") + ', ' + str(list(city_number_of_homes.values())).replace('[', '').replace(']', '') + '\n')
f.close()
f = open('C:\\Users\\george\\Desktop\\homePrices.txt', 'a')
f.write(d.strftime("%d/%m/%Y") + ', ' + str(list(city_price.values())).replace('[', '').replace(']', '') + '\n')
f.close()
