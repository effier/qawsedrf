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
_qwer="pokefarm"
_online="https://"+_qwer+".com/online"
_user="https://"+_qwer+".com/user/"
_interact="https://"+_qwer+".com/summary/interact"
_pkrs="https://"+_qwer+".com/user/~pkrs"
_field="https://"+_qwer+".com/fields/field"
_fieldList="https://"+_qwer+".com/fields/fieldlist"
_clickback="https://"+_qwer+".com/user/~clickback"
_warning1="https://"+_qwer+".com/summary/interact-warning"
_interactions="https://"+_qwer+".com/interactions"
_notices="https://"+_qwer+".com/farm/notices"
_party="https://"+_qwer+".com/party"
_hatch="https://"+_qwer+".com/summary/hatch"
_hatch2="https://"+_qwer+".com/summary/load"
_movetofield="https://"+_qwer+".com/fields/movetofield"
_shelter="https://"+_qwer+".com/shelter"
_shelterload="https://"+_qwer+".com/shelter/load"
_daycare="https://"+_qwer+".com/daycare/"
_explock="https://"+_qwer+".com/summary/toggleexplock"

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

page="https://"+_qwer+".com/"
pages=['party','farm#tab=1','farm#tab=2','farm#tab=3','farm#tab=4','forge','scour','fields','boxes','shelter','marketboard','daycare','shinyhunt','ubercharm','hypermode','albinohunt','lab','forum',]
forum=['110','130','220','225','135']
forumlink="https://"+_qwer+".com/forum/thread/"
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
        'Host': ""+_qwer+".com",
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
    req.add_header('Host', ""+_qwer+".com")
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
        population=population/2+1000
    elif population >=4000 and population <6000:
        print "population is greater than 4000, so interaction is cut to 1/3."
        population=population/3+1000
    elif population >=6000:
        print "population is greater than 6000, so interaction is cut to 1/4."
        population=population/4+1000
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
            time.sleep(randint(2,5))
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

def checkInteracted(ra):
    clickcount=re.findall(r'clickcount_act_sent">(.*?)<',ra)[0].replace(",","")
    if int(clickcount)==0:
        return False
    else:
        print "user has been interacted today | "+str(clickcount)+" "+time.strftime("%H:%M:%S")
        return True
    
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
            field(clickback[i],sid,(randint(1,25)/100.0))
            raw2=download3(userLink,sid)
            pm=re.findall(r'data-pid="(.*?)"', raw2)
            for j in range(0,(len(pm))):
                data=data1+pm[j]+data2
                download(_interact,data,sid)
                time.sleep(0.5)
            antilog(sid)
    else:
        print "no one to clickback to"
        antilog(sid)
        raw=download3(_online,sid)
        user=re.findall(r'"url":"(.*?)"', raw)
        randid=user[randint(0, len(user)-1)]
        userLink=_user+randid
	raw2=download3(userLink,sid)
        if checkInteracted(raw2)==False:
            #userLink=_user+randid
            field(randid,sid,(randint(1,25)/100.0))
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
        time.sleep(5)

def checkparty(sid,uid,hunt):
    print "---CHECKING PARTY START---"+time.strftime("%H:%M:%S")
    raw=download3(_party,sid)
    pm=re.findall(r'data-pid="(.*?)"', raw)
    if len(pm) <6:
        print "Not a full party. "+time.strftime("%H:%M:%S")
        adopt(sid,hunt)
    pmclass=re.findall(r'\)" class="(.*?)"', raw)
    partysplit=[]
    partydata=[]
    hatchable=[]
    partysplit=raw.split("<div data-pid=")
    for i in range(1,len(partysplit)):
        partydata.append(partysplit[i])
    for j in range(0,len(partydata)):
        if "data-hatch>Hatch the Egg!" in partydata[j]:
            hatchable.append("hatchable")
        elif 'class="disabled">Hatch the Egg'in partydata[j]:
            hatchable.append("egg")
        else:
            hatchable.append("pm")
##    print pm
##    print pmclass
##    print hatchable
    for k in range(0,len(hatchable)):
        if hatchable[k]=="hatchable":
            download(_hatch,'{"id": "'+pm[k]+'"}',sid)
            download(_hatch2,'{"id": "'+pm[k]+'","smallberries":"true"}',sid)
            print "hatched: "+pm[k]+" "+time.strftime("%H:%M:%S")
	    download(_explock,'{"id": "'+pm[k]+'"}',sid)
	    print "explocked: "+pm[k]+" "+time.strftime("%H:%M:%S")
            movetofield(sid,uid,pm[k])
            adopt(sid,hunt)
        elif hatchable[k]=="pm":
            movetofield(sid,uid,pm[k])
            adopt(sid,hunt)
        elif hatchable[k]=="egg":
            print "egg, can't do anything yet"
        time.sleep(1)
    print "---CHECKING PARTY END---"+time.strftime("%H:%M:%S")+"\n"

def adopt(sid,hunt):
    adopted=False
    while adopted==False:
        raw=download3(_daycare,sid)
        dcid=re.findall(r'data-id="(.*?)"', raw)
        dcadopt=[]
        daycarelimit=0
        if "reached the daily adoption limit" in raw:
            daycarelimit=0
        elif "more for free" in raw:
            daycarelimit=re.findall(r'You may adopt (.*?) more for free', raw)[0]
        else:
            daycarelimit=6
        if int(daycarelimit) > 0:
            if hunt=="dexpm" or hunt=="dexegg":
                dcadopt=dcid[randint(0,len(dcid)-1)]
                print str(daycarelimit)+ " daycare adoptions left for today."+" "+time.strftime("%H:%M:%S")
                download("https://pokefarm.com/daycare/adopt",'{"id": "'+dcadopt+'"}',sid)
                data=data1+dcadopt+data2
                download(_interact,data,sid)
                print "adopted for dexegg "+time.strftime("%H:%M:%S")
                adopted=True
                break
            else:
                break
        else:
            print "Today's daycare adoption limit has used up."+" "+time.strftime("%H:%M:%S")
            break
    download3(_shelter,sid)
    while adopted==False:
        raw=download(_shelterload,'{"flute": "first"}',sid)
        if hunt !="dexpm":
            raw=download(_shelterload,'{"flute": "black"}',sid)
        else:
            raw=download(_shelterload,'{}',sid)
        try:
            adoptionlimit=re.findall(r'Therefore, you have <b>(.*?) adoptions', raw)[0]
        except:
            adoptionlimit=re.findall(r'Therefore, you have <b>(.*?) adoption', raw)[0]
        if int(adoptionlimit) > 0:
            print adoptionlimit+ " shelter adoption left for today."+" "+time.strftime("%H:%M:%S")
            info=raw.split('{"i')
            pmname=[]
            #pmstage=[]
            pmid=[]
            pmimg=[]
            for i in range (1, len(info)):
                #print info[i]
                if re.findall(r'"name":"(.*?) \(', info[i]) ==[]:
                    pmname.append(re.findall(r'"name":"(.*?)"', info[i])[0])
                else:
                    pmname.append(re.findall(r'"name":"(.*?) \(', info[i])[0])       
                pmid.append(re.findall(r'd":"(.*?)","stage"', info[i])[0])
                pmimg.append(re.findall(r'pkmn/(.*?)","name', info[i])[0])
                #pmstage.append(re.findall(r'stage":"(.*?)"', info[i])[0])
    ##        print pmname
    ##        print str(len(pmname))
    ##        print pmstage
    ##        print str(len(pmstage))
    ##        print pmid
    ##        print str(len(pmid))
                if hunt=="dexpm":
                    if adopted==False:
                        for j in range (0,len(pmname)):
                            if pmname[j]=="Pok\\u00e9mon":
                                download("https://"+_qwer+".com/shelter/getinfo",'{"id": "'+pmid[j]+'"}',sid)
                                download("https://"+_qwer+".com/shelter/adopt",'{"id": "'+pmid[j]+'"}',sid)
                                data=data1+pmid[j]+data2
                                printdownload(_interact,data,sid)
                                print "adopted for dexpm "+time.strftime("%H:%M:%S")
                                adopted=True
                                break
                    else:
                        break
                elif hunt=="dexegg":
                    if adopted==False:
                        for k in range (0,len(pmname)):
                            if pmname[k]=="Egg":
                                download("https://"+_qwer+".com/shelter/getinfo",'{"id": "'+pmid[k]+'"}',sid)
                                download("https://"+_qwer+".com/shelter/adopt",'{"id": "'+pmid[k]+'"}',sid)
                                data=data1+pmid[k]+data2
                                printdownload(_interact,data,sid)
                                print "adopted for dexegg "+time.strftime("%H:%M:%S")
                                adopted=True
                                break
                    else:
                        break
                else:
                    if adopted==False:
                        for l in range (0,len(pmname)):
                            if hunt+" Egg" in pmname[l]:
                                download("https://"+_qwer+".com/shelter/getinfo",'{"id": "'+pmid[l]+'"}',sid)
                                download("https://"+_qwer+".com/shelter/adopt",'{"id": "'+pmid[l]+'"}',sid)
                                data=data1+pmid[l]+data2
                                download(_interact,data,sid)
                                print "adopted for "+hunt+" "+time.strftime("%H:%M:%S")
                                adopted=True
                                break
                            elif hunt=="vulpix_ice" and "Vulpix Egg" in pmname[l] and "b/y/1/6.png/t=1482399766" in pmimg[l]:
                                download("https://"+_qwer+".com/shelter/getinfo",'{"id": "'+pmid[l]+'"}',sid)
                                download("https://"+_qwer+".com/shelter/adopt",'{"id": "'+pmid[l]+'"}',sid)
                                data=data1+pmid[l]+data2
                                download(_interact,data,sid)
                                print "adopted for "+hunt+" "+time.strftime("%H:%M:%S")
                                adopted=True
                                break
                            elif hunt=="vulpix_fire" and "Vulpix Egg" in pmname[l] and "7/z/0.png/t=1478697860" in pmimg[l]:
                                download("https://"+_qwer+".com/shelter/getinfo",'{"id": "'+pmid[l]+'"}',sid)
                                download("https://"+_qwer+".com/shelter/adopt",'{"id": "'+pmid[l]+'"}',sid)
                                data=data1+pmid[l]+data2
                                download(_interact,data,sid)
                                print "adopted for "+hunt+" "+time.strftime("%H:%M:%S")
                                adopted=True
                                break
                    else:
                        break
	    time.sleep(randint(1,7))
	    if hunt=="dexegg" or hunt=="dexpm":
		antilog(sid)
        else:
            print "Today's daycare and shelter adoption limits have all used up."+" "+time.strftime("%H:%M:%S")
            if hunt=="dexegg" or hunt=="dexpm":
                download3("https://"+_qwer+".com/lab",sid)
                raw3=download("https://"+_qwer+".com/lab/eggs",'{"use_reloader": "false"}',sid)
                if "false" in raw3:
                    print "can't reload lab egg page yet. "+time.strftime("%H:%M:%S")
                    raw4=download("https://pokefarm.com/lab/eggs","{}",sid)
		    key=re.findall(r'"targettime":(.*?),',raw4)[0]
		    if adopted==False:
                        download("https://"+_qwer+".com/lab/adopt",'{"egg": "'+str(0)+'", "key": "'+key+'"}',sid)
                        print "adopted repeated egg "+time.strftime("%H:%M:%S")
                        adopted=True
                        break
                else:
                    labegg=re.findall(r'"name":"(.*?)"',raw3)
                    key=re.findall(r'"targettime":(.*?),',raw3)[0]
                    if adopted==False:
                        for m in range(0,len(labegg)):
                            if "?" in labegg[m]:
                                download("https://"+_qwer+".com/lab/adopt",'{"egg": "'+str(m)+'", "key": "'+key+'"}',sid)
                                print "adopted lag egg for dexegg "+time.strftime("%H:%M:%S")
                                adopted=True
                                break
                    else:
                        break
	    else:
		print hunt+"hunt going on, so lab adoption is ignored. "+time.strftime("%H:%M:%S")
		adopted=True
		break

def movetofield(sid,uid,pmid):
    #download3("https://"+_qwer+".com/fields",sid)
    raw=download(_fieldList,'{"uid": "'+uid+'"}',sid)
    fieldinfo=raw.split('{"i')
    fieldid=[]
    fieldname=[]
    fieldtype=[]
    fieldsize=[]
    for i in range (1, len(fieldinfo)):
        fieldname.append(re.findall(r'"name":"(.*?)"', fieldinfo[i])[0])      
        fieldid.append(re.findall(r'd":(.*?),', fieldinfo[i])[0])
        fieldtype.append(re.findall(r'"type":"(.*?)"', fieldinfo[i])[0])
        fieldsize.append(re.findall(r'"count":(.*?)}', fieldinfo[i])[0])
##    print fieldname
##    print str(len(fieldname))
##    print fieldid
##    print str(len(fieldid))
##    print fieldtype
##    print str(len(fieldtype))
##    print fieldsize
##    print str(len(fieldsize))
    for i in range (0,len(fieldsize)):
        if int(fieldsize[i])<40:
            download(_movetofield,'{"id": "'+pmid+'","field":"'+str(i)+'","getEmptySlot":"true"}',sid)
            print "pmid: "+pmid+" is put into box name: "+fieldname[i]+" | box id: "+fieldid[i]+" "+time.strftime("%H:%M:%S")
            break
        else:
            print "box name: "+fieldname[i]+" | box id: "+fieldid[i]+" is full."+" "+time.strftime("%H:%M:%S")

def antilog(sid):
    ran=(randint(0,10))
    if ran==7:
        print "---ANTI-LOG START---"+time.strftime("%H:%M:%S")
        for i in range(0,randint(1,4)):
            ranpage=randint(0,len(pages)-1)
            print "visiting : "+pages[ranpage]+" "+time.strftime("%H:%M:%S")
            if ranpage==len(pages)-1:
                raw=download3(page+pages[len(pages)-1]+"/"+forum[randint(0,len(forum)-1)],sid)
                post=re.findall(r'/forum/thread/(.*?)">',raw)
                postlink=[]
                for i in range(1,len(post)/2):
                    postlink.append(post[i*2-1])
                for j in range(0,randint(1,len(postlink)/5)):
                    postname=postlink[randint(0,len(postlink)-1)]
                    print "visiting : "+postname+" "+time.strftime("%H:%M:%S")
                    download3(forumlink+postname,sid)
                    time.sleep(randint(5,90))
            else:
                download3(page+pages[ranpage],sid)
            time.sleep(5)
        print "---ANTI-LOG End---"+time.strftime("%H:%M:%S")+"\n"

def checkinteraction(sid):
    raw=download("https://"+_qwer+".com/farm/graph","null",sid)
    act=re.findall(r'"acts":(.*?),', raw)
    todayact=act[len(act)-1]
    print "Current interaction point is: "+str(todayact)+" "+time.strftime("%H:%M:%S")
    return int(todayact)
#===================================================================================
def pkrs(sid,uid,hunt):
    goal=10000
    while True:
	print "Script Started. "+time.strftime("%H:%M:%S")
	try:
	    if goal>=200000:
                print "Goal is reset. "+time.strftime("%H:%M:%S")
                goal=10000
            else:
                goal+=randint(20000,30000)
            raw=download3(_online,sid)
            user=re.findall(r'"url":"(.*?)"', raw)
            randid=user[randint(0, len(user)-1)]
            userLink=_user+randid
            raw2=download3(userLink,sid)
            if checkInteracted(raw2)==False:
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
        except urllib2.HTTPError:
            print "HTTPError! Maintainence or Internet Problem."
            time.sleep(60*20)
            pass
        while checkinteraction(sid) <=goal and checkinteraction(sid)<85000:
	    print "Today's interaction goal is: "+str(goal)
            try:
                userNow=getPkrs(sid)
		userLink=_user+userNow
                raw2=download3(userLink,sid)
                if checkInteracted(raw2) ==False:
                    print "current pkrs is "+userNow+"  "+time.strftime("%H:%M:%S")
                    field(userNow,sid,0.95)
                    pm=re.findall(r'data-pid="(.*?)"', raw2)
                    for j in range(0,(len(pm))):
                        data=data1+pm[j]+data2
                        download(_interact,data,sid)
                        time.sleep(0.5)
                    time.sleep(10)
                    checkparty(sid,uid,hunt)
                    antilog(sid)
                    print "\n"
                else:
                    print "pkrs is the same person:"+userNow
                    print "interacting clickbacks if any"
                    clickback(sid)
                    antilog(sid)
                    checkparty(sid,uid,hunt)
                    time.sleep(10)
            except:
                print "Error! Probably PKRS is self."
		try:
		    checkparty(sid,uid,hunt)
                    clickback(sid)
                    antilog(sid)
                    checkparty(sid,uid,hunt)
                    time.sleep(10)
		except urllib2.HTTPError:
		    print "HTTPError! Maintainence or Internet Problem."
		    time.sleep(60*20)
		    pass
                pass
        else:
            antilog(sid)
            checkinteraction(sid)
            print "Sleep mode "+time.strftime("%H:%M:%S")
	    sleeptime=randint(2,4)
	    print "Will sleep for "+str(sleeptime)+" hours."
            time.sleep(60*60*sleeptime)
	    print "Slept "+str(sleeptime)+" hour."+time.strftime("%H:%M:%S")
	    if goal>=150000:
		print "Goal is reset. "+time.strftime("%H:%M:%S")
		goal=10000
	    else:
		goal+=randint(20000,30000)
    
#===================================================================================
#clear()
#account
sid='08uamffkib6m3rgl2h6gpu3f41'
uid='xailabris'
#(hunt: put pokemon name, or 'dexpm'-adopt random pm for dex, 'dexegg'-adopt random egg for dex)
hunt='Corsola'
#hunt='dexegg'
#=====================
#field("lado1139",sid,0.95)
#antilog(sid)
#checkparty(sid,uid,hunt)
#checkinteraction(sid)
#====================
#main(sid,uid,hunt)
pkrs(sid,uid,hunt)
