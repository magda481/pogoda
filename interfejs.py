import sys
import requests
from datetime import datetime, timedelta
history = {}
historia = []
daty = []
opis = []
slownik = dict()
fd = "historia.txt"
url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
api = sys.argv[1]
querystring = {"q":"new york","lat":"35","lon":"139","cnt":"10","units":"metric or imperial"}

headers = {
	"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	"X-RapidAPI-Key": str(api)
}
if len(sys.argv) == 3:
	dzien = sys.argv[2]
else:
	currentTimeDate = datetime.now() + timedelta(days=1)
	dzien = str(currentTimeDate.strftime('%Y-%m-%d'))


class WeatherForecast:

	def __init__(self, api):
		self.api = api
		self.slownik = slownik

	def __getitem__(self, key):
		self.slownik = dict(zip(daty, opis))
		return self.slownik[key]

	def __iter__(self):
		return iter(daty)

	def items(self):
		self.slownik = dict(zip(daty, opis))
		for k,v in self.slownik.items():
			print("{}: {}".format(k, v))

	def sprawdz(self):
		with open(fd, 'r') as f:
			historia = f.readlines()

		for idx in range(len(historia)):
			historia[idx] = str(historia[idx].strip())

		daty = historia[0::2]
		opis = historia[1::2]

		if dzien in daty:
			a = daty.index(dzien)
		else:
			pobierz_api()


def pobierz_api():

	response = requests.request("GET", url, headers=headers,
								params=querystring)
	answer = response.json()

	for day in answer['list']:
		date = str(datetime.fromtimestamp(day['dt']).date())
		rain = day.get('rain', "Nie bedzie padac")
		history[date] = rain

	if history.get(dzien) is not None:
		zapis = {}
		zapis[dzien] = history.get(dzien)
		daty.append(dzien)
		opis.append("Bedzie padac" if zapis[dzien] != "Nie bedzie padac" else
			zapis[dzien])
		with open(fd,"a") as f:
			f.write(dzien+'\n')
			f.write(("Bedzie padac" if zapis[dzien] != "Nie bedzie padac" else
			zapis[dzien])+'\n')
	else:
		daty.append(dzien)
		opis.append("Ni wiem")
		with open(fd, "a") as f:
			f.write(dzien+'\n')


with open(fd, 'r') as f:
	historia = f.readlines()

for idx in range(len(historia)):
	historia[idx] = str(historia[idx].strip())

daty = historia[0::2]
opis = historia[1::2]

if dzien in daty:
	a = daty.index(dzien)
else:
	pobierz_api()

with open(fd, 'r') as f:
	historia = f.readlines()

for idx in range(len(historia)):
	historia[idx] = str(historia[idx].strip())

daty = historia[0::2]
opis = historia[1::2]


pogoda = WeatherForecast(api)

for d in pogoda:
	print(d)
print()
print(pogoda[dzien])
print()
pogoda.items()
