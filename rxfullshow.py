#!/usr/bin/python3

# Display users information on Akatsuki
# Author: Murmurtwins

from PIL import Image,ImageDraw,ImageFont,ImageFilter
from io import BytesIO
import requests, json, time, math

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
font2=ImageFont.truetype('GOTHIC.ttf',48)
font21=ImageFont.truetype('GOTHIC.ttf',36)
font22=ImageFont.truetype('GOTHIC.ttf',24)
font23=ImageFont.truetype('GOTHIC.ttf',38)
font24=ImageFont.truetype('GOTHIC.ttf',30)
font3=ImageFont.truetype('seguihis.ttf',48)
font31=ImageFont.truetype('seguihis.ttf',17)
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

draw.text((341,415),format(SS+SSH,','),font=font24,fill=(255,255,255))
draw.text((506,415),format(S+SH,','),font=font24,fill=(255,255,255))
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
draw.text((302,367),str(level_int)+' ('+str(format(level_res,'0.3f'))+'%)',font=font24,fill=(255,255,255))
t1=time.strftime("%y-%m-%d %H:%M:%S",time.localtime())
draw.text((804,430),t1,font=font31,fill=(255,0,0))

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

image.save('result.png','PNG')
image.show()
