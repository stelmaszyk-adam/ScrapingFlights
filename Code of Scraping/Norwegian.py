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
            #path = "chromedriver.exe"
            self.chromeOptions = Options()
            # self.chromeOptions.add_argument("--user-agent=" + fake)
            self.chromeOptions.add_argument('--disable-extensions')
            self.chromeOptions.add_argument('--profile-directory=Default')
            self.chromeOptions.add_argument("--disable-infobars")
            self.chromeOptions.add_argument("--incognito")
            self.chromeOptions.add_argument("--disable-plugins-discovery")
            self.chromeOptions.add_argument("--start-maximized")
            # self.chromeOptions.add_argument('--proxy-server=' + get_proxies())
            self.driver = webdriver.Chrome(chrome_options=self.chromeOptions, executable_path=path)
            self.driver.set_window_size(882, 880)
            self.driver.set_window_position(0, 0)
        except:
            print("Problem with initial class Scraping")

    tax_flight_global = ""

    def scraping_data(self, class_flight, data_calender,departuRE, arriVE, calender_data,data_cal, directory):

        table = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "","",""]
        table[23] = "€"
        table[0] = class_flight
        table[1] = data_calender
        table[2] = calender_data
        table[3] = departuRE
        table[4] = arriVE

        time_flight = self.driver.find_elements_by_css_selector("div.content.emphasize")
        len(time_flight)
        for fl in time_flight:
            print(fl.text)
        table[7] = time_flight[0].text
        print("Table 7: "+table[7])
        table[8] = time_flight[1].text
        print("Table 8: " + table[8])

        time.sleep(4)

        res = self.driver.execute_script("return document.documentElement.outerHTML")
        self.soup = BeautifulSoup(res, 'lxml')

        time.sleep(4)

        flight_number = self.soup.find_all("td", {"class": "leftcell"})
        flight_number1 = flight_number[2].text
        flight_number1 = flight_number1.replace("D8", "")
        flight_number2 = re.sub("[^0-9]", "", flight_number1)
        table[5] = "D8"
        table[6] = flight_number2

        time.sleep(2)
        final_price = self.soup.find_all("td", {"class": "rightcell emphasize"})
        a=0


        for fi in final_price:
            print(a)
            a=a+1
            print(fi.text)

        final_price1 = final_price[0].text
        final_price2 = re.sub("[^0-9.]", "", final_price1)
        print("Final Price : " + final_price2)
        print(final_price2)

        if self.tax_flight_global == "":
            tax_airport = final_price[a-1].text
            tax_airport = re.sub("[^0-9.]", "", tax_airport)
            print("TAX airport table[9]: "+tax_airport)
            table[9] = tax_airport
            self.tax_flight_global = tax_airport
        else:
            table[9] = self.tax_flight_global
            print("TAX GLOBAL table[9]: "+table[9])
            tax_airport = self.tax_flight_global



        discount_price = self.soup.find_all("td", {"class": "leftcell togglebox"})
        discount_price1 = discount_price[0].text
        discount_price2 = re.sub("[^0-9.]", "", discount_price1)
        print("Discout PRICE2: "+discount_price2)

        base_price = "0"
        try:
            equation: float = float(discount_price2) + float(final_price2)
            equation1 = int(equation)
            base_price = str(equation1)
            table[11] = base_price
            print("BASE PRICE: table[11]"+table[11])
        except:
            table[11] = ""
            print("problem with equation1")

        try:
            equation = float(base_price) - float(tax_airport)
            equation1 = int(equation)
            table[12] = str(equation1)
            print("BASE FARE NON RES: table[12]"+table[12])
        except:
            table[12] = ""
            print("problem with equation2")

        table[14] = tax_airport
        print("TABLE[14]: "+table[14])
        table[16] = final_price2
        print("TABLE[16]: "+table[16])
        try:
            equation = float(final_price2) - float(tax_airport)
            equation1 = int(equation)
            table[18] = str(equation1)
            print("TABLE[18]: "+table[18])
        except:
            table[18] = ""
            print("problem with equation3")
        table[19] = discount_price2
        print("TABLE[19]: "+table[19])

        with open(directory, 'a') as writeFile:
            writer = csv.writer(writeFile, lineterminator='\n')
            writer.writerow(table)

    def login(self, website, departure, arrive,calender_data, data_cal, directory):

        try:
            self.driver.get(website)

            the_basic = self.driver.find_elements_by_css_selector("td.inputselect.avafareinfo.standardlowfare")
            time.sleep(4)
            if len(the_basic) == 0:
                self.driver.quit()
                return 2


            calender_time = data_cal[2] + "/" + data_cal[1] + "/" + data_cal[0]


            print("NUmber: ")
            numer_of_loop = len(the_basic)
            print(numer_of_loop)

            time.sleep(3)
            a = 0
            while numer_of_loop > a:
                try:
                    #the_basic = self.driver.find_elements_by_css_selector("td.inputselect.avafareinfo.standardlowfare")
                    the_basic =  self.driver.find_elements_by_css_selector("input#FlightSelectOutboundStandardLowFare0.radio-ajax")
                    print("Liczba elementow1: "+str(len(the_basic)) + str(a))
                    time.sleep(4)
                    the_basic[a].click()
                    time.sleep(4)
                    self.scraping_data("Low Fare", calender_time, departure, arrive, calender_data, data_cal,directory)
                    time.sleep(4)
                except:
                    print("Problem with Low Fare")

                try:
                    the_basic = self.driver.find_elements_by_css_selector(
                        "td.inputselect.avafareinfo.standardlowfareplus")
                    print("Liczba elementow2: " + str(len(the_basic))+ str(a))

                    the_basic[a].click()
                    self.scraping_data("Low Fare+", calender_time, departure, arrive, calender_data, data_cal,directory)
                    time.sleep(4)
                except:
                    print("Problem with Low Fare+")

                try:
                    the_basic = self.driver.find_elements_by_css_selector(
                        "td.inputselect.avafareinfo.standardflex.endcell")
                    print("Liczba elementow3: " + str(len(the_basic))+ str(a))
                    the_basic[a].click()  # 2
                    self.scraping_data("Flex", calender_time, departure, arrive, calender_data, data_cal,directory)
                    time.sleep(4)
                except:
                    print("Problem with Flex")
                a = a + 1

            self.driver.quit()
            return 0

        except:
            print("Problem with login class")
            self.driver.quit()
            return 1


def create_table(data_cal):
    directory = 'D8 '+data_cal[2]+data_cal[1]+data_cal[0]+' TCI Output.csv'
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
    with open('norwegia_flight.csv') as File:
        reader = csv.reader(File)
        a = 0
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
for words in inpu:
    try:
        it_is_work = 1
        while it_is_work != 0:
            word = words.split(",")
            word[1] = word[1].strip()
            word[2] = word[2].strip()
            #word[1] = "PMI"
            #word[2] = "MAD"

            data_calender12 = str(datetime.date(datetime.today() + timedelta(days=10)))

            data_calender = data_calender12.split("-")
            data_calender12 = data_calender[2] + "/" + data_calender[1] + "/" + data_calender[0]
            print(word[1])
            print(word[2])
            date_calnder = datetime.date(datetime.today())
            web_day = str(date_calnder.day)
            web_month = str(date_calnder.month)
            web_year = str(date_calnder.year)

            scraping = Scraping("fake")
            web = "https://www.norwegian.com/en/ipc/availability/avaday?A_City=" + word[
                2] + "&AdultCount=1&ChildCount=0&CurrencyCode=EUR&D_City=" + word[
                      1] + "&D_Day=" + data_calender[2] + "&D_Month=" + data_calender[0] + data_calender[
                      1] + "&D_SelectedDay=" + data_calender[
                      2] + "&IncludeTransit=true&InfantCount=0&R_Day=" + web_day + "&R_Month=" + web_year + web_month + "&SubsidyDefinitionId=RD&TripType=1&mode=ab"

            it_is_work = scraping.login(web, word[1], word[2], data_calender12, data_cal, directory)
            if it_is_work == 2:
                break

        print("End of program")
    except:
        print("Big problem")




