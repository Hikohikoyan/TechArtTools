import tkinter as tk

def click():
    txt = entry.get()
    print(txt)
    label.configure(text = txt)

root = tk.Tk()
label = tk.Label(root,text = "请输入你的愿望")
label.grid(row=0,column=0,columnspan=2)
entry = tk.Entry(root)
entry.grid(row=1,column=0)
button = tk.Button(root,text = "确认",command=click)
button.grid(row=1,column=1)
root.mainloop()