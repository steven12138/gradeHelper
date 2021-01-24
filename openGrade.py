# import os
import time
from selenium import webdriver

import time
import tkinter.messagebox
import tkinter.filedialog
import tkinter as tk


usr_name = ""
usr_pwd = ""
usr_path = ""

window = tk.Tk()
window.title('阅卷系统登录')
window.geometry('450x230')
window.resizable(False, False,)

f = False

tk.Label(window, text='登录到阅卷系统,请确保用户名密码正确').place(x=120, y=10)
tk.Label(window, text='用户名:').place(x=100, y=50)
tk.Label(window, text='密码:').place(x=100, y=90)
tk.Label(window, text='ChromeDriver Path[非必填]').place(x=100, y=130)
tk.Label(window, text='Made By steven12138').place(x=310, y=210)

var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=50)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd)
entry_usr_pwd.place(x=160, y=90)

# getpath


def callback():
    global usr_path
    usr_path = tkinter.filedialog.askopenfile().name
    print(usr_path)


file_select = tk.Button(window, text="选择文件", command=callback)
file_select.place(x=270, y=125)

# entry_usr_path = tk.Entry(window, textvariable=var_usr_path)
# entry_usr_path.place(x=160, y=130)


def usr_log_in():
    global usr_name
    global usr_pwd
    # global usr_path
    global f
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    # usr_path = var_usr_path.get()
    if(usr_name == "" or usr_pwd == ""):
        tkinter.messagebox.showerror("错误", "用户名密码不能为空")
        exit()
    f = True
    window.destroy()


bt_login = tk.Button(window, text='登录', command=usr_log_in, width=15)
bt_login.place(x=175, y=180)
window.mainloop()


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False,)
        self.root.wm_attributes('-topmost', 1)
        self.root.title('成绩发布提醒小助手')
        self.label = tk.Label(text="")
        self.label.pack()
        self.root.geometry('300x20')
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--headless")
        if(usr_path != ""):
            self.browser = webdriver.Chrome(
                executable_path=usr_path, chrome_options=self.option)
        else:
            self.browser = webdriver.Chrome(chrome_options=self.option)
        # print(options)

        self.browser.implicitly_wait(3)

        self.browser.get(
            "https://bdfzres.lexuewang.cn:8008/analyse/web/index.html#/login")
        self.browser.find_element_by_css_selector(
            "#app > div.login > div > div.right > div:nth-child(2) > div > input").send_keys(usr_name)
        self.browser.find_element_by_css_selector(
            "#app > div.login > div > div.right > div:nth-child(3) > div > input").send_keys(usr_pwd)
        self.browser.find_element_by_css_selector(
            "#app > div.login > div > div.right > div.loginBtn > button").click()
        try:
            self.browser.find_element_by_css_selector(
                "#app > div.examList > div.content > div > div:nth-child(1) > div.list_right > button").click()
        except BaseException:
            tkinter.messagebox.showerror("发现未知错误", "可能是密码错误，请重试！")
            exit()
        self.glist = []
        self.lastnum = None

        self.f = 0
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        self.browser.refresh()
        tbody = self.browser.find_elements_by_css_selector(
            "#pane--1 > div > div:nth-child(1) > div.allCourseStatistics > div.el-table.el-table--fit.el-table--border.el-table--scrollable-x.el-table--enable-row-hover.el-table--enable-row-transition.el-table--small > div.el-table__body-wrapper.is-scrolling-left > table > tbody>tr")
        num = len(tbody)-1
        nglist = []
        for i in range(num):
            # print("#pane--1 > div > div:nth-child(1) > div.allCourseStatistics > div.el-table.el-table--fit.el-table--border.el-table--scrollable-x.el-table--enable-row-hover.el-table--enable-row-transition.el-table--small > div.el-table__body-wrapper.is-scrolling-left > table > tbody>tr:nth-child(%d)>td:nth-child(1)>div" % (i+2))
            title = self.browser.find_element_by_css_selector("#pane--1 > div > div:nth-child(1) > div.allCourseStatistics > div.el-table.el-table--fit.el-table--border.el-table--scrollable-x.el-table--enable-row-hover.el-table--enable-row-transition.el-table--small > div.el-table__body-wrapper.is-scrolling-left > table > tbody>tr:nth-child(%d)>td:nth-child(1)>div" % (i+2)).text
            grade = self.browser.find_element_by_css_selector("#pane--1 > div > div:nth-child(1) > div.allCourseStatistics > div.el-table.el-table--fit.el-table--border.el-table--scrollable-x.el-table--enable-row-hover.el-table--enable-row-transition.el-table--small > div.el-table__body-wrapper.is-scrolling-left > table > tbody>tr:nth-child(%d)>td:nth-child(3)>div" % (i+2)).text
            nglist.append((title, grade))
        print(nglist)
        if self.lastnum != None and num != self.lastnum:
            self.lastnum = num
            nitem=[]
            for item in nglist:
                if item not in self.glist:
                    nitem.append(item)
            sr="发布了新的成绩\n"
            for item in nitem:
                sr+=item[0]+"："+item[1]+"\n"
            tkinter.messagebox.showwarning('提示', sr)
        now = time.strftime(
            "%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))+" "+"当前发布科目数量："+str(num)
        self.label.configure(text=now)
        sec = 5
        self.root.after(sec*1000, self.update_clock)


if f:
    app = App()
