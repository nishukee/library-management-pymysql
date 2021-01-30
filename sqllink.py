import sqlite3 as s3
from sqlite3 import OperationalError
import random as ran
import pandas as pd

def add_book_sql(book_name,book_author,book_isbn,book_price):
    con = check_table()
    book_id = book_name[0:2].upper()+"-"+book_author[0:2].upper()+"-"+book_isbn[0:2]+"-"+str(ran.randint(100,999))
    con.execute("INSERT INTO book (book_id,book_name,book_author,isbn,price) \
                    VALUES ('"+book_id+"',"+"'"+book_name+"','"+book_author+"','"+book_isbn+"',"+book_price+");")
    con.commit()
    con.close()
    return True

def get_book_details():
    con = check_table()
    books_obj = con.execute('Select * from book;')
    books = []
    for row in books_obj:
        books.append(row)
    return books

def get_del_book_details():
    con = check_table()
    books_del_obj = con.execute('Select book_id,book_name from book;')
    del_books = {}
    del_book_id = []
    for row in books_del_obj:
        del_books[row[0]] = row[1]
        del_book_id.append(row[0])
    return del_book_id, del_books

def delete_book(book_id_str):
    con = check_table()
    try:
        con.execute("Delete from book where book_id = '"+book_id_str+"';")
        con.commit()
        return True
    except OperationalError:
        return False

def export_books(export_file_path):
    con = check_table()
    dict_books = {'Book ID': [], 'Book Name': [], 'Author': [], 'ISBN': [], 'Price': [], 'Availability': []}
    rows = con.execute('Select * from book;')
    for row in rows:
        dict_books['Book ID'].append(row[0])
        dict_books['Book Name'].append(row[1])
        dict_books['Author'].append(row[2])
        dict_books['ISBN'].append(row[3])
        dict_books['Price'].append(row[4])
        dict_books['Availability'].append(row[5])
    df = pd.DataFrame(dict_books, columns = ['Book ID', 'Book Name', 'Author', 'ISBN', 'Price', 'Availability'])
    df.to_excel(export_file_path, index=False, header=True)

def delete_all():
    con = check_table()
    con.execute('Delete from book;')
    con.commit()
    return True

def check_table():
    try:
        conn = s3.connect('library.db')
        conn.execute("""CREATE TABLE IF NOT EXISTS book(
                        book_id	text NOT NULL,
	                    book_name	text NOT NULL,
	                    book_author	text NOT NULL,
	                    isbn	text NOT NULL,
	                    price	real NOT NULL,
	                    status	text NOT NULL DEFAULT 'Available',
	                    PRIMARY KEY(book_id));""")
    except:
        print("No database found")
    else:
        return conn
con=check_table()
cur = con.execute("SELECT * FROM book;")
for row in cur:
    print(row)
con.close()