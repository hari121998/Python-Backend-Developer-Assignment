import sqlite3

def start_connection_with_database():
    return sqlite3.connect("quotes.db")

def get_query_from_table(table_query):

    connection = start_connection_with_database()
    cursor_object = connection.cursor()
    cursor_object.execute(table_query)
    result = cursor_object.fetchall()
    connection.commit()
    connection.close()
    print(result)

def create_query_for_number_of_quotations():
    return '''
    SELECT 
        COUNT() as total_no_of_quotations
    FROM 
        quotes;
    '''
def create_query_for_authors_number_of_quotations():
    word = input("please enter the valid authors name: ").lower()
    query= '''
    SELECT 
        author_name,
        COUNT() as total_no_of_quotations
    FROM 
        quotes INNER JOIN authors 
        ON quotes.author_id = authors.id
        
    WHERE 
        LOWER(authors.author_name) = '{}'
    GROUP BY 
        author_id;
    '''
    string_query = query.format(word)
    return string_query

def create_query_for_min_max_avg_tags():
    return '''
    SELECT
        MAX(total_tags) as maximum_tags,
        MIN(total_tags) as minimum_tags,
        AVG(total_tags) as average_tags
        
    FROM (SELECT    
            COUNT(tag_name) as total_tags 
        FROM 
            tags
        GROUP BY
            quote_id
        ORDER BY 
            total_tags DESC);
    '''
def create_query_for_maximum_number_of_authors_on_quotations():
    number = input("Please Enter the Number of highest authors on quotations: ")
    query =  '''
    SELECT 
        author_id,
        author_name,
        COUNT() as no_of_quotes
    FROM 
        quotes INNER JOIN authors
        ON quotes.author_id = authors.id
    GROUP BY 
        author_id
    ORDER BY 
        no_of_quotes DESC
    LIMIT {}
    '''
    string_query = query.format(number)
    return string_query
total_number_of_quotations = create_query_for_number_of_quotations()

number_of_quotations_authored = create_query_for_authors_number_of_quotations()

maximum_minimum_average_of_tags = create_query_for_min_max_avg_tags()

top_n_authors_on_total_quotaions=create_query_for_maximum_number_of_authors_on_quotations()

get_query_from_table(total_number_of_quotations)
get_query_from_table(number_of_quotations_authored)
get_query_from_table(maximum_minimum_average_of_tags)
get_query_from_table(top_n_authors_on_total_quotaions)