'''
Get the current date time
Get the list of events for the day
Get list of births for the day
Get list of deaths for the day

Priorities:
Ecuador, USA, Lenght(), Nobel

Refresh the priorities list if it is a new day
Get 8 tweets text 
Then tweet the text with a format
'''
from datetime import date
import datetime
import requests
from bs4 import BeautifulSoup
import copy


class TweetsList(object):
    main_text = None
    meses_espanol = ["enero", "febrero", "marzo", "abril",
                     "mayo", "junio", "julio", "agosto",
                     "septiembre", "octubre", "noviembre", "diciembre"]
    MAX_EVENTS = 40
    def __init__(self):
        self.get_date()
        self.build_url()
        self.parse_url()
        self.get_events()
        self.filter_and_prio()
    
    def get_date(self):
        self.date = datetime.datetime.today().strftime("%Y-%m-%d")
        self.currentDay = datetime.datetime.now().day
        self.currentMonth = datetime.datetime.now().month
        self.currentYear = datetime.datetime.now().year

    def update(self):
        if self.date != datetime.datetime.today().strftime("%Y-%m-%d"):
            self.get_date()
            self.parse_url()
            self.get_events()
            self.filter_and_prio()

    def build_url(self):
        self.url = "https://www.hoyenlahistoria.com/efemerides/{}/{}".format(
            self.meses_espanol[self.currentMonth-1], self.currentDay)

    def parse_url(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        paragraph = soup.find(id="main_text")
        main_text = paragraph.find_all("p")
        self.main_text = main_text

    def get_events(self):
        self.events = []
        for p in self.main_text:
            if "efemerides/fecha" in str(p):
                p = str(p)[3:-4]  # deleting initial fields
                e_list = p.split("\n")
                for l in e_list:
                    try:
                        year_txt, e_txt = l.split("</a> -</b>")
                        year_txt = year_txt[-4:]
                        if "<br/>" in e_txt:
                            e_txt = e_txt[:-5]
                        text = "Un día como hoy, {}/{}/{},{}".format(
                            self.currentDay,
                            self.currentMonth,
                            year_txt,
                            e_txt)
                        self.events.append(text)
                    except:
                        pass

    def filter_and_prio(self):
        events_temp = copy.deepcopy(self.events)
        events_temp.reverse()
        self.filtered_list = []
        if len(self.events)<self.MAX_EVENTS:
            self.MAX_EVENTS=len(self.events)

        for c, i in enumerate(events_temp):
            if any(word in i.lower() for word in ["ecuador", "quito", "ecuatoriano", "guayaquil", "cuenca"]):
                self.filtered_list.append(i)
                events_temp.pop(c)

            if any(word in i.lower() for word in ["estados unidos", "estadounidense"]):
                self.filtered_list.append(i)
                events_temp.pop(c)

        if len(self.filtered_list) < self.MAX_EVENTS:
            for i in range(self.MAX_EVENTS-len(self.filtered_list)):
                self.filtered_list.append(events_temp[i])

    def remove_top_event(self):
        self.filtered_list.pop(0)


if __name__ == "__main__":
    '''
    tl = TweetsList()
    y = tl.filtered_list
    for t in y:
        print(t[:80])
    '''