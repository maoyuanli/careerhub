import tkinter as tk
from tkinter import simpledialog, messagebox


class Popup:

    def __init__(self):
        pass

    def keywords_input(self):
        root = tk.Tk()
        root.withdraw()
        answer: str = simpledialog.askstring("Search for Keywords", "Use space between multiple keywords", parent=root)
        return answer

    def msgbox(self, msgTitle: str, msgContent: str):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(msgTitle, msgContent)
