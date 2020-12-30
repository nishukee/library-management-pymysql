import tkinter as tk
# import tkinter.ttk as tkk
from PIL import ImageTk, Image


class MainWindow:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Library')
        self.parent.resizable(False, False)
        self.bg_image = Image.open('Book_shelf.png')
        self.bg_image = self.bg_image.resize((600, 300), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.bg_image)
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.lbl = tk.Label(image=self.img).grid(row=0, column=0)
        self.menuBar = tk.Menu(self.parent, bg='#75421d', activebackground='#7a3b0b')
        self.parent.config(menu=self.menuBar)

        self.bookOp_menu = tk.Menu(self.menuBar, bg='#4a2910', activebackground='#663109')
        self.menuBar.add_cascade(label="Book Options", menu=self.bookOp_menu)
        self.bookOp_menu.add_command(label="Add Books to Database")
        self.bookOp_menu.add_command(label="View Book List")
        self.bookOp_menu.add_command(label="Delete Books from Database")

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

    def quit(self):
        self.parent.destroy()


def main():
    root = tk.Tk()
    root.geometry('600x300')
    root.configure(background='#301806')
    # root.overrideredirect(1)
    # root.attributes('-topmost', True)
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
