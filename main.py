try:
    from bs4 import BeautifulSoup
except ImportError:
    print("No module named 'BeautifullSoup' found")
import requests
import datetime


class Get_message:
    def __init__(self, series):
        self.series = series
        self.id = 0

    def get_imdb_url(self):
        r = requests.get("https://www.imdb.com/find?q=" + "+".join(self.series.split()))
        soup = BeautifulSoup(r.text, features="html.parser")
        title = soup.find_all("td", class_="result_text")[0].a['href']
        self.id = title.split('/')[2]

        return "https://www.imdb.com/title/" + self.id + "/episodes"

    def get_episode_date(self):
        r = requests.get(self.get_imdb_url())
        soup = BeautifulSoup(r.text, features="html.parser")
        year_span = soup.find_all("span", "nobr")[0].text
        if len(year_span.strip()) == 11:
            return "The show has finished streaming all its episodes"
        date = self.get_air_date(soup)

        if date == None:
            season = soup.find_all("h3", id="episode_top")[0].text.split()[-1]
            date = self.get_next_season_date(int(season) + 1)
            if date == None:
                return "Air date of next episode unkown"
            elif type(date)==int:
                return "The next season episode is scheduled in year " + str(date)
            else:
                return "The next season episode is scheduled on" + str(date.day) + str(date.month) + str(date.year)

        elif date.day == 0:
            return "The next episode is scheduled in year " + str(date.year) + ", exact date not known"

        else:
            return "The next episode is scheduled " + str(date.day) + str(date.month) + str(date.year)

    def get_next_season_date(self, season):
        print("https://www.imdb.com/title/"+str(self.id)+"/episodes?season=" + str(season))
        r = requests.get("https://www.imdb.com/title/"+str(self.id)+"/episodes?season=" + str(season))
        soup = BeautifulSoup(r.text, features="html.parser")
        season_on_page = soup.find_all("h3", id="episode_top")[0].text.split()[-1]
        if int(season_on_page)!=int(season):
            return None
        return self.get_air_date(soup)

    def get_air_date(self, soup):
        date_today = datetime.datetime.now()
        for episode_date in soup.find_all("div", class_="airdate"):
            if len(episode_date.text.strip()) == 0:
                continue
            try:
                date = datetime.datetime.strptime(episode_date.text.strip(), "%d %b. %Y")
            except:
                try:
                    date = datetime.datetime.strptime(episode_date.text.strip(), "%d %b %Y")
                except:
                    date = datetime.datetime.strptime(episode_date.text.strip(), "%Y")
                    if date.year >= date_today.year:
                        return date.year
            if date > date_today:
                return date
        return None

email = input()
series = input().split(",")
for i in series:
    print(i)
    a = Get_message(i)
    print(a.get_imdb_url())
    print(a.get_episode_date())
