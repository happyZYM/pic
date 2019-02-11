import db
from sys import argv
from subprocess import run
from os import remove
from time import sleep
from os import system

if(len(argv)!=2):
    exit()
title=argv[1]
while True:
    que=db.load("que.db")
    if(len(que)==0):
        raise ObjectNotFound
    if(que[0]==title):
        break
    sleep(0.05)
run("git add --all >>log.txt",shell=True)
run("git commit -m \""+title+"\" >>log.txt",shell=True)
run("git push -u show master >>log.txt",shell=True)
run("git push -u origin master >>log.txt",shell=True)
que=db.load("que.db")
que=que[1:]
db.write("que.db",que)
