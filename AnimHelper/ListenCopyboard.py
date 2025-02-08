try:
    from Tkinter import Tk, Text, END   # Python 2
except ImportError:
    from tkinter import Tk, Text, END   # Python 3
import pyperclip

last_copied = ""

def checkClipboard(*args):
    global last_copied
    current_copy = pyperclip.paste()
    if current_copy != last_copied:
        last_copied = current_copy
        txtBox.delete('1.0',END)
        txtBox.insert(END, current_copy)
    root.after(ms=100, func=checkClipboard)

root = Tk()
txtBox = Text(root)
txtBox.config(font=("consolas", 12), undo=True, wrap='word')
txtBox.pack(fill='both', expand=True)

root.bind("<Control-c>", lambda e: "break")  # Disable copy event binding
root.protocol("WM_DELETE_WINDOW", lambda: None)  # Remove close button

root.after(ms=100, func=checkClipboard)
root.mainloop()