# -*- coding:utf-8 -*-
from fabric.api import run,env
env.hosts=['root@192.168.1.128:22']
env.password="921730779"

def runall(cmd):
    return run(cmd).replace("\t"," ").split('\r\n')


       
   
