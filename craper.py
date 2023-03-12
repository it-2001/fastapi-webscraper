import requests
from bs4 import BeautifulSoup
import json

MONTHS = 15

def scrape():
    URL = "https://blog.iservery.com/"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    def scrape_month(link):
        page_temp = requests.get(link)
        sp = BeautifulSoup(page_temp.content, "html.parser")
        names_raw = sp.select("h2.entry-title>a")
        names = [name.text for name in names_raw]
        content_urls = [url["href"] for url in names_raw]
        publication_dates_raw = sp.select("time.entry-date.updated")
        publication_dates = [date.text for date in publication_dates_raw]
        authors_raw = sp.select("a.url.fn.n")
        authors = [author.text for author in authors_raw]
        result = []
        for i in range(len(content_urls)):
            article = {
                "name": names[i],
                "date":publication_dates[i],
                "author":authors[i],
                "url": content_urls[i],
                "content": scrape_content(content_urls[i])
            }
            result.append(article)
        return result

    def scrape_content(link):
        page_temp = requests.get(link)
        sp = BeautifulSoup(page_temp.content, "html.parser")
        content_raw = sp.select("div.entry-content")
        content = content_raw[0].get_text()
        return content


    pages = soup.select("section.widget.widget_archive>ul>li>a")
    months = [page.text for page in pages]
    urls = [page["href"] for page in pages]

    result = []

    for i in range(MONTHS):
        months_sraped = scrape_month(urls[i])
        # month_scraped = {
        #     "month": months[i],
        #     "entries": len(months_sraped),
        #     "pages": months_sraped,
        # }
        print(len(months_sraped), months_sraped)
        result.extend(months_sraped)
    return result


def write_to_db(content):
    with open("articles.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(content))


write_to_db(scrape())