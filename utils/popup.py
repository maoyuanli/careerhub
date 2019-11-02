import tkinter as tk
from tkinter import simpledialog, messagebox


class Popup:

    def keywords_input(self):
        root = tk.Tk()
        root.withdraw()
        root.geometry('200x100')
        answer: str = simpledialog.askstring("Search for Keywords", "Use space between multiple keywords", parent=root)
        return answer

    def msgbox(self, msgTitle: str, msgContent: str):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(msgTitle, msgContent)
