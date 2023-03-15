import requests
from facebook_api import token, base, user_id
import itertools 
from datetime import datetime, timedelta
from fanpage import tgl_list
import pandas as pd
import json
import sys

parameter = {'access_token':token}
def get_id_account():
    node = "{}/adaccounts?fields=name".format(user_id)
    url = base + node
    obj = requests.get(url, params=parameter).json()
    akun_id = obj['data']
    return akun_id

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
last_month = (datetime.now() - timedelta(30)).strftime('%Y-%m-%d')

def listAllCampaign():
    id_akun = get_id_account()
    all_id_campaign = []
    for i in id_akun:
        if i['id'] == 'act_679657615950119' or i['id'] == 'act_350108546929466':
            continue
        else:
            node = "{}/campaigns?fields=name,start_time,stop_time,status&limit=50".format(i['id'])
            url = base + node
            obj = requests.get(url, params=parameter).json()
            campaign = obj['data']
            all_id_campaign.append(campaign)

    data = list(itertools.chain.from_iterable(all_id_campaign))
    return data

def aggregationAds(id_campaign, startDate, endDate):
    print("ini id campaig")
    print(id_campaign)
    print('ini akan startdate')
    print(startDate)
    print("ini endDate")
    print(endDate)
    node = "{}/ads?fields=name".format(id_campaign)
    url = base + node
    obj = requests.get(url, params=parameter).json()
    print(obj)
    # listAd = obj['data']
    print("listAd")
    # print(listAd)
    sys.exit()
    adInsights = []
    if startDate == "" or endDate == "":
        for i in listAd:
            node = "{}/insights?fields=impressions,reach,clicks,spend,campaign_name".format(i['id'])
            url = base + node
            obj = requests.get(url, params=parameter).json()
            ads = obj['data']
            print(ads)
            adInsights.append(ads)
            print("ini tdk ad tanggalnya")
            print(adInsights)
    else:
        for i in listAd:
            node = "{}/insights?fields=impressions,reach,clicks,spend,campaign_name&time_range[since]={}&time_range[until]={}".format(i['id'], startDate, endDate)
            url = base + node
            obj = requests.get(url, params=parameter).json()
            ads = obj['data']
            adInsights.append(ads)
            print("ini ad tanggalnya")
            print(adInsights)
        
    data = list(itertools.chain.from_iterable(adInsights))
    print("ini aggregations")
    print(data)
    df_type = pd.DataFrame(data)
    df = df_type.astype({'impressions':int, 'clicks':int, 'reach':int, 'spend':int})
    agg_impressions = sum(df['impressions'])
    agg_reach = sum(df['reach'])
    agg_click = sum(df['clicks'])
    agg_cpc = sum(df['spend']) / agg_click
    agg_cpc = "{:.2f}".format(agg_cpc)

    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    data = {'agg_impressions':human_format(agg_impressions), 'agg_reach':human_format(agg_reach),
            'agg_click':human_format(agg_click), 'agg_cpc':agg_cpc, 'campaign_name':df_type['campaign_name'][0]}
    return data

def adsBreakBodyAssets(id_campaign, startDate, endDate):
    node = "{}/ads?fields=name".format(id_campaign)
    url = base + node
    obj = requests.get(url, params=parameter).json()
    listAd = obj['data']
    adInsights = []

    if startDate == "" or endDate == "":
        for i in listAd:
            node = "{}/insights?fields=impressions,clicks,cpc,reach,ctr,spend&breakdowns=body_asset".format(i['id'])
            url = base + node
            obj = requests.get(url, params=parameter).json()
            ads = obj['data']
            adInsights.append(ads)
    else:
        for i in listAd:
            node = "{}/insights?fields=impressions,clicks,cpc,reach,ctr,spend&breakdowns=body_asset&time_range[since]={}&time_range[until]={}".format(i['id'], startDate, endDate)
            url = base + node
            obj = requests.get(url, params=parameter).json()
            ads = obj['data']
            adInsights.append(ads)
    data = list(itertools.chain.from_iterable(adInsights))
    
    return data

def adsBreakTitleAssets(id_campaign, startDate, endDate):
    node = "{}/ads?fields=name".format(id_campaign)
    url = base + node
    obj = requests.get(url, params=parameter).json()
    listAd = obj['data']
    adInsights = []
    if startDate == "" or endDate == "":
        for i in listAd:
            node = "{}/insights?fields=impressions,clicks,cpc,reach,ctr,spend&breakdowns=title_asset".format(i['id'])
            url = base + node
            obj = requests.get(url, params=parameter).json()
            ads = obj['data']
            adInsights.append(ads)
    else:
        for i in listAd:
            node = "{}/insights?fields=impressions,clicks,cpc,reach,ctr,spend&breakdowns=title_asset&time_range[since]={}&time_range[until]={}".format(i['id'], startDate, endDate)
            url = base + node
            obj = requests.get(url, params=parameter).json()
            ads = obj['data']
            adInsights.append(ads)
    
    data = list(itertools.chain.from_iterable(adInsights))
    print(data)
    return data
    
