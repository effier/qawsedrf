import httplib 
import urllib 
import urllib2
import time
import re
from datetime import datetime
from random import randint
import thread

#device
ua="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"

url_opener=urllib2.build_opener()

#soloevent related commands
_online="https://pokefarm.com/online"
_user="https://pokefarm.com/user/"
_interact="https://pokefarm.com/summary/interact"
_pkrs="https://pokefarm.com/user/~pkrs"
_field="https://pokefarm.com/fields/field"
_fieldList="https://pokefarm.com/fields/fieldlist"
_clickback="https://pokefarm.com/user/~clickback"
_warning1="https://pokefarm.com/summary/interact-warning"
_interactions="https://pokefarm.com/interactions"
_notices="https://pokefarm.com/farm/notices"

#data
def randberry():
    berries=["aspear","cheri","chesto","pecha","rawst"]
    randb=randint(0,4)
    return berries[randb]


data1="{\"berry\":null,\"pid\":[{\"pid\":\""
data2='\",\"berry\":\"'+"aspear"+'\"}],\"ismulticlick\":true,\"returnformat\":\"party\"}'

data3="{\"id\": "
data4=", \"uid\": \""
data5="\", \"mode\": \"public\"}"

data6='{"pid":'
data6_1=',"berry":"'+randberry()+'","check":false}'
data7=',"berry":"'+randberry()+'","ismulticlick":true}'
dalao="Lilith ErrahM Plu Meu Temporal Tony KaraKara Meik Methos SparkyPrower Caramel_Lyth Killjoy Asia Sable Juice Spiker125 Thurdoyol Blue Wintersun Hyper_Beam Atra Garney DrWho Moriiarty The_Falling_Blue Shiro Suriya MattyMohawk Ruhler Serra_Taylor KikiTheCat Muffinnz Earthsong ErrahM Touka yCr Mail_Jeevas Zan Krambambuli Eltafez Meu Mekkor BananaLizard Scorpyia RedCydranth Temporal Kamilejszon DarkNova181 TechmasterSM4000 Tyrani-Kase HybridYuki"
daily=dalao.split()
notices='{"getnice": true}'


#===================================================================================
def download2(raw):
    doc=parser.fromstring(raw)
    return doc

def download(url,d,s):
    req = urllib2.Request(url,d, {
##        'Accept':'application/json, text/javascript, */*; q=0.01',
##        'Accept-Language':'en-US,en;q=0.8,zh;q=0.6,zh-TW;q=0.4',
        'Connection':"keep-alive",
        'Cookie': 'PHPSESSID=%s' % s,
        'User-Agent': ua,
        'Host': "pokefarm.com",
        'X-Requested-With': "Love"
    })
    raw = url_opener.open(req).read()
    return raw

def download3(url,sid):
    req = urllib2.Request(url)
##    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
##    req.add_header('Accept-Language', 'en-US,en;q=0.8,zh;q=0.6,zh-TW;q=0.4')
    req.add_header('Cookie', 'PHPSESSID=%s' % sid)
    req.add_header('User-Agent', ua)
    req.add_header('Host', "pokefarm.com")
    req.add_header('X-Requested-With', "Love")
    raw = url_opener.open(req).read()
    return raw

def getPkrs(sid):
    raw=download3(_pkrs,sid)
    user=re.findall(r'data-nice="(.*?)"', raw)
    return user[0]

def getPopulation(user,sid):
    population=0
    raw=download(_fieldList,'{"uid": "'+user+'"}',sid)
    box=re.findall(r'count":(\d+)',raw)
    for i in range(0,len(box)):
        population+=int(box[i])
    if population >=3000 and population <4000:
        print "population is greater than 3000, so interaction is cut to 1/2."
        population=population/2+500
    elif population >=4000 and population <6000:
        print "population is greater than 4000, so interaction is cut to 1/3."
        population=population/3+500
    elif population >=6000:
        print "population is greater than 6000, so interaction is cut to 1/4."
        population=population/4+500
    elif population==0:
        print "population is 0, probably a seed or all fields are hidden."
    return population

def field(user,sid,coverage):
    print user+"  "+time.strftime("%H:%M:%S")
    page=0
    pm=[]
    count=0
    population=getPopulation(user,sid)
    while count<(population*coverage)and population !=0:
        raw=download(_field,data3+str(page)+data4+user+data5,sid)
        pm+=re.findall(r'data-id=\\"(.*?)\\"', raw)
        if len(pm)>0:
            print "currently on "+user+" Page: "+str(page+1)+" | "+time.strftime("%H:%M:%S")
            temp=""
            for i in range (0, len(pm)):
                temp+=data6+'"'+pm[i]+'"'+data6_1+","
                full=data6+"["+temp[:-1]+"]"+data7
                count+=1
            temp=""
            page+=1
            time.sleep(5)
            print user+" | page #"+str(page)+" | pm #"+str(count)+"/"+str(population)+" | "+time.strftime("%H:%M:%S")+"\n"
            act=download(_interact,full,sid)
            if "false" in act:
                print act
                safewarning(sid)
            full=""
            pm=[]
            notice(sid)
            time.sleep(2)
        else:
            print "empty box \n"
            page+=1
    print "field done"
    print "--------------------------------------------------\n"

def safewarning(sid):
    check=download(_warning1,"null",sid)
    if "true" in check:
        print "---warning checked?---"+time.strftime("%H:%M:%S")
    else:
        print "warning returned false?"
        print check
    time.sleep(5)

def notice(sid):
    ran=(randint(0,25))
    if ran ==5:
        download(_notices,notices,sid)
        print "---notice?---"+time.strftime("%H:%M:%S")
        time.sleep(2)
    time.sleep(0.3)

def checkInteracted(user,sid):
    raw=download3(_interactions,sid)
    raw2=raw.split('Reciprocated')[1]
    interacted=re.findall(r'user/(.*?)" class="',raw2)
    if user.upper() in (name.upper() for name in interacted):
        return True
    else:
        print user+" has not been interacted today"
        return False
    
def clickback(sid):
    raw=download3(_clickback,sid)
    clickback=re.findall(r'data-name="(.*?)"', raw)
    cb=0
    if len(clickback)>=10:
        cb=int(len(clickback)/4)
    else:
        cb=int(len(clickback)/3)
    if cb>0:
        for i in range(0, cb):
            userLink=_user+clickback[i]
            field(clickback[i],sid,0.25)
            raw2=download3(userLink,sid)
            pm=re.findall(r'data-pid="(.*?)"', raw2)
            for j in range(0,(len(pm))):
                data=data1+pm[j]+data2
                download(_interact,data,sid)
                time.sleep(0.5)
    else:
        print "no one to clickback to"
        raw=download3(_online,sid)
        user=re.findall(r'"url":"(.*?)"', raw)
        randid=user[randint(0, len(user)-1)]
        if checkInteracted(randid,sid) ==False:
            userLink=_user+randid
            field(randid,sid,0.2)
            raw2=download3(userLink,sid)
            pm=re.findall(r'data-pid="(.*?)"', raw2)
            if len(pm)>0:
                for j in range(0,(len(pm))):
                    data=data1+pm[j]+data2
                    download(_interact,data,sid)
                    time.sleep(1)
                time.sleep(10)
                print "\n"
        else:
            print randid+" has been interacted already----- "
        time.sleep(30)
#===================================================================================
def main(url,sid):
    while True:
        try:
            raw=download3(url,sid)
            user=re.findall(r'"url":"(.*?)"', raw)
            randid=user[randint(0, len(user)-1)]
            if checkInteracted(randid,sid) ==False:
                userLink=_user+randid
                field(randid,sid,0.2)
                raw2=download3(userLink,sid)
                pm=re.findall(r'data-pid="(.*?)"', raw2)
                if len(pm)>0:
                    for j in range(0,(len(pm))):
                        data=data1+pm[j]+data2
                        download(_interact,data,sid)
                        time.sleep(1)
                    time.sleep(30)
                    print "\n"
            else:
                print randid+" has been interacted already----- "
        except:
            pass

def pkrs(sid):
    while True:
        try:
            userNow=getPkrs(sid)
            if checkInteracted(userNow,sid) ==False:
                user=userNow
                print "current pkrs is "+user+"  "+time.strftime("%H:%M:%S")
                field(user,sid,0.95)
                userLink=_user+user
                raw2=download3(userLink,sid)
                pm=re.findall(r'data-pid="(.*?)"', raw2)
                for j in range(0,(len(pm))):
                    data=data1+pm[j]+data2
                    download(_interact,data,sid)
                    time.sleep(0.5)
                time.sleep(1)
                print "\n"
            else:
                print "pkrs is the same person:"+userNow
                print "interacting clickbacks if any"
                clickback(sid)
                time.sleep(100)
        except:
            print "Error! Probably PKRS is self."
            clickback(sid)
            time.sleep(100)
            pass

def dailydalao(sid):
    while True:
        try:
            user=daily[randint(0,len(daily)-1)]
            if checkInteracted(user,sid) ==False:
                print user+"  "+time.strftime("%H:%M:%S")
                page=0
                pm=[]
                count=0
                population=getPopulation(user,sid)
                while count<(population*.95)and population !=0:
                    raw=download(_field,data3+str(page)+data4+user+data5,sid)
                    pm+=re.findall(r'data-id=\\"(.*?)\\"', raw)
                    if len(pm)>0:
                        print "currently on "+user+" Page: "+str(page+1)+" | "+time.strftime("%H:%M:%S")
                        temp=""
                        for i in range (0, len(pm)):
                            temp+=data6+'"'+pm[i]+'"'+data6_1+","
                            full=data6+"["+temp[:-1]+"]"+data7
                            count+=1
                        temp=""
                        page+=1
                        time.sleep(5)
                        print user+" | page #"+str(page)+" | pm #"+str(count)+"/"+str(population)+" | "+time.strftime("%H:%M:%S")+"\n"
                        act=download(_interact,full,sid)
                        if "false" in act:
                            print act
                            safewarning(sid)
                        full=""
                        pm=[]
                        notice(sid)
                        time.sleep(2)
                    else:
                        print "empty box \n"
                        page+=1
                print "field done"
                print "--------------------------------------------------\n"
                time.sleep(60)
            else:
                print user+" has been interacted already----- "
        except:
            print "--------ERROR!------------"+time.strftime("%H:%M:%S")
            time.sleep(30)
            pass
        
    
#===================================================================================
#clear()
#account
sid='bl9ufeumbkm1s3qnamfa559494'
#sid='7p7i2a1j1ma8vl2ch6pqllkmo3'
#=====================
#field("Belthazar194",sid,0.95)
#====================
#main(_online,sid)
pkrs(sid)
#dailydalao(sid)
