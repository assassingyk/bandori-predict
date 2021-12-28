import os
import hoshino.modules.bandori_predict.DataRef as DataRef
import hoshino.modules.bandori_predict.GraphDraw as GraphDraw
import time,requests

from traceback import format_exc

from hoshino import Service, R
from hoshino.typing import *

from hoshino.modules.bandori_predict.config import imgbasePath,basePath,areacode

#make sure of Dir is create
if not os.path.exists(imgbasePath):
    os.mkdir(imgbasePath)
if not os.path.exists(basePath):
    os.mkdir(basePath)
for area in range(0,5):
    if not os.path.exists(os.path.join(basePath,str(area))):
        os.mkdir(os.path.join(basePath, str(area)))

sv_help = '''
[<邦邦档线/预测线/ycx>50/100/300/500/1k/2k] 邦邦当期活动档线预测，数据来自besdori
[<邦邦档线/预测线/ycx><国服/日服/台服/韩服/国际服>50/100/300/500/1k/2k] 指定预测服务器
'''.strip()

sv = Service('bangdream-predict', help_=sv_help)

def load_areacode(string=None):
    code_dict = {"日服":0, "国际服":1, "台服":2, "国服":3, "韩服":4}
    if string and string in code_dict.keys():
        return code_dict[string]
    else:
        return areacode

#@sv.on_prefix(('邦邦档线', '预测线', 'ycx'))
@sv.on_rex(r'^(邦邦档线|邦邦预测|ycx|预测线)( )?(国服|日服|韩服|台服|国际服)?(.+)?')
async def bang_predict(bot, ev):
    #key = ev.message.extract_plain_text().strip()
    match = ev["match"]
    key = match.group(4).strip()
    areacode = load_areacode(match.group(3).strip())
    ranktype=-1
    if not key:
        msg = "未指定档线，默认预测1k线……"
        await bot.send(ev, f"{msg}")
        ranktype=4
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
        #print(now)
        enum=0
        #print(areacode)
        for event in Dict:
            if Dict[event]['startAt'][areacode] is None:
                continue
            start=int(Dict[event]['startAt'][areacode])
            end=int(Dict[event]['endAt'][areacode])
            if end>now and start<now:
                #print(Dict[event])
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

