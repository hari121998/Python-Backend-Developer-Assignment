import json 
import sqlite3

def get_json_data():
    with open('quotes.json','r') as read_file:
        obj_file = json.loads(read_file.read())
    return obj_file

def get_list_from_quotes_authors_obj(json_obj,obj_name):
    return json_obj[obj_name]

quotes_authors_obj = get_json_data()
quotes_list = get_list_from_quotes_authors_obj(quotes_authors_obj,"quotes")
authors_list = get_list_from_quotes_authors_obj(quotes_authors_obj,"authors")
print(len(authors_list))