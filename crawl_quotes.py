import requests
from bs4 import BeautifulSoup
import json

def request_and_get_parsed_file(page_url):
        requested_file = requests.get(page_url)
        soup = BeautifulSoup(requested_file.content,'html.parser')
        return soup

def request_parsed_file_return_quote_list_container(page_url):
    parsed_file =request_and_get_parsed_file(page_url)
    html_scrape=parsed_file.select_one("body>div>div:nth-child(2)>div.col-md-8")
    #css selector file_path extracted by copying from developer_tools -> copy_selector
    return html_scrape.select('.quote')

def get_tags_list_for_each_quote(tags_html_list):
    new_tag_list=[]
    for each_tag_name in tags_html_list:
        new_tag_list.append(each_tag_name.text.strip())   
    return new_tag_list

def create_and_get_quote_object(each_quote_element):
    quote_object_container = {}
    quote_text = each_quote_element.select_one('span').text.strip()

    # In the below line we cannot use strip('"') because text contains invalid inverted quotes 
    quote_object_container["quote"] = quote_text.strip('\u201c').strip('\u201d')
    quote_object_container['author'] = each_quote_element.select_one('.author').text.strip()

    tags_html_list = each_quote_element.select('div .tags a')
    quote_object_container["tags"] = get_tags_list_for_each_quote(tags_html_list)
    return quote_object_container

def iterating_and_appending_each_quote(quote_tags_container,quote_list,):
    for each_quote_tag in quote_tags_container:
        each_quote_object= create_and_get_quote_object(each_quote_tag)    
        quote_list.append(each_quote_object)
       
def create_append_quotes_list(quote_list,page_url):
    all_quote_html_tags =request_parsed_file_return_quote_list_container(page_url)
    iterating_and_appending_each_quote(all_quote_html_tags,quote_list)
    return quote_list

def get_author_born_details_from_bio_page(author_bio_page):
    author_parsed_file = request_and_get_parsed_file(author_bio_page)
    author_bio_container = author_parsed_file.select_one('body > div > div.author-details')
    author_born_details = author_bio_container.select('p span')

    born_date = author_born_details[0].text.strip()
    born_location = author_born_details[1].text.strip()
    return born_date+" "+born_location

def create_and_get_author_object_from_each_quote_tag(each_quote_tag):
    each_author_object = {}
    author_bio_page = each_quote_tag.select_one('span a')['href']+'/'
    author_bio_page = "http://quotes.toscrape.com" + author_bio_page 

    each_author_object['name'] = each_quote_tag.select_one('.author').text.strip()
    each_author_object['born'] = get_author_born_details_from_bio_page(author_bio_page)
    each_author_object['reference'] = author_bio_page
    
    return each_author_object
    
def iterating_and_appending_each_author(quote_html_tags,author_list):
    for each_quote_tag in quote_html_tags:
        each_author_object= create_and_get_author_object_from_each_quote_tag(each_quote_tag)    
        author_list.append(each_author_object)
       
def create_append_authors_list(author_list,page_url):
    all_quote_html_tags = request_parsed_file_return_quote_list_container(page_url)
    iterating_and_appending_each_author(all_quote_html_tags,author_list)
    return author_list

def get_author_unique_list(authors_list):
    new_list=[]
    unique_author_list = []
    for each_author in authors_list:
        if each_author['name'] not in new_list:
            new_list.append(each_author['name'])
            unique_author_list.append(each_author)
    return unique_author_list

def request_and_return_next_page_url_if_exists(page_url):
    parsed_file = request_and_get_parsed_file(page_url)
    next_page_class = parsed_file.select('nav ul li')[-1]['class']
    if ''.join(next_page_class) == 'next':
        next_page_url =parsed_file.select('nav ul li a')[-1]['href']
        return "http://quotes.toscrape.com" + next_page_url    
    return ""

quote_list = []
author_list=[]
page_url = "http://quotes.toscrape.com"
while True: 
    quote_list_container = create_append_quotes_list(quote_list,page_url)
    author_list_container = create_append_authors_list(author_list,page_url)
    page_url = request_and_return_next_page_url_if_exists(page_url)
    if page_url=="":
        break

quotes_and_author_details_object = {}
quotes_and_author_details_object['quotes'] = quote_list
quotes_and_author_details_object['authors'] = get_author_unique_list(author_list)

with open('quotes.json','w') as json_file:
    json.dump(quotes_and_author_details_object,json_file)
print("Scrapped data succesfully Stored in quotes.json_file")

