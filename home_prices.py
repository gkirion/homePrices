import urllib.request
import datetime
import re
import random
import time
from pyquery import PyQuery

city_codes = {
    'Γουδή': 83040,
    'Κέντρο Αθήνας': 82271,
    'Εξάρχεια': 82399,
    'Περισσός': 83175,
    'Μαρούσι': 82433,
    'Ζωγράφου': 82470
}

cookie = "property_preferences=%257B%2522closedClusters%2522%253A%257B%257D%252C%2522selectedPois%2522%253A%255B%255D%252C%2522cpOpen%2522%253Afalse%252C%2522proPagesClusters%2522%253A%257B%257D%252C%2522comparisonListHeight%2522%253A0%252C%2522last_searched_in%2522%253A%255B%257B%2522id%2522%253A%252283040%2522%252C%2522loc%2522%253A%2522%25u0393%25u03BF%25u03C5%25u03B4%25u03AE%2522%257D%255D%257D; __SID=0B518BB8-BE2D-11EA-9BFC-3AF6DEF8D836; __XE_COOKIE=b8e0e87f610334c416c9ca73b13e1ac0; xe_preferences=%257B%2522comparisonListHeight%2522%253A154%252C%2522cpOpen%2522%253Afalse%257D; _ga=GA1.2.920661430.1593809642; _gid=GA1.2.1191612314.1593809642; __utma=175768868.920661430.1593809642.1593811754.1593882342.3; __utmc=175768868; __utmz=175768868.1593809642.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _fbp=fb.1.1593809642583.140122355; intercom-id-bewzsb79=ba599372-e1a2-443c-9910-88588d8bf95b; intercom-session-bewzsb79=; cto_lwid=97c4cf0f-29cd-4122-8d96-cc7093b79952; cto_bundle=eGl_SF9WNjk4VXZramJZelJwWHdFVUFXaXJqTDdlUkh1UGFoJTJCSFYlMkJuUExzYkJJR2pWRGhrUXAxVWlUdlA0dFBWZiUyRkRGZ2szTGc0b1YyRVJHd2Zic2cweGc4ZXN1ZjkwZGglMkJtOTR6enF0NkwxSWRYbCUyRkg2RjklMkJ0ZkJvOFJ2MXJoclJSZ1AlMkZKRzU4Tmc0VGVPZGJDNk92cVQyUGVPOCUyQkdVQmNkc3BJeVQlMkZvTVJHYVklM0Q; __utmb=175768868.36.9.1593891638551; reese84=3:wE78ZmklHyeaVr661QIJKQ==:t69T0nFgJfYVtN7k8XVLTg6tytB7Yrkd4oChwgEElvdSjjoe+ialYAkqeSeCh7h39OLtxE2KYWWVcq31pz7SuRbTnWoCOcBsnqz0RDnh6JaUVTiUCRVd0vg+XuFf2x70hf7I+wyFAIeexF1XxTomcOaDBLHjOaE1Qy1tEbjl/93qMtXQpDVaM6tDprFaehjntEYLtGWh1fzTdTTYVEbqo23BHFod29r/hRd32J33Ic7xuqkeME5sSJ2JlG18/Yp0RcErzk8mVRJrU1D8tCItaZ14PkLUEbGTb+wxIh4vDmXMNQv8BFdyU0fXWwHzh0t2iZakf0CjUmee8JxJGKMOxgG811UOvu9TPJV3oMMQMTVISCkKoVfjw20FmVkAuSyA7HNcSiDBhQ35z/89j8cgobXVO/XZ1hFLOv0aqazeqONuBzKBPaSfSQw5PBs/xvUHU1jrXdtGHJpAUNIC37DOrATvW5viZWyKFxFdVjLfSOE=:je4mqpHymOpQlBbkaKZ0yvj0NQCPUk66nWiymp5dvOQ=; __utmt=1; _gat_UA-88292460-1=1"

def get_stats_for_city(city, area_from, area_to):
    request = urllib.request.Request("https://www.xe.gr/property/search?Geo.area_id_new__hierarchy={}&System.item_type=re_residence&Transaction.type_channel=117541&Item.area.from={}&Item.area.to={}&page={}".format(city_codes[city], area_from, area_to, 1))
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0")
    request.add_header("Cookie", cookie)
    
    response = urllib.request.urlopen(request).read()
    pyquery = PyQuery(response)
    number_of_pages = get_number_of_pages(pyquery)
        
    print("number of pages: {}".format(number_of_pages))
    total_number_of_homes = 0
    total_size = 0
    total_price = 0
    for page in range(1, number_of_pages + 1):
        time_wait = 5 + random.randrange(0, 10)
        print("waiting for: {} seconds".format(time_wait))
        time.sleep(time_wait)
        print("page: {}".format(page))
        request = urllib.request.Request("https://www.xe.gr/property/search?Geo.area_id_new__hierarchy={}&System.item_type=re_residence&Transaction.type_channel=117541&Item.area.from={}&Item.area.to={}&page={}".format(city_codes[city], area_from, area_to, page))
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0")
        request.add_header("Cookie", cookie)

        response = urllib.request.urlopen(request).read()
        pyquery = PyQuery(response)
        homes = pyquery(".articleInfo")
        number_of_homes = len(list(homes.items()))
        print("page {} number of homes: {}".format(page, number_of_homes))
        for home in homes.items():
            home_info = list(home.items("h1"))[0].html()
            home_info = home_info.split("\n")[2]
            print("home info: {}".format(home_info))
            cleanr = re.compile('<.*?>')
            home_info = re.sub(cleanr, '', str(home_info))
            print("home info: {}".format(home_info))
            home_info = home_info.split("|")
            try:
                print("size: {}".format(home_info[0].strip()))
                print("price: {}".format(home_info[1].strip()))
                size = int(home_info[0].strip().replace("τ.μ.", ""))
                price = int(home_info[1].strip().replace("€", "").replace(".", ""))
                try:
                    if price > 20000:
                        raise ValueError
                    total_size += size
                    total_price += price
                    total_number_of_homes += 1
                except ValueError:
                    pass
            except:
                pass

    return (total_number_of_homes, total_size, total_price)

def get_number_of_pages(pyquery):
    page_label = pyquery(".pager")
    number_of_pages = 0
    for item in page_label.items("a"):
        try:
            num = int(item.html())
            if num > number_of_pages:
                number_of_pages = num
        except ValueError:
            pass
    return number_of_pages
            
city = input('Περιοχή: ')
area_from = input('Τετραγωνικά (από): ')
area_to = input('Τετραγωνικά (έως): ')

(total_number_of_homes, total_size, total_price) = get_stats_for_city(city, area_from, area_to)            
d = datetime.datetime.now()
print("date: {}".format(d.strftime("%d/%m/%Y")))
print("city: {}".format(city))
print("size: {}-{} τ.μ.".format(area_from, area_to))
print("found {} homes".format(total_number_of_homes))
print("avg. size: {} τ.μ.".format(round(total_size / total_number_of_homes, 2)))
print("avg. price: {} €".format(round(total_price / total_number_of_homes, 2))) 
