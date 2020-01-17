#!/usr/bin/python3

# Display users information on Akatsuki
# Author: Murmurtwins

from PIL import Image,ImageDraw,ImageFont,ImageFilter
from io import BytesIO
import requests, json, time, math, collections

def generate_stat(uid):
    result = json.loads(requests.get('https://akatsuki.pw/api/v1/users/rxfull?id={}'.format(uid)).text)

    level = result['std']['level']
    level_int = int(level)
    level_res = int(100 * (level - level_int))

    upp = count = bpk = 0
    rankdic, inf = collections.defaultdict(int), ''
    for page in range(1, 100):
        result2 = json.loads(requests.get('http://akatsuki.pw/api/v1/users/scores/best?mode=0&p={}&l=100&rx=1&id={}'.format(page, uid)).text)
        try:
            for item in range(0, 100):
                try:
                    ppitem = result2['scores'][item]['pp']
                    rankdic[result2['scores'][item]['rank']] += 1
                    if page == 10 and item == 99:
                        bpk = ppitem
                    upp += ppitem
                except IndexError:
                    count = (page - 1) * 100 + item
                    if count < 1000:
                        inf = '/'
                    break
        except TypeError:
            break

    image = Image.new('RGB', (951, 460), (255, 255, 255))
    font12 = ImageFont.truetype('{}ARLRDBD.ttf'.format(SKIN_DIC), 30) # PATH (SAME FOR BELOW)
    font21 = ImageFont.truetype('{}GOTHIC.ttf'.format(SKIN_DIC), 36) 
    font23 = ImageFont.truetype('{}GOTHIC.ttf'.format(SKIN_DIC), 38)
    font24 = ImageFont.truetype('{}GOTHIC.ttf'.format(SKIN_DIC), 30)
    font3 = ImageFont.truetype('{}seguihis.ttf'.format(SKIN_DIC), 48)
    font31 = ImageFont.truetype('{}seguihis.ttf'.format(SKIN_DIC), 17)
    font4 = ImageFont.truetype('{}inkfree.ttf'.format(SKIN_DIC), 30)
    imgtemp = Image.open("{}template2.png".format(SKIN_DIC)) # ----------------
    image.paste(imgtemp, (0, 0))

    draw = ImageDraw.Draw(image)
    draw.text((351, 25), result['username'], font=font21, fill=(0, 0, 0))
    draw.text((414, 64), '#{}'.format(result['std']['global_leaderboard_rank']), font=font3, fill=(0, 0, 0))
    draw.text((468, 117), str(result['std']['pp']), font=font23, fill=(54, 54, 54))
    draw.text((154, 175), 'Ranked Score', font=font4, fill=(0, 0, 0))
    draw.text((148, 222), 'Hit Accuracy', font=font4, fill=(0, 0, 0))
    draw.text((160, 271), 'Play Count', font=font4, fill=(0, 0, 0))
    draw.text((500, 271), 'Score Count', font=font4, fill=(0, 0, 0))
    draw.text((181, 319), 'Replays', font=font4, fill=(0, 0, 0))
    draw.text((440, 319), 'Unweighted PP', font=font4, fill=(0, 0, 0))
    draw.text((93, 366), 'Current Level', font=font4, fill=(0, 0, 0))
    draw.text((514, 366), 'BP1000', font=font4, fill=(0, 0, 0))
    draw.text((176, 417), 'Ranks', font=font4, fill=(0, 0, 0))
    draw.text((293, 417), 'S', font=font12, fill=(210, 105, 30))
    draw.text((298, 417), 'S', font=font12, fill=(210, 105, 30))
    draw.text((443, 417), 'S', font=font12, fill=(210, 105, 30))
    draw.text((593, 417), 'A', font=font12, fill=(0, 255, 0))

    draw.text((341, 415), format(rankdic["SS"] + rankdic["SSH"], ','), font=font24, fill=(0, 0, 0))
    draw.text((491, 415), format(rankdic["S"] + rankdic["SH"], ','), font=font24, fill=(0, 0, 0))
    draw.text((641, 415), format(rankdic["A"], ','), font=font24, fill=(0, 0, 0))

    draw.text((671, 269), format(count, ','), font=font24, fill=(0, 0, 0))
    draw.text((656, 317), format(upp, '0,.2f'), font=font24, fill=(0, 0, 0))

    if count < 1000:
        draw.text((641, 364), inf, font=font24, fill=(0, 0, 0))
    else:
        draw.text((641, 364), format(bpk, '0,.2f'), font=font24, fill=(0, 0, 0))

    draw.text((360, 174), format(result['std']['ranked_score'], ','), font=font24, fill=(0, 0, 0))
    draw.text((346, 222), format(result['std']['accuracy'], '0.2f') + '%', font=font24, fill=(0, 0, 0))
    draw.text((332, 269), format(result['std']['playcount'], ','), font=font24, fill=(0, 0, 0))
    draw.text((316, 318), format(result['std']['replays_watched'], ','), font=font24, fill=(0, 0, 0))
    draw.text((302, 367), '{} ({}%)'.format(level_int, level_res), font=font24, fill=(0, 0, 0))
    draw.text((804, 430), time.strftime("%y-%m-%d %H:%M:%S", time.localtime()), font=font31, fill=(255, 0, 0))

    BytesIOOBj = BytesIO()
    BytesIOOBj2 = BytesIO()
    BytesIOOBj.write(requests.get('https://a.akatsuki.pw/{}'.format(uid)).content)
    BytesIOOBj2.write(requests.get('https://www.countryflags.io/{}/shiny/64.png'.format(result['country'])).content)
    image.paste(Image.open(BytesIOOBj).resize((125, 125)), (166, 27))
    image.paste(Image.open(BytesIOOBj2).crop((2, 12, 62, 52)), (601, 80))
    draw.text((687, 64), '#{}'.format(result['std']['country_leaderboard_rank']), font=font3, fill=(0, 0, 0))

    bg = '{}{}s.PNG'.format('RESULT', uid)
    image.save(bg, 'PNG')
    return bg

if __name__=='__main__':
        generate_stat(USER_ID) # SUBSTITUTE USER_ID TO AN INTEGER
