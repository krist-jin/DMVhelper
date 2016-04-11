import requests
from user_data import user_data_1, user_data_2, DMVBody, cr_list, rf_dict, pd_dict, searchAppts_body
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_datetime
import datetime
import time
import traceback
import random
import urllib
from copy import deepcopy
import re

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
    # "Content-Length": "552",
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

URLS = {
    "welcome": "https://www.dmv.ca.gov/portal/dmv/detail/portal/foa/welcome/",
    "clear": "https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=driveTest&localeName=en",
    "searchAppts": "https://www.dmv.ca.gov/wasapp/foa/searchAppts.do"
}

def getCommonCookies():
    commonCookies1 = []
    
    # get first part of common cookies at welcome page
    r = requests.get(URLS['welcome'], headers=HEADERS)
    cookie_string1 = r.headers.get('Set-Cookie')
    if cookie_string1:
        commonCookies1 = cookie_string1.rstrip('; Path=/').split('; Path=/, ')
    commonCookies1 = list(set(commonCookies1))  # remove duplicates

    # get the other part of common cookies at /wasapp/foa/clear.do
    this_headers = deepcopy(HEADERS)
    this_headers["Cookie"] = "; ".join(commonCookies1)
    this_body = deepcopy(DMVBody)
    this_body[1] = ("TS0141aebd_cr", cr_list[0])
    this_body[4] = ("TS0141aebd_md", 1)
    this_body[5] = ("TS0141aebd_rf", URLS["welcome"])
    this_body[6] = ("TS0141aebd_ct", 0)
    this_body[7] = ("TS0141aebd_pd", 0)
    r = requests.post(URLS['clear'], headers=this_headers, data=this_body)
    cookie_string2 = r.headers.get('Set-Cookie')
    if cookie_string2:
        commonCookies2 = cookie_string2.rstrip('; Path=/').split('; Path=/, ')
    
    # combine two parts
    return commonCookies1[:2] + commonCookies2[1:]

def getCurrentAppDatetime(commonCookies):
    this_headers = deepcopy(HEADERS)
    this_headers["Cookie"] = "; ".join(commonCookies)
    r = requests.post(URLS["searchAppts"], headers=this_headers, data=searchAppts_body)
    print r.text
    # # parse html using bs4
    # soup = BeautifulSoup(r.text, 'html.parser')
    
    # # extract result from soup result
    # result_table = soup.find(id="ApptForm").find_all("table")[0]
    # current_app = result_table.find_all("tr")[0].find_all("td")[1].get_text()
    # dt_beg_idx = current_app.find("Date/Time: ")+11
    # dt_end_idx = current_app.find("Confirmation Number")-1
    # current_datetime = current_app[dt_beg_idx:dt_end_idx]
    # print parse_datetime(current_datetime)
    # # return parse_datetime(current_datetime)

def getFirstAvailableAppDatetime():
    pass

def getReturnDatetime(app_datetime, office_name):
    oid, dis_time_minutes = DMV_OFFICES[office_name]
    dis_time = datetime.timedelta(minutes=dis_time_minutes)
    return (app_datetime + EXAM_AND_WAIT_TIME + dis_time)

def makeApp(newCookies):
    pass

def main():
    while True:
        try:
            print "\n******* %s *******" % str(datetime.datetime.now())
            commonCookies = getCommonCookies()
            currentAppDatetime = getCurrentAppDatetime(commonCookies)
            for office_name in DMV_OFFICES:
                first_available_datetime, newCookies = getFirstAvailableAppDatetime(office_name, commonCookies)
                returnDatetime = getReturnDatetime(first_available_datetime, office_name)
                if returnDatetime.time() >= RETURN_TIME:
                    print "%s: %s, return time: %s --- too late" % (office_name, first_available_datetime, returnDatetime.time())
                elif returnDatetime >= currentAppDatetime:
                    print "%s: %s, return time: %s --- later than current app" % (office_name, first_available_datetime, returnDatetime.time())
                else:
                    print "%s: %s, return time: %s --- perfect and earliest ever" % (office_name, first_available_datetime, returnDatetime.time())
                    makeApp(newCookies)
                time.sleep(1)
                
        except Exception, e:
            traceback.print_exc()
            time.sleep(INTERVAL*33)
            continue
        else: # succeed
            time.sleep(INTERVAL*33)

def test():
    commonCookies = getCommonCookies()
    getCurrentAppDatetime(commonCookies)

if __name__ == '__main__':
    test()