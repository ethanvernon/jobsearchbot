import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ChromeOptions

# https://www.youtube.com/watch?v=cnPlKLEGR7E
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("jobSearchTwo").sheet1
sheet.clear()

# makes class
class IndeedBot:
    # init
    def __init__(self):
        opts = ChromeOptions()

        opts.add_experimental_option("detach", True)
        self.bot = webdriver.Chrome("./chromedriver/chromedriver.exe")

    # executes search, copies up to 50 urls to global variable links
    def findJobs(self):
        bot = self.bot
        jobs = list()
        global links
        links = list()
        # run once

        # https://www.indeed.com/jobs?as_and=web+developer+remote&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=1&limit=50&sort=&psf=advsrch&from=advancedsearch
        # https://www.indeed.com/jobs?as_and=web+developer+title%3Aremote&jt=all&fromage=1&limit=50&psf=advsrch&from=advancedsearch
        # https://www.indeed.com/jobs?q=web+developer+title%3Ajunior&limit=50&fromage=1&radius=25&start=0&l=Chicago%2C+IL
        # https://www.indeed.com/jobs?as_and=web+developer+javascript&as_phr=&as_any=&as_not=&as_ttl=junior&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=United+States&fromage=3&limit=50&sort=date&psf=advsrch&from=advancedsearch
        bot.get(
            "https://www.indeed.com/jobs?as_and=web+developer+javascript&as_phr=&as_any=&as_not=&as_ttl=junior&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=United+States&fromage=3&limit=50&sort=date&psf=advsrch&from=advancedsearch"
        )
        time.sleep(10)

        # finds all titles
        jobs = bot.find_elements_by_class_name("jobtitle")

        # saves href values from all titles
        links = [elem.get_attribute("href") for elem in jobs]

    # find the jobs that can be applied to directly from indeed
    def sortByApplyType(self):
        bot = self.bot
        global links
        global sheet
        count = 0

        # enumerates over links
        for idx, link in enumerate(links):
            # goes to link
            bot.get(link)
            time.sleep(5)

            # adds link to first column of sheet
            sheet.update_cell(idx + 1, 1, link)

            # gets values from job ad
            jobName = bot.find_element_by_class_name(
                "jobsearch-JobInfoHeader-title"
            ).text

            jobCompany = bot.find_element_by_css_selector(
                ".jobsearch-InlineCompanyRating > div:first-of-type"
            ).text

            jobLocation = bot.find_element_by_css_selector(
                ".jobsearch-InlineCompanyRating > div:last-of-type"
            ).text

            # saves values to clumns in sheets
            sheet.update_cell(idx + 1, 3, jobName)
            sheet.update_cell(idx + 1, 4, jobCompany)
            sheet.update_cell(idx + 1, 5, jobLocation)

            try:  # try quick apply button
                print("clicking apply button")
                # clicks on button
                bot.execute_script(
                    'document.querySelector(".jobsearch-IndeedApplyButton-contentWrapper").click();'
                )
                print("saved to list")

                # updates sheet for job as instant-apply
                sheet.update_cell(idx + 1, 2, "insta-apply")
                time.sleep(1)

                # open new blank tab
                count += 1
                bot.execute_script("window.open();")

                # switch to the new window which is second in window_handles array
                bot.switch_to_window(bot.window_handles[count])
            except:
                # if click event fails, adds no to instant-apply column in sheet
                print("no button")
                sheet.update_cell(idx + 1, 2, "no")


ethan = IndeedBot()

# gets urls from search results
ethan.findJobs()

# goes through each url and saves info to row in sheets
ethan.sortByApplyType()
