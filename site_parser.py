from urllib import request
from bs4 import BeautifulSoup
import re
from functools import partial

water_url = "http://sevvodokanal.org.ru/"
electro_url_emergency = "http://sevenergo.net/avarijnye-i-vneplanovye-otklyucheniya.html"
electro_url_plan = "http://sevenergo.net/ezhemesyachnyj-grafik-planovykh-remontnykh-rabot.html"

parse_attrs_water = {"class": "right-preview"}
parse_attrs_electro= {"itemprop": "blogPost"}

def get_page_data(url, num_news, parse_attrs):
    with request.urlopen(url) as page:
        soup = BeautifulSoup(page, "html.parser")
        news = soup.find_all("div", attrs=parse_attrs, limit=num_news)
    return news

def parse_news_water(news):
    tmp = {}
    tmp["date"] = news.find("span").text
    tmp["title"] = news.find("h1").text
    tmp["text"] = re.sub("[\r\n\t]", "",
                        news.find("div", attrs={"class": "text-preview"}).text)
    tmp["link"] = water_url[:-1] + news.find("a")["href"]
    return tmp

def generate_messages(data, function):
    return list(map(function, data))

def get_date_electro(calendar):
    day = calendar.find("div", attrs = {"class": "day"}).text
    month = calendar.find("div", attrs = {"class": "month"}).text
    year = calendar.find("div", attrs = {"class": "year"}).text
    return "-".join([day,month,year])

def parse_news_electro_helper(news, link):
    tmp = {}
    tmp["date"] = get_date_electro(news.find("div", attrs = {"class": "calendar"}))
    tmp["title"] = news.find("p", attrs = {"style": "text-align: center;"}).text
    tmp["text"] = " ".join(list(map(lambda x: x.text ,news.find_all("p"))))
    tmp["link"] = link
    return tmp

def parse_news_electro_plan(news):
    parser = partial(parse_news_electro_helper, link=electro_url_plan)
    return parser(news)

def parse_news_electro_emergency(news):
    parser = partial(parse_news_electro_helper, link=electro_url_emergency)
    return parser(news)

def get_messages_main(message_type, count=3):
    if message_type == "water":
        news_list_water = get_page_data(water_url, count, parse_attrs_water)
        return generate_messages(news_list_water, parse_news_water)
    elif message_type == "electro_plan":
        news_list_electro_plan = get_page_data(electro_url_plan, 1, parse_attrs_electro)
        return generate_messages(news_list_electro_plan, parse_news_electro_plan)
    elif message_type == "electro_emg":
        news_list_electro_emrg = get_page_data(electro_url_emergency, count, parse_attrs_electro)
        return generate_messages(news_list_electro_emrg, parse_news_electro_emergency)

if __name__ == "__main__":
    news_list_water = get_page_data(water_url, 3, parse_attrs_water)
    news_list_electro_plan = get_page_data(electro_url_plan, 1, parse_attrs_electro)
    news_list_electro_emrg = get_page_data(electro_url_emergency, 3, parse_attrs_electro)
    water_messages = generate_messages(news_list_water, parse_news_water)
    electro_plan_messages = generate_messages(news_list_electro_plan, parse_news_electro_plan)
    electro_emg_messages = generate_messages(news_list_electro_emrg, parse_news_electro_emergency)
