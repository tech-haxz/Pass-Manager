from tkinter import Tk, Button, Label, ttk, messagebox, Entry
from PIL import Image, ImageTk
import aesutil
from db_config import dbconfig
from rich import print as printc
import pyperclip
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512


# objective: site_name, url, email, username, password

def fetch_pass():
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
    window.title("Pass-Manager(Retrieved Pass)")
    window.geometry("1010x460")
    window.config(background="#1c2729")
    window.after(1, lambda: window.focus_force())
    window.resizable(width=False, height=False)
    icon_logo = Image.open("GUI\\assets\\Pass-Manager_logo.ico")
    icon = ImageTk.PhotoImage(icon_logo)
    window.iconphoto(False, icon)
    center_window(window)

    def back():
        window.destroy()
        menu()

    back_arrow = Image.open("GUI\\assets\\back_arrow.jpg").resize((30, 30))

    back_btn01 = ImageTk.PhotoImage(back_arrow)

    back_btn = Button(master=window, text="Back", image=back_btn01, bd=1, relief="raised", command=back, compound="top", bg="#1c2729", fg="white", activeforeground="white", activebackground="#1c2729")
    back_btn.pack(anchor="nw")

    table = ttk.Treeview(master=window, columns=("Sitenames", "Urls", "Emails", "Usernames", "Passwords"),
                         show="headings")
    table.heading("#1", text="Sitenames")
    table.heading("#2", text="Urls")
    table.heading("#3", text="Emails")
    table.heading("#4", text="Usernams")
    table.heading("#5", text="Passwords")

    for i in range(1, 5 + 1):
        table.column(f"#{i}", anchor="center")

    table.pack(padx=20, pady=10)

    # retrieving data from database
    def retrieve_data():
        db = dbconfig()
        cursor = db.cursor()
        query = "SELECT * FROM entries"

        cursor.execute(query)
        results = cursor.fetchall()

        if len(results) == 0:
            messagebox.showwarning(title="No result found", message="Credentials not found !")
            printc("[yellow][-][/yellow] No results for the search")
            back()
            window.destroy()
            return

        elif (len(results) >= 1):
            for i in results:
                table.insert("", "end", values=(i[0], i[1], i[2], i[3], "{Hidden}"))

    retrieve_data()

    #############################################################################
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

    def copy_passwd():
        if copy_pass.get() != "":
            try:
                db = dbconfig()
                cursor = db.cursor()
                query = f"SELECT password FROM entries WHERE sitename = '{copy_pass.get()}'"

                cursor.execute(query)
                result = cursor.fetchall()[0][0]

                # Copy choosen password by the user
                mk = computeMasterkey(mp_ds()[0], mp_ds()[1])
                decrypted = aesutil.decrypt(key=mk, source=result, keyType="bytes")

                # Decrypting and copying password to clipboard
                pyperclip.copy(decrypted.decode())
                messagebox.showinfo(title="Status",
                                    message=f"{copy_pass.get()} Password successfully copied to clipboard !")
                copy_pass.delete(0, "end")
                printc("[green][+][/green] Password copied to clipboard")

            except Exception:
                messagebox.showerror(title="Not found", message="Incorrect sitename !")
                copy_pass.delete(0, "end")
        else:
            messagebox.showerror(title="Not found", message="Fill the entry !")
            back()

    copy_pass_label = Label(master=window, text="Enter sitename to copy password to clipboard !",
                            font=("Comic Sans Ms", 15, "bold"), bg="#1c2729", fg="white").pack()

    copy_pass = Entry(master=window, font=("Sans-serif", 15), width=30)
    copy_pass.pack()

    btn = Button(master=window, text="Copy Password", font=("Comic Sans Ms", 15, "bold"), bg="#00FF00",
                 command=copy_passwd)
    btn.pack(pady=20)

    window.mainloop()


if __name__ == "__main__":
    fetch_pass()
