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

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
cookie = "property_preferences=%257B%2522cpOpen%2522%253Afalse%252C%2522comparisonListHeight%2522%253A0%257D; _ga=GA1.2.1523927993.1587634174; _fbp=fb.1.1587634174520.968124052; intercom-id-bewzsb79=f05fe1c0-f331-41bb-982a-afc4cb9c5723; __utmz=175768868.1590512322.5.4.utmcsr=xe.gr|utmccn=(referral)|utmcmd=referral|utmcct=/; __XE_COOKIE=d4b2b9b4ae8dfe7f5fa4765255e65b55; xe_preferences=%257B%2522comparisonListHeight%2522%253A152%252C%2522cpOpen%2522%253Afalse%257D; __utmc=175768868; _gid=GA1.2.876816069.1593892901; intercom-session-bewzsb79=; reese84=3:CeImY8+rWFaLg1TWjJVejg==:AOWYR7lVSXSgSCtaaZDLf4iIYzyRYTVRqjoZxp2ybHWYEi0ER66+314uWMU2uoq1hxL30lLyUdhJAbOHwnsZnfwuW7tVYCwnF56+Ncq7M3XFPUy1V45/sp5t+9a2dZDOjVC7RapmPAhdYILHA7YA/DLrw9Qh5mncGlP31Q95VGSX3iH1wAg7qx793Bfw353pCXilgUuUmDVqiN4HljEbLfgrFowjEOrJ45eUSgVXAW0RPB+5uTZ8TkAO6YNUq1NteXZTZ/DHPhDaBlo6OUZK9eCy4VqMV4a+Z0WfQscpaA9Gp8OVHLrJRS70LjcdXwDMCtv9eEzteuB29G/NIF2lKLHZUn7iCZT3nn/O+rAk9iGGYXs099zGaLMlhLrfEqDYdG8ircYTBj+7wTf6spgBTINoJKGzMsK8DVzoL5BUWPo=:8QMsNXc8OVI6c3w1jN973nmXiYMES07MSHmWeutkDUg=; __SID=A355267E-BE4E-11EA-941A-480570352EC9; __utma=175768868.1523927993.1587634174.1593892901.1593905562.7; __utmt=1; __utmb=175768868.3.10.1593905562"

def get_stats_for_city(city, area_from, area_to, floor_from, floor_to, construction_from, construction_to):
    
    total_number_of_homes = 0
    total_size = 0
    total_price = 0

    page = 1
    while True:
        time_wait = 5 + random.randrange(0, 10)
        print("waiting for: {} seconds".format(time_wait))
        time.sleep(time_wait)
        print("page: {}".format(page))

        request = urllib.request.Request("https://www.xe.gr/property/search?Geo.area_id_new__hierarchy={}&System.item_type=re_residence&Transaction.type_channel=117541&Item.area.from={}&Item.area.to={}&Publication.level_num.from={}&Publication.level_num.to={}&Item.construction_year.from={}&Item.construction_year.to={}&page={}".format(city_codes[city], area_from, area_to, floor_from, floor_to, construction_from, construction_to, page))
        request.add_header("User-Agent", user_agent)
        request.add_header("Cookie", cookie)

        response = urllib.request.urlopen(request).read()
        pyquery = PyQuery(response)
        (number_of_homes, size, price) = parse_page(pyquery)
        print("page {} number of homes: {}".format(page, number_of_homes))
        total_number_of_homes += number_of_homes
        total_size += size
        total_price += price
        number_of_pages = get_number_of_pages(pyquery)
        if number_of_pages <= page:
            break
        page += 1
    return (total_number_of_homes, total_size, total_price)

    

def parse_page(pyquery):   
    total_number_of_homes = 0
    total_size = 0
    total_price = 0

    homes = pyquery(".articleInfo")
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
floor_from = input('Όροφος (από): ')
floor_to = input('Όροφος (έως): ')
construction_from = input('Χρονολογία (από): ')
construction_to = input('Χρονολογία (έως): ')

(total_number_of_homes, total_size, total_price) = get_stats_for_city(city, area_from, area_to, int(floor_from) + 1, int(floor_to) + 1, construction_from, construction_to)            
d = datetime.datetime.now()
print("date: {}".format(d.strftime("%d/%m/%Y")))
print("city: {}".format(city))
print("size: {}-{} τ.μ.".format(area_from, area_to))
print("found {} homes".format(total_number_of_homes))
if (total_number_of_homes > 0):
    print("avg. size: {} τ.μ.".format(round(total_size / total_number_of_homes, 2)))
    print("avg. price: {} €".format(round(total_price / total_number_of_homes, 2))) 
