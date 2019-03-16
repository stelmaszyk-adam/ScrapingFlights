import requests
import os
import csv
import re
from datetime import timedelta
from datetime import datetime

def scrapingData(web,calender,departure ,arrive ,directoryName):
    response = requests.get(web)
    parser = response.json()
    try:
        list = parser['outbound']
        for li in list:

            # print(li)
            if str(li['stops']) != '0':
                continue
            flightDetails = li['medium']
            departureTime = flightDetails['flights']
            flightNumber = departureTime[0]['flightNumber']
            departureHour = departureTime[0]['departureTime']
            arriveHour = departureTime[0]['destinationTime']
            carrieR = departureTime[0]['airline']
            price = li['totalLowestAdultGrossFare']

            '''
            print(li['totalLowestAdultGrossFare'])
            print(flightNumber)
            print(departureHour)
            print(arriveHour)
            '''
            table = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

            table[0] = calender
            table[1] = "www.flybe.com"


            table[2] = departure

            table[4] = arrive

            table[6] = str(flightNumber)

            table[7] = str(carrieR)
            table[8] = str(departureHour)
            table[9] = str(arriveHour)
            table[10] = str(price)
            table[11] = str(price)
            table[12] = "GBP"

            with open(directoryName, 'a') as writeFile:
                writer = csv.writer(writeFile, lineterminator='\n')
                writer.writerow(table)
    except:
        print("We don't have the kind of destination")





def create_table(data_cal):
    directory = 'BE ' + data_cal[2] + data_cal[1] + data_cal[0] + ' TCI Output.csv'
    if not os.path.exists(directory):
        line = ["Date", "WebSiteSource", "OriginAirportCode","OriginAirportName", "DestinationAirportCode","OriginAirportName", "outbound_FlightCode",
                "outbound_Carrier","outbound_DepartTime","outbound_ArrivalTime",
                "outbound_FareAdultStandard","TotalFare","Currency","outbound_FareClass","TimeTaken"
                ,"ThreadNo","outbound_TrueFareClass","IsOutboundFlightNumberMatch"]
        with open(directory, 'w') as writeFile:
            writer = csv.writer(writeFile, lineterminator='\n')
            writer.writerow(line)

    return directory



def open_file():
    inputCSV = []
    with open('Input_BE_4_1_2019.csv') as File:
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

last_word1 = ""
last_word2 = ""
dataCalender = str(datetime.date(datetime.today()))
dataCalenderTable = dataCalender.split("-")
number_row = 2
directory = create_table(dataCalenderTable)
input = open_file()
for words in input:
    try:
        word = words.split(",")
        word[1] = word[1].strip()
        word[2] = word[2].strip()
        #if(word[1] == last_word1) and (word[2] == last_word2):
            #continue
        #last_word1 = word[1]
        #last_word2 = word[2]
        # word[1] = 'BHX'
        # word[2] = 'LYS'
        print(word[1])
        print(word[2])

        #dataCalenderTenDays = str(datetime.date(datetime.today() + timedelta(days=10)))
        #print(dataCalenderTenDays)


        data_calender = word[0].split("/")
        print(word[0])

        webSite = 'https://www.flybe.com/api/fares/day/new/' + word[1] + '/' + word[2] + '?depart=' + word[
            1] + '&arr=' + word[2] + '&departing=' + data_calender[2] + '-' + data_calender[1] + '-' + data_calender[
                      1] + '&returning=&promo-code=&adults=1&teens=0&children=0&infants=0'

        scrapingData(webSite, word[0], word[1], word[2], directory)

        print("End of program")
    except:
        print("Big problem")




