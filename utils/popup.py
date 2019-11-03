import tkinter as tk
from tkinter import simpledialog, messagebox


class Popup:

    def keywords_input(self):
        root = tk.Tk()
        root.withdraw()
        root.geometry('200x100')
        answer: str = simpledialog.askstring('Search for Keywords', 'Use space between multiple keywords', parent=root)
        return answer

    def msgbox(self, msg_title: str, msg_content: str):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(msg_title, msg_content)


class ProceedButton:

    def __init__(self, target_func):
        self.target_func = target_func

    def bind_func(self):
        root = tk.Tk()
        root.title('Click OK to Proceed Distilling after Crawling')
        frame = tk.Frame(root)
        frame.pack()

        quit_button = tk.Button(frame, text='QUIT', fg='red', command=quit)
        quit_button.pack(side=tk.LEFT)
        ok_button = tk.Button(frame, text='OK', fg='green', command=self.target_func)
        ok_button.pack(side=tk.LEFT)

        root.mainloop()


if __name__ == '__main__':
    def print_something():
        print('this app is easy to use!')


    pb = ProceedButton()
    pb.bind_func(print_something)
