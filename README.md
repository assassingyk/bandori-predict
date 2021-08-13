# bandori-predict

适用hoshino的邦邦档线预测插件

本体档线预测部分代码来自[Rinko-Predict-Python](https://github.com/Electronicute/Rinko-Predict-Python)，活动与档线数据来自besdori

进行了少量魔改以适应hoshino插件调用需要）

因为用的人不多所以没太仔细改，功能比较粗糙，底图什么的也没换）

感谢[CYDXDianXian](https://github.com/CYDXDianXian)大佬帮助完善

## 安装方法

1. 将bandori_predict文件夹放到`HoshinoBot/hoshino/modules`目录下

2. 将resources文件夹放到imgbasePath目录下，默认位置`HoshinoBot/res/img/bangdreampic/predict`，可自行在init.py修改

3. 安装依赖   `pip install -r requirements.txt`

4. 在`HoshinoBot/hoshino/config/__bot__.py`中添加bandori_predict模块

5. 重启Hoshino


## 指令列表

- `<邦邦档线/预测线/ycx> 50/100/300/500/1k/2k`  邦邦进行中活动对应档线预测，未提供具体档线时默认预测1k线

## to do

- 增加往期活动档线数据查询
- 增加区服切换
- 将数据拉取部分改为异步（虽然影响应该不大）
- 更新底图部分已过时信息 ~~(RIP bandoriAPI)~~
