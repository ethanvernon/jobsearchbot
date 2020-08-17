# how to run

## start
1. clone repo

## install dependencies
2. ```pip install gspread oauth2client``` (also part of step 8)

## chromedriver
3. mkdir chromedriver in root directory
4. download selenium driver for your version of chrome: https://chromedriver.chromium.org/downloads
5. copy chromedriver.exe to chromedriver folder

## install dependencies
6. ```pip install gspread oauth2client```

## connect to google sheets
7. create a ```creds.json``` in root directory

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

8. Follow from beggining to minute 7 this Youtube tutorial for how to populate and install: https://www.youtube.com/watch?v=cnPlKLEGR7E
   * text version: https://techwithtim.net/tutorials/google-sheets-python-api-tutorial/

9. Replace sheet name with your sheet name on line 17: ```sheet = client.open("sheetName").sheet1```

## run
10. run with ```python app.py```

## review
11. wait for bot to finish
12. check the google sheet for results

## customizing
13. Change the urls used in ```bot.get('')``` on line 42
14. Capture additional data from job ad by modifying lines 59-107
15. Save results outside of google sheets e.g. a .txt file or e-mail
