# -*- coding: utf-8 -*-
from flask import Flask,redirect
from flask import request
from flask.templating import render_template
from flask.helpers import url_for
import pymysql
import psutil
import datetime
from fabric.tasks import execute
from web1 import demo1
import urllib
import json
app=Flask(__name__)
db=pymysql.connect(host="127.0.0.1",user="root",passwd='', db='web')
cur=db.cursor()
# nowtime= datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
nowtime=psutil.boot_time()
zbx_url="http://192.168.1.128/zabbix/api_jsonrpc.php"
zabbix_user="Admin"
zabbix_pwd="zabbix"

def get_token():
    url=zbx_url
    header={"Content-Type":"application/json"}
    data='''{"jsonrpc":"2.0","method":"user.login","params":{"user":"%s","password":"%s"},"id": 0}''' % (zabbix_user,zabbix_pwd)
    request=urllib.request.Request(url,data.encode())
    for key in header:
        request.add_header(key, header[key])
    try:
        result=urllib.request.urlopen(request)
    except urllib.request.URLError as e:
        print("ERROR",e.code)
    else:
        response=json.loads(result.read())
        result.close()
        return response['result']
print(get_token())
def zbx_req(zbx_action, zbx_params,zbx_token):
    header = {"Content-Type": "application/json"}
    url = zbx_url
    data='''{"jsonrpc": "2.0","method": "%s","params": %s,"auth": "%s","id": 1 }''' % (zbx_action, zbx_params, zbx_token)
    request = urllib.request.Request(url, data.encode())
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib.request.urlopen(request)
    except urllib.request.URLError as e:
        print('error')
    else:
        response = json.loads(result.read())
        if 'error' in response:
            print (response['error'])
            return False
        elif not response['result']:
            print (response)
            return False
        else:
            return response['result']
        result.close()
        
    
#创建CPU数据库
# cur.execute("DROP TABLE IF EXISTS cpu")
# SQL="""CREATE TABLE cpu(
#   
# nowtime CHAR(200) NOT NULL,
# user float NOT NULL ,
# system float NOT NULL,
# idle float NOT NULL,
# interrupt float NOT NULL,
# dpc float NOT NULL)
# """
# cur.execute(SQL)
#创建sign数据库
# cur.execute("DROP TABLE IF EXISTS sign")
# SQL5="""CREATE TABLE sign(
#   
#   
# username CHAR(200) NOT NULL ,
# password CHAR(200) NOT NULL)
# """
# cur.execute(SQL5)


@app.route('/login',methods=['GET']) 
def login():
    return render_template('login.html')
@app.route('/login',methods=['POST']) 
def login_post():
    username = request.form['username']
    password = request.form['password']
    sql = """ select username,password from sign where username='%s' and password='%s' """%(username,password)
    cur.execute(sql)
    results = cur.fetchone()
    if results:
        return render_template('info.html')
        db.close()
    else:
        return render_template('sign.html')
        db.close()
@app.route('/zhuce',methods=['POST'])
def zhuce():
    return render_template('sign.html')
    
@app.route('/',methods=['POST']) 
def zhuce2():
    
    nickname = request.form['username']
    rename="""
    select * from sign where username='%s'
    """
    n = cur.execute(rename % nickname)
    db.commit()
    if n<0:
       return render_template('sign.html') 
    else:
        password = request.form['password']
        sql_insert="""
    insert into sign values('%s','%s')
    """
        cur.execute(sql_insert % (nickname,password))
        db.commit()
        return render_template('login.html')
    db.close()
    
@app.route('/cpu',methods=['POST']) 
def cpu():
    #往CPU数据库中传数据
    infos=psutil.cpu_times(percpu=False)
    user=infos[0]
    system=infos[1]
    idle=infos[2]
    interrupt=infos[3]
    dpc=infos[4]
    sql_inset="""
    insert into cpu(user,system,idle,interrupt,dpc,nowtime)
    values(%s,%s,%s,%s,%s,%s);
      
    """%(user,system,idle,interrupt,dpc,nowtime)
    cur.execute(sql_inset)
    db.commit()
    select="""
    select  user,system,idle,interrupt,dpc from cpu order by nowtime desc limit 1;
    """
    cur.execute(select)
    db.commit()
    infos=cur.fetchall()
    print(infos)
    for info in infos:
        user1=info[0]
        system1=info[1]
        idle1=info[2]
        interrupt1=info[3]
        dpc1=info[4]
        return render_template('CPU.html',user=user1,system=system1,
                           idle=idle1,interrupt=interrupt1,dpc=dpc1)
    db.commit()
    db.close()
@app.route('/memory',methods=['POST']) 
def memory():
    #往memory数据库中传数据
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
    db.commit()
    select="""
    select  total,available,percent,used,free from memory order by free desc limit 1;
    """
    cur.execute(select)
    db.commit()
    infos=cur.fetchall()
    print(infos)
    for info in infos:
        total1=info[0]
        available1=info[1]
        percent1=info[2]
        used1=info[3]
        free1=info[4]
        return render_template('memory.html',total=total1,available=available1,
                           percent=percent1,used=used1,free=free1)
    db.commit()
    db.close()
@app.route('/cmd',methods=['GET'])
def index():
    return render_template('info.html')
@app.route('/cmd',methods=['POST'])
def getInfo():
    cmd=request.form['cmd']
    result=execute(demo1.runall,cmd)
    print(result)
    for a in result.values():
        print(a)
       
      
    return render_template('info2.html',result=a[0],cmd=cmd)
@app.route('/zabbix') 
def zabbix():
    return render_template('info.html')

@app.route('/zabbix',methods=['POST']) 
def zabbix_host():
    zbx_action=request.form['action']
    zbx_params=request.form['params']
    zbx_token=get_token()
    reponse=zbx_req(zbx_action, zbx_params, zbx_token)
    return render_template("info2.html",message=reponse)
     
 

    
app.run( '127.0.0.1', port=6789, debug=True)
