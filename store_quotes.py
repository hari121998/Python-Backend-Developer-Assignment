import json 
import sqlite3

def get_json_data():
    with open('quotes.json','r') as read_file:
        object_file = json.loads(read_file.read())
    return object_file

def get_list_from_quotes_authors_obj(json_object,object_name):
    return json_object[object_name]

def distinct_author_names_list(author_list):
    author_name_list = []
    for each_name in author_list:
        if each_name['name'] not in author_name_list:
            author_name_list.append(each_name['name'])            
    return author_name_list

def connect_sqlite_to_database():
    return sqlite3.connect('quotes.db')

def create_table_in_database(table_statement,table_name):
    connection = connect_sqlite_to_database()
    cursor_object = connection.cursor()
    drop_sql = "DROP TABLE IF EXISTS {}"
    cursor_object.execute(drop_sql.format(table_name))
    cursor_object.execute('''PRAGMA foreign_keys = ON''')
    cursor_object.execute(table_statement)
    connection.close()

def create_and_get_quotes_table_statement():
    return '''
        CREATE TABLE quotes(
            id INTEGER NOT NULL PRIMARY KEY,
            quote VARCHAR,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id) 
            ON DELETE CASCADE
            );
            '''   

def create_and_get_authors_table_statement():
    return '''
        CREATE TABLE authors(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            author_name VARCHAR(250),
            born VARCHAR(200),
            reference VARCHAR(250)
            );
            '''
    
def create_and_get_tags_table_statement():
    return '''
        CREATE TABLE tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name VARCHAR(250),
            quote_id INTEGER,
            FOREIGN KEY (quote_id) REFERENCES quotes(id) 
            ON DELETE CASCADE
            );
            '''

def create_and_get_author_insert_statement():
    return '''
    INSERT INTO 
        authors(author_name,born,reference)
    VALUES(
        "{}",
        "{}",
        "{}"
    );
    '''
def create_and_get_quotes_insert_statement():
    return '''
    INSERT INTO 
        quotes(id,quote,author_id)
    VALUES(
        {},
       "{}",
        {}
    );
    '''
def create_and_get_tags_insert_statement():
    return '''
    INSERT INTO 
        tags(tag_name,quote_id)
    VALUES(
    "{}",
     {}
    );
    '''

def inserting_data_into_table(insert_table_query):
    connection  = connect_sqlite_to_database()
    cursor_obj = connection.cursor()
    cursor_obj.executescript(insert_table_query)
    connection.commit()
    connection.close()

def get_and_insert_author_into_database(each_author_row,insert_string):
    name = each_author_row['name']
    born = each_author_row['born']
    reference = each_author_row['reference']
    
    insert_data = insert_string.format(name,born,reference)
    inserting_data_into_table(insert_data)

def get_and_insert_quotes_into_database(id,each_row_quotes,insert_string):
    quote=each_row_quotes['quote'].strip('... ')   
    author_name = each_row_quotes['author']
    author_id = author_names_list.index(author_name)+1
    quotes_insert_data = insert_string.format(id,quote,author_id)

    inserting_data_into_table(quotes_insert_data)

def get_and_insert_tags_into_database(quote_count,insert_tag,each_tag_list):
    if len(each_tag_list)==0:
        string_format = insert_tag.format('',quote_count)
        inserting_data_into_table(string_format)
    for each_tag in each_tag_list:
        string_format = insert_tag.format(each_tag,quote_count)
        inserting_data_into_table(string_format)

quotes_authors_object = get_json_data()
quotes_list = get_list_from_quotes_authors_obj(quotes_authors_object,"quotes")
authors_new_list = get_list_from_quotes_authors_obj(quotes_authors_object,"authors")

author_names_list = distinct_author_names_list(authors_new_list)

quotes_create_statement = create_and_get_quotes_table_statement()
authors_create_statement = create_and_get_authors_table_statement()
tags_create_statement = create_and_get_tags_table_statement()

create_table_in_database(authors_create_statement,"authors")
create_table_in_database(quotes_create_statement,"quotes")
create_table_in_database(tags_create_statement,"tags")

author_insert_statement = create_and_get_author_insert_statement()
quotes_insert_statement = create_and_get_quotes_insert_statement()
tags_insert_statement = create_and_get_tags_insert_statement()

for each_row_item in authors_new_list:
    get_and_insert_author_into_database(each_row_item,author_insert_statement)
    
id_count=0
for each_row_item in quotes_list:
    id_count+=1
    get_and_insert_quotes_into_database(id_count,each_row_item,quotes_insert_statement)
    get_and_insert_tags_into_database(id_count,tags_insert_statement,each_row_item['tags'])
    
print("Data created and Inserted into quotes.db")