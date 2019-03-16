import time
import re
import random
import csv
import os
from datetime import timedelta
from datetime import datetime
from datetime import date


from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup



class Scraping:

    def __init__(self, fake):
        try:
            path = "/Users/adamstelmaszyk/chromedriver"
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

    def choose_data_in_calender(self,website, day_of_flight):
        try:
            time.sleep(2)
            self.driver.get(website)

            time.sleep(2)

            print("Label")
            one_way = self.driver.find_elements_by_css_selector("div.float-right-h20")
            print(len(one_way))
            one_way[0].click()
            time.sleep(3)

            day_of_flight = day_of_flight.split("-")

            calender_data = self.driver.find_elements_by_id("searchDates")
            time.sleep(3)
            calender_data11 = calender_data[0].find_elements_by_css_selector("div.input.text")
            calender_data11[0].click()
            time.sleep(3)

            find_moths = self.driver.find_elements_by_css_selector("table.ui-datepicker-calendar")

            day = 0
            year1 = int(day_of_flight[0])

            month1 = int(day_of_flight[1])

            day1 = int(day_of_flight[2])

            print(str(datetime(year1, month1, 1).weekday()))
            day_to_search = int(datetime(year1, month1, 1).weekday())
            day = day_to_search + day1



            #str(datetime.date(datetime.today() + timedelta(days=10)))

            date_calnder = datetime.today()
            if str(date_calnder.month) == str(day_of_flight[1]):
                try:
                    now_month = find_moths[0].find_elements_by_css_selector("td")
                    print("Now month")
                    now_month[day].click()
                except:
                    print("we have problem with calender")
                    return True
            else:
                try:
                    new_month = find_moths[1].find_elements_by_css_selector("td")
                    print("New month")
                    new_month[day].click()
                except:
                    print("we have problem with caleder")
                    return True


            return False
        except:
            print("Problems ... we don't what problems")
            return False

    def scrap_basic_price(self, departure, arrive):
        price_table = []
        try:


            time.sleep(5)

            city_origin = self.driver.find_elements_by_css_selector("div.styled-select.margin-bottom-5")
            print(len(city_origin))

            time.sleep(3)
            city_origin[0].click()
            time.sleep(4)


            city1_origin = self.driver.find_elements_by_id("destinationItem"+departure)
            print(len(city1_origin))

            if len(city1_origin) == 0:
                print("Problem with DESTINATIONITEM1")
                price_table.append("0")
                self.driver.quit()
                return price_table


            time.sleep(3)

            city1_origin[0].click()
            time.sleep(4)

            city_origin[1].click()
            time.sleep(3)
            city_arrive1 = self.driver.find_elements_by_id("destinationItem"+arrive)
            print(len(city_arrive1))
            time.sleep(2)

            if len(city_arrive1) ==  0:
                print("Problem with DESTINATIONITEM2")
                price_table.append("0")
                self.driver.quit()
                return price_table


            city_arrive1[0].click()

            time.sleep(3)

            resident = self.driver.find_elements_by_id("ADT")
            time.sleep(2)
            print(len(resident))
            resident[0].click()
            time.sleep(3)

            resident1 = resident[0].find_elements_by_css_selector("option")
            time.sleep(2)
            print(len(resident1))
            resident1[1].click()

            time.sleep(4)
            button_confirm = self.driver.find_elements_by_id("buttonSubmit")
            button_confirm[0].click()

            time.sleep(7)

            price_basic = self.driver.find_elements_by_css_selector("div.availability-cell-right")
            print(len(price_basic))

            #the web serachs base_price

            amount_of_flights2 = 0
            flights1 = self.driver.find_elements_by_css_selector(
                "div.availability-row.availability-row-even.color-333")
            try:
                flights2 = self.driver.find_elements_by_css_selector(
                    "div.availability-row.availability-row-odd.color-333")
                amount_of_flights2 = int(len(flights2))
            except:
                print("Problem with flights2")

            flights = flights1[0]
            when_end = 0

            try:
                one_way = flights.find_elements_by_css_selector("span.modal-info-flight")
                print("HOW MUCH FLIGHTS in  one way: ")
                print(len(one_way))
                print(one_way[0].text)
                if len(one_way) > 1:
                    price_table.append("0")
                    print("NO ONE WAY")
                    self.driver.quit()
                    return price_table
            except:
                print("Problems with one_way")

            i = 0
            k = 0
            loop_number = int(len(flights1)) + amount_of_flights2

            time.sleep(6)

            print("ile jest lotow: ")
            print(len(flights1))
            print(len(flights2))

            while loop_number > k:
                try:
                    time.sleep(5)

                    if k % 2 == 0:
                        flights1 = self.driver.find_elements_by_css_selector(
                            "div.availability-row.availability-row-even.color-333")
                        flights = flights1[i]
                    elif k % 2 != 0:
                        flights2 = self.driver.find_elements_by_css_selector(
                            "div.availability-row.availability-row-odd.color-333")
                        flights = flights2[i]

                    a = 0



                    pri = flights.find_elements_by_css_selector("div.availability-cell-right")
                    size1 = len(pri)
                    print("PRICE NUMBERS")
                    print(len(pri))
                    while 5 > a:
                        pri = flights.find_elements_by_css_selector("div.availability-cell-right")

                        if pri[a].text == "No seats available":
                            a = a + 1
                            continue
                        pri[a].click()
                        time.sleep(8)
                        final_price = self.driver.find_elements_by_id("finalPriceValue")
                        print(final_price[0].text)
                        final_price1 = final_price[0].text
                        final_price1 = re.sub("[^0-9,]", "", final_price1)
                        final_price1 = final_price1.replace(",", ".")
                        print(final_price1)
                        print()
                        price_table.append(final_price1)
                        a = a + 1
                    if k % 2 != 0:
                        i = i + 1
                    k = k + 1
                    print("koniec")

                except:
                    print("Problem with basic price")


            self.driver.quit()

            return price_table
        except:
            print("Problem with login to web")
            return price_table

    def function_next_web(self, basicprice, departuRE, arriVE, date_calender12, directory_name):


        name_of_class = ["FlexiMas", "Flexible", "Economica", "Promo", "Superpromo"]
        table_price = basicprice

        res = self.driver.execute_script("return document.documentElement.outerHTML")
        self.soup = BeautifulSoup(res, 'lxml')

        number_of_flight = []
        information_about_flight = self.soup.find_all('span', {'class': 'modal-info-flight'})
        for inf in information_about_flight:
            number_of_flight.append(inf.text)


        amount_of_flights2 = 0
        flights1 = self.driver.find_elements_by_css_selector("div.availability-row.availability-row-even.color-333")
        try:
            flights2 = self.driver.find_elements_by_css_selector(
                "div.availability-row.availability-row-odd.color-333")
            amount_of_flights2 = int(len(flights2))
        except:
            print("Don't have second row")

        flights = flights1[0]

        i = 0
        k = 0
        g = 0
        loop_number = int(len(flights1)) + amount_of_flights2

        time.sleep(6)

        print("ile jest lotow: ")
        print(len(flights1))
        print(len(flights2))

        number_of_problems = 0


        while loop_number > k:
            try:
                time.sleep(5)

                if k%2 == 0:
                    flights1 = self.driver.find_elements_by_css_selector(
                        "div.availability-row.availability-row-even.color-333")
                    flights = flights1[i]
                elif k%2 != 0:
                    flights2 = self.driver.find_elements_by_css_selector(
                        "div.availability-row.availability-row-odd.color-333")
                    flights = flights2[i]

                time.sleep(2)
                fl = flights.find_elements_by_css_selector("div.availability-subrow-info")
                time.sleep(3)
                hours = fl[0].find_elements_by_css_selector("div")
                time.sleep(2)
                departure = hours[0].text
                print(departure)
                time.sleep(3)
                arrive = hours[1].text
                print(arrive)

                a = 0
                pri = flights.find_elements_by_css_selector("div.availability-cell-right")
                size1 = len(pri)
                while 5 > a:
                    table = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                             ""]
                    table[23] = "€"
                    time.sleep(5)

                    try:
                        print("G is....")
                        print(g)
                        table[11] = table_price[g]
                    except:
                        print("Problem with ARRAY PRICE")


                    print("TABLE PRICE")
                    try:
                        table[3] = departuRE
                    except:
                        print("Departure has some problem")

                    try:
                        table[4] = arriVE
                    except:
                        print("Arrive has some problem")

                    try:
                        table[2] = date_calender12
                    except:
                        print("Problem with calender ")
                    try:
                        table[7] = departure
                    except:
                        print("Problem with departure hours")

                    try:
                        table[8] = arrive
                    except:
                        print("Problem with arrive hours")
                    try:
                        table[6] = number_of_flight[k]
                    except:
                        print("problem with number of flights")

                    try:
                        print(table_price[g])
                    except:
                        print("Problem with table price")
                    try:
                        pri = flights.find_elements_by_css_selector("div.availability-cell-right")
                        print(len(pri))
                    except:
                        print("Pri not exist")


                    if pri[a].text=="No seats available":
                        a = a + 1
                        continue

                    print("NEW FLIGHT")
                    print(pri[a].text)
                    print(a)
                    print()
                    pri[a].click()
                    time.sleep(8)

                    final_price = self.driver.find_elements_by_id("finalPriceValue")
                    print(final_price[0].text)
                    final_price1 = final_price[0].text
                    final_price1 = re.sub("[^0-9,]", "", final_price1)
                    final_price1 = final_price1.replace(",", ".")
                    if final_price1 == "":
                        final_price1="0"
                    print(final_price1)
                    table[16] = final_price1

                    time.sleep(2)

                    Fare = self.driver.find_elements_by_id("priceRatesValue")
                    print(len(Fare))

                    Fare1 = Fare[0].text
                    Fare1 = re.sub("[^0-9,]", "", Fare1)
                    Fare1 = Fare1.replace(",", ".")
                    if Fare1 == "":
                        Fare1 = "0"
                    print(Fare1)
                    table[18] = Fare1

                    taxe = self.driver.find_elements_by_id("priceTaxesValue")
                    print(len(taxe))

                    taxe1 = taxe[0].text
                    taxe1 = re.sub("[^0-9,]", "", taxe1)
                    taxe1 = taxe1.replace(",", ".")
                    if taxe1 == "":
                        taxe1 = "0"
                    print(taxe1)
                    table[10] = taxe1
                    table[15] = taxe1
                    table[5] = "NT"

                    issue_fees = self.driver.find_elements_by_id("priceFeesValue")
                    print(len(issue_fees))
                    issue_fees1 = issue_fees[0].text
                    issue_fees1 = re.sub("[^0-9,]", "", issue_fees1)
                    issue_fees1 = issue_fees1.replace(",", ".")
                    if issue_fees1 == "":
                        issue_fees1 = "0"
                    table[9] = issue_fees1
                    table[14] = issue_fees1
                    print(issue_fees1)

                    table[0] = name_of_class[a]
                    data_calender_TAB = str(datetime.date(datetime.today()))
                    data_calender_table = data_calender_TAB.split("-")
                    table[1] = data_calender_table[2] + "/" + data_calender_table[1] + "/" + data_calender_table[0]
                    print("Dodawanie cen: ")
                    try:
                        equation = float(table_price[g]) - float(issue_fees1)
                        table[12] = str(equation)
                    except:
                        table[12] = ""
                        print("Problem with equation")
                    try:
                        equation1 = float(table_price[g]) - float(final_price1)
                        equation = str(equation1)
                        index_dot = equation.index(".")
                        index_dot = index_dot + 3
                        table[19] = equation[:index_dot]
                    except:
                        table[19] = ""
                        print("Problem with equation2")
                    a = a + 1
                    g = g + 1

                    #search_data = str(datetime.date(datetime.today() + timedelta(days=10)))
                    #directory = 'Binter_text' + search_data + '.csv'

                    with open(directory_name, 'a') as writeFile:
                        writer = csv.writer(writeFile, lineterminator='\n')
                        writer.writerow(table)

                if k % 2 != 0:
                    i = i + 1
                k = k + 1
                print("end")
            except:
                print("Problem where")
                number_of_problems = number_of_problems + 1
                if number_of_problems > 5:
                    return

    def login(self, tableprice, departure, arrive, data_calender12, directory_name):
        try:


            print("TABle price:")
            print(len(tableprice))

            time.sleep(5)

            city_origin = self.driver.find_elements_by_css_selector("div.styled-select.margin-bottom-5")
            print(len(city_origin))

            time.sleep(3)
            city_origin[0].click()
            time.sleep(4)

            city1_origin = self.driver.find_elements_by_id("destinationItem"+departure)
            print(len(city1_origin))

            time.sleep(3)
            city1_origin[0].click()

            time.sleep(4)
            city_origin[1].click()
            time.sleep(3)

            city_arrive1 = self.driver.find_elements_by_id("destinationItem"+arrive)
            print(len(city_arrive1))
            time.sleep(2)
            city_arrive1[0].click()
            time.sleep(3)


            resident = self.driver.find_elements_by_id("ADTDC")
            time.sleep(2)
            print(len(resident))
            resident[0].click()
            time.sleep(3)

            resident1 = resident[0].find_elements_by_css_selector("option")
            time.sleep(2)
            print(len(resident1))
            resident1[1].click()

            time.sleep(4)

            try:
                print("conditions")
                condition_resident = self.driver.find_elements_by_id("conditions")
                print(len(condition_resident))
                condition_resident[0].click()
            except:
                print("it isn't work")

            time.sleep(4)
            button_confirm = self.driver.find_elements_by_id("buttonSubmit")
            button_confirm[0].click()

            time.sleep(7)

            self.function_next_web(tableprice, departure, arrive, data_calender12, directory_name)

            self.driver.quit()
            return True

        except:
            print("Problem with login to web")
            return False


def create_table(data_cal):
    directory = 'NT ' + data_cal[2] + data_cal[1] + data_cal[0] + ' TCI Output.csv'
    if not os.path.exists(directory):
        line = ["FareClass", "ObservationDate", "Departure_Date", "ORG", "Dst", "Carrier"
            , "Flight_Code", "Dep_time", "Arr_time", "Apt_Fees", "Gov_Tax", "Total_Price_Non_Res",
                "Base_Fare_Non_Res", "Base_Fare_Non_Res_Calc", "Airport_Fees_Res", "Gov_Tax_Res",
                "Total_Price_Res", "Base_Fare_Res", "Base_Fare_Res_Calc", "Discount_Value",
                "Discount_Value_Calc", "Security", "Security Tax", "Currency"]
        with open(directory, 'w') as writeFile:
            writer = csv.writer(writeFile, lineterminator='\n')
            writer.writerow(line)

    return directory;


def open_file():
    inputCSV = []
    with open('bintes.csv') as File:
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
directory_name = create_table(data_cal)
inpu = open_file()
for words in inpu:
    try:
        it_is_work = False
        while it_is_work != True:

            word = words.split(",")
            word[1] = word[1].strip()
            word[2] = word[2].strip()
            #word[1] = "VDE"
            #word[2] = "LPA"
            print(word[1])
            print(word[2])


            scraping = Scraping("fake")
            web = "https://www.bintercanarias.com/eng"
            data_calender = str(datetime.date(datetime.today() + timedelta(days=9)))
            print(data_calender)

            calender_everything_okey = scraping.choose_data_in_calender(web, data_calender)
            if calender_everything_okey:
                break
            table_price = scraping.scrap_basic_price(word[1], word[2])
            if table_price[0] == "0":
                break
            for table in table_price:
                print(table)


            scraping1 = Scraping("fake")
            time.sleep(2)
            calender_everything_okey = scraping1.choose_data_in_calender(web, data_calender)
            if calender_everything_okey:
                break

            data_calender12 = str(datetime.date(datetime.today() + timedelta(days=10)))

            data_calender = data_calender12.split("-")
            data_calender12 = data_calender[2] + "/" + data_calender[1] + "/" + data_calender[0]
            it_is_work = scraping1.login(table_price, word[1], word[2], data_calender12, directory_name)

        print("End of program")
    except:
        print("Big problem")

