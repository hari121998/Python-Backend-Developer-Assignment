import requests
from bs4 import BeautifulSoup
import json

def save_html_file(html,path): 
    with open(path,"wb") as writing_file:
        writing_file.write(html)

def open_html_file(path):
    with open(path,"rb") as read_file:
        return read_file.read()

def get_tag_list_text(html):
    new_tag_list=[]
    for each_tag in html:
        new_tag_list.append(each_tag.text.strip())   

    return new_tag_list

def get_html_parsed_file(file):
    return BeautifulSoup(file,"html.parser")

def create_and_get_quote_obj(each_tag):

    quotes_container = {}
    quote_text = each_tag.select_one('span').text.strip()

    quotes_container["quote"] = quote_text[1:len(quote_text)-1]
    quotes_container['author'] = each_tag.select_one('.author').text.strip()
    tags_html_list = each_tag.select('div .tags a')
    quotes_container["tags"] = get_tag_list_text(tags_html_list)

    return quotes_container


def get_author_birth_details(url):

    requested_file = requests.get(url)

    save_html_file(requested_file.content,"author_details.html")
    author_html_file = open_html_file("author_details.html")
    parsed_file = get_html_parsed_file(author_html_file)

    scrape_tag = parsed_file.select_one('body > div > div.author-details')
    born_html_file = scrape_tag.select('p span')
    
    first_born_text = born_html_file[0].text.strip()
    second_born_text = born_html_file[1].text.strip()

    return first_born_text+" "+second_born_text


def create_and_get_author_details_obj(each_tag,page_url):

    author_container={}
    author_reference_url = each_tag.select_one('span a')['href']
    author_reference_url =page_url+ author_reference_url +'/'
    
    author_container["name"]= each_tag.select_one('.author').text.strip()
    author_container["born"] = get_author_birth_details(author_reference_url)
    author_container['reference'] = author_reference_url

    return author_container

def create_append_quotes_authors_list(list_1,list_2,page_number,web_url):

    page_number = page_number+1
    page_url = web_url+"/page/"+str(page_number)+"/"

    if page_number>10:
        return list_1,list_2
    else:
        request_html_file = requests.get(page_url)

        save_html_file(request_html_file.content,"crawling.html")

        html_file = open_html_file("crawling.html")        

        parsered_file = get_html_parsed_file(html_file)

        html_scrape=parsered_file.select_one("body>div>div:nth-child(2)>div.col-md-8")
        #css selector file_path extracted by copying from developer_tools -> copy_selector

        quote_html_tag = html_scrape.select('.quote')


        for each_quote in quote_html_tag:
            quote_obj= create_and_get_quote_obj(each_quote)    
            author_obj=create_and_get_author_details_obj(each_quote,web_url)

            list_1.append(quote_obj)
            list_2.append(author_obj)
        return create_append_quotes_authors_list(list_1,list_2,page_number,web_url)

web_url = "http://quotes.toscrape.com"

page_num = 0
quotes_list = []
author__list=[]


quotes,authors=create_append_quotes_authors_list(quotes_list,author__list,page_num,web_url)

    
quotes_and_author_details_obj = {}
quotes_and_author_details_obj['quotes'] = quotes
quotes_and_author_details_obj['authors'] = authors

print(quotes_and_author_details_obj)

with open('quotes.json','w') as json_file:
    json.dump(quotes_and_author_details_obj,json_file)




