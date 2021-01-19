import sqlite3 as s3

def add_book_sql(book_name,book_author,book_isbn,book_price):
    con = check_table()
    

def check_table():
    try:
        conn = s3.connect('library.db')
        conn.execute("""CREATE TABLE IF NOT EXISTS book(
                        book_id	integer NOT NULL,
	                    book_name	text NOT NULL,
	                    book_author	text NOT NULL,
	                    isbn	text NOT NULL,
	                    price	real NOT NULL,
	                    status	text NOT NULL DEFAULT 'Available',
	                    PRIMARY KEY(book_id AUTOINCREMENT));""")
    except Error as e:
        print(e)
    else:
        return conn