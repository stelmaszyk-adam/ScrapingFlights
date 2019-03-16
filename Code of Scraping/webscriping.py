import csv
import datetime
import os
import time
import re
import random

import sys

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from lxml.html import fromstring
from itertools import cycle
from requests import Request, Session
from bs4 import BeautifulSoup

it_is_work = False


class Kayak:

    def __init__(self, fake):
        try:
            path = "/Users/adamstelmaszyk/chromedriver"
            self.chromeOptions = Options()
            self.chromeOptions.add_argument("--user-agent=" + fake)
            self.chromeOptions.add_argument('--disable-extensions')
            self.chromeOptions.add_argument('--profile-directory=Default')
            self.chromeOptions.add_argument("--disable-infobars")
            # self.chromeOptions.add_argument("--incognito")
            self.chromeOptions.add_argument("--disable-plugins-discovery")
            self.chromeOptions.add_argument("--start-maximized")
            self.chromeOptions.add_argument('--proxy-server=' + get_proxies())
            self.driver = webdriver.Chrome(chrome_options=self.chromeOptions, executable_path=path)
            self.driver.set_window_size(882, 880)
            self.driver.set_window_position(490, 0)
        except:
            print("Chrome go out")


    def login(self, date, origin, destination):
        elements = []
        it_is_work = False
        try:
            website = "https://www.kayak.co.uk/flights/" + origin + "-" + destination + "/" + date + "?sort=price_a"
            self.driver.get(website)

            time.sleep(10)

            res = self.driver.execute_script("return document.documentElement.outerHTML")
            self.soup = BeautifulSoup(res, 'lxml')
            title = self.driver.title

            time.sleep(4)
            if title == "":
                print("Fail security")
                self.driver.quit()
                return it_is_work
            elif title == "www.kayak.co.uk":
                print("Fail internet")
                self.driver.quit()
                return it_is_work

            print(self.driver.title)

            money = []
            brands = []

            departs = self.soup.find_all('span', {'class': 'depart-time base-time'})
            time.sleep(3)
            arrivals = self.soup.find_all('span', {'class': 'arrival-time base-time'})
            time.sleep(4)
            money1 = self.soup.find_all('div', {'class': 'multibook-dropdown'})
            a = 0
            for mon in money1:
                time.sleep(2)
                mone = mon.find('span', {'class': 'price option-text'})
                money.append(mone)

            time.sleep(6)

            brands1 = self.soup.find_all('div', {'class': 'section times'})
            for br in brands1:
                time.sleep(5)
                brand = br.find('div', {'class': 'bottom'})
                brands.append(brand)

            print(a)

            cale_text = []
            caly = ""

            a = 0
            print("Departure")
            for de in departs:
                #print(de.text)
                cale_text.append("Departure: " + de.text)
                a = a + 1
            #print(a)
            if a == 0:
                for a in range(0, 15):
                    cale_text.append("Departure: None")
            a = 0

            print("Arrival")
            for ar in arrivals:
                #print(ar.text)
                cale_text[a] = cale_text[a] + ", Arrival: " + ar.text
                a = a + 1

            #print(a)
            a = 0

            print("money")
            for mo in money:
                #print(str(mo.text).replace('\n', ""))

                cale_text[a] = cale_text[a] + ", Cost: " + str(mo.text).replace('\n', "")
                a = a + 1
            a = 0
            for br in brands:
                cale_text[a] = cale_text[a] + ", Brand: " + br.text
                a = a + 1

            #print(a)
            f = open("flights.txt", "a+")
            f.write(title + "\n")
            for caly in cale_text:
                print(caly)
                f.write(caly + "\n")
            a = 0
            #print("Work")
            f.close()

            it_is_work = True
            self.driver.quit()
            return it_is_work
        except:
            print("Something went wrong")
            return it_is_work


def get_proxies():
    #Take fake proxy from web
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    a = 0
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            # print(proxy)
            a = a + 1
            proxies.append(proxy)

    index = random.randint(0, a)
    ret = proxies[index]
    print("IP: " + ret)
    return ret


def get_fake_agent():
    #take fake agent from web3
    number_of_page = random.randint(0, 3000)
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/'+str(number_of_page)
    response = requests.get(url)
    parser = fromstring(response.text)
    fake_agen = []
    a = 0
    time.sleep(8)
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[4][contains(text(),"Computer")]'):
            # Grabbing IP and corresponding PORT
            time.sleep(3)
            fake_a = i.xpath('.//td[1]/a/text()')
            a = a + 1
            fake_agen.append(fake_a)
    return fake_agen


input = []
a = 0
InputFile = open("Input2.txt", "r")
for i in InputFile:
    a = a + 1
    input.append(i)
word = input[1].split(",")

fake_agents = get_fake_agent()
exist_fake_agent = 0
for words in input:
    it_is_work = False
    while it_is_work == False:
        try:
            exist_fake_agent = exist_fake_agent + 1
            if(exist_fake_agent > 10):
                fake_agents = get_fake_agent()
                exist_fake_agent = 0
            index = random.randint(0, len(fake_agents))
            fake_agent = ""
            fake_agent = fake_agents[index]
            char_list = ["\[", "\]", "'"]
            fake_agent2 = re.sub("|".join(char_list), "", str(fake_agent))
            print(fake_agent2)
            time.sleep(1)
            kayak = Kayak(fake_agent2)
            word = words.split(",")
            time.sleep(4)
            it_is_work = kayak.login("2018-09-30", word[1], word[2])
        except:
            print("Something when wrong")
            continue

