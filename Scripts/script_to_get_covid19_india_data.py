from bs4 import BeautifulSoup
import requests
import json

request_url = "https://www.mohfw.gov.in"
page = requests.get(request_url)
soup = BeautifulSoup(page.text, "lxml")

info = soup.find('ol')
points = info.findAll('strong')
air_screening = points[0].text
total_cases = points[1].text.split(':')[1].split()[0]

table = info.find('tbody')
rows = table.findAll('tr')
totals = rows[-1].findAll('td')

data_obj = {}
data_obj['screened_at_airport'] = air_screening
data_obj['total_cases'] = total_cases
data_obj['total_domestic_cases'] = totals[1].text
data_obj['total_international_cases'] = totals[2].text
data_obj['total_cured_cases'] = totals[3].text
data_obj['total_death_cases'] = totals[4].text
data_obj['states'] = {}

for row in rows[:-1]:
	cols = row.findAll('td')
	data_obj['states'][cols[1].text] = {
		'sl.no' : cols[0].text,
		'name' : cols[1].text,
		'domestic_cases' : cols[2].text,
		'international_cases' : cols[3].text,
		'cured_cases' : cols[4].text,
		'death_cases' : cols[5].text
	}

with open('../DataJSON/test.json', 'w', encoding='utf-8') as f:
    json.dump(data_obj, f, ensure_ascii=False, indent=4)