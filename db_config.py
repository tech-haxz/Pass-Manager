import sqlite3
from rich import print as printc
from rich.console import Console

console = Console()

def dbconfig():
    try:
        db = sqlite3.connect("passm.db")
    
    except Exception as e:
        console.print_exception(show_locals=True)

    return db

if __name__ == "__main__":
    dbconfig()