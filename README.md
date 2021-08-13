# bandori-predict

适用hoshino的邦邦档线预测插件

本体档线预测部分代码来自[Rinko-Predict-Python](https://github.com/Electronicute/Rinko-Predict-Python)，活动与档线数据来自besdori

进行了少量魔改以适应hoshino插件调用需要）

因为用的人不多所以没太仔细改，功能比较粗糙，底图什么的也没换）

## 安装方法

1. 将bandori_predict文件夹放到`HoshinoBot/hoshino/modules`目录下

2. 将resources文件夹放到`HoshinoBot/res/img/bangdreampic/predict/resources`目录下

3. 安装resources文件夹内的两个字体文件

4. 安装依赖

   `pip install -r requirements.txt`

5. 在...HoshinoBot/hoshino/config/bot.py中添加bandori_predict模块

6. 重启Hoshino

   `cd HoshinoBot`

   `python run.py`

## 指令列表

- `邦邦档线 100/1k/2k`  邦邦进行中活动对应档线预测，未提供具体档次时三档全部预测一次

## to do

- 增加往期活动档线数据查询
- 增加区服切换
