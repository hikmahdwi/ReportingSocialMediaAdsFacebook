from sqlalchemy.orm import sessionmaker
from connection_sql import db
from model_table import User
import requests
import json

token = "EAAFPPWVIn1UBAI6cPUDPcBKx5hFfay2x9atfk2FanZB5XO8Ytxm16h1qTNBNLhb2GQ6ZCCB911CsZCQYRQE3QNeK4LHHyxewvVl3GeAgpkJRsoEPMQp4GNZACS0nPBg7P7MiYix70OkbID1mwE3n4oz6uc3T10HqBz5igFl6nNh4uUIlFKpAgb8FZAAfS1r8ZD"
my_app_id = '368600087568213'
my_app_secret = '2946751e583c056b21fb7e5aca98b593'
account_id = "act_1674442666029101"
user_id = "261068098791729"
api_ver = "v12.0"
base = "https://graph.facebook.com/v12.0/"

Session = sessionmaker(bind=db)
sesion = Session()

def list_akunfb_table(username):
    x = sesion.query(User.akun).filter(User.username == username)
    y = x.first()[0]
    arr = y.split(',')
    return arr

def list_info_akunfb(username):
    la = list_akunfb_table(username)
    array_akun = []
    for i in la:
        node = '{}?fields=name'.format(i)
        url = base+node
        parameters={'access_token':token}
        obj=requests.get(url,params=parameters).json()
        array_akun.append(obj)
    return array_akun

    

