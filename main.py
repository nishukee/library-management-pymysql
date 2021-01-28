import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import sqllink as sql3

class Book_Register:

    def declare_book_reg_widgets(self):
        self.breg = tk.Tk()
        self.breg.title('Book Register')
        self.breg.resizable(False, False)
        #Add Book widgets
        self.add_book_frame = tk.Frame(self.breg, bg='#7a3b0b')
        self.book_name_lbl = tk.Label(self.add_book_frame, text="Book Name", bg='#7a3b0b', font=('FreeSans',14))
        self.book_author_lbl = tk.Label(self.add_book_frame, text="Author", bg='#7a3b0b', font=('FreeSans',14))
        self.book_isbn_lbl = tk.Label(self.add_book_frame, text="ISBN", bg='#7a3b0b', font=('FreeSans',14))
        self.book_price_lbl = tk.Label(self.add_book_frame, text="Price", bg='#7a3b0b', font=('FreeSans',14))
        self.book_name = ""
        self.book_name_entry = tk.Entry(self.add_book_frame, bg='#4a2910')
        self.author = ""
        self.book_author_entry = tk.Entry(self.add_book_frame, bg='#4a2910')
        self.isbn = ""
        self.book_isbn_entry = tk.Entry(self.add_book_frame, bg='#4a2910')
        self.price = ""
        self.book_price_entry = tk.Entry(self.add_book_frame, bg='#4a2910')
        self.submit_btn = tk.Button(self.add_book_frame, text="Submit",command=self.book_to_database, bg='#512202', activebackground='#4a2910')
        self.quit_breg_btn = tk.Button(self.add_book_frame, text="Quit", command=self.breg.destroy, bg='#512202', activebackground='red')

    #Methods for regisering book to database

    def add_book_window(self):
        self.declare_book_reg_widgets()
        self.breg.lift()
        self.add_book_frame.grid(row=0, column=0, sticky='nsew')
        self.book_name_lbl.grid(row=2, column=1, ipadx=3)
        self.book_author_lbl.grid(row=3,column=1, ipadx=3)
        self.book_isbn_lbl.grid(row=4,column=1, ipadx=3)
        self.book_price_lbl.grid(row=5,column=1, ipadx=3)
        self.book_name_entry.grid(row=2, column=3, ipadx=40)
        self.book_author_entry.grid(row=3, column=3, ipadx=40)
        self.book_isbn_entry.grid(row=4, column=3, ipadx=40)
        self.book_price_entry.grid(row=5, column=3, ipadx=40)
        self.submit_btn.grid(row=7, column=2, sticky='s')
        self.quit_breg_btn.grid(row=7, column=3, sticky='s')

    def book_to_database(self):
        self.book_name = self.book_name_entry.get()
        self.author = self.book_author_entry.get()
        self.isbn = self.book_isbn_entry.get()
        self.price = self.book_price_entry.get()
        messagebox.showinfo("Connecting to Database","Writing Book Details to Database")
        if (len(self.book_name_entry.get())==0 or len(self.book_author_entry.get())==0 or len(self.book_isbn_entry.get())==0 or len(self.book_price_entry.get())==0):
            messagebox.showerror("Value Error","Please Enter All Values")
        elif (sql3.add_book_sql(self.book_name,self.author,self.isbn,self.price)):
            messagebox.showinfo("SQL Connected","Data Inserted Succesfully!")
        else:
            messagebox.showerror("Connection Unsuccesful","Database not found")
        self.clear_entry()
    
    def clear_entry(self):
        self.book_name_entry.delete(0,tk.END)
        self.book_author_entry.delete(0,tk.END)
        self.book_isbn_entry.delete(0,tk.END)
        self.book_price_entry.delete(0,tk.END)
        self.breg.destroy()
        self.add_book_window()


class Book_View:

    def declare_view_widgets(self):
        self.bview = tk.Tk()
        self.bview.title('Books Table')
        self.bview.resizable(False, False)
         #View Book widgets
        self.view_book_frame = tk.Frame(self.bview)
        self.cols = ('Book ID','Book Name','Author','ISBN','Price','Status')
        self.list_books = ttk.Treeview(self.view_book_frame, columns=self.cols, show='headings', selectmode='browse')
        self.verscrlbar = ttk.Scrollbar(self.view_book_frame, orient=tk.VERTICAL,command=self.list_books.yview)
        self.quit_view_btn = tk.Button(self.view_book_frame, text="Quit View", command=self.bview.destroy)
        for self.col in self.cols:
            self.list_books.heading(self.col, text=self.col)
        self.book_details = []
        self.index = self.iid = 0
    
        #Methods for Viewing Book List

    def view_book_window(self):
        self.declare_view_widgets()
        self.bview.lift()
        self.book_details = sql3.get_book_details()
        self.view_book_frame.grid(row=0, column=0, sticky='nsew')
        self.list_books.grid(row=1, column=1, columnspan=6)
        for self.i in self.list_books.get_children():
            self.list_books.delete(self.i)
        for self.row in self.book_details:
            self.list_books.insert('',self.index,self.iid,values=self.row)
            self.index = self.iid = self.index + 1
        self.verscrlbar.grid(row=1,column=0, sticky='ns')
        self.list_books.configure(yscrollcommand = self.verscrlbar.set)
        self.quit_view_btn.grid(row=4,column=3)

class Book_Delete:
    def declare_book_delete_widgets(self):
        self.bdel = tk.Tk()
        self.bdel.title('Delete Books')
        self.bdel.resizable(False, False)
        self.retrieve_books()
        self.book_delete_frame = tk.Frame(self.bdel)
        self.book_id_str = tk.StringVar()
        self.combo_box = ttk.Combobox(self.book_delete_frame, width=27, textvariable = self.book_id_str, values=self.bookids)
        self.combo_box.set('Pick Book ID')
        self.book_name_str = tk.StringVar()
        self.del_book_entry = tk.Entry(self.book_delete_frame, textvariable=self.book_name_str)
        self.del_book_entry.insert(0, 'Book Name')
        self.chk_book_btn = tk.Button(self.book_delete_frame, text="Check Book Name", command=self.check_book)
        self.del_btn = tk.Button(self.book_delete_frame, text="Delete", command=self.book_delete)
        self.quit_del_btn = tk.Button(self.book_delete_frame, text="Quit", command=self.bdel.destroy)
    
    def retrieve_books(self):
        self.bookids, self.bookdict = sql3.get_del_book_details()
    
    def delete_book_window(self):
        self.declare_book_delete_widgets()
        self.bdel.lift()
        self.book_delete_frame.grid(row=0, column=0)
        self.combo_box.grid(row=2, column=1)
        self.del_book_entry.grid(row=2, column=3)
        self.chk_book_btn.grid(row=4, column=2)
        self.del_btn.grid(row=4, column=3)
        self.quit_del_btn.grid(row=4, column=4)

    def check_book(self):
        if self.combo_box.get()=='Pick Book ID':
            messagebox.showwarning('Value not selected','Select Book ID')
        else :
            self.book_id_str = self.combo_box.get()
            self.book_name_str = self.bookdict[self.book_id_str]
            self.del_book_entry.delete(0, tk.END)
            self.del_book_entry.insert(0, self.book_name_str)
        
    def book_delete(self):
        messagebox.showinfo("Connecting to Database","Deleting Book")
        if sql3.delete_book(self.book_id_str)==True:
            messagebox.showinfo('Connection Succesful','Book Deleted')
            del self.bookdict[self.book_id_str]
            self.bdel.destroy()
            self.delete_book_window()
        else:
            messagebox.showerror('Connection Unsuccesful','Book not deleted')

class MainWindow:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Library')
        self.parent.resizable(False, False)
        self.bg_image = Image.open('Book_shelf.png')
        self.bg_image = self.bg_image.resize((600,300), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.bg_image)
        self.main_frame = tk.Frame(parent)
        self.bg_img_lbl = tk.Label(image=self.img)
        self.menuBar = tk.Menu(self.parent, bg='#75421d', activebackground='#7a3b0b')
        self.parent.config(menu=self.menuBar)

        self.bookOp_menu = tk.Menu(self.menuBar, bg='#4a2910', activebackground='#663109')
        self.menuBar.add_cascade(label="Books", menu=self.bookOp_menu)
        self.bookOp_menu.add_command(label="Register Books to Database", command=self.add_book)
        self.bookOp_menu.add_command(label="View Book List", command=self.view_book)
        self.bookOp_menu.add_command(label="Delete Books from Database", command=self.delete_book)
        self.bookOp_menu.add_command(label="Book Status")

        self.bookIsR_menu = tk.Menu(self.menuBar, bg='#4a2910', activebackground='#663109')
        self.menuBar.add_cascade(label="Book Issue/Return", menu=self.bookIsR_menu)
        self.bookIsR_menu.add_command(label="Issue Books")
        self.bookIsR_menu.add_command(label="Return Books")

        self.bookMembers_menu = tk.Menu(self.menuBar, bg='#4a2910', activebackground='#663109')
        self.menuBar.add_cascade(label="Library Members", menu=self.bookMembers_menu)
        self.bookMembers_menu.add_command(label="Register New Member")
        self.bookMembers_menu.add_command(label="Delete Registered Member")

        self.quit_btn = tk.Menu(self.menuBar, bg='#4a2910', activebackground='red')
        self.menuBar.add_cascade(label="Quit", menu=self.quit_btn)
        self.quit_btn.add_command(label="Exit Program", command=quit)
        self.book_reg = Book_Register()
        self.book_view = Book_View()
        self.book_del = Book_Delete()
    
    def main_window(self):

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.bg_img_lbl.place(anchor='nw')

    def add_book(self):
        self.book_reg.add_book_window()
    
    def view_book(self):
        self.book_view.view_book_window()
    
    def delete_book(self):
        self.book_del.delete_book_window()


def main():
    root = tk.Tk()
    root.geometry('600x300')
    root.configure(background='#301806')
    app = MainWindow(root)
    app.main_window()
    root.mainloop()


if __name__ == '__main__':
    main()
