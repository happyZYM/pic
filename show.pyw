import tkinter as tk
from sys import argv
import db
import win32clipboard as w
import win32con
from os import remove
from PIL import Image, ImageTk

if(len(argv)!=2):
    exit()

def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT,aString)
    w.CloseClipboard()

def copy():
    setText("https://happyzym.gitee.io/pic/p/"+url)

d=db.load(argv[1])
#d=db.load("C:\\Users\\ZHUAN_~1\\AppData\\Local\\Temp\\45526.db")
pic=d["pic"]
url=d["url"]

wd=tk.Tk()
wd.title("图片上传 - "+url)
lx,ly=pic.size[0],pic.size[1]
lx=max(500,lx)
wd.geometry(str(lx)+"x"+str(ly+40)+"+10+"+str(wd.winfo_screenheight()-80-40-20-ly))
pic = ImageTk.PhotoImage(pic)
label_img = tk.Label(wd, image = pic)
label_img.pack(side=tk.TOP)
B = tk.Button(wd,text="复制",command=copy)
text = tk.Entry(wd, highlightcolor = 'red',width=60)
text.insert(0,"https://happyzym.gitee.io/pic/p/"+url)
text.pack(side=tk.LEFT)
B.pack(side=tk.RIGHT)
wd.mainloop()
remove(argv[1])
cpy()
