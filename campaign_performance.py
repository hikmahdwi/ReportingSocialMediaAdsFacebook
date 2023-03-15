from logging import warning
import requests
from facebook_api import token, base, user_id
import itertools 
from datetime import datetime, timedelta
import pandas as pd
import json

parameters={'access_token':token}

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
last_2d = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
last_2month = (datetime.now() - timedelta(60)).strftime('%Y-%m-%d')

node = "{}/adaccounts?fields=name".format(user_id)
url = base + node
obj = requests.get(url, params=parameters).json()
id_akun = obj['data']

def campaign_warning():
    all_id_campaign = []
    for i in id_akun:
        if i['id'] == 'act_679657615950119' or i['id'] == 'act_350108546929466':
            continue
        else:
            node = "{}/campaigns?fields=name,start_time,stop_time,effective_status".format(i['id'])
            url = base + node
            json_array = {
            "method": "GET",
            "relative_url": node
            }
            all_id_campaign.append(json_array)

    json_batch = json.dumps(all_id_campaign)
    parameters = {'access_token':token, 'batch':json_batch}
    campaignId = requests.post(base, params=parameters).json()

    requestCampaignId = []
    for i in campaignId:
        body = json.dumps(i['body'])
        body = json.loads(i['body'])
        requestCampaignId.append(body['data'])

    dataCampaignId = list(itertools.chain.from_iterable(requestCampaignId))

    campaign_running = []
    for i in dataCampaignId:
        start_time = i['start_time']
        start_time = start_time[:10]
        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        stop_time = i['stop_time']
        stop_time = stop_time[:10]
        stop_time = datetime.strptime(stop_time, '%Y-%m-%d')
        if start_time <= datetime.now() and datetime.now() <= stop_time:
            periode = (stop_time-start_time).days
            data = {'campaign_id':i['id'], 'start_time':i['start_time'], 'stop_time':i['stop_time'], 
                    'effective_status': i['effective_status'], 'periode':periode}
            campaign_running.append(data)

    listAds = []
    for i in campaign_running:
        node = '{}/ads?fields=effective_status'.format(i['campaign_id'])
        json_array = {
            "method": "GET",
            "relative_url": node
        }
        listAds.append(json_array)

    json_batch = json.dumps(listAds)
    parameters = {'access_token':token, 'batch':json_batch}
    objAds = requests.post(base, params=parameters).json()

    requestInsightsAds = []
    effectiveStatus = []
    for i in objAds:
        print(i['body'])
        body = json.dumps(i['body'])
        body = json.loads(i['body'])
        effectiveStatus.append(body['data'])
        for x in body['data']:
            node = 'v12.0/{}/insights?fields=ad_id,ad_name,campaign_id,conversion_rate_ranking,engagement_rate_ranking,quality_ranking,ctr,cpc,cpp,spend,objective,reach,actions&time_range[since]={}&time_range[until]={}'.format(x['id'], last_2month, yesterday)
            query = {
            "method": "GET",
            "relative_url": node
            }
            requestInsightsAds.append(query)
    json_batch_ads = json.dumps(requestInsightsAds)
    parameters = {'access_token':token, 'batch':json_batch_ads}
    objAdsInsights = requests.post(base, params=parameters).json()

    resultInsightsAds = []
    for i in objAdsInsights:
        body = json.dumps(i['body'])
        body = json.loads(i['body'])
        # print(body)
        resultInsightsAds.append(body['data'])

    dataInsightsAds = list(itertools.chain.from_iterable(resultInsightsAds))
    dataEffectiveStatus = list(itertools.chain.from_iterable(effectiveStatus))

    campaignwarning = 0
    adsInsightsAll = []
    for i in dataInsightsAds:
        if i['objective'] == 'LINK_CLICKS':
            for x in i['actions']:
                if x['action_type'] == 'link_click':
                    link_result = x['value']
            for y in dataEffectiveStatus:
                if y['id'] == i['ad_id']:
                    effective_status = y['effective_status']
            cost_per_result = int(i['spend']) / int(link_result)
            cost_per_result =  round(cost_per_result)
            cpc = float(i['cpc'])
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            if ctr < 2 or cost_per_result > 500:
                status = '#d9534f'
                campaignwarning = campaignwarning + 1
            else :
                status = ''
            data = {'effStatus':effective_status, 'result':link_result, 'cost_per_result':'Rp '+str(cost_per_result), 'status':status, 'objective':i['objective'], 'ad_id':i['ad_id'], 'ad_name':i['ad_name'], 'campaign_id':i['campaign_id'], 'conversion_rate_ranking':i['conversion_rate_ranking'],
                    'cpc':'Rp '+str(round(cpc)), 'ctr':str(ctr)+'%', 'engagement_rate_ranking':i['engagement_rate_ranking'], 'quality_ranking':i['quality_ranking']}
        elif i['objective'] == 'MESSAGES':
            for x in i['actions']:
                if x['action_type'] == 'onsite_conversion.messaging_conversation_started_7d':
                    message_result = x['value']
            for y in dataEffectiveStatus:
                if y['id'] == i['ad_id']:
                    effective_status = y['effective_status']
            cost_per_result = int(i['spend']) / int(message_result)
            cost_per_result = round(cost_per_result)
            cpc = float(i['cpc'])
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            if ctr < 2 or cost_per_result > 6000:
                status = '#d9534f'
                campaignwarning = campaignwarning + 1
            else :
                status = ''
            data = {'effStatus':effective_status, 'result':message_result, 'cost_per_result':'Rp '+str(cost_per_result), 'status':status, 'objective':i['objective'], 'ad_id':i['ad_id'], 'ad_name':i['ad_name'], 'campaign_id':i['campaign_id'], 'conversion_rate_ranking':i['conversion_rate_ranking'],
                    'cpc':'Rp '+str(round(cpc)), 'ctr':str(ctr)+'%', 'engagement_rate_ranking':i['engagement_rate_ranking'], 'quality_ranking':i['quality_ranking']}
        elif i['objective'] == 'POST_ENGAGEMENT' or i['objective'] == 'OUTCOME_ENGAGEMENT':
            for x in i['actions']:
                if x['action_type'] == 'post_engagement':
                    post_result = x['value']
            for y in dataEffectiveStatus:
                if y['id'] == i['ad_id']:
                    effective_status = y['effective_status']
            cost_per_result = int(i['spend']) / int(post_result)
            cost_per_result = round(cost_per_result)
            cpc = float(i['cpc'])
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            if ctr < 2 or cost_per_result > 8:
                status = '#d9534f'
                campaignwarning = campaignwarning + 1
            else :
                status = ''
            data = {'effStatus':effective_status, 'result':post_result, 'cost_per_result':'Rp '+str(cost_per_result), 'status':status, 'objective':i['objective'], 'ad_id':i['ad_id'], 'ad_name':i['ad_name'], 'campaign_id':i['campaign_id'], 'conversion_rate_ranking':i['conversion_rate_ranking'],
                    'cpc':'Rp '+str(round(cpc)), 'ctr':str(ctr)+'%', 'engagement_rate_ranking':i['engagement_rate_ranking'], 'quality_ranking':i['quality_ranking']}
        elif i['objective'] == 'REACH':
            for y in dataEffectiveStatus:
                if y['id'] == i['ad_id']:
                    effective_status = y['effective_status']
            reach_result = i['reach']
            cost_per_result = float(i['cpp'])
            cost_per_result = round(cost_per_result)
            cpc = float(i['cpc'])
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            if ctr < 2 or cost_per_result > 3000:
                status = '#d9534f'
                campaignwarning = campaignwarning + 1
            else :
                status = ''
            data = {'effStatus':effective_status, 'result':reach_result, 'cost_per_result':'Rp '+str(cost_per_result), 'status':status, 'objective':i['objective'], 'ad_id':i['ad_id'], 'ad_name':i['ad_name'], 'campaign_id':i['campaign_id'], 'conversion_rate_ranking':i['conversion_rate_ranking'],
                    'cpc':'Rp '+str(round(cpc)), 'ctr':str(ctr)+'%', 'engagement_rate_ranking':i['engagement_rate_ranking'], 'quality_ranking':i['quality_ranking']}
        elif i['objective'] == 'BRAND_AWARENESS' or i['objective'] == 'OUTCOME_AWARENESS':
            for y in dataEffectiveStatus:
                if y['id'] == i['ad_id']:
                    effective_status = y['effective_status']
            reach_result = i['reach']
            cost_per_result = float(i['cpp'])
            cost_per_result = round(cost_per_result)
            cpc = float(i['cpc'])
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            if ctr < 2 or cost_per_result > 3000:
                status = '#d9534f'
                campaignwarning = campaignwarning + 1
            else :
                status = ''
            data = {'effStatus':effective_status, 'result':reach_result, 'cost_per_result':'Rp '+str(cost_per_result), 'status':status, 'objective':i['objective'], 'ad_id':i['ad_id'], 'ad_name':i['ad_name'], 'campaign_id':i['campaign_id'], 'conversion_rate_ranking':i['conversion_rate_ranking'],
                    'cpc':'Rp '+str(round(cpc)), 'ctr':str(ctr)+'%', 'engagement_rate_ranking':i['engagement_rate_ranking'], 'quality_ranking':i['quality_ranking']}
        adsInsightsAll.append(data)
    return adsInsightsAll

def campaign_list_notif():
    all_id_campaign = []
    for i in id_akun:
        if i['id'] == 'act_679657615950119' or i['id'] == 'act_350108546929466':
            continue
        else:
            node = "{}/campaigns?fields=name,start_time,stop_time,effective_status".format(i['id'])
            url = base + node
            json_array = {
            "method": "GET",
            "relative_url": node
            }
            all_id_campaign.append(json_array)

    json_batch = json.dumps(all_id_campaign)
    parameters = {'access_token':token, 'batch':json_batch}
    campaignId = requests.post(base, params=parameters).json()
    # print(campaignId)
    requestCampaignId = []
    for i in campaignId:
        # print(i)
        body = json.dumps(i['body'])
        body = json.loads(i['body'])
        requestCampaignId.append(body['data'])

    dataCampaignId = list(itertools.chain.from_iterable(requestCampaignId))

    campaign_running = []
    for i in dataCampaignId:
        start_time = i['start_time']
        start_time = start_time[:10]
        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        stop_time = i['stop_time']
        stop_time = stop_time[:10]
        stop_time = datetime.strptime(stop_time, '%Y-%m-%d')
        if start_time <= datetime.now() and datetime.now() <= stop_time:
            periode = (stop_time-start_time).days
            data = {'campaign_id':i['id'], 'start_time':i['start_time'], 'stop_time':i['stop_time'], 
                    'effective_status': i['effective_status'], 'periode':periode}
            campaign_running.append(data)

    listAds = []
    for i in campaign_running:
        node = '{}/ads'.format(i['campaign_id'])
        json_array = {
            "method": "GET",
            "relative_url": node
        }
        listAds.append(json_array)

    json_batch = json.dumps(listAds)
    parameters = {'access_token':token, 'batch':json_batch}
    objAds = requests.post(base, params=parameters).json()

    requestInsightsAds = []
    for i in objAds:
        body = json.dumps(i['body'])
        body = json.loads(i['body'])
        for x in body['data']:
            node = 'v12.0/{}/insights?fields=ad_id,ad_name,campaign_id,conversion_rate_ranking,engagement_rate_ranking,quality_ranking,ctr,cpc,cpp,spend,objective,reach,actions&time_range[since]={}&time_range[until]={}'.format(x['id'], last_2month, yesterday)
            query = {
            "method": "GET",
            "relative_url": node
            }
            requestInsightsAds.append(query)
    json_batch_ads = json.dumps(requestInsightsAds)
    parameters = {'access_token':token, 'batch':json_batch_ads}
    objAdsInsights = requests.post(base, params=parameters).json()

    resultInsightsAds = []
    for i in objAdsInsights:
        body = json.dumps(i['body'])
        body = json.loads(i['body'])
        # print(body)
        resultInsightsAds.append(body['data'])

    dataInsightsAds = list(itertools.chain.from_iterable(resultInsightsAds))

    campaignwarning = 0
    dataNotif = []
    for i in dataInsightsAds:
    # print(i)
        if i['objective'] == 'LINK_CLICKS':
            for x in i['actions']:
                if x['action_type'] == 'link_click':
                    link_result = x['value']
            cost_per_result = int(i['spend']) / int(link_result)
            cost_per_result =  round(cost_per_result)
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            dt = i['date_stop']
            # ddt = datetime.strptime(dt, '%Y-%m-%d')
            # conf = ddt.strftime('%d %b, %Y')
            if ctr < 2 or cost_per_result > 500:
                campaignwarning = campaignwarning + 1
                dataN = {'ad_name':i['ad_name'], 'date':dt, 'ctr':str(ctr)+'%'}
                dataNotif.append(dataN)
        elif i['objective'] == 'MESSAGES':
            for x in i['actions']:
                if x['action_type'] == 'onsite_conversion.messaging_conversation_started_7d':
                    message_result = x['value']
            cost_per_result = int(i['spend']) / int(message_result)
            cost_per_result = round(cost_per_result)
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            dt = i['date_stop']
            # ddt = datetime.strptime(dt, '%Y-%m-%d')
            # conf = ddt.strftime('%d %b, %Y')
            if ctr < 2 or cost_per_result > 6000:
                campaignwarning = campaignwarning + 1
                dataN = {'ad_name':i['ad_name'], 'date':dt, 'ctr':str(ctr)+'%'}
                dataNotif.append(dataN)
        elif i['objective'] == 'POST_ENGAGEMENT' or i['objective'] == 'OUTCOME_ENGAGEMENT':
            for x in i['actions']:
                if x['action_type'] == 'post_engagement':
                    post_result = x['value']
            cost_per_result = int(i['spend']) / int(post_result)
            cost_per_result = round(cost_per_result)
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            dt = i['date_stop']
            # ddt = datetime.strptime(dt, '%Y-%m-%d')
            # conf = ddt.strftime('%d %b, %Y')
            if ctr < 2 or cost_per_result > 8:
                campaignwarning = campaignwarning + 1
                dataN = {'ad_name':i['ad_name'], 'date':dt, 'ctr':str(ctr)+'%'}
                dataNotif.append(dataN)
        elif i['objective'] == 'REACH':
            cost_per_result = float(i['cpp'])
            cost_per_result = round(cost_per_result)
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            dt = i['date_stop']
            # ddt = datetime.strptime(dt, '%Y-%m-%d')
            # conf = ddt.strftime('%d %b, %Y')
            if ctr < 2 or cost_per_result > 3000:
                campaignwarning = campaignwarning + 1
                dataN = {'ad_name':i['ad_name'], 'date':dt, 'ctr':str(ctr)+'%'}
                dataNotif.append(dataN)
        elif i['objective'] == 'BRAND_AWARENESS' or i['objective'] == 'OUTCOME_AWARENESS':
            cost_per_result = float(i['cpp'])
            cost_per_result = round(cost_per_result)
            ctr = float(i['ctr'])
            ctr = round(ctr ,2)
            dt = i['date_stop']
            # ddt = datetime.strptime(dt, '%Y-%m-%d')
            # conf = ddt.strftime('%d %b, %Y')
            if ctr < 2 or cost_per_result > 3000:
                campaignwarning = campaignwarning + 1
                dataN = {'ad_name':i['ad_name'], 'date':dt, 'ctr':str(ctr)+'%'}
                dataNotif.append(dataN)
    return campaignwarning, dataNotif