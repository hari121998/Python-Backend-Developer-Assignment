import json 
import sqlite3
from tkinter.font import names

def get_json_data():
    with open('quotes.json','r') as read_file:
        obj_file = json.loads(read_file.read())
    return obj_file

def get_list_from_quotes_authors_obj(json_obj,obj_name):
    return json_obj[obj_name]

def distinct_author_list(list_1):
    name_list = []
    new_list= []
    for each_name in list_1:
        if each_name['name'] not in name_list:
            name_list.append(each_name['name'])
            new_list.append(each_name)
    return new_list,name_list

def connect_sqlite_to_database():
    return sqlite3.connect('quotes.db')

def create_table(table,table_name):
    connection = connect_sqlite_to_database()
    cursor_obj = connection.cursor()
    drop_sql = "DROP TABLE IF EXISTS {}"
    cursor_obj.execute(drop_sql.format(table_name))
    cursor_obj.execute('''PRAGMA foreign_keys = ON''')
    cursor_obj.execute(table)
    connection.close()

def inserting_data_into_table(insert_query):
    connection  = connect_sqlite_to_database()
    cursor_obj = connection.cursor()
    cursor_obj.execute(insert_query)
    connection.commit()
    connection.close()


quotes_authors_obj = get_json_data()
quotes_list = get_list_from_quotes_authors_obj(quotes_authors_obj,"quotes")
authors_list = get_list_from_quotes_authors_obj(quotes_authors_obj,"authors")

authors_new_list,author_names_list = distinct_author_list(authors_list)

quotes_table='''
        CREATE TABLE quotes(
            id INTEGER NOT NULL PRIMARY KEY,
            quote TEXT,
            author_name VARCHAR(250),
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id) 
            ON DELETE CASCADE
            );
            '''
authors_table='''
        CREATE TABLE authors(
            id INTEGER NOT NULL PRIMARY KEY,
            author_name VARCHAR(250),
            born TEXT(300),
            reference TEXT(400)
            );
            '''
tags_table = '''
        CREATE TABLE tags(
            id INTEGER,
            tag VARCHAR(250),
            quote_id INTEGER,
            FOREIGN KEY (quote_id) REFERENCES quotes(id) 
            ON DELETE CASCADE
            );
            '''

create_table(authors_table,"authors")
create_table(quotes_table,"quotes")
create_table(tags_table,"tags")

insert_author = '''
    INSERT INTO 
        authors(id,author_name,born,reference)
    VALUES(
        {},
        "{}",
        "{}",
        "{}"
    );
'''

id_count = 0
for each in authors_new_list:
    id_count+=1
    insert_data = insert_author.format(id_count,each['name'],each['born'],each['reference'])
    inserting_data_into_table(insert_data)
