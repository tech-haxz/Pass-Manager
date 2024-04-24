from tkinter import Tk, Entry, Button, Label, messagebox
from PIL import Image, ImageTk
from rich import print as printc
from db_config import dbconfig
import hashlib
import sys

def login():
    from GUI.menu import menu
    def center_window(root):
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')


    window = Tk()
    window.geometry("700x400")
    window.title("Password-Manager(Login)")
    window.config(background="#1c2729")
    background = "#1c2729"
    window.resizable(width=False, height=False)
    icon_logo = Image.open("GUI\\assets\\Pass-Manager_logo.ico")
    icon = ImageTk.PhotoImage(icon_logo)
    window.iconphoto(False, icon)
    center_window(window)

    def l_details():
        mp= str(entry.get())
        if mp != "":
            mp_hashed = hashlib.sha256(mp.encode()).hexdigest()

            db = dbconfig()
            cursor = db.cursor()
            query = "SELECT * FROM secrets"
            cursor.execute(query)
            result = cursor.fetchall()[0]

            # print(mp_hashed)
            # print(result[1])  # Printing device secret key

            if mp_hashed != result[0]:
                printc("[red][!] Wrong master key [/red]")
                messagebox.showerror(title="Warning", message="Wrong master key !")
                sys.exit(0)
            else:
                window.destroy()
                menu()
        else:
            messagebox.showwarning(title="Warning", message="Fill the entry !")
            # sys.exit(1)
##########################################################################################
    #Creating a Label
    label = Label(master=window, text="Login", font=("Comic Sans Ms", 50, "bold"), bg=background, fg="#00FF00")
    label.pack(pady=35)

    text_login = Label(window, text="Enter your Master Password to Login!", font=("Caveat", 18),bg=background, fg="white").pack(pady=10)

    #Entry box for login master password
    entry = Entry(master=window, font=("Comic Sans Ms", 20), show="*")
    entry.focus_set()
    entry.pack()

    #Login Button
    login_btn = Button(master=window, text="Submit", font=("Comic Sans Ms", 15, "bold"), bg="#00FF00", command=l_details)
    login_btn.pack(pady=20)
    window.mainloop()

    # return l_details()

if __name__ == "__main__":
    login()