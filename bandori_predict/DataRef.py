"""system Import"""
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
"""custom APIs"""
import os
import hoshino.modules.bandori_predict.getData as getData
import hoshino.modules.bandori_predict.getPred as getPred
import hoshino.modules.bandori_predict.outData as outData
#import requests
#import json
#import time,datetime
from traceback import format_exc

def __Main__RunPred(filepath,enum,etp,AreaCode=3,pred_Length=3,gamma_Threshold=1):
    '''this is the EntryPoint of the specific NLD_Core
    :filepath ~ a path of Content should be Save :like "D:/asd/"
        you must keep the last slash(/) to keep the code running
    :enum ~ it's the Event Number 
    :AreaCode ~ for which is stands for Services Region 
        and which 0-4 is for jp:0/en:1/tw:2/cn:3/kr:4
        for default is cn:3
    :etp ~ it's EventType which is correspond to 0-2 is 100,1k,2k
    :pred_Length ~ is the corr of predict which the determinator of LLB
        this represent the LBSB (left Block Span Block)'s 
        RCPD (Rest Control Position Determinator)
        it's the determinator of whole predict
        don't change it if you don't konw what you're doing 
        please leave at 3-6
    :gamma_Threshold ~ is the Threshold of the final predict Threshold
        if you don't know what will happen please do not change it,
        as we test it's best to leave it at 1 or 2
    '''
    
    #this file dir needs to create as two parameter which in flat mode
    fp = os.path.join(filepath, str(AreaCode), f"e{str(enum)}")
    if not os.path.exists(fp):
        os.mkdir(fp)
    fp = os.path.join(fp, f"t{str(etp)}")
    if not os.path.exists(fp):
        os.mkdir(fp)

    fir = pd.DataFrame()
    #getData using BAC and Bestdori Database
    fir = getData.get(fp,enum,etp,AreaCode)
    #predict Data
    mid = getPred.PreProcessData(fp,enum,etp,fir,pred_Length,gamma_Threshold) #middle ware of predict
    #Outpu Data
    outData.OutPut(fp,enum,etp,mid)
    return True

def GetDataStorage(dirs,AreaCode=3,PredNow=True,enum=0,RankType=-1):
    '''This is the Core Main entry of the Predict Function for All
    :AreaCode ~ is default for cn which country code is ref as (0:jp/1:en/2:tw/3:cn/4:kr)
    :dirs ~ controls of Whole Predict File Puts, In General Which this should be BASE DIR of the Progress
    :PredNow ~ unless Debug, Please DO NOT CHANGE this Boolean Value, which will controls the Prediction for Pic Output
        **** if which you switch the PredNow to False hense you dont know the following value
        :Benum ~ is the EventNumber you want to predict
        ~ Attention which this is the RANKTYPE will get all parameter which (0-2)
    '''
    
    if RankType in range(0,6):
        try:
            __Main__RunPred(dirs,enum,RankType,AreaCode,3,1)
            #this is a predict-ivity reference, Which is Encoded in this frame of function.
        except:
            print("ON Main Func,",enum,"->",RankType,"'s Pred is Fail",format_exc())
        
    else:
        for RankType in range(0,6):
            try:
                __Main__RunPred(dirs,enum,RankType,AreaCode,3,1)
                #this is a predict-ivity reference, Which is Encoded in this frame of function.
            except:
                print("ON Main Func,",enum,"->",RankType,"'s Pred is Fail",format_exc())
