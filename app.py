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
    # init with self, username, and password
    def __init__(self):
        # self.username = username
        # self.password = password
        # bot as webdriver
        opts = ChromeOptions()

        opts.add_experimental_option("detach", True)
        # self.bot = webdriver.Chrome(chrome_options=opts)
        self.bot = webdriver.Chrome("./chromedriver/chromedriver.exe")

    # self.bot = webdriver.Chrome('../../../Downloads/chromedriver')

    # goes to page, inputs username password, hits enter, waits 60s in case user needs to beat captcha
    # def login(self):
    #     bot = self.bot
    #     # goes to url
    #     bot.get(
    #         "https://secure.indeed.com/account/login?service=my&hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F"
    #     )
    #     print("inputting email and password")
    #     # finds email input by id and saves as var
    #     email = bot.find_element_by_id("login-email-input")
    #     password = bot.find_element_by_id("login-password-input")
    #     # clears forms
    #     email.clear()
    #     password.clear()
    #     # types in username/passwords in inputs
    #     email.send_keys(self.username)
    #     password.send_keys(self.password)
    #     # hits Return
    #     password.send_keys(Keys.RETURN)
    #     # waits in case captcha
    #     print("waiting 60s for possible captcha")
    #     time.sleep(1)
    #     print("10s before search")
    #     time.sleep(10)
    #     print("starting search")

    # executes search, copies all 50 urls to global variable links
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
        jobs = bot.find_elements_by_class_name("jobtitle")
        links = [elem.get_attribute("href") for elem in jobs]
        # run for multiple pages
        # for x in range(3):
        # 	bot.get('https://www.indeed.com/jobs?q=web+developer+title%3Ajunior&limit=50&fromage=1&radius=25&start='+str(50*x))
        # 	time.sleep(3)
        # 	jobs = bot.find_elements_by_class_name('jobtitle')
        # 	links += [elem.get_attribute('href') for elem in jobs]
        # 	print(links)

    # store all links in first column of google sheets
    # def storeJobs(self):
    #     bot = self.bot
    #     global links
    #     global sheet
    #     for idx, link in enumerate(links):
    #         sheet.update_cell(idx + 1, 1, link)

    # find the jobs that can be applied to directly from indeed
    def sortByApplyType(self):
        bot = self.bot
        global links
        global sheet
        count = 0
        for idx, link in enumerate(links):
            bot.get(link)
            time.sleep(5)
            # get and save url, job title, company, location, description
            sheet.update_cell(idx + 1, 1, link)
            jobName = bot.find_element_by_class_name(
                "jobsearch-JobInfoHeader-title"
            ).text
            jobCompany = bot.find_element_by_css_selector(
                ".jobsearch-InlineCompanyRating > div:first-of-type"
            ).text
            jobLocation = bot.find_element_by_css_selector(
                ".jobsearch-InlineCompanyRating > div:last-of-type"
            ).text
            sheet.update_cell(idx + 1, 3, jobName)
            sheet.update_cell(idx + 1, 4, jobCompany)
            sheet.update_cell(idx + 1, 5, jobLocation)
            # jobMatch=0
            # jobDescription=bot.find_element_by_class_name("jobsearch-jobDescriptionText")
            try:  # try quick apply button
                print("clicking apply button")
                bot.execute_script(
                    'document.querySelector(".jobsearch-IndeedApplyButton-contentWrapper").click();'
                )
                # applyOnLinkedInLinks.append(link)
                print("saved to list")
                sheet.update_cell(idx + 1, 2, "insta-apply")
                time.sleep(1)
                # open new blank tab
                count += 1
                bot.execute_script("window.open();")
                # switch to the new window which is second in window_handles array
                bot.switch_to_window(bot.window_handles[count])
            except:
                print("no button")
                sheet.update_cell(idx + 1, 2, "no")
        # print(applyOnLinkedInLinks)

    # def openJobs(self):
    #     bot = self.bot
    #     global links
    #     for link in links:
    #         print("going to job")
    #         bot.get(link)
    #         try:
    #             # wait page to load
    #             time.sleep(2)
    #             print("clicking apply button")
    #             # bot.find_element_by_class_name('jobsearch-IndeedApplyButton-contentWrapper').click()
    #             bot.execute_script(
    #                 'document.querySelector(".jobsearch-IndeedApplyButton-contentWrapper").click();'
    #             )
    #             # wait ad to load
    #             time.sleep(3)
    #             print("searching for iframes")
    #             iframes = bot.find_elements_by_tag_name("iframe")
    #             print(iframes)
    #             # wait iframe to load (needed?)
    #             time.sleep(1)
    #             print("switching to 2nd frame")
    #             iframesTwo = bot.find_elements_by_tag_name("iframe")
    #             bot.switch_to.frame(1)
    #             print(iframesTwo)
    #             print("switching to 1st frame of 2nd frame")
    #             bot.switch_to.frame(0)
    #             # wait iframe to load (needed?)
    #             time.sleep(1)
    #             print("clicking continue button")
    #             bot.find_element_by_class_name("ia-FormActionButtons-continue").click()
    #             # bot.execute_script('document.querySelector(".ia-FormActionButtons-continue").click();')
    #             # wait for second page of application to load
    #             time.sleep(5)
    #             print("clicking submit button")
    #             # bot.find_element_by_class_name('jobsearch-IndeedApplyButton-contentWrapper').click()
    #             # bot.execute_script('document.querySelector("#form-action-submit").click();')
    #             bot.find_element_by_id("form-action-submit").click()
    #             # wait for the submit to go through
    #             time.sleep(5)
    #         except Exception as ex:
    #             print(ex)
    #             time.sleep(3)


ethan = IndeedBot()

# ethan.login()
ethan.findJobs()
ethan.sortByApplyType()
