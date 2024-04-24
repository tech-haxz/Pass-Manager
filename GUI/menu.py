from tkinter import *
from PIL import Image, ImageTk


def menu():
    from GUI.add_pass_gui import add_pass_gui
    from GUI.fetch_pass_gui import fetch_pass
    from GUI.delete_pass_gui import delete

    def center_window(root):
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
    #Defining window
    root = Tk()
    root.geometry("740x350")
    root.title("Password-Manager(Menu)")
    root.config(background="#1c2729")
    root.after(1, lambda: root.focus_force())
    root.resizable(width=False, height=False)
    icon_logo = Image.open("GUI\\assets\\Pass-Manager_logo.ico")
    icon = ImageTk.PhotoImage(icon_logo)
    root.iconphoto(False, icon)
    center_window(root)

    #Creating Label
    label = Label(master=root, text="Menu", font=("Comic Sans Ms", 40, "bold"), bg="#1c2729", fg="#00FF00").pack()


    #Loading images
    image1 = Image.open("GUI\\assets\\add.jpg").resize((100, 100))
    image2 = Image.open("GUI\\assets\\fetch.png").resize((100, 100))
    image3 = Image.open("GUI\\assets\\delete.png").resize((100, 100))


    #temporary function to test buttons

    def add():
        root.destroy()
        add_pass_gui()
        print("Password added to the database")

    def fetched():
        root.destroy()
        fetch_pass()
        print("Passwords are fetched successfully!")

    def deleted():
        root.destroy()
        delete()
        print("Passwords are deleted!")


    #Converting images into supported form
    photo1 = ImageTk.PhotoImage(image1)
    photo2 = ImageTk.PhotoImage(image2)
    photo3 = ImageTk.PhotoImage(image3)
    img1 = Button(master=root, 
                text="Add Password", 
                image=photo1, 
                padx=30, 
                compound="top",
                bg="white", 
                font=("Comic Sans Ms", 15, "bold"), 
                bd=5, 
                relief=RAISED,
                command=add,
                cursor="plus"
            ).pack(side="left", padx=20)

    img2 = Button(master=root, 
                text="Fetch Passwords", 
                image=photo2, 
                padx=30, 
                compound="top",
                bg="white", 
                font=("Comic Sans Ms", 15, "bold"), 
                bd=5, 
                relief=RAISED,
                command=fetched
            ).pack(side="left", padx=20)

    img3 = Button(master=root, 
                text="Delete Entry", 
                image=photo3, 
                padx=30, 
                compound="top",
                bg="white", 
                font=("Comic Sans Ms", 15, "bold"), 
                bd=5, 
                relief=RAISED,
                command=deleted,
                cursor="pirate"
            ).pack(side="left", padx=20)

    root.mainloop()
    
if __name__ == "__main__":
    menu()