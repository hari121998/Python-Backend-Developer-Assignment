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

def get_html_parsed_file(file):
    return BeautifulSoup(file,"html.parser")

def get_author_details(url):
    request_file = requests.get(url)
    save_html_file(request_file.content,"author_details.html")
    author_html_file = get_html_file("author_details.html")
    parsed_file = get_html_parsed_file(author_html_file)
    scrape_tag = parsed_file.select_one('body > div > div.author-details')
    data = scrape_tag.select('p span')
    print(data[0].text+data[1].text)







page_url = "http://quotes.toscrape.com/"

request_html_file = requests.get(page_url)

save_html_file(request_html_file.content,"crawling.html")

html_file = get_html_file("crawling.html")        

html_parsered_file = get_html_parsed_file(html_file)

html_file_scrape_tag = html_parsered_file.select_one("body > div > div:nth-child(2) > div.col-md-8")
#css selector file_path extracted by copying from developer_tools -> copy_selector

quote_html_tag = html_file_scrape_tag.select('.quote')

quotes_authors_tags_list = []
author_details_list=[]
for each_quote in quote_html_tag[:1]:

    quotes_container = {}
    author_container={}

    quotes_container["quote"] = each_quote.select_one('span').text.strip()
    quotes_container['author'] = each_quote.select_one('.author').text.strip()
    tags_html_list = each_quote.select('div .tags a') 
    quotes_container["tags"] = get_tag_list_text(tags_html_list)

    author_reference_url = each_quote.select_one('span a')['href']
    author_reference_url =page_url+ author_reference_url +'/'
    print(author_reference_url)
    get_author_details(author_reference_url)

    author_container['reference'] = author_reference_url
    # print(author_reference_url)


    quotes_authors_tags_list.append(quotes_container)

# print(quotes_authors_tags_list)
    







