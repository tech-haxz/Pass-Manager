from tkinter import Tk, Button, Entry, Label, messagebox
from PIL import Image, ImageTk
from db_config import dbconfig
from rich import print as printc

def delete():
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
    window.title("Pass-Manager(Delete)")
    window.geometry("700x400")
    window.config(background="#1c2729")
    window.after(1, lambda: window.focus_force())
    window.resizable(width=False, height=False)
    icon_logo = Image.open("GUI\\assets\\Pass-Manager_logo.ico")
    icon = ImageTk.PhotoImage(icon_logo)
    window.iconphoto(False, icon)
    center_window(window)

    #Function to goto previous window
    def back():
        window.destroy()
        menu()


    back_arrow = Image.open("GUI\\assets\\back_arrow.jpg").resize((30, 30))

    back_btn01 = ImageTk.PhotoImage(back_arrow)

    back_btn = Button(master=window, text="Back", image=back_btn01, bd=1, relief="raised", command=back, compound="top", bg="#1c2729", fg="white", activeforeground="white", activebackground="#1c2729")
    back_btn.pack(anchor="nw")


    label = Label(master=window, text="Delete Entry", font=("Comic Sans Ms", 30, "bold"), bg="#1c2729", fg="#00FF00")
    label.pack()

    delete = Label(window, text="Enter the Sitename to delete !! ", font=("Comic Sans Ms", 15), fg="white", bg="#1c2729").pack(pady=30)
    Entry_box = Entry(master=window, width=20, font=("Sans-serif", 20))
    Entry_box.focus_set()
    Entry_box.pack()

    #Function to delete data row from database.
    def Delete_entry(e=None):
        sitename = Entry_box.get()
        if sitename != "":
            try:
                usr_choice = messagebox.askokcancel(title="Deleting data", message="Are you sure to delete?")
                if usr_choice:
                    db = dbconfig()
                    cursor = db.cursor()
                    query = f"DELETE FROM entries WHERE sitename = '{sitename}'"
                    cursor.execute(query)
                    db.commit()
                    rows_affected = cursor.rowcount #It will return 1,2,... if data or any row affect(DELETE, UPDATE, ADD) otherwise returns -1.

                    if rows_affected > 0:
                        messagebox.showinfo(title="Status", message=f"{rows_affected} row(s) deleted successfully!")
                        Entry_box.delete(0, "end")

                    else:
                        messagebox.showwarning(title="No result found", message="Credentials not found!")
                        Entry_box.delete(0, "end")
                        printc("[yellow][-][/yellow] No results for the search")

                else:
                    messagebox.showinfo(title="Status", message="Deletion canceled.")
                    back()

            except Exception as e:
                    messagebox.showerror(title="Error", message=f"An error occurred: {str(e)}")
                    printc(f"[red][!][/red] Error: {str(e)}")
            finally:
                if 'db' in locals():
                    db.close()  # Close the database connection
        else:
            messagebox.showerror(title="Status", message="Fill the entry!")



    dlt_btn = Button(master=window, text="Delete Entry", font=("Comic Sans Ms", 15, "bold"), bg="#00FF00", command=Delete_entry)
    dlt_btn.pack(pady=20)

    window.bind('<Return>', Delete_entry)


    window.mainloop()

if __name__ == "__main__":
    delete()