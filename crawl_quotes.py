import requests
from bs4 import BeautifulSoup

def save_html_file(html,path):
    with open(path,"wb") as writing_file:
        writing_file.write(html)


def get_html_file(path):
    with open(path,"rb") as read_file:
        return read_file.read()

request_html_file = requests.get("http://quotes.toscrape.com/")

save_html_file(request_html_file.content,"crawling.html")

html_file = get_html_file("crawling.html")        



print(html_file)



