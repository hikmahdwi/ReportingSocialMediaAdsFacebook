import requests
import json
import pandas as pd
from facebook_api import token
from datetime import datetime, timedelta, date
from connection_sql import db
from sqlalchemy.orm import sessionmaker
from model_table import User
import time

base='https://graph.facebook.com/v11.0'
Session = sessionmaker(bind=db)
sesion = Session()

# yesterday = datetime.now() - timedelta(1)
# last_30 = datetime.now() - timedelta(30)

# unix_yes = int((yesterday - datetime(1970, 1, 1)).total_seconds())
# unix_l30 = int((yesterday - datetime(1970, 1, 1)).total_seconds())

def list_fanpage(username):
    # parameters={'access_token':token}
    # obj=requests.get(url,params=parameters).json()
    # time.sleep(0.01)
    x = sesion.query(User.id_fb).filter(User.username == username)
    y = x.first()[0]
    # y = '261068098791729'
    # token="EAADAAZCOVZA3cBAOiZAiRU4TXyx0QO4DM7hLxZAx3NavfdbKZCGNGMLhzAH5JeYXrYZCw7DyHKbIHhHoXwHV3o4sYZBfpDS2PaUZBoH0rYTMwPpqgun7FrwlQQ13v90D4KQYYRUJqTlmsISFXhtZAC7w50OMgbS6rY806TbORnZA7ePgqX6np9gvRB"
    node='/{}/accounts?'.format(y)
    url=base+node
    parameters={'access_token':token, 'limit':200}
    obj=requests.get(url,params=parameters).json()
    # print("ini obj")
    # print(obj)
    data = []
    while(True):
        try:
            for x in obj['data']:
                data.append(x)
            obj=requests.get(obj['paging']['next']).json()
        except KeyError:
            break

    dt_js = json.dumps(data)
    djs = json.loads(dt_js)
    return djs

def breakdowns(obj):
    tanggal = []
    for x in range(len(obj['data'][0]['values'])):
        date = obj['data'][0]['values'][x]['end_time']
        tgl = date[:-14]
        tanggal.append(tgl)

    value = []
    for x in range(len(obj['data'][0]['values'])):
        date = obj['data'][0]['values'][x]['value']
        value.append(date)

    # tanggal = pd.DataFrame(tanggal, columns=["Tanggal"])
    # value = pd.DataFrame(value, columns=["Value"])

    # com = pd.concat([tanggal, value], axis=1)
    # result = com.to_json(orient="records")
    result = [tanggal, value]
    return result

def tgl_list(startDate, endDate):
    if startDate == "":
        last_31 = (datetime.now() - timedelta(14)).strftime('%Y, %m, %d')
        year,month,day = last_31.split(',')
        yesterday = date(int(year),int(month),int(day))

        start_date = yesterday
        number_of_days = 14

        date_list = []
        for day in range(number_of_days):
            a_date = (start_date + timedelta(days = day)).isoformat()
            date_list.append(a_date)
        return date_list
    else :
        date_list = pd.date_range(start=startDate,end=endDate).strftime('%Y-%m-%d').tolist()
        return date_list

def page_impressions(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_impressions'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
        print("kosong tanggal")
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
        print("tidak kosong tanggal")
    obj=requests.get(url,params=parameters).json()

    if obj['data'] == []:
        tanggal = tgl_list()
        value = []
        result = [tanggal, value]
        return result
    else :
        result = breakdowns(obj)    
        print(result)
        return result 
        
def page_posts_impressions_unique(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_posts_impressions_unique'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()
    result = breakdowns(obj)  
    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        value = []
        result = [tanggal, value]
        return result
    else :
        result = breakdowns(obj)    
        return result

def page_post_engagements(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_post_engagements'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()
    result = breakdowns(obj)  
    if obj['data'] == []:
        tanggal = tgl_list()
        value = []
        result = [tanggal, value]
        return result
    else :
        result = breakdowns(obj)    
        return result

def page_fans_online(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_fans_online_per_day'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()
    
    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        value = []
        tanggal = pd.DataFrame(tanggal, columns=["Tanggal"])
        value = pd.DataFrame(value, columns=["Value"])

        rgn = len(tanggal)
        tgl = tanggal['Tanggal'][rgn-1]
        valu = 0
        fans_o = 0
        perc = "0%"
        statm = "No changes"
        warna = "red"
        return int(valu), perc, statm, warna

    else :
        tanggal = []
        for x in range(len(obj['data'][0]['values'])):
            date = obj['data'][0]['values'][x]['end_time']
            tgl = date[:-14]
            tanggal.append(tgl)

        value = []
        for x in range(len(obj['data'][0]['values'])):
            date = obj['data'][0]['values'][x]['value']
            value.append(date)

        tanggal = pd.DataFrame(tanggal, columns=["Tanggal"])
        value = pd.DataFrame(value, columns=["Value"])

        rgn = len(tanggal)
        if rgn < 3 :
            statm = "No changes"
            warna = "#4ade2c"
            valu = value.iloc[0]['Value']
            perc = "0%"
        else :
            val = int(rgn-1)
            val2 = int(rgn-2)
            valu = value['Value'][val]
            valu2 = value['Value'][val2]
            fans_o = int(valu) - int(valu2)
            diff = (int(valu) - int(valu2))/int(valu2)
            perc = "{:.0%}".format(diff)
            if fans_o < 0:
                statm = "Lower than before"
                warna = "red"
            elif fans_o == 0 :
                statm = "No changes"
                warna = "#4ade2c"
            else :
                statm = "Higher than before"
                warna = "#4ade2c"
        return int(valu), perc, statm, warna

def page_engaged_consumptions(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_engaged_users,page_consumptions'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()

    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        engaged_user = []
        consumptions = []
        result = [tanggal, engaged_user, consumptions]
        return result
    else:
        tanggal = []
        for x in range(len(obj['data'][0]['values'])):
            date = obj['data'][0]['values'][x]['end_time']
            tgl = date[:-14]
            tanggal.append(tgl)

        engaged_user = []
        for x in range(len(obj['data'][0]['values'])):
            date = obj['data'][0]['values'][x]['value']
            engaged_user.append(date)

        consumptions = []
        for x in range(len(obj['data'][1]['values'])):
            date = obj['data'][1]['values'][x]['value']
            consumptions.append(date)

        result = [tanggal, engaged_user, consumptions]
        return result

def page_engaged_impressions_unique(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_impressions_unique,page_engaged_users'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()

    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        impre_unique = []
        engaged_user = []
        result = [tanggal, impre_unique, engaged_user]
        return result
    else:
        tanggal = []
        for x in range(len(obj['data'][0]['values'])):
            date = obj['data'][0]['values'][x]['end_time']
            tgl = date[:-14]
            tanggal.append(tgl)

        impre_unique = []
        for x in range(len(obj['data'][0]['values'])):
            date = obj['data'][0]['values'][x]['value']
            impre_unique.append(date)

        engaged_user = []
        for x in range(len(obj['data'][1]['values'])):
            date = obj['data'][1]['values'][x]['value']
            engaged_user.append(date)

        result = [tanggal, impre_unique, engaged_user]
        return result

def page_impresions_organic(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_impressions_organic'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()

    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        value = []
        # tanggal = pd.DataFrame(tanggal, columns=["Tanggal"])
        # value = pd.DataFrame(value, columns=["Value"])

        # com = pd.concat([tanggal, value], axis=1)
        # result = com.to_json(orient="records")
        result = [tanggal, value]
        return result
    else :
        result = breakdowns(obj)    
        return result

def page_impression_paid(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_impressions_paid'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()
    result = breakdowns(obj)  
    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        value = []
        # tanggal = pd.DataFrame(tanggal, columns=["Tanggal"])
        # value = pd.DataFrame(value, columns=["Value"])

        # com = pd.concat([tanggal, value], axis=1)
        # result = com.to_json(orient="records")
        result = [tanggal, value]
        return result
    else :
        result = breakdowns(obj)    
        return result

def page_fans_city(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_fans_city'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate}
    data=requests.get(url,params=parameters).json()
    # print(data)
    if data['data'] == []:
        kota = ['kota a', 'kota b', 'kota c', 'kota d', 'kota e']
        val = []

        result = [kota, val]
        return result
    else :  
        dat = data['data'][0]['values'][-1]['value']
        key_list = list(dat.keys())
        val_list = list(dat.values())

        key = pd.DataFrame(key_list, columns=['x'])
        val = pd.DataFrame(val_list, columns=['y'])

        bar = pd.concat([key, val], axis=1)
        dess = bar.sort_values('y', ascending=False)
        pott = dess.head(15)
        kota = pott['x'].values.tolist()
        val = pott['y'].values.tolist()
        result = [kota, val]
        return result

def gender_breakdown(dat):
    key_list = list(dat.keys())
    val_list = list(dat.values())
    ar = []
    for a in range(len(key_list)):
        txt = key_list[a].split(".") 
        ar.append(txt)

    val = pd.DataFrame(val_list, columns=['val'])
    mr = pd.DataFrame(ar, columns=['gender', 'age'])
    conc = pd.concat([mr, val], axis = 1)
    M = conc.loc[conc['gender']=='M']
    F = conc.loc[conc['gender']=='F']
    merged_df = M.merge(F, how = 'inner', on = ['age'])
    sel = merged_df[['age', 'val_x', 'val_y']]
    r_sel = sel.rename(columns={'val_x':'male', 'val_y':'female'})
    age = r_sel['age'].values.tolist()
    male = r_sel['male'].values.tolist()
    female = r_sel['female'].values.tolist()
    result = [age, male, female]
    return result

def page_fans_gender_age(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_fans_gender_age'.format(id_)
    url=base+node
    if startDate == "":
        parameters={'access_token':token}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate}
    data=requests.get(url,params=parameters).json()
    
    if data['data'] == []:
        age = ['55-64', '35-44', '18-24', '25-34', '13-17', '65+', ]
        male = []
        female = []
        result = [age, male, female]
        return result        
    elif len(data['data'][0]['values']) == 1:
        dat = data['data'][0]['values'][0]['value']
        result = gender_breakdown(dat)
        return result
    else :  
        dat = data['data'][0]['values'][-1]['value']
        result = gender_breakdown(dat)
        return result

def action_page(id_, token, startDate, endDate):
    node='/{}/insights?metric=page_total_actions'.format(id_)
    url=base+node
    if startDate == "":
         parameters={'access_token':token, 'date_preset':'last_14d'}
    else:
        parameters={'access_token':token, 'since':startDate, 'until':endDate, 'period':'day'}
    obj=requests.get(url,params=parameters).json()
    result = breakdowns(obj)  
    if obj['data'] == []:
        tanggal = tgl_list(startDate, endDate)
        value = []
        result = [tanggal, value]
        return result
    else :
        result = breakdowns(obj) 
        return result

def insta_profile(id_a):
    node='/{}?fields=instagram_business_account'.format(id_a)
    url=base+node
    parameters={'access_token':token}
    jdata=requests.get(url,params=parameters).json()

    if 'instagram_business_account' in jdata:
        id_ig = jdata['instagram_business_account']['id']

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

        return follower, follows, post, pict_url, u_name, id_ig, growth

    else: 
        follower = '-'
        follows = '-'
        post = '-'
        pict_url = '../static/nifass/img/profile-photos/1.png'  
        u_name = '-'
        id_ig = '#'
        growth = ''
        return follower, follows, post, pict_url, u_name, id_ig, growth

    
    