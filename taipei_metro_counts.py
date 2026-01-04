#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 00:24:24 2023

@author: fattabby
"""
import wget
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
#now=datetime.now()
#data_202301=pd.read_csv("/home/fattabby/下載/臺北捷運每日分時各站OD流量統計資料_202301.csv")
#data_202302=pd.read_csv("/home/fattabby/下載/臺北捷運每日分時各站OD流量統計資料_202301.csv")
#McKinney, pp.354
start=datetime.date(datetime(2023,1,1)) #最早的資料是2017,1,1
#end=now.year,now.month,now.day
end=datetime.date(datetime.now())


location=os.path.expanduser("~/Metro_Downloads/")
months=pd.date_range(start,end,freq="MS")
target_datasets=[]
#%%
for a in months:
    if a.month<10:
        serial=str(a.year)+"0"+str(a.month)        
        #globals()['data_'+str(a.year)+"0"+str(a.month)] = pd.read_csv()
    else:
        serial=str(a.year)+str(a.month)
        #globals()['data_'+str(a.year)+str(a.month)] = "A"           
    link="http://tcgmetro.blob.core.windows.net/stationod/臺北捷運每日分時各站OD流量統計資料_{}.csv".format(serial)
    print("downloading", link) #這裡主要是用來Debug    
    #https://www.golinuxcloud.com/python-get-home-directory/
    #https://www.programcreek.com/python/example/83386/wget.download
    try:
        filename=wget.download(link, out=location)
        #globals()['data_'+serial] = pd.read_csv(filename) #理論上要一氣呵成，但是在比較弱的電腦好像會把系統搞掛
    except Exception as e:
        print("錯誤訊息:", e)
#%%    
for a in months:
    if a.month<10:
        serial=str(a.year)+"0"+str(a.month)        
        #globals()['data_'+str(a.year)+"0"+str(a.month)] = pd.read_csv()
    else:
        serial=str(a.year)+str(a.month)
    try:
        print("dealing with", "臺北捷運每日分時各站OD流量統計資料_{}.csv".format(serial))
        globals()['data_'+serial] = pd.read_csv(location+"臺北捷運每日分時各站OD流量統計資料_{}.csv".format(serial))
        target_datasets.append(['data_'+serial])
        print("dealt with", "臺北捷運每日分時各站OD流量統計資料_{}.csv".format(serial))
    except Exception as e:
        print("錯誤訊息:", e)
#%%
# =============================================================================
# for i in target_datasets:
#     print([i])
#     data=pd.concat([i])
# =============================================================================
data=pd.concat([data_202301, data_202302, data_202303])
stations=data["進站"].unique() #若你想知道該資料集包含哪些車站時候用
print(stations)
sum=data_202301.shape[0]+data_202302.shape[0]+data_202303.shape[0] #檢核列數是否相符用
if sum==data.shape[0]:
    print("shape equivalent")
    del data_202301, data_202302, data_202303
else:
    print("shape not equivalent")
data2=data.set_index("日期")
del data
Qizhang_in=data2[data2["進站"]=="七張"]
Qizhang_in2=Qizhang_in.groupby(['日期'])['人次'].sum()
Qizhang_out=data2[data2["出站"]=="七張"]
Qizhang_out2=Qizhang_out.groupby(['日期'])['人次'].sum()
del Qizhang_in, Qizhang_out
#Qizhang_inrush=data2[(data2["進站"]=="七張")&(data2["時段"]<9)&(6<data2["時段"])]
Shisizhang_in=data2[data2["進站"]=="十四張"]
#Shisizhang_inrush=data2[(data2["進站"]=="十四張")&(data2["時段"]<9)&(6<data2["時段"])]
Shisizhang_in2=Shisizhang_in.groupby(['日期'])['人次'].sum()
Shisizhang_out=data2[data2["出站"]=="十四張"]
Shisizhang_out2=Shisizhang_out.groupby(['日期'])['人次'].sum()
del Shisizhang_in, Shisizhang_out
#['rebounds'].nunique()
#plt.figure(figsize=(10,6))
#plt.xlabel("index")
#plt.ylabel("value")
#plt.title("A simple plot")
#plt.plot(Shisizhang_in2.index, Shisizhang_in2, Qizhang_in2)
#注意你之前幹的事：data2=data.set_index("日期")，所以抓日期的標籤時要往這裡抓
#plt.savefig("fig3.svg",dpi=350) 

XDOffice_in=data2[data2["進站"]=="新店區公所"]
XDOffice_in2=XDOffice_in.groupby(['日期'])['人次'].sum()
#plt.plot(XDOffice_in2)
XDOffice_out=data2[data2["出站"]=="新店區公所"]
XDOffice_out2=XDOffice_out.groupby(['日期'])['人次'].sum()    
del XDOffice_in, XDOffice_out

#%%    
fig, ax = plt.subplots(layout='constrained',figsize=(16,6))
#,sharey=True,sharex=True 是在另外一種型態的子圖才會用到，如McKinney, pp.287
fig.subplots_adjust(right=0.75)
twin1 = ax.twinx()
index=Shisizhang_in2.index
p1,=ax.plot(index,
            Shisizhang_in2,
            "yellow",
            label="Shisizhang Login")
#要領：須將日期轉成index才不會變成密密麻麻很可怕的東西
p2,=twin1.plot(index,
               Qizhang_in2,
               "r-",
               label="Qizhang Login")
twin2 = ax.twinx()
p3,=twin2.plot(index, #Remember to add comma after p3
               XDOffice_in2,
               "b-",
               label="Xindian Dist. Office Login")
#p1=ax.plot
twin2.spines.right.set_position(("axes", 1.05))
ax.legend(handles=[p1, p2, p3])
ax.set_title("Comparisons Login")
plot_1=plt.savefig("figs.svg",dpi=350) 
plt.show()
#%%    
fig, ax = plt.subplots(layout='constrained',figsize=(16,6))
fig.subplots_adjust(right=0.75)
twin1 = ax.twinx()
#index=Shisizhang_out2.index
p1,=ax.plot(index,
            Shisizhang_out2,
            "yellow",
            label="Shisizhang Logout")
#要領：須將日期轉成index才不會變成密密麻麻很可怕的東西
p2,=twin1.plot(index,
               Qizhang_out2,
               "r-",
               label="Qizhang Logout")
twin2 = ax.twinx()
p3,=twin2.plot(index, #Remember to add comma after p3
               XDOffice_out2,
               "b-",
               label="Xindian Dist. Office Logout")
#p1=ax.plot
twin2.spines.right.set_position(("axes", 1.05))
ax.legend(handles=[p1, p2, p3])
ax.set_title("Comparisons Logout")
plot_2=plt.savefig("figs2.svg",dpi=350) 
plt.show()

#%%
plt.figure(layout='constrained',figsize=(16,6))
plt.plot(Shisizhang_in2)
#plt.set_title("Comparisons Out")
plt.title("Shisizhang login")
#plt.legend()
plot_3=plt.savefig("figs3.svg",dpi=350) 
plt.show()
