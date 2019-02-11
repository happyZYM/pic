import pickle as pkl
import time
from sys import argv
from win32api import ShellExecute
from os import remove
from shutil import copy
from os import system
import hashlib
import os

def GetFileMd5(fn):
    if not os.path.isfile(fn):
        return
    m=hashlib.md5()
    f=open(fn,"rb")
    while True:
        b=f.read(4096)
        if not b:
            break
        m.update(b)
    f.close()
    return m.hexdigest()

def RunCmd(pro,cmd):
    ShellExecute(0,"",pro,cmd,"",0)

def HaveFile(name):
    try:
        f=open(name)
        f.close()
        return True
    except FileNotFoundError:
        return False

def Log(msg):
    fo=open("log.txt","a")
    s=time.strftime('%Y-%m-%d %H:%M:%S > ',time.localtime(time.time()))+msg
    print("LOG :",s)
    fo.write(s+"\n")
    fo.close()

def load(name):
    fi=open(name,"rb")
    dt=pkl.load(fi)
    fi.close()
    return dt
"""
def write(name,dt):
    if not HaveFile(name):
        f=open(name,"w")
        f.close()
    copy(name,name+"-pre")
    try:
        fo=open(name,"wb")
        try:
            pkl.dump(dt,fo)
        except:
            fo.close()
            remove(name)
            copy(name+"-pre",name)
            Log("Error : in db.py : failed to write db (1)")
            raise Err1
        fo.close()
    except:
        remove(name)
        copy(name+"-pre",name)
        Log("Error : in db.py : failed to write db (2)")
        raise Rrr2
    finally:
        remove(name+"-pre")
"""
def write(name,dt):
    fo=open(name,"wb")
    pkl.dump(dt,fo)
    fo.close()
