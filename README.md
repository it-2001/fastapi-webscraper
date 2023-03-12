# fastapi-webscraper

script for scraping contents of Iservery blog https://blog.iservery.com/ and saving them into json file.
Contents are then read into fastapi database runniong on port 8000.

## how to use
### load contents
python3 craper.py {months}

- {months} how many months will be scraped, defaults to 15
- wait until program finishes
- right now you can not control number of scraped articles
### start fastapi server
pip install -r requirements.txt

uvicorn main:app 
