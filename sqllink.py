# This is the backend of the application. Here all data creation and manipulation inside the databes takes place.

#Following are the packages used
import sqlite3 as s3
from sqlite3 import OperationalError
import random as ran
import pandas as pd
from datetime import datetime

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
    members_obj = con.execute("Select member_id, fName || ' ' || lName as 'Full Name', mobile_no, email, address from members;")
    memebrs = []
    for row in members_obj:
        memebrs.append(row)
    con.close()
    return memebrs

def member_reg(fName, lName, mobileno, email, address):
    member_id = fName[0:2]+lName[0]+'-'+str(ran.randint(1000,9999))
    con = check_table()
    con.execute("INSERT INTO members (member_id, fName, lName, mobile_no, email,  address) \
                    VALUES ('"+member_id+"','"+fName+"','"+lName+"','"+mobileno+"','"+email+"','"+address+"');")
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

def delete_allm():
    con = check_table()
    con.execute('Delete from members;')
    con.commit()
    con.close()
    return True

def export_members(export_file_path):
    con = check_table()
    dict_books = {'Member ID': [], 'First Name': [], 'Last Name': [], 'Mobile': [], 'E-mail': [], 'Address': []}
    rows = con.execute('Select * from members;')
    for row in rows:
        dict_books['Member ID'].append(row[0])
        dict_books['First Name'].append(row[1])
        dict_books['Last Name'].append(row[2])
        dict_books['Mobile'].append(row[3])
        dict_books['E-mail'].append(row[4])
        dict_books['Address'].append(row[5])
    df = pd.DataFrame(dict_books, columns = ['Member ID', 'First Name', 'Last Name', 'Mobile', 'E-mail', 'Address'])
    df.to_excel(export_file_path, index=False, header=True)
    con.close()

def get_issue_details():
    book_id,books = get_avail_book_details()
    member_id,members = get_del_member_details()
    return book_id, books, member_id, members

def get_avail_book_details():
    con = check_table()
    con = check_table()
    books_del_obj = con.execute('Select book_id,book_name from book\
                                    where availability = "Available";')
    books = {}
    book_id = []
    for row in books_del_obj:
        books[row[0]] = row[1]
        book_id.append(row[0])
    con.close()
    return book_id, books
 
def issue_book(member_id, book_id, duration):
    con = check_table()
    avail = 'Issued'
    con.execute("INSERT INTO book_status(book_id, member_id, issue_date, return_date, availability)\
                    VALUES('"+book_id+"','"+member_id+"', date('now','localtime'), date('now','localtime','+"+duration+" days'), '"+avail+"');")
    con.commit()
    con.execute('Update book set availability = "Issued"\
                    where book_id = "'+book_id+'";')
    con.commit()
    con.close()
    write_to_records(member_id, book_id, duration)
    return True

def get_return_date(member_id,book_id):
    con = check_table()
    dates = con.execute("Select return_date from book_status\
                            where member_id = '"+member_id+"' and book_id = '"+book_id+"';")
    date = ""
    for row in dates:
        date = row[0]
    return date


def get_return_date_details(member_id,book_id):
    con = check_table()
    dates = con.execute("Select return_date from book_status\
                            where member_id = '"+member_id+"' and book_id = '"+book_id+"';")
    return_date_str = ""
    for row in dates:
        return_date_str = row[0]
    return_date = datetime.strptime(return_date_str,"%Y-%m-%d")
    now_date = datetime.now()
    difference = return_date - now_date
    if difference.days > 0:
        due = "before"
    elif difference.days < 0:
        due = "after"
    else:
        due = "on"
    return difference.days,due,return_date_str

def get_return_details():
    con = check_table()
    member_id = []
    book_id = []
    members = {}
    books = {}
    members_obj = con.execute('Select bs.member_id, m.fName || " " ||  m.lName as "Full Name" from book_status bs inner join members m \
                                using(member_id);')
    for row in members_obj:
        members[row[0]]=row[1]
        member_id.append(row[0])
    books_obj = con.execute('Select bs.book_id, b.book_name from book_status bs inner join book b\
                                using(book_id);')
    for row in books_obj:
        books[row[0]]=row[1]
        book_id.append(row[0])
    con.close()
    return member_id, members, book_id, books

def update_return_book_details(book_id, member_id):
    con = check_table()
    con.execute('Update book set availability = "Available" where book_id = "'+book_id+'";')
    con.commit()
    con.execute('Delete from book_status where member_id = "'+member_id+'" and book_id = "'+book_id+'";')
    con.commit()
    con.close()
    return True

def get_issued_book_details():
    con = check_table()
    issue_book_obj = con.execute('''Select book_status.book_id, book.book_name, members.fName || " " || members.lName as "Full Name", book_status.issue_date, book_status.return_date
                                    from book_status left join book using(book_id)
                                    left join members using(member_id);''')
    issue_book_details = []
    for row in issue_book_obj:
            issue_book_details.append(row)
    con.close()
    return issue_book_details

def export_stats(export_file_path):
    dict_stats = {'Book ID': [], 'Book Name': [], 'Member Name': [], 'Issue Date': [], 'Return Date': []}
    rows = get_issued_book_details()
    for row in rows:
        dict_stats['Book ID'].append(row[0])
        dict_stats['Book Name'].append(row[1])
        dict_stats['Member Name'].append(row[2])
        dict_stats['Issue Date'].append(row[3])
        dict_stats['Return Date'].append(row[4])
    df = pd.DataFrame(dict_stats, columns = ['Book ID', 'Book Name', 'Member Name', 'Issue Date', 'Return Date'])
    df.to_excel(export_file_path, index=False, header=True)

def write_to_records(member_id,book_id,duration):
    conn = check_table()
    con = check_records()
    mem = conn.execute('Select fName || " " || lName as "Full Name" from members\
                            where member_id = "'+member_id+'";')
    member_name = ""
    for row in mem:
        member_name = row[0]
    bname = conn.execute('Select book_name from book\
                            where book_id = "'+book_id+'";')
    book_name = ""
    for row in bname:
        book_name = row[0]
    con.execute("Insert into records(book_id,book_name,member_id,member_name,issue_date,return_date)\
                    values('"+book_id+"','"+book_name+"','"+member_id+"','"+member_name+"', date('now','localtime'), date('now','localtime','+"+duration+" days'));")
    con.commit()
    con.close()
    conn.close()

def get_record_details():
    con = check_records()
    rec_obj = con.execute('Select book_id,book_name,member_id,member_name,issue_date,return_date from records;')
    records = []
    for row in rec_obj:
        records.append(row)
    con.close()
    return records

def export_records(export_file_path):
    con = check_records()
    dict_records = {'Record ID': [],'Book ID': [], 'Book Name': [],'Member ID': [], 'Member Name': [], 'Issue Date': [], 'Return Date': []}
    rows = con.execute('Select * from records;')
    for row in rows:
        dict_records['Record ID'].append(row[0])
        dict_records['Book ID'].append(row[1])
        dict_records['Book Name'].append(row[2])
        dict_records['Member ID'].append(row[3])
        dict_records['Member Name'].append(row[4])
        dict_records['Issue Date'].append(row[5])
        dict_records['Return Date'].append(row[6])
    df = pd.DataFrame(dict_records, columns = ['Record ID','Book ID', 'Book Name', 'Member ID', 'Member Name', 'Issue Date', 'Return Date'])
    df.to_excel(export_file_path, index=False, header=True)

def check_records():
    try:
        con = s3.connect('databases/record.db')
        con.execute("""CREATE TABLE IF NOT EXISTS records(
                        record_id integer PRIMARY KEY AUTOINCREMENT,
                        book_id text NOT NULL,
                        book_name text NOT NULL,
                        member_id text NOT NULL,
                        member_name text NOT NULL,
                        issue_date text NOT NULL,
                        return_date text NOT NULL);""")
    except:
        print("No Databse found")
    else:
        return con

def check_table():
    try:
        conn = s3.connect('databases/library.db')
        conn.execute("""CREATE TABLE IF NOT EXISTS book(
                        book_id	text NOT NULL,
	                    book_name	text NOT NULL,
	                    book_author	text NOT NULL,
	                    isbn	text NOT NULL,
	                    price	real NOT NULL,
	                    availability text NOT NULL DEFAULT 'Available',
	                    PRIMARY KEY(book_id));""")
        conn.execute("""CREATE TABLE IF NOT EXISTS members(
                        member_id text NOT NULL,
                        fName text NOT NULL,
                        lName text NOT NULL,
                        mobile_no text NOT NULL,
                        email text,
                        address text,
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
conn=check_records()
#cur = con.execute("SELECT * FROM book;")
#cur = get_member_details()
#cur = get_return_date('PrS-2910','TH-ST-97-238')
#print(cur)