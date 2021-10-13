#!/usr/bin/python3

# Display users information on Akatsuki
# Author: Murmurtwins

from PIL import Image,ImageDraw,ImageFont,ImageFilter
from io import BytesIO
import requests, json, time, math
import pymysql

ID=int(input('Your ID? (An integer):')) # 输入ID
mode=input('Relax or Regular?:')
url='https://akatsuki.pw/api/v1/users/full?id='+str(ID)
url2='https://a.akatsuki.pw/'+str(ID)
r=requests.get(url)
result=json.loads(r.text)
username=result['username']
country=result['country']

#url3='https://www.countryflags.io/'+country+'/shiny/64.png'
#url3='https://flagcdn.com/w40/'+country+'.png'

if mode == 'Relax':
        var=1
else:
        var=0

globalrank=result['stats'][var]['std']['global_leaderboard_rank']
countryrank=result['stats'][var]['std']['country_leaderboard_rank']
pp=result['stats'][var]['std']['pp']
rankedscore=result['stats'][var]['std']['ranked_score']
acc=result['stats'][var]['std']['accuracy']
pc=result['stats'][var]['std']['playcount']
replay=result['stats'][var]['std']['replays_watched']
level=result['stats'][var]['std']['level']
level_int=int(level)
level_res=100*(level-level_int)

url4='http://akatsuki.pw/api/v1/users/scores/best?mode=0&p='
upp=0
A=0
B=0
C=0
D=0
S=0
SS=0
SH=0
SSH=0
count=0
bpk=0
realscore=0
inf=''
for page in range(1,300):
        pagestr=str(page)
        print('Now we are at page:',page)
        url5='&l=100&rx='+str(var)+'&id='+str(ID)
        fullurl=url4+pagestr+url5
#        time.sleep(10)
        r2=requests.get(fullurl)
        result2=json.loads(r2.text)
        try:
                for item in range(0,100):
                        try:
                                ppitem=result2['scores'][item]['pp']
                                rank=result2['scores'][item]['rank']
                                rscore=result2['scores'][item]['score']
                                if rank=="A":
                                        A=A+1
                                if rank=="B":
                                        B=B+1
                                if rank=="C":
                                        C=C+1
                                if rank=="D":
                                        D=D+1
                                if rank=="S":
                                        S=S+1
                                if rank=="SS":
                                        SS=SS+1
                                if rank=="SH":
                                        SH=SH+1
                                if rank=="SSH":
                                        SSH=SSH+1
                                if page==10 and item==99:
                                        bpk=ppitem
                                upp+=ppitem
                                realscore+=rscore
                                count=(page-1)*100+item+1
                        except IndexError:
                             count=(page-1)*100+item
                             if count<1000:
                                  inf='/'
                             break;
        except TypeError:
                break;

image=Image.new('RGB',(953,462),(255,255,255))
font1=ImageFont.truetype('ARLRDBD.ttf',48)
font11=ImageFont.truetype('ARLRDBD.ttf',36)
font12=ImageFont.truetype('ARLRDBD.ttf',30)
font2=ImageFont.truetype('Torus Regular.otf',48)
font21=ImageFont.truetype('Torus Regular.otf',36)
font22=ImageFont.truetype('Torus Regular.otf',24)
font23=ImageFont.truetype('Torus Regular.otf',38)
font24=ImageFont.truetype('Torus Regular.otf',30)
font25=ImageFont.truetype('Torus Regular.otf',20)
font3=ImageFont.truetype('Torus SemiBold.otf',48)
font31=ImageFont.truetype('Torus SemiBold.otf',17)
font4=ImageFont.truetype('inkfree.ttf',30)
imgtemp=Image.open("template2.png")
image.paste(imgtemp,(0,0))

draw=ImageDraw.Draw(image)
draw.text((351,25),username,font=font21,fill=(255,255,255))
draw.text((414,64),'#'+str(globalrank),font=font3,fill=(255,255,255))
draw.text((468,117),str(pp),font=font23,fill=(201,201,201))
draw.text((154,175),'Ranked Score',font=font4,fill=(255,255,255))
draw.text((148,222),'Hit Accuracy',font=font4,fill=(255,255,255))
draw.text((160,271),'Play Count',font=font4,fill=(255,255,255))
draw.text((500,271),'Score Count',font=font4,fill=(255,255,255))
draw.text((181,319),'Replays',font=font4,fill=(255,255,255))
draw.text((440,319),'Unweighted PP',font=font4,fill=(255,255,255))
draw.text((93,366),'Current Level',font=font4,fill=(255,255,255))
draw.text((514,366),'BP1000',font=font4,fill=(255,255,255))
draw.text((176,417),'Ranks',font=font4,fill=(255,255,255))
draw.text((293,417),'S',font=font12,fill=(210,105,30))
draw.text((298,417),'S',font=font12,fill=(210,105,30))
draw.text((458,417),'S',font=font12,fill=(210,105,30))
draw.text((623,417),'A',font=font12,fill=(0,255,0))

total_ss=SS+SSH
total_s=S+SH

draw.text((341,415),format(total_ss,','),font=font24,fill=(255,255,255))
draw.text((506,415),format(total_s,','),font=font24,fill=(255,255,255))
draw.text((671,415),format(A,','),font=font24,fill=(255,255,255))

if count>=30000:
        draw.text((671,269),format(count,','),font=font24,fill=(255,255,0))
else:
        draw.text((671,269),format(count,','),font=font24,fill=(255,255,255))

if upp>=8500000:
        draw.text((656,317),format(upp,'0,.2f'),font=font24,fill=(255,255,0))
else:
        draw.text((656,317),format(upp,'0,.2f'),font=font24,fill=(255,255,255))

if count<1000:
        draw.text((641,364),inf,font=font24,fill=(255,255,255))
else:
        draw.text((641,364),format(bpk,'0,.2f'),font=font24,fill=(255,255,255))

draw.text((360,174),format(rankedscore,','),font=font24,fill=(255,255,255))
draw.text((346,222),format(acc,'0.2f')+'%',font=font24,fill=(255,255,255))
draw.text((332,269),format(pc,','),font=font24,fill=(255,255,255))
draw.text((316,318),format(replay,','),font=font24,fill=(255,255,255))

if level_int>=97:
	draw.text((302,367),str(level_int)+' ('+str(format(level_res,'0.3f'))+'%)',font=font24,fill=(255,255,0))
else:
	draw.text((302,367),str(level_int)+' ('+str(format(level_res,'0.3f'))+'%)',font=font24,fill=(255,255,255))

t1=time.time()
t2=time.strftime("%y-%m-%d %H:%M:%S",time.localtime())
draw.text((804,432),t2,font=font31,fill=(255,0,0))

response=requests.get(url2)
#response2=requests.get(url3)
response=response.content
#response2=response2.content
BytesIOOBj=BytesIO()
#BytesIOOBj2=BytesIO()
BytesIOOBj.write(response)
#BytesIOOBj2.write(response2)
imgprof=Image.open(BytesIOOBj)
flag=Image.open('flags/'+country+'.png')
region=imgprof.resize((125,125))
image.paste(region,(166,27))
image.paste(flag,(601,85))
draw.text((670,64),'#'+str(countryrank),font=font3,fill=(255,255,255))
if mode == 'Regular':
        status=Image.open('rx.png')
        image.paste(status,(855,345))
else:
        pass

# Modify this part to fit for your configurations in MySQL
#----------------------------------------------------------------------------
conn = pymysql.connect(host='localhost',port=3307,db='name_of_database',
                       user='mysql_username',passwd='',charset='utf8')
#----------------------------------------------------------------------------

cursor=conn.cursor()
sql1 = "SELECT * FROM akatsukistat.player_stat WHERE user_id = %s AND rx_state = %s"
cursor.execute(sql1,(ID,var))
result_old=cursor.fetchone()
try:
    old_globalrank=result_old[3]
    old_countryrank=result_old[4]
    old_pp=result_old[5]
    old_rankedscore=result_old[6]
    old_acc=result_old[7]
    old_pc=result_old[8]
    old_replay=result_old[9]
    old_level=result_old[10]
    old_count=result_old[11]
    old_upp=result_old[12]
    old_bpk=result_old[13]
    old_ss=result_old[14]
    old_s=result_old[15]
    old_a=result_old[16]
    old_time=result_old[17]
except TypeError:
        old_globalrank = 0
        old_countryrank = 0
        old_pp = 0
        old_rankedscore = 0
        old_acc = 0
        old_pc = 0
        old_replay = 0
        old_level = 0
        old_count = 0
        old_upp = 0
        old_bpk = 0
        old_ss = 0
        old_s = 0
        old_a = 0
        old_time = 0

sql2 = "DELETE FROM akatsukistat.player_stat WHERE user_id = %s AND rx_state = %s"
cursor.execute(sql2,(ID,var))
sql3 = "INSERT INTO akatsukistat.player_stat(username,user_id,rx_state,world_rank,country_rank,pp,ranked_score,hit_accuracy,playcount,replays,current_level,score_count,unweightedpp,bponek,ss_count,s_count,a_count,time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.execute(sql3,(username,ID,var,globalrank,countryrank,pp,rankedscore,acc,pc,replay,level,count,upp,bpk,total_ss,total_s,A,t1))
conn.commit()

diff_globalrank=globalrank-old_globalrank
diff_countryrank=countryrank-old_countryrank
diff_pp=pp-old_pp
diff_rankedscore=rankedscore-old_rankedscore
diff_acc=round(acc,2)-round(old_acc,2)
diff_pc=pc-old_pc
diff_replay=replay-old_replay
diff_level=round(level,5)-round(old_level,5)
diff_count=count-old_count
diff_upp=round(upp,5)-round(old_upp,5)
diff_bpk=bpk-old_bpk
diff_ss=total_ss-old_ss
diff_s=total_s-old_s
diff_a=A-old_a
diff_t1=t1-old_time

conn.close()

if diff_globalrank>0:
        draw.text((534,59), '-' + format(diff_globalrank,','), font=font25, fill=(255, 0, 0))
if diff_globalrank<0:
        draw.text((534,59), '+' + format(-diff_globalrank,','), font=font25, fill=(0, 255, 0))
if diff_globalrank==0:
        draw.text((534,59), '=', font=font25, fill=(255, 255, 0))

if diff_countryrank>0:
        draw.text((764,59), '-' + format(diff_countryrank,','), font=font25, fill=(255, 0, 0))
if diff_countryrank<0:
        draw.text((764,59), '+' + format(-diff_countryrank,','), font=font25, fill=(0, 255, 0))
if diff_countryrank==0:
        draw.text((764,59), '=', font=font25, fill=(255, 255, 0))

if diff_pp>0:
        draw.text((608,131), '+' + format(diff_pp,','), font=font25, fill=(0, 255, 0))
if diff_pp<0:
        draw.text((608,131), '-' + format(-diff_pp,','), font=font25, fill=(255, 0, 0))
if diff_pp==0:
        draw.text((608,131), '=', font=font25, fill=(255, 255, 0))

if diff_rankedscore>0:
        draw.text((600,179), '+' + format(diff_rankedscore,','), font=font25, fill=(0, 255, 0))
if diff_rankedscore<0:
        draw.text((600,179), '-' + format(-diff_rankedscore,','), font=font25, fill=(255, 0, 0))
if diff_rankedscore==0:
        draw.text((600,179), '=', font=font25, fill=(255, 255, 0))

if diff_acc>0:
        draw.text((514,227), '+' + format(diff_acc*100,'0.2f') + '%', font=font25, fill=(0, 255, 0))
if diff_acc<0:
        draw.text((514,227), '-' + format(-diff_acc*100,'0.2f') + '%', font=font25, fill=(255, 0, 0))
if diff_acc==0:
        draw.text((514,227), '=', font=font25, fill=(255, 255, 0))

if diff_pc>0:
        draw.text((430,252), '+' + format(diff_pc,','), font=font25, fill=(0, 255, 0))
if diff_pc<0:
        draw.text((430,252), '-' + format(-diff_pc,','), font=font25, fill=(255, 0, 0))
if diff_pc==0:
        draw.text((430,252), '=', font=font25, fill=(255, 255, 0))

if diff_replay>0:
        draw.text((406,300), '+' + format(diff_replay,','), font=font25, fill=(0, 255, 0))
if diff_replay<0:
        draw.text((406,300), '-' + format(-diff_replay,','), font=font25, fill=(255, 0, 0))
if diff_replay==0:
        draw.text((406,300), '=', font=font25, fill=(255, 255, 0))

if diff_level>0:
        draw.text((386,349), '+' + format(diff_level*100,'0.2f') + '%', font=font25, fill=(0, 255, 0))
if diff_level<0:
        draw.text((386,349), '-' + format(-diff_level*100,'0.2f') + '%', font=font25, fill=(255, 0, 0))
if abs(diff_level)==0:
        draw.text((386,349), '=', font=font25, fill=(255, 255, 0))

if diff_count>0:
        draw.text((810,277), '+' + format(diff_count,','), font=font25, fill=(0, 255, 0))
if diff_count<0:
        draw.text((810,277), '-' + format(-diff_count,','), font=font25, fill=(255, 0, 0))
if diff_count==0:
        draw.text((810,277), '=', font=font25, fill=(255, 255, 0))

if diff_upp>0:
        draw.text((749,349), '+' + format(diff_upp,'0,.2f'), font=font25, fill=(0, 255, 0))
if diff_upp<0:
        draw.text((749,349), '-' + format(-diff_upp,'0,.2f'), font=font25, fill=(255, 0, 0))
if diff_upp==0:
        draw.text((749,349), '=', font=font25, fill=(255, 255, 0))

if diff_bpk>0:
        draw.text((790,370), '+' + format(diff_bpk,','), font=font25, fill=(0, 255, 0))
if diff_bpk<0:
        draw.text((790,370), '-' + format(-diff_bpk,','), font=font25, fill=(255, 0, 0))
if diff_bpk==0:
        draw.text((790,370), '=', font=font25, fill=(255, 255, 0))

if diff_ss>0:
        draw.text((350,396), '+' + format(diff_ss,','), font=font25, fill=(0, 255, 0))
if diff_ss<0:
        draw.text((350,396), '-' + format(-diff_ss,','), font=font25, fill=(255, 0, 0))
if diff_ss==0:
        draw.text((350,396), '=', font=font25, fill=(255, 255, 0))

if diff_s>0:
        draw.text((519,396), '+' + format(diff_s,','), font=font25, fill=(0, 255, 0))
if diff_s<0:
        draw.text((519,396), '-' + format(-diff_s,','), font=font25, fill=(255, 0, 0))
if diff_s==0:
        draw.text((519,396), '=', font=font25, fill=(255, 255, 0))

if diff_a>0:
        draw.text((686,396), '+' + format(diff_a,','), font=font25, fill=(0, 255, 0))
if diff_a<0:
        draw.text((686,396), '-' + format(-diff_a,','), font=font25, fill=(255, 0, 0))
if diff_a==0:
        draw.text((686,396), '=', font=font25, fill=(255, 255, 0))

if diff_t1<=60:
        draw.text((690,154), '(compared with ' +str(int(diff_t1))+ 's ago)', font=font25, fill=(255, 0, 0))
if 60<diff_t1<=3600:
        draw.text((690,154), '(compared with ' +str(int(int(diff_t1)/60)) + 'min ago)', font=font25, fill=(255, 0, 0))
if 3600<diff_t1<=86400:
        draw.text((690,154), '(compared with ' +str(int(int(diff_t1)/3600)) + 'h ago)', font=font25, fill=(255, 0, 0))
if 86400<diff_t1<=172800:
        draw.text((690,154), '(compared with '+str(int(int(diff_t1)/86400)) + 'day ago)', font=font25, fill=(255, 0, 0))
if diff_t1>172800:
        draw.text((690,154), '(compared with ' +str(int(int(diff_t1)/86400)) + 'days ago)', font=font25, fill=(255, 0, 0))
image.save('result.png','PNG')
image.show()