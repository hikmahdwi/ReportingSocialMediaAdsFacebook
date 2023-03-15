from statistics import mode
import requests
import json
import pandas as pd
from facebook_api import token
from datetime import datetime, timedelta
from fanpage import tgl_list
from connection_sql import db
from model_table import modelIgFollower
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

base='https://graph.facebook.com/v12.0'

Session = sessionmaker(bind=db)
sesion = Session()

last_30 = (datetime.now() - timedelta(14)).strftime('%Y-%m-%d')
now = (datetime.now()).strftime('%Y-%m-%d')

def follower_account(id_ig, startDate, endDate):
    # nod = '/{}?fields=followers_count'.format(id_ig)
    # url=base+nod
    # parameters={'access_token':token}
    # obj=requests.get(url,params=parameters).json()
        
    # if obj['followers_count'] > 100:
    #     node='/{}/insights?metric=follower_count'.format(id_ig)
    #     url=base+node
    #     if startDate == "":
    #         parameters={'access_token':token, 'period':'day', 'since':last_30, 'until':now}
    #     else:
    #         parameters={'access_token':token, 'period':'day', 'since':startDate, 'until':endDate}
    #     obj=requests.get(url,params=parameters).json()
    #     if 'data' in obj:
    #         value = obj['data'][0]['values']
    #         follower = []
    #         for i in value :
    #             follower.append(i['value'])

    #         tanggal = []
    #         for x in range(len(obj['data'][0]['values'])):
    #             date = obj['data'][0]['values'][x]['end_time']
    #             tgl = date[:-14]
    #             tanggal.append(tgl)
    #     else:
    #         tanggal = tgl_list(startDate, endDate)
    #         follower = []
    # else :
    #     tanggal = tgl_list(startDate, endDate)
    #     follower = []
    # result = [tanggal, follower]

    if startDate and endDate != "":
        data = []
        for dt in sesion.query(modelIgFollower.date, func.max(modelIgFollower.followers_count))\
            .filter(modelIgFollower.ig_business==id_ig, modelIgFollower.date.between(startDate, endDate)).group_by(modelIgFollower.date):
            data.append(dt)
    else:
        data = []
        for dt in sesion.query(modelIgFollower.date, func.max(modelIgFollower.followers_count))\
            .filter(modelIgFollower.ig_business==id_ig, modelIgFollower.date.between(last_30, now)).group_by(modelIgFollower.date):
            data.append(dt)
    # print(data)
    tanggal = []
    follower = []
    for i in data:
        xx = list(i)
        xy = xx[0].strftime('%Y-%m-%d')
        xz = xx[1]
        tanggal.append(xy)
        follower.append(xz)
    result = [tanggal, follower]
    return result

def reach_account(id_ig, startDate, endDate):
    node='/{}/insights?metric=reach'.format(id_ig)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'period':'day', 'since':last_30, 'until':now}
    else:
        parameters={'access_token':token, 'period':'day', 'since':startDate, 'until':endDate}
    obj=requests.get(url,params=parameters).json()
    value = obj['data'][0]['values']
    follower = []
    for i in value :
        follower.append(i['value'])

    tanggal = []
    for x in range(len(obj['data'][0]['values'])):
        date = obj['data'][0]['values'][x]['end_time']
        tgl = date[:-14]
        tanggal.append(tgl)

    result = [tanggal, follower]
    return result

def impression_account(id_ig, startDate, endDate):
    node='/{}/insights?metric=impressions'.format(id_ig)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'period':'day', 'since':last_30, 'until':now}
    else:
        parameters={'access_token':token, 'period':'day', 'since':startDate, 'until':endDate}
    obj=requests.get(url,params=parameters).json()
    value = obj['data'][0]['values']
    follower = []
    for i in value :
        follower.append(i['value'])

    tanggal = []
    for x in range(len(obj['data'][0]['values'])):
        date = obj['data'][0]['values'][x]['end_time']
        tgl = date[:-14]
        tanggal.append(tgl)

    result = [tanggal, follower]
    return result

def profile_views(id_ig, startDate, endDate):
    node='/{}/insights?metric=profile_views'.format(id_ig)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'period':'day', 'since':last_30, 'until':now}
    else:
        parameters={'access_token':token, 'period':'day', 'since':startDate, 'until':endDate}
    obj=requests.get(url,params=parameters).json()
    value = obj['data'][0]['values']
    follower = []
    for i in value :
        follower.append(i['value'])

    tanggal = []
    for x in range(len(obj['data'][0]['values'])):
        date = obj['data'][0]['values'][x]['end_time']
        tgl = date[:-14]
        tanggal.append(tgl)

    result = [tanggal, follower]
    return result


def media_insights(id_ig):
    node='/{}/media?fields=id,caption,comments_count,thumbnail_url,media_url,like_count,permalink,insights.metric(engagement,impressions,reach)'.format(id_ig)
    url=base+node
    parameters={'access_token':token}
    obj=requests.get(url,params=parameters).json()
    nex = obj['paging']
    best_post = obj
    return obj['data'], nex

def next_prev(ur_):
    obj=requests.get(ur_).json()
    nex = obj['paging']
    return obj['data'], nex

def best_engagement(id_ig):
    node = '/{}/media?fields=id,caption,comments_count,thumbnail_url,media_url,like_count,insights.metric(engagement,impressions,reach)'.format(id_ig)
    node_pic = '/{}?fields=profile_picture_url'.format(id_ig)
    params = {'access_token':token}
    url = base + node
    pic_url = base + node_pic
    obj = requests.get(url, params=params).json()
    obj_url = requests.get(pic_url, params=params).json()
    data = []
    for i in obj['data'] :
        eng = i['insights']['data'][0]['values'][0]['value']
        impr = i['insights']['data'][1]['values'][0]['value']
        reac = i['insights']['data'][2]['values'][0]['value']
        if 'thumbnail_url' in i:
            if 'caption' in i:
                data.append({'like_count':i['like_count'], 'thumbnail_url':i['thumbnail_url'], 'comments_count':i['comments_count'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': i['caption']})
            else:
                data.append({'like_count':i['like_count'], 'thumbnail_url':i['thumbnail_url'], 'comments_count':i['comments_count'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': ''})
        else:
            if 'caption' in i:
                data.append({'like_count':i['like_count'], 'comments_count':i['comments_count'], 'media_url':i['media_url'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': i['caption']})
            else:
                data.append({'like_count':i['like_count'], 'comments_count':i['comments_count'], 'media_url':i['media_url'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': ''})
    datf = pd.DataFrame(data)
    # print(datf)
    largest_post = datf['engagement'].nlargest(n = 3, keep='all')
    idx_max = (largest_post.index).tolist()

    data = []
    for i in idx_max:
        best = datf.iloc[[i]]
        d = best.to_json(orient="records")
        data.append(d)

    engagement = []
    for i in data:
        js_data = json.loads(i)
        engagement.append(js_data)

    return engagement

def best_impressions(id_ig):
    node = '/{}/media?fields=id,caption,comments_count,thumbnail_url,media_url,like_count,insights.metric(engagement,impressions,reach)'.format(id_ig)
    node_pic = '/{}?fields=profile_picture_url'.format(id_ig)
    params = {'access_token':token}
    url = base + node
    pic_url = base + node_pic
    obj = requests.get(url, params=params).json()
    obj_url = requests.get(pic_url, params=params).json()
    data = []
    for i in obj['data'] :
        eng = i['insights']['data'][0]['values'][0]['value']
        impr = i['insights']['data'][1]['values'][0]['value']
        reac = i['insights']['data'][2]['values'][0]['value']
        if 'thumbnail_url' in i:
            if 'caption' in i:
                data.append({'like_count':i['like_count'], 'thumbnail_url':i['thumbnail_url'], 'comments_count':i['comments_count'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': i['caption']})
            else:
                data.append({'like_count':i['like_count'], 'thumbnail_url':i['thumbnail_url'], 'comments_count':i['comments_count'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': ''})
        else:
            if 'caption' in i:
                data.append({'like_count':i['like_count'], 'comments_count':i['comments_count'], 'media_url':i['media_url'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': i['caption']})
            else:
                data.append({'like_count':i['like_count'], 'comments_count':i['comments_count'], 'media_url':i['media_url'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': ''})
    datf = pd.DataFrame(data)
    # print(datf)

    largest_post2 = datf['impressions'].nlargest(n = 3, keep='all')
    idx_max2 = (largest_post2.index).tolist()

    data2 = []
    for i in idx_max2:
        best = datf.iloc[[i]]
        d = best.to_json(orient="records")
        data2.append(d)
    
    impression = []
    for i in data2:
        js_data = json.loads(i)
        impression.append(js_data)

    return impression

def best_reach(id_ig):
    node = '/{}/media?fields=id,caption,comments_count,thumbnail_url,media_url,like_count,insights.metric(engagement,impressions,reach)'.format(id_ig)
    node_pic = '/{}?fields=profile_picture_url'.format(id_ig)
    params = {'access_token':token}
    url = base + node
    pic_url = base + node_pic
    obj = requests.get(url, params=params).json()
    obj_url = requests.get(pic_url, params=params).json()
    data = []
    for i in obj['data'] :
        eng = i['insights']['data'][0]['values'][0]['value']
        impr = i['insights']['data'][1]['values'][0]['value']
        reac = i['insights']['data'][2]['values'][0]['value']
        if 'thumbnail_url' in i:
            if 'caption' in i:
                data.append({'like_count':i['like_count'], 'thumbnail_url':i['thumbnail_url'], 'comments_count':i['comments_count'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': i['caption']})
            else:
                data.append({'like_count':i['like_count'], 'thumbnail_url':i['thumbnail_url'], 'comments_count':i['comments_count'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': ''})
        else:
            if 'caption' in i:
                data.append({'like_count':i['like_count'], 'comments_count':i['comments_count'], 'media_url':i['media_url'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': i['caption']})
            else:
                data.append({'like_count':i['like_count'], 'comments_count':i['comments_count'], 'media_url':i['media_url'], 'engagement':eng, 'impressions':impr, 'reach':reac, 'caption': ''})
    datf = pd.DataFrame(data)
    # print(datf)
    largest_post3 = datf['reach'].nlargest(n = 3, keep='all')
    idx_max2 = (largest_post3.index).tolist()

    data3 = []
    for i in idx_max2:
        best = datf.iloc[[i]]
        d = best.to_json(orient="records")
        data3.append(d)

    reach = []
    for i in data3:
        js_data = json.loads(i)
        reach.append(js_data)

    return reach

def profile_ig(id_ig):
    node='/{}/?fields=username,followers_count,media_count,follows_count,profile_picture_url'.format(id_ig)
    url=base+node
    parameters={'access_token':token}
    data=requests.get(url,params=parameters).json()

    follower = data['followers_count']
    follower = f"{follower:,}"
    follows = data['follows_count']
    follows = f"{follows:,}"
    post = data['media_count']
    post = f"{post:,}"
    pict_url = str(data['profile_picture_url'])
    u_name = str(data['username'])
    
    if int(data['followers_count']) > 100:
        follower_growth = '/{}/insights?metric=follower_count&period=day'.format(id_ig)
        url=base+follower_growth
        parameters={'access_token':token}
        fol_data=requests.get(url,params=parameters).json()

        growth = int(fol_data['data'][0]['values'][0]['value']) - int(fol_data['data'][0]['values'][1]['value'])
    else:
        growth = "Follower count under 100"

    data = {'follower':follower, 'follows':follows, 'post':post, 'pict_url':pict_url, 'u_name':u_name, 'growth':growth}    

    return data
