# -*- encoding:utf-8 -*-
import wx
import re
import time
import tkinter as tk
import threading as thd
from PIL import Image, ImageTk
from os import chdir
from os import system
from shutil import copy
import db
import win32clipboard as w
import win32con
from subprocess import run
import UpdLib
from sys import argv
import random
from os import environ

rt="C:\\Users\\zhuan_z6tlgsj\\Documents\\OI\\pic"

def CheckName(s):
    return re.match(".+\\.(png|jpg|jpeg|gif|bmp|svg)",s.lower()) != None
class MyApp(wx.App):
    pass

que=[]
class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
          wx.FileDropTarget.__init__(self)
          self.window = window

    def OnDropFiles(self,  x,  y, fileNames):
        for it in fileNames:
            if CheckName(it):
                print("found",it)
                global que
                queL.acquire()
                que.append(it)
                queL.release()
                #op=ShowpicWindow_thd()
                #op.daemon=True
                #op.FileName=it
                #op.start()

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = '图片上传', size = (300,200))
        panel=wx.Panel(self)
        textBox=wx.TextCtrl(panel,pos = (0,0),size =(300, 200))
        dropTarget = FileDropTarget(textBox)
        textBox.SetDropTarget( dropTarget )

def proc(s):
    p=0
    for i in range(0,len(s)):
        if s[i:i+1]=="/" or s[i:i+1]=="\\":
            p=i+1
    return s[p:]

def SetSize(img):
    MaxWidth=1000
    MaxHeight=600
    width=img.size[0]
    height=img.size[1]
    if hasattr(img,'_getexif'):
        dt=img._getexif()
        try:
            if dt[274]==3:
                img=img.rotate(180,expand=True)
            elif dt[274]==6:
                width,height=height,width
                img=img.rotate(-90,expand=True)
            elif dt[274]==8:
                width,height=height,width
                img=img.rotate(90,expand=Truee)
        except:
            pass
    if width<=MaxWidth and height<=MaxHeight:
        return img
    a=MaxWidth/width
    b=MaxHeight/height
    print("a=",a,"b=",b)
    return img.resize( (int(width*min(a,b)) , int(height*min(a,b))) )

def rds():
    rdm.acquire()
    s="-"
    s=s+random.choice('0123456789')
    s=s+random.choice('0123456789')
    s=s+random.choice('0123456789')
    rdm.release()
    return s

class Push_thd(thd.Thread):
    title=''
    def run(self):
        psh.acquire()
        que=db.load("que.db")
        que.append(self.title)
        db.write("que.db",que)
        db.RunCmd("pythonw","commit.pyw "+self.title)
        psh.release()

class Show_thd(thd.Thread):
    pic=""
    url=""
    def run(self):
        ouf=environ["TMP"]+"\\"+random.choice('0123456789')+random.choice('0123456789')+random.choice('0123456789')+random.choice('0123456789')+random.choice('0123456789')+".db"
        db.write(ouf,{"pic":self.pic,"url":self.url})
        #system("start pythonw show.pyw "+ouf)
        db.RunCmd("pythonw","show.pyw "+ouf)
        
class que_thd(thd.Thread):
    FileName=''
    wd=None
    spic=None
    ipic=None
    url=""
    def upload(self):
        UpdLib.upd()
        print("上传",self.FileName)
        chdir(rt)
        to=proc(self.FileName)
        p=0
        for i in range(0,len(to)):
            if to[i:i+1]==".":
                p=i+1
        to=to[p:]
        title=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+rds()
        to=title+"."+to
        print("md5=",db.GetFileMd5(self.FileName))
        PicDb=db.load("pic.db")
        print("db=",PicDb)
        if db.GetFileMd5(self.FileName) in PicDb:
            print("visit Case1")
            self.wd.destroy()
            sht=Show_thd()
            sht.pic=self.ipic
            sht.url=PicDb[db.GetFileMd5(self.FileName)]
            sht.start()
            return
            print("visit Case2")
        copy(self.FileName,"p/"+to)
        p=Push_thd()
        p.title=title
        p.start()
        PicDb[db.GetFileMd5(self.FileName)]=to
        print("modify db to",PicDb)
        db.write("pic.db",PicDb)
        self.wd.destroy()
        sht=Show_thd()
        sht.pic=self.ipic
        sht.url=to
        sht.start()
        
    def cancel(self):
        self.wd.destroy()
        
    def main(self):
        self.wd=tk.Tk()
        self.wd.title("图片上传 - "+proc(self.FileName))
        img_open = Image.open(self.FileName)
        self.spic=img_open
        img_open=SetSize(img_open)
        lx,ly=img_open.size[0],img_open.size[1]
        #print("(",lx,",",ly,")")
        #print("(",img_open.size[0],",",img_open.size[1],")")
        self.ipic=img_open
        lx=max(lx,450)
        self.wd.geometry(str(lx)+"x"+str(ly+40)+"+"+str(self.wd.winfo_screenwidth()-lx-10)+"+"+str(self.wd.winfo_screenheight()-ly-80-40))
        img_png = ImageTk.PhotoImage(img_open)

        tkl.acquire()
        label_img = tk.Label(self.wd, image = img_png)
        tkl.release()
        
        label_img.pack(side=tk.TOP)
        B=tk.Button(self.wd,text="上传",command=self.upload,width=30)
        C=tk.Button(self.wd,text="取消",command=self.cancel,width=30)
        B.pack(side=tk.LEFT)
        C.pack(side=tk.RIGHT)
        self.wd.mainloop()
        
    def run(self):
        while True:
            global que
            if len(que)>0:
                queL.acquire()
                pic=que[0]
                que=que[1:]
                queL.release()
                self.FileName=pic
                self.main()
            time.sleep(0.05)

chdir(rt)
rdm=thd.RLock()
psh=thd.RLock()
queL=thd.RLock()
tkl=thd.RLock()

random.seed(int(time.time()*1000))

if len(argv)!=2:
    qm=que_thd()
    qm.daemon=True
    qm.start()
    app=MyApp()
    frame=MyFrame(parent=None,id=-1)
    frame.Center()
    frame.Show(True)
    app.MainLoop()
else:
    fn=argv[1]
    UpdLib.upd()
    chdir(rt)
    PicDb=db.load("pic.db")
    if db.GetFileMd5(fn) in PicDb:
        print("url=","https://happyzym.gitee.io/pic/p/"+PicDb[db.GetFileMd5(fn)])
        exit()
    to=proc(fn)
    p=0
    for i in range(0,len(to)):
        if to[i:i+1]==".":
            p=i+1
    to=to[p:]
    title=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+rds()
    to=title+"."+to
    copy(fn,"p/"+to)
    p=Push_thd()
    p.title=title
    p.start()
    PicDb[db.GetFileMd5(fn)]=to
    db.write("pic.db",PicDb)
    print("url=","https://happyzym.gitee.io/pic/p/"+PicDb[db.GetFileMd5(fn)])
