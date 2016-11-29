# -*- coding:utf-8 -*-
import Ultimate_ComSpider
from Tkinter import *
root = Tk()
root.title("Weibo_Spider")
root.geometry('500x250')
l = Label(root, text="show", bg="green", font=("Arial", 12), width=5, height=2)
#设置标签
l = Label(root, text="请输入要搜索的微博关键词", bg="PURPLE", font=("Arial", 12), width=25, height=2)
l.pack(side=TOP)  #这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
#设置单行文本框
var = StringVar()
e = Entry(root, textvariable = var)
var=Text(root)
e.pack()
#输入文本
# t = Text(root)
# t.insert(1.0, 'hello\n')
# t.insert(END, 'hello000000\n')
# t.insert(END, 'nono')
# t.pack()
p=Ultimate_ComSpider.weibocom()
#创建按钮
#Button(root, text="开始爬取",command=p.start_html(var)).pack()
root.mainloop()