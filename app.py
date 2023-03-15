from crypt import methods
# from functools import cache
import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from flask_caching import Cache
from random import randint
from fanpage import list_fanpage, page_impressions, page_posts_impressions_unique, page_fans_online, page_post_engagements, page_engaged_consumptions, page_engaged_impressions_unique, page_impresions_organic, page_impression_paid, page_fans_city, page_fans_gender_age, insta_profile, action_page
from ig_insights import media_insights, next_prev, follower_account, profile_views, reach_account, impression_account, best_engagement, best_impressions, best_reach, profile_ig
from campaign_insights import get_id_account, aggregation_metrics, table_metrics, impression_reach, click_ratio, cost_spend, click_cpc, location, age_gender, gender_perc
from ads_insights import listAllCampaign, aggregationAds, adsBreakBodyAssets, adsBreakTitleAssets
from campaign_performance import campaign_warning, campaign_list_notif


app = Flask(__name__)
cache = Cache()
app.secret_key = "Iya22TeRaha77siana"
app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

@app.route('/fanpage')
def fanpage():
    u_name = 'hashhash'
    data = list_fanpage(u_name)
    return render_template("fanpage-list.html", page_title="Fanpage List", data_=data)

################################################ START ASYNC IG ######################################################
@app.route("/media-insights", methods=['GET', 'POST'])
def mediaInsights():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        dat, paging = media_insights(id_)
        return jsonify({'data':dat, 'paging':paging})

@app.route('/instagram-dashboard', methods=['GET', 'POST'])
def fanpage_ig():
    title = "Instagram Insights"
    return render_template("ig-media-list.html", page_title=title)

@app.route("/media-insights-next", methods=['GET', 'POST'])
def nex_prev():
    if request.method == 'POST':
        data = request.get_json(force=True)
        url = data['url']
        lnjt, nex = next_prev(url)
        return jsonify({'data':lnjt, 'paging':nex})

@app.route("/ig-profile2", methods=["GET", "POST"])
def igDtProfile():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        ig_profile = profile_ig(id_)
        # print(ig_profile)
        return jsonify({'profile':ig_profile})

@app.route("/best-engagement", methods=["GET", "POST"])
def bestEngagement():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        best = best_engagement(id_)
        return jsonify({'bestEnga':best})

@app.route("/best-impression", methods=["GET", "POST"])
def bestImpres():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        best = best_impressions(id_)
        return jsonify({'bestImpres':best})

@app.route("/best-reach", methods=["GET", "POST"])
def bestReach():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        best = best_reach(id_)
        return jsonify({'bestReach':best})

@app.route("/ig-FollowerAkun", methods=['GET', 'POST'])
def igFollowerAkun():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        dateStart = data['startDate']
        dateStop = data['endDate']
        follower = follower_account(id_, dateStart, dateStop)
        return jsonify({'data':follower})

@app.route("/ig-ReachAkun", methods=['GET', 'POST'])
def igReachAkun():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        dateStart = data['startDate']
        dateStop = data['endDate']
        reach = reach_account(id_, dateStart, dateStop)
        return jsonify({'data':reach})

@app.route("/ig-ImpressionsAkun", methods=['GET', 'POST'])
def igImpressionsAkun():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        dateStart = data['startDate']
        dateStop = data['endDate']
        impressions = impression_account(id_, dateStart, dateStop)
        return jsonify({'data':impressions})

@app.route("/ig-ProvileViews", methods=['GET', 'POST'])
def igProfileViews():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        dateStart = data['startDate']
        dateStop = data['endDate']
        profileview = profile_views(id_, dateStart, dateStop)
        return jsonify({'data':profileview})

@app.route('/instagram-dashboard-filter', methods=['GET', 'POST'])
def fanpage_ig_filtered():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        strDate = data['startDate']
        endDate = data['endDate']
        follower = follower_account(id_, strDate, endDate)
        reach = reach_account(id_, strDate, endDate)
        impression = impression_account(id_, strDate, endDate)
        profile = profile_views(id_, strDate, endDate)
        return jsonify({'data': render_template("ig-media-list-graph.html", follower=follower, reach=reach, impression=impression, profile_views=profile)})

################################################## END ASYNC IG ######################################################

################################################## START ASYNC FANPAGE ###############################################

@app.route('/fanpage-dashboard-details', methods=['GET', 'POST'])
def fanpage_fb_post_async(): 
    u_name = 'hashhash'
    title = 'Fanpage Insights'
    return render_template("fanpage-fb-visual-async.html", title=title)

@app.route('/daily-online', methods=['GET', 'POST'])
def dailyOnline():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        valu, perc, statm, warna = page_fans_online(id_, token, strDate, endDate) 
        return jsonify({'value':valu, 'perc':perc, 'statm':statm, 'warna':warna})

@app.route('/ig-profile', methods=['GET', 'POST'])
def igProfile():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_a = data['id_']
        follower, follows, post, pict_url, u_name, id_ig, growth = insta_profile(id_a)
        return jsonify({'follower':follower, 'follows':follows, 'post':post, 'pict_url':pict_url, 'uname':u_name, 'idIg':id_ig, 'growth':growth})

@app.route('/fanpage-list', methods=['GET', 'POST'])
def fanpage_list():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['uname']
        listfp = list_fanpage(id_)
        print(len(listfp))
        return jsonify({'data':listfp})

@app.route('/page_engaged_impre_unique', methods=['GET', 'POST'])
def page_engaged_impre_unique(): 
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl6 = page_engaged_impressions_unique(id_, token, strDate, endDate)
        return jsonify({'data':hasl6})
        
@app.route('/page_impressions_paid', methods=['GET', 'POST'])
def page_impressions_paid(): 
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl8 = page_impression_paid(id_, token, strDate, endDate)
        return jsonify({'data':hasl8})

@app.route('/page_impressions_organic', methods=['GET', 'POST'])
def page_impressions_organic(): 
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl7 = page_impresions_organic(id_, token, strDate, endDate)
        return jsonify({'data':hasl7})

@app.route('/page_impressions', methods=['GET', 'POST'])
def page_impression(): 
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl2 = page_impressions(id_, token, strDate, endDate)
        return jsonify({'data':hasl2})

@app.route('/page_engaged_consumptions', methods=['GET', 'POST'])
def page_engaged_consumption(): 
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl5 = page_engaged_consumptions(id_, token, strDate, endDate)
        print(hasl5)
        return jsonify({'data':hasl5})

@app.route('/page_post_impressions_unique', methods=['GET', 'POST'])
def page_post_impression_unique():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl6 = page_posts_impressions_unique(id_, token, strDate, endDate)
        return jsonify({'data':hasl6})

@app.route('/daily_post_engagements', methods=['GET', 'POST'])
def post_engagements():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl7 = page_post_engagements(id_, token, strDate, endDate)
        return jsonify({'data':hasl7})

@app.route('/page_fans_city', methods=['GET', 'POST'])
def fans_city():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl8 = page_fans_city(id_, token, strDate, endDate)
        return jsonify({'data':hasl8})

@app.route('/page_age_gender', methods=['GET', 'POST'])
def fans_age_gender():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl9 = page_fans_gender_age(id_, token, strDate, endDate)
        return jsonify({'data':hasl9})

@app.route('/page_action', methods=['GET', 'POST'])
def page_actions():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_ = data['id_']
        token = data['token']
        strDate = data['startDate']
        endDate = data['endDate']
        hasl10 = action_page(id_, token, strDate, endDate)
        return jsonify({'data':hasl10})

################################################## END ASYNC FANPAGE ###############################################

################################################## START CAMPAIGN INSIGHTS #####################################################

@app.route('/', methods=['GET', 'POST'])
def campaignInsights(): 
    title = 'Campaign Insights'
    return render_template("campaign-insights.html", page_title=title)

@app.route('/campaign-insights-detail', methods=['GET', 'POST'])
def campaignInsightDetails(): 
    title = 'Campaign Insight Details'
    return render_template("campaigns-insight-details.html", page_title=title)

@app.route('/client-mid', methods=['GET', 'POST'])
def adAccountList():
    if request.method == 'POST':
        df = pd.read_csv('mid.csv')
        data = df.to_json(orient='records')
        data = json.loads(data)
        return jsonify({'data':data})

@app.route('/get-id-account', methods=['GET', 'POST'])
@cache.cached(timeout=86400)
def getIdAccount():
    if request.method == 'POST':
        # if 'ad_account_list' in session:
        idIklan = get_id_account()
        return jsonify({'data':idIklan})

@app.route('/campaign-aggregation', methods=['GET', 'POST'])
def campaignOrg():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate'] 
        endDate = data['endDate']
        data = aggregation_metrics(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/campaign-table-metrics', methods=['GET', 'POST'])
def campaignTableMetrics():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = table_metrics(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/impressions-reach-graph', methods=['GET', 'POST'])
def graphImpressionsReach():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = impression_reach(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/ctr-graph', methods=['GET', 'POST'])
def graphCtr():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate'] 
        endDate = data['endDate']
        data = click_ratio(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/cost-graph', methods=['GET', 'POST'])
def costSpend():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = cost_spend(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/click-cpc', methods=['GET', 'POST'])
def clickCPC():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = click_cpc(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/location-region', methods=['GET', 'POST'])
def locRegion():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = location(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})

@app.route('/age-gender', methods=['GET', 'POST'])
def ageGender():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = age_gender(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})
    
@app.route('/gender-perc', methods=['GET', 'POST'])
def genderPerc():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_akun = data['id_acc']
        mid = data['mid']
        startDate = data['startDate']
        endDate = data['endDate']
        data = gender_perc(id_akun, mid, startDate, endDate)
        return jsonify({'data':data})
################################################## END CAMPAIGN INSIGHTS #####################################################

################################################## START ADS INSIGHTS #####################################################

@app.route('/ads-insights', methods=['GET', 'POST'])
def adsInsights(): 
    title = 'Ads Insights'
    return render_template("ads-insights.html", page_title=title)

@app.route('/ads-insight-details', methods=['GET', 'POST'])
def adsInsightDetails(): 
    title = 'Ad Insight Details'
    return render_template("ads-insight-details.html", page_title=title)

@app.route('/get-campaign-list', methods=['GET', 'POST'])
@cache.cached(timeout=43200)
def getCampaignList():
    if request.method == 'POST':
        data = listAllCampaign()
        return jsonify({'data':data})

@app.route('/aggregation-ads', methods=['GET', 'POST'])
def aggreAds():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_campaign = data['id_campaign']
        startDate = data['startDate']
        endDate = data['endDate']
        data = aggregationAds(id_campaign, startDate, endDate)
        return jsonify({'data': data})

@app.route('/ads-breaks-bodyAsset', methods=['GET', 'POST'])
def adsBodyAsset():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_campaign = data['id_campaign']
        startDate = data['startDate']
        endDate = data['endDate']
        data = adsBreakBodyAssets(id_campaign, startDate, endDate)
        return jsonify({'data': data})

@app.route('/ads-breaks-titleAsset', methods=['GET', 'POST'])
def adsTitleAsset():
    if request.method == 'POST':
        data = request.get_json(force=True)
        id_campaign = data['id_campaign']
        startDate = data['startDate']
        endDate = data['endDate']
        data = adsBreakTitleAssets(id_campaign, startDate, endDate)
        return jsonify({'data': data})

################################################## END ADS INSIGHTS #####################################################

################################################## START CAMPAIGN CPC ###################################################

@app.route('/campaign-performance', methods=['GET', 'POST'])
def cmpgPerformance(): 
    title = 'Campaign Performance'
    return render_template("campaign-performances.html", page_title=title)


@app.route('/campaign-table-insights', methods=['GET', 'POST'])
@cache.cached(timeout=43200)
def campaignCPC():
    if request.method == 'POST':
        adsInsightsAll = campaign_warning()
        return jsonify({'data':adsInsightsAll})

# @app.route('/source-campaign-notif', methods=['GET', 'POST'])
# def sourceCpgNotif():
#     if request.method == 'POST':
#         data = campaign_list_notif()
#         session['campaignDataNotif'] = data
#         return jsonify({'Message':'Data Provided'})

@app.route('/list-campaign-notif', methods=['GET', 'POST'])
@cache.cached(timeout=43200)
def listCpgNotif():
    if request.method == 'POST':
        jmlhCmpgWarning, notif = campaign_list_notif()
        return jsonify({'jmlh_warning':jmlhCmpgWarning, 'data':notif})

# @app.route('/notif-list', methods=['GET', 'POST'])
# def notifList():
#     if request.method == 'POST':
#         # if 'campaignDataNotif' in session:
#         notif = campaign_list_notif()
#         datacmpgdf = pd.DataFrame(notif)
#         datacmpgwarn = datacmpgdf[datacmpgdf.status == '#d9534f']
#         notif = datacmpgwarn.to_json(orient='records')
#         notif = json.loads(notif)
#         return jsonify({"data":notif})
    

################################################## END CAMPAIGN CPC #####################################################

@app.route('/logout')
def logout():
    return 'no'

@app.route('/dashboard')
def dashboard():
    'no'

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
