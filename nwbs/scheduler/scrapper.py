import json 
import asyncio 
import aiohttp
import os
import config

from bs4 import BeautifulSoup
from nwbs.scheduler.utils import MeetingParser


class JWIZARD:
    def __init__(self, basepath = "", weeklist=[], month=[], pname="nwb"):
        self.basepath = basepath
        self.weeklist = weeklist
        self.month = month
        self.pname = pname
        self.pathdict = {}

    def get_all_urls(self):
        weeklist = self.weeklist
        for week in weeklist:
            self.pathdict[week] = self.basepath.format(num=str(week), year=str(2024))
        return self.pathdict
    
    @staticmethod
    def rm_dups(items):
        seen = set()
        return [item for item in items if not (item in seen or seen.add(item))]

    @staticmethod
    def clean_duplicates(preaching_divs):
        preaching_h3s, preaching_points, preaching_time = [], [], []
        # Get the titles for the different preaching parts only
        for pd in preaching_divs:
            if pd.text.strip().startswith("DE USE ALL YOUR HEART PREACH"):
                preaching_h3s = pd.find_all_next(name="h3", attrs={"class": "du-color--gold-700"})
                break
        preaching_h3s = [x.text.strip().split(".")[-1].strip() for x in preaching_h3s]
        # create a list that will search for the first and last occurance of a div between
        # De use all your heart preach
        # and get their indexes so we can loop through them and get their child elements
        pos = []
        for p in preaching_divs:
            if p.text.strip().startswith("DE USE ALL YOUR HEART PREACH"):
                pos.append(preaching_divs.index(p))
                continue

            if p.text.strip().startswith("DE LIVE CHRISTIAN LIFE"):
                pos.append(preaching_divs.index(p))
                continue

        # we are adding +1 on the pos[0] because we want to remove the last item before the header
        # DE USE ALL YOUR HEART PREACH so we can select just one of the p tags and escape the nontype error
        los = []
        for p in preaching_divs[pos[0]+1:pos[-1]]:
            los.append(p.select_one("p").text.strip())
            preaching_points += p.select("a")
        
        # loop through loc to get the preaching preaching_time
        preaching_time = [x.strip()[1:3] for x in JWIZARD.rm_dups(los)]
        # filters the list to keep only text starting with lmd
        cas = []
        for p in preaching_points:
            if p.text.strip().startswith("lmd"):
                cas.append(p.text)
        preaching_points = JWIZARD.rm_dups(cas)

        return preaching_h3s, preaching_time, preaching_points

    async def fetch_data(self,session, url):
        # try:
        async with session.get(url) as response:
            print("fetching ", url)
            return await response.text()
        # except Exception as error:
        #     print(error)
    def scrap_data(self, html) -> dict:
        soup = BeautifulSoup(html, "html5lib") # If this line causes an error, run 'pip install html5lib' or install html5lib
        #soup.prettify()

        WeekItems = soup.find("div", {"class":"todayItems"})
        ###sections
        SectionX0 = WeekItems.select(".itemData #p1")
        SectionX1 = WeekItems.select(".bodyTxt")  
        SectionX2 = WeekItems.select(".itemData #p2")


        ###section1
        nwb_date = SectionX0[0].text
        reading = SectionX2[0].select("strong")[0].text

        opening_song = SectionX1[0].select("h3#p3 a")[0].text
        fine_fine_lesson = SectionX1[0].select("h3#p5 strong")[0].text.split("1.")[-1].strip()

        preaching_divs = SectionX1[0].select("div")
        
        br = []
        for pd in preaching_divs:
            if pd.text.strip().startswith("FINE-FINE LESSON"):
                br.append(preaching_divs.index(pd))
                continue
            if pd.text.strip().startswith("DE USE ALL YOUR HEART PREACH"):
                br.append(preaching_divs.index(pd))
                break


        br = preaching_divs[br[0]:br[-1]][-1].select("p")[0].text.split(" ")        
        bible_reading = " ".join(br[2:4])
        bible_reading_point = br[-1].replace(")", "")


        nwb_parts, nwb_parts_time, nwb_parts_point = self.clean_duplicates(preaching_divs)

        christian_life = SectionX1[0].select("div")
        cl_h3s = []
        cl_ps = []
        for t in christian_life:
            if t.text.strip().startswith("DE LIVE CHRISTIAN LIFE"):
                cl_h3s = t.find_all_next(name="h3",string=True)
                cl_ps = t.find_all_next(attrs={"class": "du-margin-inlineStart--5 du-margin-inlineStart-desktopOnly--6"})


        middle_song = cl_h3s[0].text.strip()    
        # cleans the messages and extracts only those that start with
        # "(" and starts with a string literal that can be converted to an integer
        nwb_lac, nwb_details, nwb_lac_time = [], [], []
        for i in cl_h3s:
            try:
                if int(i.text[0]):
                    nwb_lac.append(i.text.split(".")[-1].strip())
            except ValueError:
                continue

       # get congregation bible study
        book_study = ""
        for i in cl_ps:
            d = i.text.strip()[0:4]
            try:
                if d.startswith("(") and int(d[1:3]):
                    if i.text.strip().startswith("(30 min.)"):
                        book_study = i.text.split("(30 min.)")[-1].strip()
                        continue
                    nwb_details.append(i.text)
                    nwb_lac_time.append(d[1:3])
            except ValueError:
                continue
        #"remove the congregation bible study from the list"
        nwb_lac.pop(-1)
        concluding_song = SectionX1[0].select("span[class='dc-icon--music dc-icon-size--basePlus1 dc-icon-margin-inlineStart--2 dc-icon-margin-inlineEnd--8']")[0]
        concluding_song = concluding_song.select_one("strong").text

        nwb = {
            'month': nwb_date,
            'reading': reading,
            'opening_song': opening_song,
            'fine_fine_lesson': fine_fine_lesson,
            'bible_reading': bible_reading,
            'bible_reading_point': bible_reading_point,
            'preaching': nwb_parts,
            'preaching_points': nwb_parts_point,
            'preaching_time': nwb_parts_time,
            'middle_song': middle_song,
            'middle_parts': nwb_lac,
            'middle_parts_time': nwb_lac_time,
            'book_study': book_study,
            'book_study_box': "",
            'concluding_song': concluding_song,
        }

        return nwb

    async def main(self):
        async with aiohttp.ClientSession() as session:
            tasklist = []
            items = {}


            for _ , url in self.get_all_urls().items():
                tasklist.append(self.fetch_data(session, url))

            htmls = await asyncio.gather(*tasklist)

            for html in htmls:
                info = self.scrap_data(html)
                items[info["month"]] = info

                with open(os.path.join(os.getcwd(), config.FOLDER_REFERENCES["meeting_parts"], f"{self.pname}.json"), 'w') as f:
                    json.dump(items, f, indent=4)


#weeklist=[x for x in range(1, 10)]
#jwizard = JWIZARD(basepath=config.SCRAPPER_LINK,weeklist=weeklist)
#asyncio.run(jwizard.main())

