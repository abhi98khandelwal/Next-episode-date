try:
    from bs4 import BeautifulSoup
except ImportError:
    print("No module named 'BeautifullSoup' found")
import requests
import datetime

class GetMessage:
    """
    A class to scrape data from imdb website and return the date of next episode.

    Args:
        series (list): A list of series

    Attributes:
        series (list): input given
        id (str): IMDB id of a series
    """
    def __init__(self, series):
        self.series = series
        self.id = ""

    def get_imdb_url(self):
        """
        Method to get the imdb url of episodes of TV series given by scraping.

        Returns:
            imdb url of episodes of the series.
        """
        r = requests.get("https://www.imdb.com/find?q=" + "+".join(self.series.split()))
        soup = BeautifulSoup(r.text, features="html.parser")
        title = soup.find_all("td", class_="result_text")[0].a['href']
        self.id = title.split('/')[2]

        return "https://www.imdb.com/title/" + self.id + "/episodes"

    def get_episode_date(self):
        """
        Method to make message that needs to be sent to user.

        Returns:
             The message that will be sent to user consisting next episode date.
        """
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
                return "The next season episode is scheduled on" + str(date.year) + "/" +str(date.month) +  "/" + str(date.day)

        elif date.day == 0:
            return "The next episode is scheduled in year " + str(date.year) + ", exact date not known"

        else:
            return "The next episode is scheduled " + str(date.year) + "/" +str(date.month) +  "/" + str(date.day)

    def get_next_season_date(self, season):
        """
        Method to get the date of next season if current season of the series is over.

        Args:
            param1 (str): Season number of the series.

        Returns:
            The starting date of next season.
            None if given season has not been released.

        """
        #print("https://www.imdb.com/title/"+str(self.id)+"/episodes?season=" + str(season))
        r = requests.get("https://www.imdb.com/title/"+str(self.id)+"/episodes?season=" + str(season))
        soup = BeautifulSoup(r.text, features="html.parser")
        season_on_page = soup.find_all("h3", id="episode_top")[0].text.split()[-1]
        if int(season_on_page)!=int(season):
            return None
        return self.get_air_date(soup)

    def get_air_date(self, soup):
        """
        Method to get the next episode date.

        Args:
            param1 (bs4 object)

        Returns:
            The date of next of episode
        """
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

if __name__=='__main__':
    email = input()
    series = input().split(",")
    for i in series:
        print(i)
        a = GetMessage(i)
        print(a.get_imdb_url())
        print(a.get_episode_date())
