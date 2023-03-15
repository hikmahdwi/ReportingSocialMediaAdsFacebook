import click
import requests
from facebook_api import token, base, user_id
import itertools 
from datetime import datetime, timedelta
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
parameters = {'access_token':token}

def request_campaign(id_akun, mid, startDate, endDate):
    all_id_campaign = []
    for i in id_akun:
        node = "{}/campaigns?fields=name".format(i)
        print('ini node')
        print(node)
        url = base + node
        obj = requests.get(url, params=parameters).json()
        campaign = obj['data']
        all_id_campaign.append(campaign)

    id_based_org = []
    for i in all_id_campaign:
        for x in i:
            if mid in x['name']:
                id_based_org.append(x['id'])

    # sys.exit()
    row_data_campaign = []
    for i in id_based_org:
        node = "{}/insights?fields=impressions,reach,clicks,spend&time_increment=1&time_range[since]={}&time_range[until]={}".format(i, startDate, endDate)
        url = base + node
        req = requests.get(url, params=parameters).json()
        # print(i)
        # print(req)
        # sys.exit()
        # print(req['data'])
        row_data_campaign.append(req['data'])
    # row_data_campaign
    data = list(itertools.chain.from_iterable(row_data_campaign))
    
    df = pd.DataFrame(data)
    df_type = df.astype({"impressions": int, "reach": int, "clicks": int, "spend":int})
    grb_a = df_type[["impressions", "reach", "clicks", "spend", "date_start"]]
    df_a = grb_a.groupby(by=["date_start"]).sum()
    df_a = df_a.reset_index()
    return df_a

def get_campaign_orgz(id_akun, mid, startDate, endDate):
    if startDate == '' or endDate == '':
        data = request_campaign(id_akun, mid, last_month, yesterday)
        return data
    else:
        data =  request_campaign(id_akun, mid, startDate, endDate)
        return data

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def aggregation_metrics(id_akun, mid, startDate, endDate):
    data = get_campaign_orgz(id_akun, mid, startDate, endDate)
    impressions = human_format(data['impressions'].sum())
    reach = human_format(data['reach'].sum())
    click = human_format(data['clicks'].sum())
    cpc = human_format(data['spend'].sum() / data['clicks'].sum())
    data = {'impressions':impressions, 'reach':reach, 'click':click, 'cpc':cpc}
    return data

def table_metrics(id_akun, mid, startDate, endDate):
    data = get_campaign_orgz(id_akun, mid, startDate, endDate)
    data = data.sort_values(by='date_start',ascending=False)
    cost_total = sum(data['spend'])
    data["date_start"] = pd.to_datetime(data["date_start"]).dt.strftime('%d %b, %Y')
    data['cpc'] = data['spend'] / data['clicks']
    data['ctr'] = (data['clicks'] / data['impressions'])*100
    data = data.to_json(orient = 'records')
    data = json.loads(data)
    tbl = {'tbl':data, 'total-cost':cost_total}
    return tbl

def impression_reach(id_akun,mid, startDate, endDate):
    data = get_campaign_orgz(id_akun, mid, startDate, endDate)
    data = {'impressions':(data['impressions']).tolist(), 'reach':(data['reach']).tolist(), 'date':(data['date_start']).tolist()}
    return data

def click_ratio(id_akun,mid, startDate, endDate):
    data = get_campaign_orgz(id_akun, mid, startDate, endDate)
    data['ctr'] = (data['clicks'] / data['impressions'])*100
    data = {'ctr':(data['ctr']).tolist(), 'date':(data['date_start']).tolist()}
    return data

def cost_spend(id_akun,mid, startDate, endDate):
    data = get_campaign_orgz(id_akun, mid, startDate, endDate)
    spend = (data['spend']).tolist()
    cost = []
    total = 0
    for i in spend:
        total = total + i
        cost.append(total)
    data = {'cost':cost, 'date':(data['date_start']).tolist()}
    return data

def click_cpc(id_akun,mid, startDate, endDate):
    data = get_campaign_orgz(id_akun, mid, startDate, endDate)
    data['cpc'] = data['spend'] / data['clicks']
    click = (data['clicks']).tolist()
    cpc = (data['cpc']).tolist()
    data = {'click':click, 'cpc':cpc, 'date':(data['date_start']).tolist()}
    return data

def location(id_akun,mid, startDate, endDate):
    all_id_campaign = []
    for i in id_akun:
        node = "{}/campaigns?fields=name".format(i)
        url = base + node
        obj = requests.get(url, params=parameters).json()
        campaign = obj['data']
        all_id_campaign.append(campaign)

    id_based_org = []
    for i in all_id_campaign:
        for x in i:
            if mid in x['name']:
                id_based_org.append(x['id'])
    
    row_data_campaign = []
    if startDate == "" or endDate == "":
        for i in id_based_org:
            node = "{}/insights?fields=impressions&time_range[since]={}&time_range[until]={}&breakdowns=region".format(i, last_month, yesterday)
            url = base + node
            req = requests.get(url, params=parameters).json()
            row_data_campaign.append(req['data'])
        data = list(itertools.chain.from_iterable(row_data_campaign))
    else:
        for i in id_based_org:
            node = "{}/insights?fields=impressions&time_range[since]={}&time_range[until]={}&breakdowns=region".format(i, startDate, endDate)
            url = base + node
            req = requests.get(url, params=parameters).json()
            row_data_campaign.append(req['data'])
        data = list(itertools.chain.from_iterable(row_data_campaign))

    df = pd.DataFrame(data)
    df_type = df.astype({"impressions": int})
    df_a = df_type.groupby(by=["region"]).sum()
    df_a['region'] = (df['region']).unique()
    df = df_a.sort_values(by=['impressions'], ascending=False)
    region = ((df['region'])).tolist()
    impressions = (df['impressions']).tolist()
    data = {'region':region, 'impressions':impressions}
    return data

def genderRequset(id_akun,mid, startDate, endDate):
    all_id_campaign = []
    for i in id_akun:
        node = "{}/campaigns?fields=name".format(i)
        url = base + node
        obj = requests.get(url, params=parameters).json()
        # print(obj)
        # sys.exit()
        campaign = obj['data']
        all_id_campaign.append(campaign)

    id_based_org = []
    for i in all_id_campaign:
        for x in i:
            if mid in x['name']:
                id_based_org.append(x['id'])

    row_data_campaign = []
    if startDate == '' or endDate == '':
        for i in id_based_org:
            node = "{}/insights?fields=impressions&time_range[since]={}&time_range[until]={}&breakdowns=age,gender".format(i, last_month, yesterday)
            url = base + node
            req = requests.get(url, params=parameters).json()
            row_data_campaign.append(req['data'])
    else:
        for i in id_based_org:
            node = "{}/insights?fields=impressions&time_range[since]={}&time_range[until]={}&breakdowns=age,gender".format(i, startDate, endDate)
            url = base + node
            req = requests.get(url, params=parameters).json()
            row_data_campaign.append(req['data'])

    data = list(itertools.chain.from_iterable(row_data_campaign))
    df = pd.DataFrame(data)

    return df

def age_gender(id_akun,mid, startDate, endDate):
    df = genderRequset(id_akun,mid, startDate, endDate)
    df = df[df["gender"].str.contains("unknown") == False]
    df = df[["age", "gender", "impressions"]]
    df_type = df.astype({"impressions": int})
    df_a = df_type.groupby(by=["age", "gender"]).sum()
    df_a = df_a.reset_index()
    male = df_a[df_a["gender"].str.contains("female") == False]
    female = df_a[df_a["gender"].str.contains("female") == True]
    data = {'female':(female['impressions']).tolist(), 'male':(male['impressions']).tolist(), 'age':(male['age']).tolist()}
    return data

def gender_perc(id_akun,mid, startDate, endDate):
    df = genderRequset(id_akun,mid, startDate, endDate)
    df = df[df["gender"].str.contains("unknown") == False]
    df_type = df.astype({"impressions": int})
    df = df_type[['gender', 'impressions']]
    df_a = df.groupby(by=['gender']).sum()
    df = df_a.reset_index()
    impressions = (df['impressions']).tolist()
    gender = (df['gender']).tolist()
    data = {'impressions':impressions, 'gender':gender}
    return data