import time
import re
import random
import csv
import os

from datetime import timedelta
from datetime import datetime

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml.html import fromstring
from bs4 import BeautifulSoup



class Scraping:

    def __init__(self, fake):
        try:
            path = "/Users/adamstelmaszyk/chromedriver"
            #path = "chromedriver.exe"
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
            self.driver.set_window_size(1000, 1000)
            self.driver.set_window_position(0, 0)
        except:
            print("Problem with initial class Scraping")

    def what_class(self, number):
        if number == 3:
            return "Basic"
        elif number == 4:
            return "Optimal"
        elif number == 5:
            return "Flexible"
        elif number == 6:
            return "Business Flexible"
        else:
            return "None"

    def scrap_information(self, the_whole_prise, name_of_class, departuRE, arriVE, time_calendER, directory_name):

        print("Inside scriping")
        print(the_whole_prise)
        the_whole_prise = the_whole_prise[:4]
        price_basic = re.sub("[^0-9,]", "", the_whole_prise)
        print(price_basic)

        scrap_true = True
        try:
            while scrap_true:
                time.sleep(1)
                print("Jestsmy przy guziku ")

                confirm = self.driver.find_elements_by_id("btn")
                print("Confirm")
                confirm[0].click()

                time.sleep(2)

                cont1 = self.driver.find_elements_by_id("enviar3")
                print("Cont1")
                cont1[0].click()

                time.sleep(2)
                more_inf = self.driver.find_elements_by_id("heading-desglose")
                print(len(more_inf))
                time.sleep(1)
                print("More inf")
                more_inf[0].click()

                try:
                    time.sleep(1)
                    table = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                             ""]
                    # calender

                    data_cal12 = str(datetime.date(datetime.today()))
                    data_cal = data_cal12.split("-")

                    table[1] = data_cal[2] + "/" + data_cal[1] + "/" + data_cal[0]
                    time.sleep(1)

                    whole_price = self.driver.find_elements_by_xpath("//tr/td")
                    print(len(whole_price))
                    for who in whole_price:
                        print(who.text)

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", whole_price[0])
                    time.sleep(1)
                    print("Fare: " + whole_price[1].text)

                    table1 = self.driver.find_elements_by_css_selector("table.table")
                    print("TABLE: ")
                    print(len(table1))
                    print(table1[0].text)
                    a = 0
                    for tabl in table1:
                        print(a)
                        a = a + 1
                        price_ba = tabl.find_elements_by_css_selector("td")
                        print(price_ba[1].text)

                    print("FINAL PRICE: ")


                    finished_price = str(whole_price[1].text)
                    print("FINISHED PRICE: LEN")
                    print(len(finished_price))
                    price_basic1 =  str(finished_price)
                    table[12] = str(finished_price)



                    include_price = self.driver.find_elements_by_class_name("prevent-default")
                    include_price[0].click

                    time.sleep(2)
                    res = self.driver.execute_script("return document.documentElement.outerHTML")
                    self.soup = BeautifulSoup(res, 'lxml')

                    time.sleep(1)

                    help2 = self.soup.find_all('dd')

                    print(len(help2))
                    Security = help2[1].text
                    index_dot = Security.index(".")
                    index_dot = index_dot + 3
                    Security = Security[:index_dot]
                    table[21] = Security

                    print("Security: " + Security)
                    Security_Tax = help2[2].text
                    index_dot = Security_Tax.index(".")
                    index_dot = index_dot + 3
                    Security_Tax = Security_Tax[:index_dot]
                    print("Security Tax: " + Security_Tax)
                    table[22] = Security_Tax
                    Departure_Charge_Spain = help2[3].text
                    index_dot = Departure_Charge_Spain.index(".")
                    index_dot = index_dot + 3
                    Departure_Charge_Spain = Departure_Charge_Spain[:index_dot]
                    #table[9] = Departure_Charge_Spain


                    table[9] = str(float(Departure_Charge_Spain)  + float(Security_Tax) + float(Security))
                    index_dot = table[9].index(".")
                    index_dot = index_dot + 3
                    table[9] = table[9][:index_dot]
                    print("Departure Charge Spain: " + Departure_Charge_Spain)
                    table[14] = table[9]
                    print("CENA PRZED: "+price_basic)

                    final_price= float(price_basic)
                    price_basic1 = str(final_price)
                    index_dot = price_basic1.index(".")
                    index_dot = index_dot + 3
                    price_basic = price_basic1[:index_dot]
                    print("Basic PRICE: "+price_basic)


                    table[23] = "€"
                    table[0] = name_of_class
                    table[11] = price_basic
                    table[2] = time_calendER
                    table[3] = departuRE
                    table[4] = arriVE
                    print(price_basic)
                    price_discount = "0"


                    try:
                        print("FINISH PRICE: ")
                        print(price_basic)
                        equation = float(price_basic) * 0.25
                        print(str(equation))
                        table[18] = str(equation)
                        price_discount = str(equation)
                    except:
                        table[18] = ""
                        print("Equation with discout price problem")

                    try:
                        equation = float(price_discount) + float(Security) + float(Security_Tax) + float(Departure_Charge_Spain)
                        equation1 = int(equation)
                        table[16] = str(equation1)
                        print(str(equation))
                    except:
                        print("Problem with adding")

                    #try:
                    #    equation = float(price_basic) - float(Departure_Charge_Spain)
                    #    equation = str(equation)
                    #    index_dot = equation.index(".")
                     #   index_dot = index_dot + 3
                    #    table[12] = equation[:index_dot]
                    #except:
                       # table[12] = ""
                       # print("Problem with equation")
                    try:
                        equation = float(price_basic) - float(price_discount)
                        equation = str(equation)
                        index_dot = equation.index(".")
                        index_dot = index_dot + 3
                        table[19] = equation[:index_dot]
                    except:
                        table[19] = ""
                        print("Problem with equation2")

                    departure = help2[4].text
                    departure = departure.strip()
                    departure = departure[:22]

                    departure = re.sub("[^0-9:]", "", departure)
                    table[7] = departure[:5]
                    print("Departure:" + table[7])

                    arrive = help2[5].text
                    arrive = arrive.strip()
                    arrive = arrive[:22]

                    arrive = re.sub("[^0-9:]", "", arrive)
                    table[8] = arrive[:5]
                    print("Arrive :" + table[8])

                    flight_number = help2[6].text
                    flight_number = flight_number.strip()
                    flight_number = flight_number[:8]
                    print("Flight number: " + flight_number)

                    table[5] = re.sub("[^a-zA-Z]", "", flight_number)
                    table[6] = re.sub("[^0-9]", "", flight_number)

                    with open(directory_name, 'a') as writeFile:
                        writer = csv.writer(writeFile, lineterminator='\n')
                        writer.writerow(table)

                    time.sleep(2)
                    self.driver.back()
                    time.sleep(3)
                    self.driver.back()
                    scrap_true = False
                    return
                except:
                    print("Some fail in scrap data ")
        except:
            print("Some problem with label")


    def login(self, website, departure, arrive, time_calendER, directory_name):
        it_is_work = False

        try:
            self.driver.get(website)
            time.sleep(2)
            try:
                title = self.driver.title
                if str(title)  == "Flight search - Iberia":
                    self.driver.quit()
                    return True

            except:
                print("Problem with title")


            try:
                flights = self.driver.find_elements_by_css_selector("tr.flight-info.flight-info-header.order-tr")
                el = flights[0].find_elements_by_css_selector("td")
                size_of_table = len(el)
                print(len(flights))
            except:
                print("the website block us")
                self.driver.quit()
                return False




            break_out = False
            i = 0
            j = 0
            g = 0

            no_problem = True
            while no_problem:
                try:
                    while len(flights) > i:
                        a = 0

                        while size_of_table > a:
                            time.sleep(1)
                            flights = self.driver.find_elements_by_css_selector(
                                "tr.flight-info.flight-info-header.order-tr")
                            time.sleep(2)
                            el = flights[i].find_elements_by_css_selector("td")
                            if a == 2:
                                nonedirect = el[a].find_elements_by_css_selector("span.escale-num")

                                stop = nonedirect[0].text
                                stop = stop.strip()
                                if stop == "1 Stopover":
                                    break_out = True
                                    break

                            if a >= 3 and el[a].text != "Not available":
                                name_of_class = self.what_class(a)
                                time.sleep(2)
                                fare = el[a].text
                                print(el[a].text)
                                print("CLICK")
                                print(a)
                                el[a].click()
                                print("CLICKED")
                                time.sleep(1)
                                print("FARE: ")
                                print(fare)
                                self.scrap_information(fare, name_of_class, departure, arrive, time_calendER, directory_name)
                                time.sleep(1)
                                g = g + 1
                            a = a + 1
                        j = j + 1
                        if break_out:
                            break
                        i = i + 1
                    no_problem = False
                except:
                    print("Problem in loop of scraping data")
                    try:
                        time.sleep(2)
                        button_problem = self.driver.find_elements_by_css_selector("button.pushtip-buttonitem")
                        time.sleep(1)
                        print("Size of button problem: ")
                        print(len(button_problem))
                        button_problem[0].click()
                    except:
                        print("It was not label")
                        self.driver.quit()
                        return False

            self.driver.quit()
            return True

        except:
            print("Something went wrong")
            self.driver.quit()
            return it_is_work


def writefinal(directory_in):
    directory = 'IB ' + data_cal[2] + data_cal[1] + data_cal[0] + ' TCI Output.csv'
    if not os.path.exists(directory):
        line = ["FareClass", "ObservationDate", "Departure_Date", "ORG", "Dst", "Carrier"
            , "Flight_Code", "Dep_time", "Arr_time", "Apt_Fees", "Gov_Tax", "Total_Price_Non_Res",
                "Base_Fare_Non_Res", "Base_Fare_Non_Res_Calc", "Airport_Fees_Res", "Gov_Tax_Res",
                "Total_Price_Res", "Base_Fare_Res", "Base_Fare_Res_Calc", "Discount_Value",
                "Discount_Value_Calc", "Security", "Security Tax", "Currency"]
        with open(directory, 'w') as writeFile:
            writer = csv.writer(writeFile, lineterminator='\n')
            writer.writerow(line)

    inputCSV = []
    with open(directory_in) as File:
        reader = csv.reader(File)
        a = 0
        for row in reader:
            if a > 1:
                word1 = str(row)
                char_list = ["\[", "\]", "'", ""]
                word1 = re.sub("|".join(char_list), "", word1)
                inputCSV.append(word1)
            a = a + 1
        previous_word = ""
        lista_lotow = []
        for words in inputCSV:
            word = words.split(",")

            if previous_word == word[6]:
                with open(directory, 'a') as writeFile:
                    writer = csv.writer(writeFile, lineterminator='\n')
                    writer.writerow(word)
                continue
            continue1 = False
            for jeden_lot in lista_lotow:
                if jeden_lot == word[6]:
                    print("jest"+word[6])
                    continue1 = True
                    break
            if(continue1):
                continue
            lista_lotow.append(word[6])
            print(word[6])
            previous_word = word[6]
            with open(directory, 'a') as writeFile:
                writer = csv.writer(writeFile, lineterminator='\n')
                writer.writerow(word)




def create_table(data_cal):
    directory = 'IB '+data_cal[2]+data_cal[1]+data_cal[0]+' TCI Output_uncorrect.csv'
    if not os.path.exists(directory):
        line = ["FareClass", "ObservationDate", "Departure_Date", "ORG", "Dst", "Carrier"
            , "Flight_Code", "Dep_time", "Arr_time", "Apt_Fees", "Gov_Tax", "Total_Price_Non_Res",
                "Base_Fare_Non_Res", "Base_Fare_Non_Res_Calc", "Airport_Fees_Res", "Gov_Tax_Res",
                "Total_Price_Res", "Base_Fare_Res", "Base_Fare_Res_Calc", "Discount_Value",
                "Discount_Value_Calc", "Security", "Security Tax", "Currency"]
        with open(directory, 'w') as writeFile:
            writer = csv.writer(writeFile, lineterminator='\n')
            writer.writerow(line)

    return directory

def open_file():
    inputCSV = []
    with open('iberiainput1.csv') as File:
        reader = csv.reader(File)
        a=0
        for row in reader:
            if a > 0:
                word1 = str(row)
                char_list = ["\[", "\]", "'", ""]
                word1 = re.sub("|".join(char_list), "", word1)
                inputCSV.append(word1)
            a = a + 1
    return inputCSV


data_cal12 = str(datetime.date(datetime.today()))
data_cal = data_cal12.split("-")
number_row = 2
inpu = open_file()
directory_name = create_table(data_cal)

for words in inpu:
    it_is_work = False
    while it_is_work != True:
        try:

            scraping = Scraping("fake_agent2")

            word = words.split(",")
            word[1] = word[1].strip()
            word[2] = word[2].strip()
            #word[1] = "BCN"
            #word[2] = "IBZ"

            print(word[1])
            print(word[2])
            data_calender12 = str(datetime.date(datetime.today() + timedelta(days=9)))

            data_calender = data_calender12.split("-")
            data_calender12 = data_calender[2] + "/" + data_calender[1] + "/" + data_calender[0]

            #web_site = "https://www.iberia.com/web/bookingForm.do?market=GB&language=en&appliesOMB=false&splitEndCity=false&initializedOMB=true&flexible=true&TRIP_TYPE=1&BEGIN_CITY_01=" + \
                       #word[1] + "&END_CITY_01=" + word[2] \
                       #+ "&BEGIN_DAY_01=" + data_calender[2] + "&BEGIN_MONTH_01=" + data_calender[0] + data_calender[1] + "&BEGIN_YEAR_01="+data_calender[0]+"&END_DAY_01=&END_MONTH_01=&END_YEAR_01=&FARE_TYPE=R&ADT=1&CHD=0&INF=0&quadrigam=IBHMPA&residentCode=&familianumerosa="

            web_site = "https://www.iberia.com/web/bookingForm.do?market=ES&language=en&appliesOMB=false&splitEndCity=false&initializedOMB=true&flexible=true&TRIP_TYPE=1&BEGIN_CITY_01=" \
                       + word[1] +"&END_CITY_01="+ word[2] +"&BEGIN_DAY_01="+ data_calender[2] +\
                       "&BEGIN_MONTH_01="+ data_calender[0] + data_calender[1] +"&BEGIN_YEAR_01="+data_calender[0]+"&END_DAY_01=&END_MONTH_01=&END_YEAR_01=&FARE_TYPE=R&ADT=1&CHD=0&INF=0&quadrigam=IBADVS&YTH=0&YCD=0&residentCode=RC&familianumerosa="

            it_is_work = scraping.login(web_site, word[1], word[2], data_calender12, directory_name)
        except:
            print("Big problem")


    print("End of program")

writefinal(directory_name)