import sys
import os
import re
import hashlib
import random
import string
from db_config import dbconfig
from rich import print as printc
from tkinter import Tk, Label, Entry, Button, LabelFrame, messagebox
from PIL import Image, ImageTk
###############################################################################################################
def gen_secret(length=10):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
    import GUI.login as lg
    os.chdir("C:\\Pass-Manager")
    dir_list = os.listdir()

    if "passm.db" not in dir_list:

        def center_window(root):
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            root.geometry(f'{width}x{height}+{x}+{y}')

        # Intializing Window
        root = Tk()

        # Title of the window
        icon_logo = Image.open("GUI\\assets\\Pass-Manager_logo.ico")
        icon = ImageTk.PhotoImage(icon_logo)
        root.iconphoto(False, icon)
        root.title("Password Manager(Sign up) - By Vinay")

        # Defining width and height of window
        root.geometry("800x330")
        welcome_text = ("Comic Sans Ms", 40, "bold")
        root.resizable(width=False, height=False)

        center_window(root)
        # Loading logo
        logo = Image.open("GUI\\assets\\logo.jpg").resize((300, 330))
        logo = ImageTk.PhotoImage(logo)

        # Assigning Labels
        greet = Label(master=root, text="Welcome", font=welcome_text, pady=20)
        image = Label(image=logo, pady=20)
        image.pack(side="left")
        greet.pack()

        # signup label
        signup_frame = LabelFrame(master=root, text="Sign up Now !", font=("Caveat", 10, "bold"))
        signup_frame.pack(expand='yes', fill='both')
        sign_text = Label(master=signup_frame, text="Enter your Master Password to Sign Up !",
                          font=("sans-serif", 15, "bold"), pady=20)
        sign_text.pack()

        # creating entry box
        password_text_style = ("Comic Sans Ms", 15, "bold")
        entry = Entry(master=signup_frame, font=password_text_style, show="*")
        entry.focus_set()
        entry.pack(pady=15)

        def validate_password(password):
            # At least 8 characters
            # At least one uppercase letter
            # At least one lowercase letter
            # At least one digit
            # At least one special character among !@#$%^&*()_+|~-=`{}[]:;<>?,./
            regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
            return re.match(regex, password) is not None

        def Value():
            mp_pass = str(entry.get())

            def dst_win():
                root.destroy()
                lg.login()

            if mp_pass != "":
                if validate_password(mp_pass):
                    db = dbconfig()
                    cursor = db.cursor()

                    printc("[green][+] Creating new config.. [/green]")

                    printc("[green][+] Database passm.db Created Successfully [/green]")

                    # Creating Table

                    query = "CREATE TABLE IF NOT EXISTS secrets \
                                (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"

                    res = cursor.execute(query)
                    printc("[green][+][/green] Table 'secret' Created")

                    query2 = "CREATE TABLE IF NOT EXISTS entries \
                                (sitename TEXT NOT NULL, url TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"

                    res = cursor.execute(query2)
                    printc("[green][+][/green] Table 'entries' Created")
                    ###############################################################################
                    master_pass = str(entry.get())
                    hashed_mpass = hashlib.sha256(master_pass.encode()).hexdigest()
                    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

                    # Generate device secret

                    dev_sec = gen_secret()
                    printc("[green][+][/green] Device Secret generated")
                    # print(dev_sec)

                    # Adding to databse
                    query = f"INSERT INTO secrets \
                                (masterkey_hash, device_secret) \
                                    VALUES \
                                    ('{hashed_mpass}', '{dev_sec}')"

                    cursor.execute(query)

                    db.commit()

                    printc("[green][+][/green] Added to database")
                    printc("[green][+] Configuration Done [/green]")

                    db.close()
                    dst_win()

                    return
                else:
                    messagebox.showinfo(title="Status", message="""Password should be: \n
At least 8 characters.
At least one uppercase letter.
At least one lowercase letter.
At least one digit.
At least one special character.""")
            else:
                messagebox.showerror(title="Status", message="Fill the entry first !")

        sbt_button = Button(master=signup_frame, text="Sign Up", font=password_text_style, bg="#00FF00", fg="black",
                            command=Value)
        sbt_button.pack()

        # mainloop of the frame
        signup_frame.mainloop()

        # mainloop of the window
        root.mainloop()


    else:
        lg.login()
        print("Database Exists")


if __name__ == "__main__":
    config()
