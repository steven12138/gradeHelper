from tkinter import ttk
from tkinter import *
root = Tk()  # 初始框的声明
columns = ("姓名", "IP地址")
treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格



treeview.column("姓名", width=100, anchor='center') # 表示列,不显示
treeview.column("IP地址", width=300, anchor='center')
 
treeview.heading("姓名", text="姓名") # 显示表头
treeview.heading("IP地址", text="IP地址")
 
treeview.pack(side=LEFT, fill=BOTH)
treeview.place(x=10,y=10)
 
name = ['电脑1','服务器','笔记本']
ipcode = ['10.13.71.223','10.25.61.186','10.25.11.163']
for i in range(min(len(name),len(ipcode))): # 写入数据
    treeview.insert('', i, values=(name[i], ipcode[i]))
root.mainloop()