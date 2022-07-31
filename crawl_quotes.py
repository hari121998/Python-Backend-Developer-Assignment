import requests
from bs4 import BeautifulSoup

def save_html_file(html,path):
    with open(path,"wb") as writing_file:
        writing_file.write(html)


def get_html_file(path):
    with open(path,"rb") as read_file:
        return read_file.read()

def get_tag_list_text(html):
    new_tag_list=[]
    for each_tag in html:
        new_tag_list.append(each_tag.text.strip())
        
    return new_tag_list


request_html_file = requests.get("http://quotes.toscrape.com/")

save_html_file(request_html_file.content,"crawling.html")

html_file = get_html_file("crawling.html")        


soup = BeautifulSoup(html_file,"html.parser")
tag = soup.select_one("body > div > div:nth-child(2) > div.col-md-8")

tag1 = tag.select('.quote')

all_quotes = []

for each_quote in tag1:

    quotes = {}
    quotes["quote"] = each_quote.select_one('span').text.strip()
    quotes['author'] = each_quote.select_one('.author').text.strip()
    tag_html_list = each_quote.select('div .tags a') 
    quotes["tag"] = get_tag_list_text(tag_html_list)

    all_quotes.append(quotes)

print(all_quotes)
    







