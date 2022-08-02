import json 
import sqlite3
import json



def get_json_data():
    with open('quotes.json','r') as read_file:
        obj_file = json.loads(read_file.read())
    return obj_file

def get_list_from_quotes_authors_obj(json_obj,obj_name):
    return json_obj[obj_name]

def distinct_author_names_list(list_1):
    name_list = []
    for each_name in list_1:
        if each_name['name'] not in name_list:
            name_list.append(each_name['name'])            
    return name_list

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
    cursor_obj.executescript(insert_query)
    connection.commit()
    connection.close()

def get_and_insert_author(id,each_obj,insert_string):
    name = each_obj['name']
    born = each_obj['born']
    reference = each_obj['reference']
    
    insert_data = insert_string.format(id,name,born,reference)
    inserting_data_into_table(insert_data)

def get_and_insert_quotes(id,each_obj,insert_string):
    quote=each_obj['quote']
    if id ==91:
        quote= quote[:10]+quote[12:31]+quote[32:]
        
    author_name = each_obj['author']
    no_of_tags = len(each_obj['tags'])

    author_id = author_names_list.index(author_name)+1
    insert_data = insert_string.format(id,quote,author_name,no_of_tags,author_id)

    inserting_data_into_table(insert_data)

def get_and_insert_tags(quote_count,insert_tag,tags_list):
    
    for each_tag in tags_list:
        string_format = insert_tag.format(each_tag,quote_count)
        inserting_data_into_table(string_format)


quotes_authors_obj = get_json_data()
quotes_list = get_list_from_quotes_authors_obj(quotes_authors_obj,"quotes")
authors_new_list = get_list_from_quotes_authors_obj(quotes_authors_obj,"authors")

author_names_list = distinct_author_names_list(authors_new_list)

quotes_table='''
        CREATE TABLE quotes(
            id INTEGER NOT NULL PRIMARY KEY,
            quote VARCHAR,
            author_name VARCHAR(250),
            no_of_tags INTEGER,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id) 
            ON DELETE CASCADE
            );
            '''
authors_table='''
        CREATE TABLE authors(
            id INTEGER NOT NULL PRIMARY KEY,
            author_name VARCHAR(250),
            born VARCHAR(200),
            reference VARCHAR(250)
            );
            '''
tags_table = '''
        CREATE TABLE tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name VARCHAR(250),
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
insert_quotes = '''
    INSERT INTO 
        quotes(id,quote,author_name,no_of_tags,author_id)
    VALUES(
        {},
       """{}""",
       "{}",
        {},
        {}
    );
'''
insert_tags = '''
    INSERT INTO 
        tags(tag_name,quote_id)
    VALUES(
    "{}",
     {}
    );
'''

id_count = 0
for each_item in authors_new_list:
    id_count+=1
    get_and_insert_author(id_count,each_item,insert_author)
    

id_count=0
for each_item in quotes_list:
    id_count+=1
    get_and_insert_quotes(id_count,each_item,insert_quotes)
    get_and_insert_tags(id_count,insert_tags,each_item['tags'])
    

print("Data created and Inserted into quotes.db")