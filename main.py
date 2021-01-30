import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from tkinter import ttk
from PIL import ImageTk, Image
import sqllink as sql3

class Book_Register:

    def declare_book_reg_widgets(self):
        self.breg = tk.Tk()
        self.breg.title('Book Register')
        self.breg.resizable(False, False)
        #Add Book widgets
        self.widget_styles()
        self.add_book_frame = ttk.Frame(self.breg)
        self.book_name_lbl = ttk.Label(self.add_book_frame, text="Book Name")
        self.book_author_lbl = ttk.Label(self.add_book_frame, text="Author")
        self.book_isbn_lbl = ttk.Label(self.add_book_frame, text="ISBN")
        self.book_price_lbl = ttk.Label(self.add_book_frame, text="Price")
        self.book_name = ""
        self.book_name_entry = ttk.Entry(self.add_book_frame)
        self.author = ""
        self.book_author_entry = ttk.Entry(self.add_book_frame)
        self.isbn = ""
        self.book_isbn_entry = ttk.Entry(self.add_book_frame)
        self.price = ""
        self.book_price_entry = ttk.Entry(self.add_book_frame)
        self.submit_btn = ttk.Button(self.add_book_frame, text="Submit",command=self.book_to_database)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_breg_btn = ttk.Button(self.add_book_frame, text="Quit", command=self.breg.destroy, style='quitbtn.TButton')

    #Methods for regisering book to database
    def widget_styles(self):
        self.s = ttk.Style(self.breg)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TLabel',foreground='snow',background='#70340c', font=('FreeSans',14))
        self.s.configure('TEntry', background='white', foreground='black')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])

    def add_book_window(self):
        self.declare_book_reg_widgets()
        self.add_book_frame.grid(row=0, column=0, sticky='nsew', ipadx=5, ipady=5)
        self.book_name_lbl.grid(row=2, column=1, ipadx=3, padx=5)
        self.book_author_lbl.grid(row=3,column=1, ipadx=3, padx=5)
        self.book_isbn_lbl.grid(row=4,column=1, ipadx=3, padx=5)
        self.book_price_lbl.grid(row=5,column=1, ipadx=3, padx=5)
        self.book_name_entry.grid(row=2, column=3, ipadx=40, pady=10)
        self.book_author_entry.grid(row=3, column=3, ipadx=40, pady=10)
        self.book_isbn_entry.grid(row=4, column=3, ipadx=40, pady=10)
        self.book_price_entry.grid(row=5, column=3, ipadx=40, pady=10)
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
        self.refresh_window_breg()

    def refresh_window_breg(self):    
        self.breg.destroy()
        self.add_book_window()
        self.breg.lift()


class Book_View:

    def declare_view_widgets(self):
        self.bview = tk.Tk()
        self.bview.title('Books Table')
        self.bview.resizable(False, False)
         #View Book widgets
        self.widget_styles()
        self.view_book_frame = ttk.Frame(self.bview)
        self.cols = ('Book ID','Book Name','Author','ISBN','Price','Status')
        self.list_books = ttk.Treeview(self.view_book_frame, columns=self.cols, show='headings', selectmode='browse')
        for self.col in self.cols:
            self.list_books.heading(self.col, text=self.col)
        self.verscrlbar = ttk.Scrollbar(self.view_book_frame, orient=tk.VERTICAL, command=self.list_books.yview)
        self.export_btn = ttk.Button(self.view_book_frame, text="Export to Excel", command=self.export_to_excel)
        self.quit_view_btn = ttk.Button(self.view_book_frame, text="Quit View", command=self.bview.destroy)
        self.book_details = []
        self.index = self.iid = 0
    
        #Methods for Viewing Book List
    def widget_styles(self):
        self.s = ttk.Style(self.bview)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('Treeview', background='#894b10', foreground='white', fieldbackground="#894b10")
        self.s.configure('TScrollbar',background='#70340c', foreground='white')
        self.s.map('TScollbar',background=[('pressed','white')])
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#70340c'),('pressed','"#894b10')])
        self.s.configure('.', background='#70340c', foreground='white')

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
        self.export_btn.grid(row=3, column=2, columnspan=2, padx=20, pady=5)
        self.quit_view_btn.grid(row=3,column=4,columnspan=2, padx=20, pady=5)
    
    def refresh_window_bview(self):
        self.bview.destroy()
        self.view_book_window()
        self.bview.lift()

    def export_to_excel(self):
        self.export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        sql3.export_books(self.export_file_path)
        self.refresh_window_bview()

class Book_Delete:
    def declare_book_delete_widgets(self):
        self.bdel = tk.Tk()
        self.bdel.title('Delete Books')
        self.bdel.resizable(False, False)
        self.retrieve_books()
        self.widget_styles()
        self.book_delete_frame = ttk.Frame(self.bdel)
        self.book_id_str = tk.StringVar()
        self.combo_box = ttk.Combobox(self.book_delete_frame, width=27, textvariable = self.book_id_str, values=self.bookids)
        self.combo_box.set('Pick Book ID')
        self.combo_box.bind("<<ComboboxSelected>>",self.check_book)
        self.book_name_str = tk.StringVar()
        self.del_book_entry = ttk.Entry(self.book_delete_frame, textvariable=self.book_name_str)
        self.del_book_entry.insert(0, 'Book Name')
        self.del_btn = ttk.Button(self.book_delete_frame, text="Delete", command=self.book_delete)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.del_all_btn = ttk.Button(self.book_delete_frame, text="Delete All Books", command=self.delete_all_books)
        self.quit_del_btn = ttk.Button(self.book_delete_frame, text="Quit", command=self.bdel.destroy, style='quitbtn.TButton')
    
    def widget_styles(self):
        self.s = ttk.Style(self.bdel)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TCombobox', background="#894b10", foreground='white')
        self.s.map('TCombobox',background=[('active','#a5570e'),('pressed','#70340c')])
        self.s.configure('TEntry', background='white', foreground='black')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])

    def retrieve_books(self):
        self.bookids, self.bookdict = sql3.get_del_book_details()
    
    def delete_book_window(self):
        self.declare_book_delete_widgets()
        self.book_delete_frame.grid(row=0, column=0, ipadx=10)
        self.combo_box.grid(row=2, column=0, padx=10, pady=20)
        self.del_book_entry.grid(row=2, column=1, pady=20, padx=15)
        self.del_btn.grid(row=2, column=3)
        self.quit_del_btn.grid(row=4, column=0,columnspan=2, padx=50)
        self.del_all_btn.grid(row=4, column=3)
            
    def check_book(self, event):
        if self.combo_box.get()!='Pick Book ID':
            self.book_id_str = self.combo_box.get()
            self.book_name_str = self.bookdict[self.book_id_str]
            self.del_book_entry.delete(0, tk.END)
            self.del_book_entry.insert(0, self.book_name_str)

    def book_delete(self):
        if self.combo_box.get()=='Pick Book ID':
            messagebox.showwarning('Value not selected','Select Book ID')
        else:
            messagebox.showinfo("Connecting to Database","Deleting Book")
            if sql3.delete_book(self.book_id_str)==True:
                messagebox.showinfo('Connection Succesful','Book Deleted')
                del self.bookdict[self.book_id_str]
            else:
                messagebox.showerror('Connection Unsuccesful','Database is locked')
        self.refresh_window_bdel()

    def refresh_window_bdel(self):
        self.bdel.destroy()
        self.delete_book_window()
        self.bdel.lift()
    
    def delete_all_books(self):
        if messagebox.askyesno('Deleting all Records','Are you sure you want to proceed?'):
            if sql3.delete_all():
                messagebox.showinfo('Deleted Records','All records deleted successfully')
            else:
                messagebox.showerror('Deletion Unsuccessful','Could not delete records')
        self.refresh_window_bdel()

class MainWindow:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Library')
        self.parent.resizable(False, False)
        self.s = ttk.Style(self.parent)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='#70340c', fieldbackground='#70340c')
        self.s.configure('.', background='#70340c', foreground='white')
        self.s.configure('TLabel', background='#70340c', foreground='white')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])
        self.bg_image = Image.open('Book_shelf.png')
        self.bg_image = self.bg_image.resize((600,300), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.bg_image)
        self.main_frame = ttk.Frame(parent)
        self.bg_img_lbl = ttk.Label(image=self.img)
        self.menuBar = tk.Menu(self.parent, bg='#5e220a', activebackground='#7a3b0b')
        self.parent.config(menu=self.menuBar)

        self.bookOp_menu = tk.Menu(self.menuBar, bg='#70340c', activebackground='#a5570e', tearoff=0)
        self.menuBar.add_cascade(label="Books", menu=self.bookOp_menu)
        self.bookOp_menu.add_command(label="Register Books to Database", command=self.add_book)
        self.bookOp_menu.add_command(label="View Book List", command=self.view_book)
        self.bookOp_menu.add_command(label="Delete Books from Database", command=self.delete_book)
        self.bookOp_menu.add_command(label="Book Status")

        self.bookIsR_menu = tk.Menu(self.menuBar, bg='#70340c', activebackground='#a5570e', tearoff=0)
        self.menuBar.add_cascade(label="Book Issue/Return", menu=self.bookIsR_menu)
        self.bookIsR_menu.add_command(label="Issue Books")
        self.bookIsR_menu.add_command(label="Return Books")

        self.bookMembers_menu = tk.Menu(self.menuBar, bg='#70340c', activebackground='#a5570e', tearoff=0)
        self.menuBar.add_cascade(label="Library Members", menu=self.bookMembers_menu)
        self.bookMembers_menu.add_command(label="Register New Member")
        self.bookMembers_menu.add_command(label="Delete Registered Member")

        self.quit_btn = tk.Menu(self.menuBar, bg='#70340c', activebackground='red', tearoff=0)
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
