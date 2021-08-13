import os
import hoshino.modules.bandori_predict.DataRef as DataRef
import hoshino.modules.bandori_predict.GraphDraw as GraphDraw
import time,requests

from traceback import format_exc

from hoshino import Service, R
from hoshino.typing import *
from hoshino.config import RES_DIR

imgbasePath=os.path.join(os.path.expanduser(RES_DIR), 'img','bangdreampic','predict')
basePath= os.path.join(os.path.abspath(os.path.realpath(os.path.dirname(__file__))), 'data')

#make sure of Dir is create
if not os.path.exists(imgbasePath):
    os.mkdir(imgbasePath)
if not os.path.exists(basePath):
    os.mkdir(basePath)
for areacode in range(0,5):
    if not os.path.exists(os.path.join(basePath,str(areacode))):
        os.mkdir(os.path.join(basePath, str(areacode)))

sv_help = '''
[<邦邦档线/预测线/ycx>50/100/300/500/1k/2k] 邦邦当期活动档线预测，数据来自besdori
'''.strip()

sv = Service('bangdream-predict', help_=sv_help)

areacode=3
TogglePara = True
Bnum=0 

@sv.on_prefix('邦邦档线', '预测线', 'ycx')
async def bang_predict(bot, ev):
    key = ev.message.extract_plain_text().strip()
    ranktype=-1
    if not key:
        msg = "未指定档线，将发送全部档线预测……"
        await bot.send(ev, f"{msg}")
    else:
        if key in ['50','五十线','50线']:
            ranktype=0
        elif key in ['100','百线','100线']:
            ranktype=1
        elif key in ['300','三百线','300线']:
            ranktype=2
        elif key in ['500','五百线','500线']:
            ranktype=3
        elif key in ['1000','千线','1k']:
            ranktype=4
        elif key in ['2000','两千线','2k']:
            ranktype=5
        else:
            await bot.send(ev, "档线输入错误，请输入50/100/300/500/1k/2k")
            return

    try:
        hd={'User_Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
        url='https://bestdori.com/api/events/all.3.json'

        Dict=requests.get(url,headers=hd, timeout=5).json()

        now=int(time.time())*1000
        print(now)
        enum=0
        for event in Dict:
            if Dict[event]['startAt'][areacode] is None:
                continue
            start=int(Dict[event]['startAt'][areacode])
            end=int(Dict[event]['endAt'][areacode])
            if end>now and start<now:
                enum=int(event)
                await bot.send(ev, f"当前活动：{int(event)}期，{Dict[event]['eventName'][areacode]}")
                break
        if enum==0:
            await bot.send(ev, "当前无活动！")
            return
        await bot.send(ev, "正在预测，请稍候……")
        DataRef.GetDataStorage(basePath,areacode,False,enum,RankType=ranktype)
    except Exception as e1:
        print('Analyse Fail!',format_exc())
        await bot.finish(ev, f"预测失败……{format_exc()}")
    await bot.send(ev, "预测结束，正在生成结果……")
    try:
        GraphDraw.GetDataPic(areacode,imgbasePath,basePath,False,enum,RankType=ranktype)   #use file to Pic
    except Exception as e2:
        print('Draw Fail!',format_exc())
        await bot.finish(ev, f"生成失败……{format_exc()}")

    #print('操作完成时间',datetime.datetime.fromtimestamp(time.time()).strftime("%m/%d %H:%M:%S"))
    if ranktype in range(0,6):
        if ranktype==0:
            await bot.send(ev, R.img('bangdreampic/predict/e50.png').cqcode)
        elif ranktype==1:
            await bot.send(ev, R.img('bangdreampic/predict/e100.png').cqcode)
        elif ranktype==2:
            await bot.send(ev, R.img('bangdreampic/predict/e300.png').cqcode)
        elif ranktype==3:
            await bot.send(ev, R.img('bangdreampic/predict/e500.png').cqcode)
        elif ranktype==4:
            await bot.send(ev, R.img('bangdreampic/predict/e1k.png').cqcode)
        elif ranktype==5:
            await bot.send(ev, R.img('bangdreampic/predict/e2k.png').cqcode)
    else:
        await bot.send(ev, R.img('bangdreampic/predict/e50.png').cqcode)
        await bot.send(ev, R.img('bangdreampic/predict/e100.png').cqcode)
        await bot.send(ev, R.img('bangdreampic/predict/e300.png').cqcode)
        await bot.send(ev, R.img('bangdreampic/predict/e500.png').cqcode)
        await bot.send(ev, R.img('bangdreampic/predict/e1k.png').cqcode)
        await bot.send(ev, R.img('bangdreampic/predict/e2k.png').cqcode)
