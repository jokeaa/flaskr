#coding=utf-8
import torndb,datetime
import json


def SqlConnection():
    db = torndb.Connection("127.0.0.1:3306","pangmao",user='root',password='123456')
    return db


def CheckAccount(username,password):
    db = SqlConnection()
    sql = 'select password from account where username = %s'
    tpassword = db.get(sql,username)
    db.close()
    if tpassword == None or tpassword["password"]!=password:
        return False
    else:
        return True

def PicSave(filename,path,pic_order,content,pic_type):
    db = SqlConnection()
    sql = 'insert into pic(filename,path,pic_order,content,pic_type) VALUE (%s,%s,%s,%s,%s)'
    db.insert(sql,filename,path,pic_order,content,pic_type)

def PicGet(pic_type):
    db = SqlConnection()

    sql = 'select * from pic where pic_type = %s'
    pics = db.query(sql,pic_type)
    return pics

def PicDel(filename):
    db = SqlConnection()
    sql = 'delete from pic where (filename=%s)'
    res = db.execute(sql,filename)
    import os
    apath = os.path.abspath('.')+'/static/img/pics/'+filename
    os.remove(apath)

def PicEdit(id,pic_order,content):
    db=SqlConnection()
    sql = 'update pic set pic_order=%s,content=%s where id = %s'
    db.update(sql,pic_order,content,id)



def GetContent():
    db = SqlConnection()
    sql = 'select title,content from webContent'
    return db.query(sql)

def ContentEdit(title,content,type):
    db = SqlConnection()
    sql = 'update webContent set title=%s,content=%s where type=%s'
    db.update(sql,title,content,type)

def JobSave(title,content,type,place):
    db = SqlConnection()
    sql = 'insert into job(title,content,job_type,work_place) VALUE (%s,%s,%s,%s)'
    db.insert(sql,title,content,type,place)


def JobEdit(title,content,type,place,show_job,id):
    db = SqlConnection()
    #print title,content,type,place,show_job,id
    sql = 'update job set title=%s,content=%s,job_type=%s,work_place=%s,show_job=%s where id =%s'
    db.update(sql,title,content,type,place,show_job,id)

def GetJobType():
    db = SqlConnection()
    sql = 'select content from job where id = 1'
    res = db.get(sql)
    return res


def GetJob(show):
    db = SqlConnection()
    # sql = 'select * from job where id != 1'
    # res = db.query(sql)
    if show == 1:
        sql = 'select * from job where id!=1 and show_job=%s;'
        jobs = db.query(sql,show)
    else:
        sql = 'select * from job where id!=1'
        jobs = db.query(sql)


    new_jobs = {}
    for job in jobs:
        if job['job_type'] in new_jobs.keys():
            new_jobs[job['job_type']][job['title']] = [job['content'],job['work_place'],job['show_job'],job['id']]
        else:
            new_jobs[job['job_type']]={}
            new_jobs[job['job_type']][job['title']] = [job['content'],job['work_place'],job['show_job'],job['id']]
    return new_jobs

def AddJobType(type):

    #print type
    db = SqlConnection()
    res = GetJobType()
    if res:
        res = res['content']
        res = res + type + "|"
        sql = 'update job set content = %s where id = 1'
    else:
        res = type + '|'
        sql = 'insert into job(id,content) value(1,%s)'
    db.update(sql,res)
if __name__ == "__main__":
    db = torndb.Connection("139.198.3.170:3306","changeIp",user='root',password='yujian')

    sql = 'select * from adsl_account'
    old = db.query(sql)
    for data in old:
        ip = data['local_ip']
        if ip != None:
            sql = 'update ipproxy set inter_ip=%s,adsl=%s where ipaddress = %s'
            db.update(sql,data['inter_ip'],data['adsl'],ip)
