#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 09:53:47 2026

@author: fattabby
功能：製作日本各都道府縣基督宗教人口/地區密度圖表的資料預備
"""
import os
import pandas as pd

if os.name=="posix":
    print("you are using Linux or Mac")
    pathname = '/home/{}/Nextcloud/japan_religion/'.format(os.getlogin())
else:
    print("you are using Windows")
    pathname = 'C:/Users/{}/Nextcloud/japan_religion/'.format(os.getlogin())
#各都道府縣宗教人數
#宗教統計調査 令和６年度 | ファイル | 統計データを探す | 政府統計の総合窓口
#https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040232603&fileKind=0

os.chdir(pathname)
data=pd.read_excel("r06sr0202.xls",sheet_name=3,skiprows=3)
stat_date=data.iloc[0,-1]
#data=pd.read_excel("r06sr0202.xls",sheet_name=3,skiprows=3)
#data=pd.read_csv("r06sr0202.csv",encoding="utf-8")
#stat_date=data.iloc[3,-1]
data=pd.read_excel("r06sr0202.xls",sheet_name=3,skiprows=3,header=4)
data=data[['人.6', '単位.1', 'Unnamed: 22']]
data.columns = ["populations_christ", "pref_name", "pref_code"]
data=data.iloc[1:data.shape[0]-1]
#data["Country"]="JP"
data_no=data['pref_code'].astype(str).str.zfill(2)
#data_no=data['Unnamed: 22']
data["ISO_code"]="JP"+data_no
data=data[["pref_name", "pref_code","ISO_code","populations_christ"]]

#行政區大小與人口密度（抓英文維基百科表格用Calc後製成csv：維基百科似乎有防爬功能）
data_wiki=pd.read_csv("japan_population.csv",encoding="utf-8")
data_wiki=data_wiki[['iso_code','population_concensus','area']]

#在QGIS使用的日本行政區劃shapefile
#source homepage: https://data.humdata.org/dataset/cod-xa-jpn/resource/f82faadf-a608-42cf-ae15-75ce672d7e69
#source: https://data.humdata.org/dataset/cod-xa-jpn/resource/f82faadf-a608-42cf-ae15-75ce672d7e69#:~:text=jpn%5Fadm%5F2019%5FSHP%2Ezip,-URL


#原ISO CODE會有"-"符號，但是為方便與在QGIS的shapefile使用故拿掉
data_wiki["iso_code"]=data_wiki["iso_code"].str.replace(" ","").str.replace("-","")

#欄位以ISO CODE為Key串接整併
data=data.join(data_wiki.set_index("iso_code"), on="ISO_code")
data["christ_ratio_by_population"]=data["populations_christ"]/data["population_concensus"]
#data["christ_ratio_by_population_pct"]=data["populations_christ"]/data["population_concensus"]*100
data["christ_ratio_by_area"]=data["populations_christ"]/data["area"]
#data["christ_ratio_by_area_pct"]=data["populations_christ"]/data["area"]*100
data.to_csv("japan_christ_merged.csv")
