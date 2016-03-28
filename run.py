import requests
from user_data import user_data
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from datetime import datetime

DESIRED_DATE = datetime(2016, 4, 4).date()

DMV_URL = "https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do"

headers = {
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

# send http post request
raw_html = requests.post(DMV_URL, headers=headers, data=user_data).text

# parse html using bs4
soup = BeautifulSoup(raw_html, 'html.parser')

# extract result from soup result
result_table = soup.find(id="app_content").table
first_available_time = result_table.find_all("tr")[2].p.get_text()
parsed_date = parse_date(first_available_time).date()
if parsed_date == DESIRED_DATE:
	print str(DESIRED_DATE) + " is available!"
else:
	print str(DESIRED_DATE) + " is not available!" 
# print raw_html
# print (soup.prettify())
# print result_table.prettify()
# print result_table.get_text()
# print first_available_time

# //*[@id="app_content"]/table