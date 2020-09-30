from bs4 import BeautifulSoup
import requests

def scraping_time():
    country_time = dict()
    # response is answer of the get of the world time in the web with url https://www.timeanddate.com/worldclock/
    response = requests.get("https://www.timeanddate.com/worldclock/")
    #using Beautifulsoup scraping the web
    bs = BeautifulSoup(response.text, 'html.parser')
    bs1 = bs.select('td a')  #this is for scraping different country
    bs2 = bs('td', attrs={'class':'rbi'}) #this is for scraping the real time of different country
    for link, time in zip(bs1, bs2):
        country_time[link.get_text()] = time.get_text()
    return country_time

def get_list_country():
    list_of_all_country = list(scraping_time().keys())
    list_reshaped_country = []
    slice_country = []
    for i in range(len(list_of_all_country)):
        if i%3 == 0 and i != 0:
            list_reshaped_country.append(slice_country)
            slice_country = []
        slice_country.append(list_of_all_country[i])
    list_reshaped_country.append(slice_country)
    return list_reshaped_country