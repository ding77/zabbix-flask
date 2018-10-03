# -*- coding: utf-8 -*-
import psutil
from astropy.cosmology.parameters import available
import datetime
#显示CPU所有信息
infos=psutil.cpu_times(percpu=False)
user=infos[0]
system=infos[0]
idle=infos[0]
interrupt=infos[0]
dpc=infos[0]
#返回每秒内的sys利用率，当percpu为True返回是每一个cpu的利用率。
cpu_use=psutil.cpu_percent(interval=1, percpu=True)
#返回cpu个数
cpu_count=psutil.cpu_count(logical=True)

print(infos)

# #内存
# Memory=psutil.virtual_memory()
# total=Memory[0]
# available=Memory[1]
# percent=Memory[2]
# used=Memory[3]
# free=Memory[4]
# 
# #磁盘
# swap=psutil.swap_memory()
# swap_total=swap[0]
# swap_used=swap[1]
# swap_free=swap[2]
# swap_percent=swap[3]
# 
# 
# #硬盘
# #psutil.disk_partitions(all=False)返回所有挂载的分区的信息的列表
# disk=psutil.disk_usage('C:\\')#返回硬盘，分区或者目录的使用情况，单位字节
# disk_total=disk[0]
# disk_used=disk[1]
# disk_free=disk[2]
# disk_percent=disk[3]
# #返回当前磁盘的io情况
# disk_info=psutil.disk_io_counters(perdisk=False)
# read_count=disk_info[0]
# write_count=disk_info[1]
# read_bytes=disk_info[2]
# write_bytes=disk_info[3]
# read_time=disk_info[4]
# write_time=disk_info[5]
# print(disk_info)
# #网络信息
# #返回整个系统的网络信息 pernic值为True，会显示具体各个网卡的信息
# network=psutil.net_io_counters(pernic=False)
# bytes_sent=network[0]
# bytes_recv=network[1]
# packets_sent=network[2]
# packets_recv=network[3]
# 
# #用户
# user=psutil.users()#返回当前系统用户登录信息
# nowtime= datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")#返回当前时间
# 
# 
# #进程
# '''
# psutil.process_iter()
# 返回一个包含Process对象的迭代器。
# 每一个对象只创建一次，创建后缓存起来。当一个进程更新时，
# 会更新缓存。遍历所有进程首选psutil.pids().迭代器排序是
# 根据pid。
# '''
# pids=psutil.pids()#返回当前运行的进程pid列表
# # for proc in psutil.process_iter():
# #     try:
# #         pinfo = proc.as_dict(attrs=['pid', 'name'])
# #     except psutil.NoSuchProcess:
# #         pass
# #     else:
# #         print(pinfo)
# 
# p = psutil.Process()
# pex=p.memory_info()
# #rss=41304064, vms=31735808, num_page_faults=21344, peak_wset=41484288, wset=41304064, peak_paged_pool=253528, paged_pool=253432, peak_nonpaged_pool=30376, 
# rss=pex[0]
# vms=pex[1]
# num_page_faults=pex[2]
# peak_wset=pex[3]
# wset=pex[4]
# peak_paged_pool=pex[5]
# paged_pool=pex[6]
# peak_nonpaged_pool=pex[7]
# nonpaged_pool=pex[8]
# pagefile=pex[9]
# peak_pagefile=pex[10]
# private=pex[11]
# io=p.io_counters()#返回进程的io状况(元祖类型）pio(read_count=1477, write_count=1, read_bytes=7774815, write_bytes=124, other_count=24478, other_bytes=1558820)
# 
# threads=p.num_threads()#返回进程开启的线程数目
# 
# for pnum in psutil.pids():
#     p = psutil.Process(pnum)
# #     print(u"进程名 %-20s  内存利用率 %-18s 进程状态 %-10s 创建时间 %-10s " \
# #     % (p.name(), p.memory_percent(), p.status(), p.create_time()))




