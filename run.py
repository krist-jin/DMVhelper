import requests
from user_data import user_data_1, user_data_2
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_datetime
import datetime
import time
import traceback

# DESIRED_DATE = datetime(2016, 4, 4).date()

DMV_URL = "https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do"
DMV_OFFICES = {
    "santa clara": ("632", 18), # 18 mins
    "san jose": ("516", 24),  # 24 mins
    # "fremont": ("644", 30), # 30 mins
    # "san mateo": ("593", 40), # 40 mins
    "redwood city": ("548", 28), # 28 mins
    "los gatos": ("640", 19) # 19 mins
}

HEADERS = {
    "Connection": "keep-alive",
    "Content-Length": "553",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Origin": "https://www.dmv.ca.gov",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.8"
}
INTERVAL = 1 # run every 1 minute

RETURN_TIME = datetime.time(10, 00) # need another 30 mins to arrive work
EXAM_AND_WAIT_TIME = datetime.timedelta(hours=1)

def getReturnTime(app_datetime, dis_time):
    return (app_datetime + EXAM_AND_WAIT_TIME + dis_time).time()

def makeApp():
    pass

def getCurrentAppDatetime():
    pass

def getFirstAvailableAppDatetime(office_name):
    oid, dis_time_minutes = DMV_OFFICES[office_name]
    # add office number to user_data
    user_data_with_office = user_data_1+oid+user_data_2

    # send http post request
    raw_html = requests.post(DMV_URL, headers=HEADERS, data=user_data_with_office).text

    # parse html using bs4
    soup = BeautifulSoup(raw_html, 'html.parser')

    # extract result from soup result
    result_table = soup.find(id="app_content").table
    first_available_datetime = result_table.find_all("tr")[2].p.get_text()
    return parse_datetime(first_available_datetime)
    

def main():
    while True:
        try:
            print "\n******* %s *******" % str(datetime.datetime.now())
            for office_name in DMV_OFFICES:
                first_available_datetime = getFirstAvailableAppDatetime(office_name)
                oid, dis_time_minutes = DMV_OFFICES[office_name]
                dis_time = datetime.timedelta(minutes=dis_time_minutes)
                returnTime = getReturnTime(first_available_datetime, dis_time)
                if returnTime >= RETURN_TIME:
                    print "%s: %s, return time: %s --- too late" % (office_name, first_available_datetime, returnTime)
                else:
                    print "%s: %s, return time: %s --- perfect" % (office_name, first_available_datetime, returnTime)
                
        except Exception, e:
            traceback.print_exc()
            time.sleep(INTERVAL*60)
            continue
        else: # succeed
            time.sleep(INTERVAL*60)

if __name__ == '__main__':
    main()
