import requests
from user_data import user_data_1, user_data_2, DMVBody, cr_list, rf_dict, pd_dict
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
# COOKIE_FILLERS = {
#     "reviewDriveTest": "TS0141aebd_77=3333_%s_rsb_0_rs_https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do_rs_0_rs_0"
# }
INTERVAL = 1 # run every 1 minute

RETURN_TIME = datetime.time(10, 00) # need another 30 mins to arrive work
EXAM_AND_WAIT_TIME = datetime.timedelta(hours=1)

def getReturnDatetime(app_datetime, dis_time):
    return (app_datetime + EXAM_AND_WAIT_TIME + dis_time)

def makeApp(cookies):
    headers_copy = deepcopy(HEADERS)
    # cookies.append(COOKIE_FILLERS["reviewDriveTest"])
    headers_copy["Cookie"] = "; ".join(cookies)
    # headers_copy["Cookie"] = "AMWEBJCT!%2Fwasapp!JSESSIONID=00005IaaGy4T82vfk-9TVwOB2-r:18u4cegug; PD_STATEFUL_05b765dc-0c5a-11e4-be4c-a224e2a50102=%2Fwasapp; TS0141aebd=014a8a21d5fb685d86dbe79b81761825a1b7214bb13f481c159bc0caf6175e98ff9a97c96ba5c8df4f7311c25d98339a226e89bafd463110795aa143b3477709ec0ddb9633; TS0141aebd_77=3333_2a878b91bd409479_rsb_0_rs_https%3A%2F%2Fwww.dmv.ca.gov%2Fwasapp%2Ffoa%2FfindDriveTest.do_rs_0_rs_0"
    print headers_copy["Cookie"]
    r = requests.post(rf_dict["reviewDriveTest"], headers=headers_copy)
    print r.text

def getCurrentAppDatetime():
    DMVBody[1] = ("TS0141aebd_cr", cr_list[0])
    DMVBody[5] = ("TS0141aebd_rf", rf_dict["searchAppts"])
    DMVBody[7] = ("TS0141aebd_pd", pd_dict["searchAppts"])
    
    # send http post request
    r = requests.post(rf_dict["searchAppts"], headers=HEADERS, data=urllib.urlencode(DMVBody))
    
    # parse html using bs4
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # extract result from soup result
    result_table = soup.find(id="ApptForm").find_all("table")[0]
    current_app = result_table.find_all("tr")[0].find_all("td")[1].get_text()
    dt_beg_idx = current_app.find("Date/Time: ")+11
    dt_end_idx = current_app.find("Confirmation Number")-1
    current_datetime = current_app[dt_beg_idx:dt_end_idx]
    return parse_datetime(current_datetime)
    # return datetime.datetime(2016, 1, 1)

def getFirstAvailableAppDatetime(office_name):
    oid, dis_time_minutes = DMV_OFFICES[office_name]
    # user_data_with_office = user_data_1+oid+user_data_2
    DMVBody[1] = ("TS0141aebd_cr", cr_list[0])
    DMVBody[5] = ("TS0141aebd_rf", rf_dict["findDriveTest"])
    DMVBody[7] = ("TS0141aebd_pd", pd_dict["findDriveTest"] % str(oid))
    
    # send http post request
    r = requests.post(rf_dict["findDriveTest"], headers=HEADERS, data=urllib.urlencode(DMVBody))
    # print r.headers
    # print r.content
    cookie_string = r.headers.get('Set-Cookie')
    if cookie_string:
        cookies = cookie_string.rstrip('; Path=/').split('; Path=/, ')
    code = re.search('a={c:"TS0141aebd_77",d:"(.*)",n:"1000', r.text).group(1)
    tricky_cookie_string = "TS0141aebd_77=3333_%s_rsb_0_rs_https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do_rs_0_rs_0" % code
    cookies.append(urllib.urlencode(tricky_cookie_string))
    # parse html using bs4
    soup = BeautifulSoup(r.text, 'html.parser')

    # extract result from soup result
    result_table = soup.find(id="app_content").table
    first_available_datetime = result_table.find_all("tr")[2].p.get_text()
    # print first_available_datetime
    return parse_datetime(first_available_datetime), cookies
    

def main():
    while True:
        try:
            print "\n******* %s *******" % str(datetime.datetime.now())
            currentAppDatetime = getCurrentAppDatetime()
            for office_name in DMV_OFFICES:
                first_available_datetime, cookies = getFirstAvailableAppDatetime(office_name)
                oid, dis_time_minutes = DMV_OFFICES[office_name]
                dis_time = datetime.timedelta(minutes=dis_time_minutes)
                returnDatetime = getReturnDatetime(first_available_datetime, dis_time)
                if returnDatetime.time() >= RETURN_TIME:
                    print "%s: %s, return time: %s --- too late" % (office_name, first_available_datetime, returnDatetime.time())
                elif returnDatetime >= currentAppDatetime:
                    print "%s: %s, return time: %s --- later than current app" % (office_name, first_available_datetime, returnDatetime.time())
                else:
                    print "%s: %s, return time: %s --- perfect and earliest ever" % (office_name, first_available_datetime, returnDatetime.time())
                    makeApp(cookies)
                time.sleep(1)
                
        except Exception, e:
            traceback.print_exc()
            time.sleep(INTERVAL*33)
            continue
        else: # succeed
            time.sleep(INTERVAL*33)

def test():
    # getCurrentAppDatetime()
    first_available_datetime, cookies = getFirstAvailableAppDatetime("santa clara")
    # print cookies
    makeApp(cookies)

if __name__ == '__main__':
    test()
