# how to run

## start
1. clone repo

## chromedriver
2. mkdir chromedriver in root directory
3. download selenium driver for your version of chrome: https://chromedriver.chromium.org/downloads
4. copy chromedriver.exe to chromedriver folder

## install dependencies
5. ```pip install gspread oauth2client```

## connect to google sheets
6. create a creds.json in root directory

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

7. Follow 12 min Youtube tutorial for how to populate and install: https://www.youtube.com/watch?v=cnPlKLEGR7E
* text version: https://techwithtim.net/tutorials/google-sheets-python-api-tutorial/

## run
8. run with ```python app.py```

## review
9. wait for bot to finish
10. check the google sheet for results

## customizing
11. Change the urls used in bot.get('') on line 42
12. Capture additional data from job ad by modifying lines 59-107
