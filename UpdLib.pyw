import os
import os.path
from os import chdir
import re
import db

def CheckName(s):
    return re.match("\\d+\\-\\d+\\-\\d+\\-\\d+\\-\\d+\\-\\d+\\.(png|jpg|jpeg|gif|bmp|svg)",s) != None or re.match("\\d+\\-\\d+\\-\\d+\\-\\d+\\-\\d+\\-\\d+\\-\\d+\\.(png|jpg|jpeg|gif|bmp|svg)",s) != None

def upd():
    rt="C:\\Users\\zhuan_z6tlgsj\\Documents\\OI\\pic\\p"
    lst=[]
    for pd,dr,fs in os.walk(rt):
        if pd==rt:
            for it in fs:
                if CheckName(it):
                    lst.append(it)
    chdir("C:\\Users\\zhuan_z6tlgsj\\Documents\\OI\\pic")
    PicDb={}
    for it in lst:
        PicDb[db.GetFileMd5("p/"+it)]=it
    db.write("pic.db",PicDb)

if __name__ == "__main__":
    upd()
