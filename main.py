import tkinter as tk
from tkinter import messagebox
# import tkinter.ttk as tkk
from PIL import ImageTk, Image

class Book_menu:

    def __init__(self, parent):
        self.bm = parent
        #Add Book widgets
        self.add_book_frame = tk.Frame(parent)
        self.book_name_lbl = tk.Label(self.add_book_frame, text="Book Name")
        self.book_author_lbl = tk.Label(self.add_book_frame, text="Author")
        self.book_isbn_lbl = tk.Label(self.add_book_frame, text="ISBN")
        self.book_price_lbl = tk.Label(self.add_book_frame, text="Price")
        self.book_name = ""
        self.book_name_entry = tk.Entry(self.add_book_frame)
        self.author = ""
        self.book_author_entry = tk.Entry(self.add_book_frame)
        self.isbn = ""
        self.book_isbn_entry = tk.Entry(self.add_book_frame)
        self.price = ""
        self.book_price_entry = tk.Entry(self.add_book_frame)
        self.submit_btn = tk.Button(self.add_book_frame, text="Submit",command=self.book_to_database)

    def add_book_window(self):
        self.add_book_frame.grid(row=0, column=0, padx=10, pady=10)
        self.book_name_lbl.grid(row=1, column=1)
        self.book_author_lbl.grid(row=2,column=1)
        self.book_isbn_lbl.grid(row=3,column=1)
        self.book_price_lbl.grid(row=4,column=1)
        self.book_name_entry.grid(row=1, column=2)
        self.book_author_entry.grid(row=2, column=2)
        self.book_isbn_entry.grid(row=3, column=2)
        self.book_price_entry.grid(row=4, column=2)
        self.submit_btn.grid(row=6, column=2)

    def book_to_database(self):
        self.book_name = self.book_name_entry.get()
        self.author = self.book_author_entry.get()
        self.isbn = self.book_isbn_entry.get()
        self.price = self.book_price_entry.get()
        messagebox.showinfo("Connecting to Database","Writing Book Details to Database")
        print(self.book_name+" "+self.author+" "+self.isbn+" "+self.price)
        self.clear_entry()
    
    def clear_entry(self):
        self.book_name_entry.delete(0,tk.END)
        self.book_author_entry.delete(0,tk.END)
        self.book_isbn_entry.delete(0,tk.END)
        self.book_price_entry.delete(0,tk.END)

class MainWindow:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Library')
        self.parent.resizable(False, False)
        self.bg_image = Image.open('Book_shelf.png')
        self.bg_image = self.bg_image.resize((600, 300), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.bg_image)
        self.main_frame = tk.Frame(parent)
        self.bg_img_lbl = tk.Label(image=self.img)
        self.menuBar = tk.Menu(self.parent, bg='#75421d', activebackground='#7a3b0b')
        self.parent.config(menu=self.menuBar)

        self.bookOp_menu = tk.Menu(self.menuBar, bg='#4a2910', activebackground='#663109')
        self.menuBar.add_cascade(label="Book Options", menu=self.bookOp_menu)
        self.bookOp_menu.add_command(label="Add Books to Database", command=self.add_book)
        self.bookOp_menu.add_command(label="View Book List")
        self.bookOp_menu.add_command(label="Delete Books from Database")
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
        self.book = Book_menu(parent)
    
    def main_window(self):

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.bg_img_lbl.place(anchor='nw')

    def add_book(self):
        self.hide_all_frames()
        self.book.add_book_window()

    def hide_all_frames(self):
        self.main_frame.grid_forget()


def main():
    root = tk.Tk()
    root.geometry('600x300')
    root.configure(background='#301806')
    # root.overrideredirect(1)
    # root.attributes('-topmost', True)
    app = MainWindow(root)
    app.main_window()
    root.mainloop()


if __name__ == '__main__':
    main()
