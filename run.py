import requests
from user_data import user_data
from bs4 import BeautifulSoup

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

raw_html = requests.post(DMV_URL, headers=headers, data=user_data)
soup = BeautifulSoup(raw_html, 'html.parser')

print (soup.prettify())
# print raw_html.text