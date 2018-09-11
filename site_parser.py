from urllib import request
from bs4 import BeautifulSoup
import re

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

def parse_news_water(news_list):
    output = []
    for news in news_list:
        tmp = {}
        tmp["date"] = news.find("span").text
        tmp["title"] = news.find("h1").text
        tmp["text"] = re.sub("[\r\n\t]", "",
                            news.find("div", attrs={"class": "text-preview"}).text)
        tmp["link"] = water_url[:-1] + news.find("a")["href"]
        output.append(tmp)
    return output

def get_date_electro(calendar):
    day = calendar.find("div", attrs = {"class": "day"}).text
    month = calendar.find("div", attrs = {"class": "month"}).text
    year = calendar.find("div", attrs = {"class": "year"}).text
    return "-".join([day,month,year])

def parse_news_electro(news_list):
    output = []
    for news in news_list:
        tmp = {}
        tmp["date"] = get_date_electro(news.find("div", attrs = {"class": "calendar"}))
        tmp["title"] = news.find("p", attrs = {"style": "text-align: center;"}).text
        tmp["text"] = " ".join(list(map(lambda x: x.text ,news.find_all("p"))))
        tmp["link"] = ""
        output.append(tmp)
    return output

if __name__ == "__main__":
    #news_list_water = get_page_data(water_url, 3)
    #print(parse_news_water(news_list))
    #news_list_electro = get_page_data(electro_url_plan, 1, parse_attrs_electro)
    #print(parse_news_electro(news_list_electro))