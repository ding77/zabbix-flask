# -*- coding: utf-8 -*-
import pymysql
import psutil
import datetime
db=pymysql.connect(host="127.0.0.1",user="root",passwd='', db='web')
cur=db.cursor()
nowtime= datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")#返回当前时间
# #创建CPU数据库
# cur.execute("DROP TABLE IF EXISTS CPU")
# SQL="""CREATE TABLE CPU(
#  
#  
# user float NOT NULL ,
# system float NOT NULL,
# idle float NOT NULL,
# interrupt float NOT NULL,
# dpc float NOT NULL)
# """
# cur.execute(SQL)
# #创建内存数据库
# cur.execute("DROP TABLE IF EXISTS MEMORY")
# SQL1="""CREATE TABLE MEMORY(
# total float NOT NULL,
# available float NOT NULL,
# percent float NOT NULL,
# used float NOT NULL,
# free float NOT NULL
# )
# """
#   
# cur.execute(SQL1)
# # #创建SWAP数据库
# cur.execute("DROP TABLE IF EXISTS SWAP")
# SQL2="""CREATE TABLE SWAP(
# swap_total float NOT NULL,
# swap_used float NOT NULL,
#  
# swap_free float NOT NULL,
# swap_percent float NOT NULL
# )
#  """
# cur.execute(SQL2)
#  
# #创建DISK数据库    
# cur.execute("DROP TABLE IF EXISTS DISK")
# SQL2="""CREATE TABLE DISK(
# disk_total float NOT NULL,
# disk_used float NOT NULL,
#  
# disk_free float NOT NULL,
# disk_percent float NOT NULL
# )
# """
# cur.execute(SQL2)
# 
# #创建network数据库
# cur.execute("DROP TABLE IF EXISTS NETWORK")
# SQL2="""CREATE TABLE NETWORK(
# bytes_sent float NOT NULL,
# bytes_recv float NOT NULL,
# packets_sent float NOT NULL,
# packets_recv float NOT NULL
# )
# """
# cur.execute(SQL2)
#往CPU数据库中传数据
infos=psutil.cpu_times(percpu=False)
user=infos[0]
system=infos[1]
idle=infos[2]
interrupt=infos[3]
dpc=infos[4]
sql_inset="""
insert into CPU(user,system,idle,interrupt,dpc)
values(%s,%s,%s,%s,%s);
  
"""%(user,system,idle,interrupt,dpc)
cur.execute(sql_inset)

#往内存数据库中传数据
Memory=psutil.virtual_memory()
total=Memory[0]
available=Memory[1]
percent=Memory[2]
used=Memory[3]
free=Memory[4]

sql_inset1="""
insert into MEMORY(total,available,percent,used,free)
values(%s,%s,%s,%s,%s);
  
"""%(total,available,percent,used,free)
cur.execute(sql_inset1)

#往SWAP中传送数据
swap=psutil.swap_memory()
swap_total=swap[0]
swap_used=swap[1]
swap_free=swap[2]
swap_percent=swap[3]
sql_inset2="""
insert into SWAP(swap_total,swap_used,swap_free,swap_percent)
values(%s,%s,%s,%s);
  
"""%(swap_total,swap_used,swap_free,swap_percent)
cur.execute(sql_inset2)
#往DISK数据库中发送数据
disk=psutil.disk_usage('C:\\')#返回硬盘，分区或者目录的使用情况，单位字节
disk_total=disk[0]
disk_used=disk[1]
disk_free=disk[2]
disk_percent=disk[3]
sql_inset3="""
insert into DISK(disk_total,disk_used,disk_free,disk_percent)
values(%s,%s,%s,%s);
  
"""%(disk_total,disk_used,disk_free,disk_percent)
cur.execute(sql_inset3)
#向NETWORK数据库中发送数据
network=psutil.net_io_counters(pernic=False)
bytes_sent=network[0]
bytes_recv=network[1]
packets_sent=network[2]
packets_recv=network[3]
sql_inset4="""
insert into NETWORK(bytes_sent,bytes_recv,packets_sent,packets_recv)
values(%s,%s,%s,%s);
  
"""%(bytes_sent,bytes_recv,packets_sent,packets_recv)
cur.execute(sql_inset4)

db.commit()
db.close()


