import sys
import requests
from datetime import datetime, timedelta
history = {}
historia = []
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
		print("Bedzie padac" if zapis[dzien] != "Nie bedzie padac" else
			zapis[dzien])
		with open(fd,"a") as f:
			f.write(dzien+'\n')
			f.write(("Bedzie padac" if zapis[dzien] != "Nie bedzie padac" else
			zapis[dzien])+'\n')
	else:
		print("Nie wiem")
		with open(fd, "a") as f:
			f.write(dzien+'\n')
			f.write("Nie wiem"+'\n')


with open(fd, 'r') as f:
	historia = f.readlines()

for idx in range(len(historia)):
	historia[idx] = str(historia[idx].strip())

daty = historia[0::2]
opis = historia[1::2]
# print(daty)
# print(opis)

if dzien in daty:
	a = daty.index(dzien)
	print(opis[a])
else:
	pobierz_api()