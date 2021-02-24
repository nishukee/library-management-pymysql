# This is a library management program for keeping track of books being issued and returned to the library along with details of the books and library memebrs

# The following are the packages used in this application
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import ImageTk, Image
# This links to the backend of the program
import sqllink as sql3

# Below lies the functionalites of issueing/returning books to the library
#To Issue a book to member

class Issue:

    def declare_issue_widgets(self):
        self.iss = tk.Tk()
        self.iss.title('Issue Book')
        self.iss.resizable(False, False)
        self.iss.geometry("+120+50")
        self.widget_styles()
        self.retrieve_values()
        self.issue_frame = ttk.Frame(self.iss)
        self.member_id_str = tk.StringVar()
        self.mem_combobox = ttk.Combobox(self.issue_frame, width=17, textvariable=self.member_id_str, values=self.member_id)
        self.mem_combobox.set('Pick Member ID')
        self.mem_combobox.bind("<<ComboboxSelected>>", self.check_member)
        self.member_name_str = tk.StringVar()
        self.member_entry = ttk.Entry(self.issue_frame, textvariable=self.member_name_str)
        self.member_entry.insert(0, 'Member Name')
        self.book_id_str = tk.StringVar()
        self.book_combobox = ttk.Combobox(self.issue_frame, width=17, textvariable=self.book_id_str, values=self.book_id)
        self.book_combobox.set('Pick Book ID')
        self.book_combobox.bind("<<ComboboxSelected>>", self.check_book)
        self.book_name_str = tk.StringVar()
        self.book_entry = ttk.Entry(self.issue_frame, textvariable=self.book_name_str)
        self.book_entry.insert(0, 'Book Name')
        self.duration = tk.StringVar()
        self.duration_lbl = ttk.Label(self.issue_frame, text="Duration")
        self.duration_entry = ttk.Entry(self.issue_frame, textvariable=self.duration)
        self.duration_entry.insert(0, 'No. of Days')
        self.duration_entry.bind("<Button-1>", self.clear_entry)
        self.submit_btn = ttk.Button(self.issue_frame, text='Issue', command=self.issue_book)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_btn = ttk.Button(self.issue_frame, style='quitbtn.TButton', text='Quit', command=self.iss.destroy)
    
    def widget_styles(self):
        self.s = ttk.Style(self.iss)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TLabel', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])
        self.s.configure('TCombobox', background="#894b10", foreground='black')
        self.s.map('TCombobox',background=[('active','#a5570e'),('pressed','#70340c')])
        self.s.configure('TEntry', background='white', foreground='black')
    
    def issue_window(self):
        self.declare_issue_widgets()
        self.issue_frame.grid(row=0, column=0, ipadx=10)
        self.mem_combobox.grid(row=2, column=0, padx=10, pady=20)
        self.member_entry.grid(row=2, column=1, pady=20, padx=15)
        self.book_combobox.grid(row=3, column=0, padx=10, pady=20)
        self.book_entry.grid(row=3, column=1, padx=15, pady=20)
        self.duration_lbl.grid(row=4, column=0, padx=10, pady=20)
        self.duration_entry.grid(row=4, column=1, padx=15, pady=20)
        self.submit_btn.grid(row=6, column=0, pady=10)
        self.quit_btn.grid(row=6, column=1, pady=10)

    def retrieve_values(self):
        self.book_id, self.books, self.member_id, self.members = sql3.get_issue_details()

    def check_member(self, event):
        if self.mem_combobox.get()!='Pick Member ID':
            self.member_id_str = self.mem_combobox.get()
            self.member_name_str = self.members[self.member_id_str]
            self.member_entry.delete(0, tk.END)
            self.member_entry.insert(0, self.member_name_str)
    
    def check_book(self, event):
        if self.book_combobox.get()!='Pick Book ID':
            self.book_id_str = self.book_combobox.get()
            self.book_name_str = self.books[self.book_id_str]
            self.book_entry.delete(0, tk.END)
            self.book_entry.insert(0, self.book_name_str)
            
    def clear_entry(self, event):
        self.duration_entry.delete(0,tk.END)

    def issue_book(self):
        if self.mem_combobox.get()=='Pick Member ID' or self.book_combobox.get()=='Pick Book ID':
            messagebox.showwarning('Value is not selected',"Select Both Id's")
        else:
            messagebox.showinfo('Connecting to Database','Issueing Book')
            self.dur = self.duration_entry.get()
            if sql3.issue_book(self.member_id_str,self.book_id_str,self.dur)==True:
                messagebox.showinfo('Connection Successsful','Book Issued')
                #del self.members[self.member_id_str]
                del self.books[self.book_id_str]
                self.return_date = sql3.get_return_date(self.member_id_str, self.book_id_str)
                messagebox.showinfo('Return Date','Return by '+self.return_date)
            else:
                messagebox.showinfo('Connection Unsuccessful','Database is locked')
        self.refresh_window_iss()

    def refresh_window_iss(self):
        self.iss.destroy()
        self.issue_window()
        self.iss.lift()   

# To return book to library

class Return:

    def declare_return_widgets(self):
        self.ret = tk.Tk()
        self.ret.title('Return Book')
        self.ret.resizable(False, False)
        self.ret.geometry("+120+50")
        self.widget_styles()
        self.retrieve_values()
        self.return_frame = ttk.Frame(self.ret)
        self.member_id_str = tk.StringVar()
        self.mem_combobox = ttk.Combobox(self.return_frame, width=17, textvariable=self.member_id_str, values=self.member_id)
        self.mem_combobox.set('Pick Member ID')
        self.mem_combobox.bind("<<ComboboxSelected>>", self.check_member)
        self.member_name_str = tk.StringVar()
        self.member_entry = ttk.Entry(self.return_frame, textvariable=self.member_name_str)
        self.member_entry.insert(0, 'Member Name')
        self.book_id_str = tk.StringVar()
        self.book_combobox = ttk.Combobox(self.return_frame, width=17, textvariable=self.book_id_str, values=self.book_id)
        self.book_combobox.set('Pick Book ID')
        self.book_combobox.bind("<<ComboboxSelected>>", self.check_book)
        self.book_name_str = tk.StringVar()
        self.book_entry = ttk.Entry(self.return_frame, textvariable=self.book_name_str)
        self.book_entry.insert(0, 'Book Name')
        self.ret_label_str = tk.StringVar()
        self.ret_label_str.set(" ")
        self.ret_label = ttk.Label(self.return_frame, text=" ")
        self.submit_btn = ttk.Button(self.return_frame, text='Return', command=self.return_book)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_btn = ttk.Button(self.return_frame, style='quitbtn.TButton', text='Quit', command=self.ret.destroy)


    def widget_styles(self):
        self.s = ttk.Style(self.ret)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TLabel', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])
        self.s.configure('TCombobox', background="#894b10", foreground='black')
        self.s.map('TCombobox',background=[('active','#a5570e'),('pressed','#70340c')])
        self.s.configure('TEntry', background='white', foreground='black')

    def ret_window(self):
        self.declare_return_widgets()
        self.return_frame.grid(row=0, column=0, ipadx=10)
        self.mem_combobox.grid(row=2, column=0, padx=10, pady=20)
        self.member_entry.grid(row=2, column=1, pady=20, padx=15)
        self.book_combobox.grid(row=3, column=0, padx=10, pady=20)
        self.book_entry.grid(row=3, column=1, pady=20, padx=15)
        self.ret_label.grid(row=4, column=0, columnspan=2, pady=20)
        self.submit_btn.grid(row=6, column=0, pady=10)
        self.quit_btn.grid(row=6, column=1, pady=10)

    def retrieve_values(self):
        self.member_id, self.members, self.book_id, self.books = sql3.get_return_details()    

    def check_member(self, event):
        if self.mem_combobox.get()!='Pick Member ID':
            self.member_id_str = self.mem_combobox.get()
            self.member_name_str = self.members[self.member_id_str]
            self.member_entry.delete(0, tk.END)
            self.member_entry.insert(0, self.member_name_str)

    def check_book(self, event):
        if self.book_combobox.get()!='Pick Book ID':
            self.book_id_str = self.book_combobox.get()
            self.book_name_str = self.books[self.book_id_str]
            self.book_entry.delete(0, tk.END)
            self.book_entry.insert(0, self.book_name_str)
            self.diff,self.due,self.ret_date_str = sql3.get_return_date_details(self.mem_combobox.get(),self.book_combobox.get())
            if self.due == "before" or self.due == "after":
                print("test2")
                self.ret_label.config(text = "Returning "+str(abs(self.diff))+" days "+self.due+" due date "+self.ret_date_str)
            elif self.due == "on":
                print("test1")
                self.ret_label.config(text = "Returning on due date "+self.ret_date_str)
    
    def return_book(self):
        if self.mem_combobox.get()=='Pick Member ID' or self.book_combobox.get()=='Pick Book ID':
            messagebox.showwarning('Value is not selected',"Select Both Id's")
        else:
            messagebox.showinfo('Connecting to Database','Returning Book')
            if sql3.update_return_book_details(self.book_combobox.get(),self.mem_combobox.get()):
                messagebox.showinfo('Connection Successful','Book Returned')
        self.refresh_window_ret()
    
    def refresh_window_ret(self):
        self.ret.destroy()
        self.ret_window()
        self.ret.lift()

# To view the status of issued books ie., thier issued and return details and which member has taken the book

class Issued_Status:

    def declare_book_status_widgets(self):
        self.statsview = tk.Tk()
        self.statsview.title('Issued Status')
        self.statsview.resizable(False, False)
        self.statsview.geometry("+120+50")
        self.widget_styles()
        self.view_status_frame = ttk.Frame(self.statsview)
        self.cols = ('Book ID','Book Name','Member Name','Issue Date','Return Date')
        self.list_status = ttk.Treeview(self.view_status_frame, columns=self.cols, show='headings', selectmode='browse')
        for self.col in self.cols:
            self.list_status.heading(self.col, text=self.col)
        self.verscrlbar = ttk.Scrollbar(self.view_status_frame, orient=tk.VERTICAL, command=self.list_status.yview)
        self.export_btn = ttk.Button(self.view_status_frame, text="Export to Excel", command=self.export_to_excel)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_view_btn = ttk.Button(self.view_status_frame,style='quitbtn.TButton', text="Quit View", command=self.statsview.destroy)
        self.status_details = []
        self.index = self.iid = 0
    
    def widget_styles(self):
        self.s = ttk.Style(self.statsview)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('Treeview', background='#894b10', foreground='white', fieldbackground="#894b10")
        self.s.configure('TScrollbar',background='#70340c', foreground='white')
        self.s.map('TScollbar',background=[('pressed','white')])
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#70340c'),('pressed','"#894b10')])
        self.s.configure('.', background='#70340c', foreground='white')

    def issue_status_window(self):
        self.declare_book_status_widgets()
        self.statsview.lift()
        self.status_details = sql3.get_issued_book_details()
        self.view_status_frame.grid(row=0, column=0, sticky='nsew')
        self.list_status.grid(row=1, column=1, columnspan=6)
        for self.i in self.list_status.get_children():
            self.list_status.delete(self.i)
        for self.row in self.status_details:
            self.list_status.insert('',self.index, self.iid, values=self.row)
            self.index = self.iid = self.index + 1
        self.verscrlbar.grid(row=1, column=0, sticky='ns')
        self.list_status.configure(yscrollcommand = self.verscrlbar.set)
        self.export_btn.grid(row=3, column=2, columnspan=2, padx=20, pady=5)
        self.quit_view_btn.grid(row=3, column=4, columnspan=2, padx=20, pady=5)

    def refresh_window_statsview(self):
        self.statsview.destroy()
        self.issue_status_window()
        self.statsview.lift()
    
    def export_to_excel(self):
        self.export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        sql3.export_stats(self.export_file_path)
        self.refresh_window_statsview()

#The following are functionalites of Members of the library
# To register a new member to the database

class Member_Register:

    def declare_member_reg_widgets(self):
        self.mreg = tk.Tk()
        self.mreg.title('Member Register')
        self.mreg.resizable(False, False)
        self.mreg.geometry("+120+50")
        self.widget_styles()
        self.add_member_frame = ttk.Frame(self.mreg)
        self.mFname_lbl = ttk.Label(self.add_member_frame, text="First Name")
        self.mLname_lbl = ttk.Label(self.add_member_frame, text="Last Name")
        self.mMob_lbl = ttk.Label(self.add_member_frame, text="Mobile")
        self.mEmail_lbl = ttk.Label(self.add_member_frame, text="Email")
        self.mAddress_lbl = ttk.Label(self.add_member_frame, text="Address")
        self.mFname_entry = ttk.Entry(self.add_member_frame)
        self.mLname_entry = ttk.Entry(self.add_member_frame)
        self.mMob_entry = ttk.Entry(self.add_member_frame)
        self.mEmail_entry = ttk.Entry(self.add_member_frame)
        self.mAddress_entry = tk.Text(self.add_member_frame,width=35, height=4, bg='white', fg='black')
        self.mFname = ""
        self.mLname = ""
        self.mMob = ""
        self.mEmail = ""
        self.mAddress = ""
        self.submit_btn = ttk.Button(self.add_member_frame, text="Submit", command=self.member_to_database)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_mreg_btn = ttk.Button(self.add_member_frame, text="Quit", command=self.mreg.destroy, style='quitbtn.TButton')
    
    def widget_styles(self):
        self.s = ttk.Style(self.mreg)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TLabel',foreground='snow',background='#70340c', font=('FreeSans',14))
        self.s.configure('TEntry', background='white', foreground='black')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])
    
    def add_member_window(self):
        self.declare_member_reg_widgets()
        self.add_member_frame.grid(row=0, column=0, sticky='nsew', ipadx=5, ipady=5)
        self.mFname_lbl.grid(row=2, column=1, ipadx=3, padx=5)
        self.mLname_lbl.grid(row=3, column=1, ipadx=3, padx=5)
        self.mMob_lbl.grid(row=4, column=1, ipadx=3, padx=5)
        self.mEmail_lbl.grid(row=5, column=1, ipadx=3, padx=5)
        self.mAddress_lbl.grid(row=6, column=1, ipadx=3, padx=5)
        self.mFname_entry.grid(row=2, column=3, ipadx=40,pady=10)
        self.mLname_entry.grid(row=3, column=3, ipadx=40,pady=10)
        self.mMob_entry.grid(row=4, column=3, ipadx=40,pady=10)
        self.mEmail_entry.grid(row=5, column=3, ipadx=40,pady=10)
        self.mAddress_entry.grid(row=6, column=3,pady=10)
        self.submit_btn.grid(row=8, column=2, sticky='s')
        self.quit_mreg_btn.grid(row=8, column=3, sticky='s')
    
    def member_to_database(self):
        self.mFname = self.mFname_entry.get()
        self.mLname = self.mLname_entry.get()
        self.mMob = self.mMob_entry.get()
        self.mEmail = self.mEmail_entry.get()
        self.mAddress = self.mAddress_entry.get('1.0', tk.END)
        messagebox.showinfo("Connecting to Database", "Writing Member Details to Database")
        if len(self.mFname)==0 or len(self.mLname)==0 or len(self.mMob)==0 or len(self.mEmail)==0 or len(self.mAddress)==0:
            messagebox.showerror("Value Error","Please Enter All Values")
        elif(sql3.member_reg(self.mFname, self.mLname, self.mMob, self.mEmail, self.mAddress)):
           messagebox.showinfo("SQL Connected","Data Inserted Successfully!")
        else:
            messagebox.showerror("Connection Unsuccessful","Database not found")
        self.clear_entry()

    def clear_entry(self):
        self.mFname_entry.delete(0, tk.END)
        self.mLname_entry.delete(0, tk.END)
        self.mMob_entry.delete(0, tk.END) 
        self.mEmail_entry.delete(0, tk.END)
        self.mAddress_entry.delete('1.0', tk.END)
        self.refresh_window_mreg()
    
    def refresh_window_mreg(self):
        self.mreg.destroy()
        self.add_member_window()
        self.mreg.lift()

# To delete members from the database

class Delete_Member:

    def declare_member_del_widgets(self):
        self.mdel = tk.Tk()
        self.mdel.title('Member Delete')
        self.mdel.resizable(False, False)
        self.mdel.geometry("+120+50")
        self.retieve_members()
        self.widget_styles()
        self.member_delete_frame = ttk.Frame(self.mdel)
        self.member_id_str = tk.StringVar(self.mdel)
        self.member_id_str.set('Pick Member ID')
        self.combo_box = ttk.Combobox(self.member_delete_frame, width=27, textvariable=self.member_id_str, values=self.memberids)
        self.combo_box.bind("<<ComboboxSelected>>", self.check_member)
        self.member_name_str = tk.StringVar()
        self.del_member_entry = ttk.Entry(self.member_delete_frame, textvariable=self.member_name_str)
        self.del_member_entry.insert(0, 'Member Name')
        self.del_btn = ttk.Button(self.member_delete_frame, text="Delete", command=self.member_delete)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.del_all_btn = ttk.Button(self.member_delete_frame, text="Delete All Members", command=self.delete_all_members)
        self.quit_del_btn = ttk.Button(self.member_delete_frame, text="Quit", command=self.mdel.destroy, style='quitbtn.TButton')
    
    def widget_styles(self):
        self.s = ttk.Style(self.mdel)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('TCombobox', background="#894b10", foreground='black')
        self.s.map('TCombobox',background=[('active','#a5570e'),('pressed','#70340c')])
        self.s.configure('TEntry', background='white', foreground='black')
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#a5570e'),('pressed','#70340c')])
    
    def retieve_members(self):
        self.memberids, self.memberNamedict = sql3.get_del_member_details()
    
    def delete_memebr_window(self):
        self.declare_member_del_widgets()
        self.member_delete_frame.grid(row=0, column=0, ipadx=10)
        self.combo_box.grid(row=2, column=0, padx=10, pady=20)
        self.del_member_entry.grid(row=2, column=1, pady=20, padx=15)
        self.del_btn.grid(row=2, column=3, pady=10)
        self.quit_del_btn.grid(row=4, column=0, columnspan=2, padx=50)
        self.del_all_btn.grid(row=4, column=3, pady=10)
    
    def check_member(self, event):
        if self.combo_box.get()!='Pick Member ID':
            self.member_id_str = self.combo_box.get()
            self.member_name_str = self.memberNamedict[self.member_id_str]
            self.del_member_entry.delete(0, tk.END)
            self.del_member_entry.insert(0, self.member_name_str)
    
    def member_delete(self):
        if self.combo_box.get()=='Pick Member ID':
            messagebox.showwarning('Value not selected','Select Member ID')
        else:
            messagebox.showinfo('Connecting to Database','Deleting Member')
            if sql3.delete_member(self.member_id_str)==True:
                messagebox.showinfo('Connection Successful','Member Deleted')
                del self.memberNamedict[self.member_id_str]
            else:
                messagebox.showerror('Connection Unsuccessful','Database is locked')
        self.refresh_window_mdel()
    
    def refresh_window_mdel(self):
        self.mdel.destroy()
        self.delete_memebr_window()
        self.mdel.lift()

    def delete_all_members(self):
        if messagebox.askyesno('Deleting all Records','Are you sure you want to proceed?'):
            if sql3.delete_allm():
                messagebox.showinfo('Deleted Records','All records deleted Successsfully')
            else:
                messagebox.showerror('Deletion Unsuccesssful','Could not delete records')
        self.refresh_window_mdel()

# To view a list of all members and their details in the database

class Member_View:

    def declare_mview_widgets(self):
        self.mview = tk.Tk()
        self.mview.title('Memebrs Table')
        self.mview.resizable(False, False)
        self.mview.geometry("+120+50")
        self.widget_styles()
        self.view_member_frame = ttk.Frame(self.mview)
        self.cols = ('Member ID','Name','Mobile', 'Email', 'Address')
        self.list_members = ttk.Treeview(self.view_member_frame, columns=self.cols, show='headings', selectmode='browse')
        for self.col in self.cols:
            self.list_members.heading(self.col, text=self.col)
        self.list_members.column(self.cols[4], width=500, anchor='w')
        self.verscrlbar = ttk.Scrollbar(self.view_member_frame, orient=tk.VERTICAL, command=self.list_members.yview)
        self.export_btn = ttk.Button(self.view_member_frame, text="Export to Excel", command=self.export_to_excel)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_view_btn = ttk.Button(self.view_member_frame,style='quitbtn.TButton', text="Quit View", command=self.mview.destroy)
        self.member_details = []
        self.index = self.iid = 0
    
    def widget_styles(self):
        self.s = ttk.Style(self.mview)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('Treeview', background='#894b10', foreground='white', fieldbackground="#894b10")
        self.s.configure('TScrollbar',background='#70340c', foreground='white')
        self.s.map('TScollbar',background=[('pressed','white')])
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#70340c'),('pressed','"#894b10')])
        self.s.configure('.', background='#70340c', foreground='white')
    
    def view_members_window(self):
        self.declare_mview_widgets()
        self.mview.lift()
        self.member_details = sql3.get_member_details()
        self.view_member_frame.grid(row=0, column=0, sticky='nsew')
        self.list_members.grid(row=1, column=1, columnspan=6, sticky='nsew')
        for self.i in self.list_members.get_children():
            self.list_members.delete(self.i)
        for self.row in self.member_details:
            self.list_members.insert('',self.index,self.iid,values=self.row)
            self.index = self.iid = self.index + 1
        self.verscrlbar.grid(row=1,column=0, sticky='ns')
        self.list_members.configure(yscrollcommand = self.verscrlbar.set)
        self.export_btn.grid(row=3, column=2, columnspan=2, padx=20, pady=5)
        self.quit_view_btn.grid(row=3,column=4,columnspan=2, padx=20, pady=5)

    def refresh_window_mview(self):
        self.mview.destroy()
        self.view_members_window()
        self.mview.lift()
    
    def export_to_excel(self):
        self.export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        sql3.export_members(self.export_file_path)
        self.refresh_window_mview()

# Below are all functionalites of Books of the library
# To register a new book to the database

class Book_Register:

    def declare_book_reg_widgets(self):
        self.breg = tk.Tk()
        self.breg.title('Book Register')
        self.breg.resizable(False, False)
        self.breg.geometry("+120+50")
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
            messagebox.showinfo("SQL Connected","Data Inserted Successfully!")
        else:
            messagebox.showerror("Connection Unsuccessful","Database not found")
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

# To View inforamtion about all books in the databse

class Book_View:

    def declare_view_widgets(self):
        self.bview = tk.Tk()
        self.bview.title('Books Table')
        self.bview.resizable(False, False)
        self.bview.geometry("+120+50")
        self.widget_styles()
        self.view_book_frame = ttk.Frame(self.bview)
        self.cols = ('Book ID','Book Name','Author','ISBN','Price','Status')
        self.list_books = ttk.Treeview(self.view_book_frame, columns=self.cols, show='headings', selectmode='browse')
        for self.col in self.cols:
            self.list_books.heading(self.col, text=self.col)
        self.verscrlbar = ttk.Scrollbar(self.view_book_frame, orient=tk.VERTICAL, command=self.list_books.yview)
        self.export_btn = ttk.Button(self.view_book_frame, text="Export to Excel", command=self.export_to_excel)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_view_btn = ttk.Button(self.view_book_frame,style='quitbtn.TButton', text="Quit View", command=self.bview.destroy)
        self.book_details = []
        self.index = self.iid = 0

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

# This class is for deleting a book from the database

class Book_Delete:
    def declare_book_delete_widgets(self):
        self.bdel = tk.Tk()
        self.bdel.title('Delete Books')
        self.bdel.resizable(False, False)
        self.bdel.geometry("+120+50")
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
        self.s.configure('TCombobox', background="#894b10", foreground='black')
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
        self.del_btn.grid(row=2, column=3, pady=10)
        self.quit_del_btn.grid(row=4, column=0,columnspan=2, padx=50)
        self.del_all_btn.grid(row=4, column=3, pady=10)
            
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
                messagebox.showinfo('Connection Successful','Book Deleted')
                del self.bookdict[self.book_id_str]
            else:
                messagebox.showerror('Connection Unsuccessful','Database is locked')
        self.refresh_window_bdel()

    def refresh_window_bdel(self):
        self.bdel.destroy()
        self.delete_book_window()
        self.bdel.lift()
    
    def delete_all_books(self):
        if messagebox.askyesno('Deleting all Records','Are you sure you want to proceed?'):
            if sql3.delete_all():
                messagebox.showinfo('Deleted Records','All records deleted Successsfully')
            else:
                messagebox.showerror('Deletion Unsuccesssful','Could not delete records')
        self.refresh_window_bdel()

# This class is to get and display information about all records of issue/return of books

class Record_History:

    def declare_book_records_widgets(self):
        self.recordsview = tk.Tk()
        self.recordsview.title('Records')
        self.recordsview.resizable(False, False)
        self.recordsview.geometry("+120+50")
        self.widget_styles()
        self.view_records_frame = ttk.Frame(self.recordsview)
        self.cols = ('Book ID','Book Name','Member ID','Member Name','Issue Date','Return Date')
        self.list_records = ttk.Treeview(self.view_records_frame, columns=self.cols, show='headings', selectmode='browse')
        for self.col in self.cols:
            self.list_records.heading(self.col, text=self.col)
        self.verscrlbar = ttk.Scrollbar(self.view_records_frame, orient=tk.VERTICAL, command=self.list_records.yview)
        self.export_btn = ttk.Button(self.view_records_frame, text="Export to Excel", command=self.export_to_excel)
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.quit_view_btn = ttk.Button(self.view_records_frame,style='quitbtn.TButton', text="Quit View", command=self.recordsview.destroy)
        self.records_details = []
        self.index = self.iid = 0
    
    def widget_styles(self):
        self.s = ttk.Style(self.recordsview)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='white', fieldbackground='#70340c')
        self.s.configure('Treeview', background='#894b10', foreground='white', fieldbackground="#894b10")
        self.s.configure('TScrollbar',background='#70340c', foreground='white')
        self.s.map('TScollbar',background=[('pressed','white')])
        self.s.configure('TButton', background="#894b10", foreground="white")
        self.s.map('TButton',background=[('active','#70340c'),('pressed','"#894b10')])
        self.s.configure('.', background='#70340c', foreground='white')

    def book_records_window(self):
        self.declare_book_records_widgets()
        self.recordsview.lift()
        self.records_details = sql3.get_record_details()
        self.view_records_frame.grid(row=0, column=0, sticky='nsew')
        self.list_records.grid(row=1, column=1, columnspan=6)
        for self.i in self.list_records.get_children():
            self.list_records.delete(self.i)
        for self.row in self.records_details:
            self.list_records.insert('',self.index, self.iid, values=self.row)
            self.index = self.iid = self.index + 1
        self.verscrlbar.grid(row=1, column=0, sticky='ns')
        self.list_records.configure(yscrollcommand = self.verscrlbar.set)
        self.export_btn.grid(row=3, column=2, columnspan=2, padx=20, pady=5)
        self.quit_view_btn.grid(row=3, column=4, columnspan=2, padx=20, pady=5)

    def refresh_window_recordsview(self):
        self.recordsview.destroy()
        self.book_records_window()
        self.recordsview.lift()
    
    def export_to_excel(self):
        self.export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        sql3.export_records(self.export_file_path)
        self.refresh_window_recordsview()

# About

class About:

    def about_widgets(self):
        self.abt = tk.Tk()
        self.abt.title("About")
        self.abt.resizable(False, False)
        self.s = ttk.Style(self.abt)
        self.s.theme_use('clam')
        self.s.configure('TFrame', background='#70340c', foreground='#70340c', fieldbackground='#70340c')
        self.s.configure('TLabel', background='#70340c', foreground='white')
        self.s.configure('quitbtn.TButton', background="#894b10", foreground="white")
        self.s.map('quitbtn.TButton',background=[('active','#d10c0c'),('pressed','red')])
        self.abt_frame = ttk.Frame(self.abt)
        self.abt_text = """
                           Library Management Application 1.0
                           Developed by Nishchay Nayak
                           Developed using Python 3.9.1 using tkinter and sqlite3 packages"""
        self.abt_label = ttk.Label(self.abt_frame, text=self.abt_text)
        self.quit_btn = ttk.Button(self.abt_frame,style='quitbtn.TButton', text="Quit", command=self.abt.destroy)
    
    def about_window(self):
        self.about_widgets()
        self.abt.lift()
        self.abt_frame.grid(row=0, column=0, ipadx=20)
        self.abt_label.grid(row=1, column=1,columnspan=2, pady=10)
        self.quit_btn.grid(row=2, column=1,columnspan=2, pady=10)

# Declaring and defining the main window
class MainWindow:

    # Using contructor to initalize and decalre widgets
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
        self.s.configure('TEntry', background='white', foreground='black')
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
        self.bookOp_menu.add_command(label="Record Histroy", command=self.book_history)

        self.bookIsR_menu = tk.Menu(self.menuBar, bg='#70340c', activebackground='#a5570e', tearoff=0)
        self.menuBar.add_cascade(label="Book Issue/Return", menu=self.bookIsR_menu)
        self.bookIsR_menu.add_command(label="Issue Books", command=self.book_issue)
        self.bookIsR_menu.add_command(label="Return Books", command=self.return_book)
        self.bookIsR_menu.add_command(label="Issued Status", command=self.issue_status)

        self.bookMembers_menu = tk.Menu(self.menuBar, bg='#70340c', activebackground='#a5570e', tearoff=0)
        self.menuBar.add_cascade(label="Library Members", menu=self.bookMembers_menu)
        self.bookMembers_menu.add_command(label="Register New Member", command=self.member_register)
        self.bookMembers_menu.add_command(label="Delete Registered Member", command=self.member_delete)
        self.bookMembers_menu.add_command(label="View Members", command=self.view_member)

        self.about_menu = tk.Menu(self.menuBar, bg='#70340c', activebackground='#a5570e', tearoff=0)
        self.menuBar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="About", command=self.about_app)

        self.quit_btn = tk.Menu(self.menuBar, bg='#70340c', activebackground='red', tearoff=0)
        self.menuBar.add_cascade(label="Quit", menu=self.quit_btn)
        self.quit_btn.add_command(label="Exit Program", command=quit)
        self.book_reg = Book_Register()
        self.book_view = Book_View()
        self.book_del = Book_Delete()
        self.member_reg = Member_Register()
        self.member_del = Delete_Member()
        self.member_view = Member_View()
        self.issue_book = Issue()
        self.status_issue = Issued_Status()
        self.records = Record_History()
        self.returnb = Return()
        self.about = About()
    
    def main_window(self):

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.bg_img_lbl.place(anchor='nw')

    # Calling different windows of different funcitonalities

    def add_book(self):
        self.book_reg.add_book_window()
    
    def view_book(self):
        self.book_view.view_book_window()
    
    def delete_book(self):
        self.book_del.delete_book_window()
    
    def member_register(self):
        self.member_reg.add_member_window()
    
    def member_delete(self):
        self.member_del.delete_memebr_window()
    
    def view_member(self):
        self.member_view.view_members_window()
    
    def book_issue(self):
        self.issue_book.issue_window()
    
    def issue_status(self):
        self.status_issue.issue_status_window()
    
    def book_history(self):
        self.records.book_records_window()
    
    def return_book(self):
        self.returnb.ret_window()
    
    def about_app(self):
        self.about.about_window()


# Main window initialization
def main():
    root = tk.Tk()
    root.iconphoto(True, tk.PhotoImage(file='images/Book_logo.png'))
    root.geometry('600x300')
    root.configure(background='#301806')
    app = MainWindow(root)
    app.main_window()
    root.mainloop()


if __name__ == '__main__':
    main()
