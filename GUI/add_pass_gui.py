from tkinter import Tk, Button, Label, LabelFrame, Entry, messagebox, Checkbutton, BooleanVar
from PIL import Image, ImageTk
from generate_pass import generatePassword
import aesutil
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from db_config import dbconfig
from rich import print as printc

###########################################################
#objective: sitename, url, email, username, password

def add_pass_gui():
    from GUI.menu import menu
    text_color = "white"
    back_color = "#1c2729"

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
    window.title("Pass-Manager(Add)")
    window.geometry("700x550")
    window.config(background="#1c2729")
    window.after(1, lambda: window.focus_force())
    window.resizable(width=False, height=False)
    icon_logo = Image.open("GUI\\assets\\Pass-Manager_logo.ico")
    icon = ImageTk.PhotoImage(icon_logo)
    window.iconphoto(False, icon)
    center_window(window)

    #function to go back to previous winodow.
    def back():
        window.destroy()
        menu()

    ########################################################################

    def mp_ds():
        db = dbconfig()
        cursor = db.cursor()
        query = "SELECT * FROM secrets"
        cursor.execute(query)
        result = cursor.fetchall()[0]
        # print(result[0]) # printing Master key 
        # print(result[1])  # Printing device secret key
        return [result[0], result[1]]


    def computeMasterkey(mp, ds):
        password = mp.encode()
        salt = ds.encode()
        key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)

        return key

    def addEntry():
        mpass = mp_ds()[0]
        dev_sec = mp_ds()[1]
        password = passwd.get()

        sitename = s_name.get()
        url = site_url.get()
        email = e_mail.get()
        username = usrname.get()

        m_key = computeMasterkey(mpass, dev_sec)  #returns this : b'\x0cB\xeb\xf8Ge\xd8\xc5\xfb\x90\x04G\xf5\xfe\xffI\x9e?\xd1\xb1\xcf\xaaaf\xe1\x84\xc4"\xc79\xc9\x00'

        encrypted = aesutil.encrypt(key=m_key, source=password, keyType="bytes")

        #Add to db
        if (sitename != "") and (url != "") and (email != "") and (password != ""):
            db = dbconfig()
            cursor = db.cursor()
            query = f"INSERT INTO entries (sitename, url, email, username, password) VALUES ('{sitename}', '{url}', '{email}', '{username}', '{encrypted}')"

            cursor.execute(query)
            db.commit()
            db.close()
            printc("[green][+][/green] Added entry to database.")
            # window.destroy()
            s_name.delete(0, "end")
            site_url.delete(0, "end")
            usrname.delete(0, "end")
            e_mail.delete(0, "end")
            passwd.delete(0, "end")
            messagebox.showinfo(title="Added", message="Credentials are added successfully !")

        else:
            messagebox.showinfo(title="Alert", message="Fill all the entries !", icon="error")

    #generate and fill the random password to password entry
    def fill_pass():
        choice = check_value.get()
        if choice:
            passwd.insert(0, generatePassword(16))
        else:
            passwd.delete(0, "end")
            
    #########################################################################

    back_arrow = Image.open("GUI\\assets\\back_arrow.jpg").resize((30, 30))

    back_btn01 = ImageTk.PhotoImage(back_arrow)

    back_btn = Button(master=window, text="Back", image=back_btn01, bd=1, relief="raised", command=back, compound="top", bg="#1c2729", fg="white", activeforeground="white", activebackground="#1c2729")
    back_btn.pack(anchor="nw")

    #Adding a Label to the window
    label = Label(master=window, text="Add Credentials", font=("Comic Sans Ms", 30, "bold"), bg=back_color, fg="#00FF00")

    label.pack()

    cred_frame = LabelFrame(master=window, text="Fill entry boxes", font=("Arial", 10, "bold"), bg=back_color, fg=text_color)
    cred_frame.pack(expand=True, fill="both")

    image = Image.open("D:\\Pass-Manager\\GUI\\assets\\banner.png").resize((340, 550))
    img = ImageTk.PhotoImage(image)

    logo = Label(master=cred_frame, image=img)
    logo.pack(side="left")
    #Creating sitename label & Entry box
    sitename_label = Label(master=cred_frame, text="Enter Sitename:", font=("Comic Sans", 15, "bold"), fg=text_color, bg=back_color).pack(anchor="nw", padx=10, pady=10)

    s_name = Entry(master=cred_frame, width=30, font=("Arial", 15))
    s_name.focus_set()
    s_name.pack(anchor="nw", padx=10)

    #Creating Url label & Entry box
    Url_label = Label(master=cred_frame, text="Enter Url:", font=("Comic Sans", 15, "bold"), fg=text_color, bg=back_color).pack(anchor="nw", padx=10)

    site_url = Entry(master=cred_frame, width=30, font=("Arial", 15))
    site_url.pack(anchor="nw", padx=10)

    #Creating Email label & Entry box
    Email_label = Label(master=cred_frame, text="Enter Email:", font=("Comic Sans", 15, "bold"), fg=text_color, bg=back_color).pack(anchor="nw", padx=10)

    e_mail = Entry(master=cred_frame, width=30, font=("Arial", 15))
    e_mail.pack(anchor="nw", padx=10)

    #Creating Username label & Entry box
    username_label = Label(master=cred_frame, text="Enter Username:", font=("Comic Sans", 15, "bold"), fg=text_color, bg=back_color).pack(anchor="nw", padx=10)

    usrname = Entry(master=cred_frame, width=30, font=("Arial", 15))
    usrname.pack(anchor="nw", padx=10)

    #Creating password label & Entry box
    password_label = Label(master=cred_frame, text="Enter Password:", font=("Comic Sans", 15, "bold"), fg=text_color, bg=back_color).pack(anchor="nw", padx=10)

    passwd = Entry(master=cred_frame, width=30, font=("Arial", 15), show="*")
    passwd.pack(anchor="nw", padx=10)

    #Creating checkbox to generate random password when checked.
    check_value = BooleanVar()
    opinion = Checkbutton(master=cred_frame, text="Generate random password", font=("Comic Sans", 10), fg=text_color, bg=back_color, selectcolor="black",activebackground=back_color, activeforeground=text_color, variable=check_value, offvalue=False, onvalue=True, command=fill_pass)
    opinion.pack(anchor="nw")

    #Creating a Button
    btn = Button(master=cred_frame, text="Submit", bg="#00FF00", font=("Comic Sans Ms", 15, "bold"), command=addEntry)
    btn.pack(pady=10)

    cred_frame.mainloop()

    #window mainloop
    window.mainloop()


if __name__ == "__main__":
    add_pass_gui()