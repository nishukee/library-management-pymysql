import sqlite3 as s3
from sqlite3 import OperationalError
import random as ran
import pandas as pd

def add_book_sql(book_name,book_author,book_isbn,book_price):
    con = check_table()
    book_id = book_name[0:2].upper()+"-"+book_author[0:2].upper()+"-"+book_isbn[0:2]+"-"+str(ran.randint(100,999))
    con.execute("INSERT INTO book (book_id,book_name,book_author,isbn,price) \
                    VALUES ('"+book_id+"','"+book_name+"','"+book_author+"','"+book_isbn+"',"+book_price+");")
    con.commit()
    con.close()
    return True

def get_book_details():
    con = check_table()
    books_obj = con.execute('Select * from book;')
    books = []
    for row in books_obj:
        books.append(row)
    con.close()
    return books

def get_del_book_details():
    con = check_table()
    books_del_obj = con.execute('Select book_id,book_name from book;')
    books = {}
    book_id = []
    for row in books_del_obj:
        books[row[0]] = row[1]
        book_id.append(row[0])
    con.close()
    return book_id, books

def delete_book(book_id_str):
    con = check_table()
    try:
        con.execute("Delete from book where book_id = '"+book_id_str+"';")
        con.commit()
        con.close()
        return True
    except OperationalError:
        con.close()
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
    con.close()

def delete_all():
    con = check_table()
    con.execute('Delete from book;')
    con.commit()
    con.close()
    return True

def get_member_details():
    con = check_table()
    members_obj = con.execute('Select * from members;')
    memebrs = []
    for row in members_obj:
        memebrs.append(row)
    con.close()
    return memebrs

def member_reg(fName, lName, mobileno, address, email):
    member_id = fName[0:2]+lName[0]+'-'+str(ran.randint(1000,9999))
    con = check_table()
    con.execute("INSERT INTO members (member_id, fName, lName, mobile_no, address, email) \
                    VALUES ('"+member_id+"','"+fName+"','"+lName+"','"+mobileno+"','"+address+"','"+email+"');")
    con.commit()
    con.close()
    return True

def get_del_member_details():
    con = check_table()
    members_obj = con.execute('Select member_id, fName, lName from members;')
    members = {}
    member_id = []
    for row in members_obj:
        members[row[0]]=row[1]+' '+row[2]
        member_id.append(row[0])
    con.close()
    return member_id, members

def delete_member(member_id_str):
    con = check_table()
    try:
        con.execute('Delete from members where member_id = "'+member_id_str+'";')
        con.commit()
        con.close()
        return True
    except OperationalError:
        return False

def get_issue_details():
    book_id,books = get_del_book_details()
    member_id,members = get_del_member_details()
    return book_id, books, member_id, members

def issue_book(book_id, member_id):
    con = check_table()
    avail = 'Issued'
    con.execute("INSERT INTO book_status(book_id, member_id, issue_date, return_date, availability)\
                    VALUES('"+book_id+"','"+member_id+"', date('now','localtime'), date('now','localtime','+15 days'), '"+avail+"');")
    con.commit()
    con.close()
    return True

def get_return_details():
    con = check_table()
    member_id = []
    members = {}
    members_obj = con.execute('Select bs.member_id, m.fName, m.lName from book_status bs inner join members m \
                                using(member_id);')
    for row in members_obj:
        members[row[0]]=row[1]+' '+row[2]
        member_id.append(row[0])
    con.close()
    return member_id, members

def update_return_book_details(book_id, member_id):
    con = check_table()
    con.execute('Update books set availability = "Available" where book_id = "'+book_id+'";')
    con.execute('Delete from book_status where member_id = "'+member_id+'" and book_id = "'+book_id+'";')
    return True

def get_issued_book_details():
    con = check_table()
    issue_book_obj = con.execute('''Select book_status.book_id, book.book_name, members.fName, members.lName, book_status.issue_date, book_status.return_date
                                    from book_status left join book using(book_id)
                                    left join members using(member_id);''')
    issue_book_details = []
    for row in issue_book_obj:
            issue_book_details.append(row)
    con.close()
    return issue_book_details

def check_table():
    try:
        conn = s3.connect('library.db')
        conn.execute("""CREATE TABLE IF NOT EXISTS book(
                        book_id	text NOT NULL,
	                    book_name	text NOT NULL,
	                    book_author	text NOT NULL,
	                    isbn	text NOT NULL,
	                    price	real NOT NULL,
	                    availability text NOT NULL DEFAULT 'Available',
	                    PRIMARY KEY(book_id)
                        FOREIGN KEY(availability) REFERENCES book_status(availability) ON UPDATE CASCADE);""")
        conn.execute("""CREATE TABLE IF NOT EXISTS members(
                        member_id text NOT NULL,
                        fName text NOT NULL,
                        lName text NOT NULL,
                        mobile_no text NOT NULL,
                        address text,
                        email text,
                        PRIMARY KEY(member_id));""")
        conn.execute("""CREATE TABLE IF NOT EXISTS book_status(
                        book_id text NOT NULL,
                        member_id text NOT NULL,
                        issue_date text NOT NULL,
                        return_date text NOT NULL,
                        availability text NOT NULL,
                        FOREIGN KEY(book_id) REFERENCES book(book_id),
                        FOREIGN KEY(member_id) REFERENCES members(member_id));""")
    except:
        print("No database found")
    else:
        return conn
con=check_table()
cur = con.execute("SELECT * FROM book;")
for row in cur:
    print(row)
con.close()