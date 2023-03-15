from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, String, Table, MetaData

Base = declarative_base(class_registry=dict())

class User(Base):
    __tablename__ = 'user_login_fb'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key = True)
    username = Column(String)
    id_fb = Column(String)
    nama = Column(String)
    akun = Column(String)
    
    def __init__(self, id, username, id_fb, nama, akun):
        self.id = id
        self.username = username
        self.id_fb = id_fb
        self.nama = nama
        self.akun = akun

class modelIgFollower(Base):
    __tablename__ = 'ig_account_performance'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key = True)
    ig_business = Column(String)
    name_account = Column(String)
    followers_count = Column(Integer)
    date = Column(Date)
    reach = Column(Integer)
    impressions = Column(Integer)
    profile_views = Column(Integer)
    
    def __init__(self, id, ig_business, name_account, followers_count, date, reach, impressions, profile_views):
        self.id = id
        self.ig_business = ig_business
        self.name_account = name_account
        self.followers_count = followers_count
        self.date = date
        self.reach = reach
        self.impressions = impressions
        self.profile_views = profile_views


def modelTbl(akun_id):
    class fbInsight(Base):
        __tablename__ = akun_id
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key = True)
        idx = Column(Integer)
        account_id = Column(String)
        account_name = Column(String)
        ad_id = Column(String)
        adset_id = Column(String)
        adset_name = Column(String)
        campaign_id = Column(String)
        campaign_name = Column(String)
        clicks = Column(Integer)
        date_start = Column(Date)
        date_stop = Column(Date)
        device_platform = Column(String)
        impression_device = Column(String)
        impressions = Column(Integer)
        inline_post_engagement = Column(Integer)
        platform_position = Column(String)
        publisher_platform = Column(String)
        spend = Column(Integer)
        reach = Column(Integer)
        

        def __init__(self, idx, account_id, account_name, ad_id, adset_id, adset_name, campaign_id, campaign_name, clicks, date_start, date_stop, device_platform, impression_device, impressions, inline_post_engagement, platform_position, publisher_platform, reach, spend):
            self.idx = idx
            self.account_id = account_id
            self.account_name = account_name
            self.ad_id = ad_id
            self.adset_id = adset_id
            self.adset_name = adset_name
            self.campaign_id = campaign_id
            self.campaign_name = campaign_name
            self.clicks = clicks
            self.date_start = date_start
            self.date_stop = date_stop
            self.device_platform = device_platform
            self.impression_device = impression_device
            self.impressions = impressions
            self.inline_post_engagement = inline_post_engagement
            self.platform_position = platform_position
            self.publisher_platform = publisher_platform
            self.spend = spend
            self.reach = reach
    return fbInsight

def modelCamp():
    class fbInsight(Base):
        __tablename__ = "all_campaign"
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key = True)
        campaign_name = Column(String)
        campaign_id = Column(String)
        account_id = Column(String)
        impressions = Column(Integer)
        clicks = Column(Integer)
        objective = Column(String)
        spend = Column(Integer)
        reach = Column(Integer)
        date_start = Column(Date)
        date_stop = Column(Date)
        country = Column(String)
        region = Column(String)
        start_time = Column(Date)
        stop_time = Column(Date)
        
        def __init__(self, campaign_name, campaign_id, account_id, impressions, clicks, objective, spend, reach, date_start, date_stop, country, region, star_time, stop_time):
            self.campaign_name = campaign_name
            self.campaign_id = campaign_id
            self.account_id = account_id
            self.impressions = impressions
            self.clicks = clicks
            self.objective = objective
            self.spend = spend
            self.reach = reach
            self.date_start = date_start
            self.date_stop = date_stop
            self.country = country
            self.region = region
            self.start_time = star_time
            self.stop_time = stop_time
    return fbInsight

def modelCampGen(akun_id):
    class fbInsight(Base):
        __tablename__ = "cpAG_{}".format(akun_id)
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key = True)
        idx = Column(Integer)
        campaign_name = Column(String)
        campaign_id = Column(String)
        impressions = Column(Integer)
        clicks = Column(Integer)
        objective = Column(String)
        spend = Column(Integer)
        reach = Column(Integer)
        date_start = Column(Date)
        date_stop = Column(Date)
        age = Column(String)
        gender = Column(String)
        
        def __init__(self, idx, campaign_name, campaign_id, impressions, clicks, objective, spend, reach, date_start, date_stop, age, gender):
            self.idx = idx
            self.campaign_name = campaign_name
            self.campaign_id = campaign_id
            self.impressions = impressions
            self.clicks = clicks
            self.objective = objective
            self.spend = spend
            self.reach = reach
            self.date_start = date_start
            self.date_stop = date_stop
            self.age = age
            self.gender = gender
    return fbInsight

def modelCampIPP(akun_id):
    class fbInsight(Base):
        __tablename__ = "cpIPP_{}".format(akun_id)
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key = True)
        idx = Column(Integer)
        campaign_name = Column(String)
        campaign_id = Column(String)
        impressions = Column(Integer)
        clicks = Column(Integer)
        objective = Column(String)
        spend = Column(Integer)
        reach = Column(Integer)
        date_start = Column(Date)
        date_stop = Column(Date)
        publisher_platform = Column(String)
        platform_position = Column(String)
        impression_device = Column(String)

        def __init__(self, idx, campaign_name, campaign_id, impressions, clicks, objective, spend, reach, date_start, date_stop, publisher_platform, platform_position, impression_device):
            self.idx = idx
            self.campaign_name = campaign_name
            self.campaign_id = campaign_id
            self.impressions = impressions
            self.clicks = clicks
            self.objective = objective
            self.spend = spend
            self.reach = reach
            self.date_start = date_start
            self.date_stop = date_stop
            self.publisher_platform = publisher_platform
            self.platform_position = platform_position
            self.impression_device = impression_device
    return fbInsight
    
# def Table_class(dt):
#     arr = [{'key':'__tablename__', 'value': dt[0]}, {'key':'id', 'value': Column(Integer, primary_key=True)}] 
#     for x in range(len(dt)):
#         if x == 0 :
#             continue
#         elif x % 2 != 0 :
#             if dt[x+1] == "String":
#                 arr.append({'key':dt[x], 'value':Column(String)})
#             elif dt[x+1] == "Integer":
#                 arr.append({'key':dt[x], 'value':Column(Integer)})
#             elif dt[x+1] == "Date":
#                 arr.append({'key':dt[x], 'value':Column(Date)})
#         else :
#             continue
#     res = dict()
#     for sub in arr:
#         res.update((sub.values(), ))
#     MyTableClass = type('MyTableClass', (Base,), res)
#     return MyTableClass

def Table_class(nm, tipe, nmtbl):
    arr = [{'key':'__tablename__', 'value': nmtbl}, {'key':'id', 'value': Column(Integer, primary_key=True)}] 
    for x in range(len(nm)):
        if tipe[x] == "char(150)":
            arr.append({'key':nm[x], 'value':Column(String)})
        elif tipe[x] == "int(11)":
            arr.append({'key':nm[x], 'value':Column(Integer)})
        elif tipe[x] == "date":
            arr.append({'key':nm[x], 'value':Column(Date)})
    res = dict()
    for sub in arr:
        res.update((sub.values(), ))
    MyTableClass = type('MyTableClass', (Base,), res)
    return MyTableClass

def Userlog():
    class userLog(Base):
        __tablename__ = "user_log"
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key = True)
        username = Column(String)
        nama_tbl = Column(String)
        tanggal = Column(Date)
        jColumn = Column(Integer)

        def __init__(self, idx, username, nama_tbl, tanggal, jColumn):
            self.idx = idx
            self.username = username
            self.nama_tbl = nama_tbl
            self.tanggal = tanggal
            self.jColumn = jColumn
    return userLog