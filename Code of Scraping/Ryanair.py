import time
import re

import csv
import os

from datetime import timedelta
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup



class Scraping:

    def __init__(self, fake):
        try:
            path = "/Users/adamstelmaszyk/chromedriver"
            self.chromeOptions = Options()
            #self.chromeOptions.add_argument("--user-agent=" + fake)
            self.chromeOptions.add_argument('--disable-extensions')
            self.chromeOptions.add_argument('--profile-directory=Default')
            self.chromeOptions.add_argument("--disable-infobars")
            self.chromeOptions.add_argument("--incognito")
            self.chromeOptions.add_argument("--disable-plugins-discovery")
            self.chromeOptions.add_argument("--start-maximized")
            #self.chromeOptions.add_argument('--proxy-server=' + get_proxies())
            self.driver = webdriver.Chrome(chrome_options=self.chromeOptions, executable_path=path)
            self.driver.set_window_size(882, 880)
            self.driver.set_window_position(0, 0)
        except:
            print("Problem with initial class Scraping")

    def end(self):
        self.driver.quit()

    def login(self, website, number,  departure, arrive, data_calender1, directory_name):

        number_row = number
        table = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "","","",""]

        try:
            self.driver.get(website)

            time.sleep(7)
            buttons = self.driver.find_elements_by_css_selector(".flight-header__min-price")
            buttons[0].click()
            i = 0

            print(len(buttons))
            while i < len(buttons):
                try:
                    time.sleep(6)
                    buttons1 = self.driver.find_elements_by_css_selector(".flight-header__min-price")

                    text_from_button = buttons1[i].text
                    if "Sold out" == text_from_button:
                        i=i+1
                        continue
                    buttons1[i].click()
                    time.sleep(10)
                    button = self.driver.find_elements_by_class_name("basket-arrow")

                    button[0].click()

                    time.sleep(5)

                    res = self.driver.execute_script("return document.documentElement.outerHTML")
                    self.soup = BeautifulSoup(res, 'lxml')

                    information_about_flight = self.soup.find('span', {'class': 'dest-info'})
                    information_about_flight1 = information_about_flight.text
                    information_about_flight1 = information_about_flight1.replace("-", "")
                    information_about_flight1 = information_about_flight1.replace("  ", " ")

                    print(information_about_flight1)
                    table_words = information_about_flight1.split(" ")
                    table[7] = table_words[3]
                    table[8] = table_words[4]
                    table[5] = table_words[5]
                    table[6] = table_words[6]
                    table[0] = "Basic"
                    table[3] = departure
                    table[4] = arrive
                    table[2] = data_calender1
                    table[23] = "€"
                    # calender
                    data_calender = str(datetime.date(datetime.today()))
                    data_calender_table = data_calender.split("-")
                    table[1] = data_calender_table[2] + "/" + data_calender_table[1] + "/" + data_calender_table[0]


                    time.sleep(4)
                    money = self.soup.find_all('strong', {'class': 'item-price'})
                    first_price = money[0].text
                    first_price = first_price.replace("€", "").replace("-", "").strip()
                    discount = money[1].text
                    discount = discount.replace("€", "").replace("-", "").strip()
                    try:
                        tax_price = money[3].text
                        tax_price = tax_price.replace("€", "").replace("-", "").strip()
                    except:
                        tax_price = "0"
                        print("Tax problem")

                    time.sleep(2)
                    final_price = self.soup.find('span', {'class': 'price-amt'})
                    final_price1 = final_price.text
                    mon = []
                    for mo in money:
                        mon.append(mo.text)
                    for mon1 in mon:
                        mon1 = mon1.replace("€", "")
                        mon1 = mon1.replace("-", "")
                        mon1 = mon1.strip()
                        print(mon1)

                    final_price1 = final_price1.replace("€", "")
                    final_price1 = final_price1.strip()


                    try:
                        table[9] = tax_price
                    except:
                        table[9] = "0"
                        print("Problem with tax price")
                    try:
                        table[11] = first_price
                    except:
                        table[11] = "0"
                        print("Problem with first price")
                    table[12] = str(float(first_price) - float(tax_price))
                    try:
                        table[14] = tax_price
                    except:
                        table[14] = "0"
                        print("Problem with tax price")
                    try:
                        table[16] = final_price1
                    except:
                        print("Problem with final price1")

                    try:
                        equation = str(float(final_price1) - float(tax_price))
                        index_dot = equation.index(".")
                        index_dot = index_dot+3
                        table[18] = equation[:index_dot]

                    except:
                        print("Problem with Base fare non res")

                    try:
                        table[19] = discount
                    except:
                        print("Problem with final price1")



                    with open(directory_name, 'a') as writeFile:
                        writer = csv.writer(writeFile, lineterminator='\n')
                        writer.writerow(table)

                    time.sleep(3)
                    self.driver.get(website)
                    time.sleep(6)
                    i=i+1
                    number_row = number_row + 1
                except:
                    print("Don't have information")
                    self.driver.get(website)
                    time.sleep(10)
                    continue

            return True

        except:

            print("Something went wrong")
            return True


def create_table(data_cal):
    directory = 'FR ' + data_cal[2] + data_cal[1] + data_cal[0] + ' TCI Output.csv'
    if not os.path.exists(directory):
        line = ["FareClass", "ObservationDate", "Departure_Date", "ORG", "Dst", "Carrier"
            , "Flight_Code", "Dep_time", "Arr_time", "Apt_Fees", "Gov_Tax", "Total_Price_Non_Res",
                "Base_Fare_Non_Res", "Base_Fare_Non_Res_Calc", "Airport_Fees_Res", "Gov_Tax_Res",
                "Total_Price_Res", "Base_Fare_Res", "Base_Fare_Res_Calc", "Discount_Value",
                "Discount_Value_Calc","Security", "Security Tax", "Currency"]
        with open(directory, 'w') as writeFile:
            writer = csv.writer(writeFile, lineterminator='\n')
            writer.writerow(line)

    return directory



def open_file():
    inputCSV = []
    with open('inputfiletenerfie.csv') as File:
        reader = csv.reader(File)
        a=0
        for row in reader:
            if a > 1:
                word1 = str(row)
                char_list = ["\[", "\]", "'", ""]
                word1 = re.sub("|".join(char_list), "", word1)
                inputCSV.append(word1)
            a = a + 1
    return inputCSV

data_cal12 = str(datetime.date(datetime.today()))
data_cal = data_cal12.split("-")
number_row = 2
directory = create_table(data_cal)
inpu = open_file()
scraping = Scraping("fake")
for words in inpu:
    try:
        it_is_work = False
        while it_is_work != True:
            word = words.split(",")
            word[1] = word[1].strip()
            word[2] = word[2].strip()
            #word[1] = "AGP"
            #word[2] = "BCN"
            print(word[1])
            print(word[2])

            data_calender12 = str(datetime.date(datetime.today() + timedelta(days=10)))
            print(data_calender12)

            data_calender = data_calender12.split("-")
            data_calender123 = data_calender[2] + "/" + data_calender[1] + "/" + data_calender[0]
            print(data_calender12)

            web_site = "https://www.ryanair.com/gb/en/booking/home/"+word[1]+"/"+word[2]+"/"+data_calender12+"//1/0/0/0?Discount=75"

            print(web_site)
            it_is_work = scraping.login(web_site, number_row, word[1],word[2], data_calender123, directory)

        print("End of program")
    except:
        print("Big problem")

scraping.end()








