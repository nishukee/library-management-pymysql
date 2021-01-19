import sqlite3 as s3

def add_book_sql(book_name,book_author,book_isbn,book_price):
    con = check_table()
    con.execute("INSERT INTO book (book_name,book_author,isbn,price) \
                    VALUES ('"+book_name+"','"+book_author+"','"+book_isbn+"',"+book_price+");")
    con.commit()
    con.close()
    return True
    

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
    except:
        print("No database found")
    else:
        return conn
con=check_table()
cur = con.execute("SELECT * FROM book;")
for row in cur:
    print(row)
con.close()