# pro tips
1. Stand on the shoulders of giants - this bot was created largely with beginner knowledge of HTML + Python after watching 2 tutorials:
  a. How to build a tiwtter bot: https://www.youtube.com/watch?v=7ovFudqFB0Q&t
  b. How to use Google Sheets with Python: https://www.youtube.com/watch?v=cnPlKLEGR7E

# how to run

## start
1. clone repo

## chromedriver
2. mkdir chromedriver in root directory
3. download selenium driver for your version of chrome: https://chromedriver.chromium.org/downloads
4. copy chromedriver.exe to chromedriver folder

## install dependencies
5. ```pip install gspread oauth2client``` (also part of step 8)

## connect to google sheets
6. create a ```creds.json``` in root directory

```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```

7. Follow from beggining to minute 7 this Youtube tutorial for how to populate and install: https://www.youtube.com/watch?v=cnPlKLEGR7E
   * text version: https://techwithtim.net/tutorials/google-sheets-python-api-tutorial/

8. Replace sheet name with your sheet name on line 17: ```sheet = client.open("sheetName").sheet1```

## run
9. run with ```python app.py```

## review
10. wait for bot to finish
11. check the google sheet for results

## customizing
12. Change the urls used in ```bot.get('')``` on line 42
13. Capture additional data from job ad by modifying lines 59-107
14. Save results outside of google sheets e.g. a .txt file or e-mail
