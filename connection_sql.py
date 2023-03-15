import sqlalchemy 
import pandas as pd

connection_name = "web-analytics-336406:asia-southeast2:webanalyticsinstances"
db_password = "webanalytics"
db_name = "analytics"
db_ippublic = "34.101.219.240"
db_user = "root"
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

db = sqlalchemy.create_engine(
sqlalchemy.engine.url.URL(
    drivername=driver_name,
    username=db_user,
    password=db_password,
    database=db_name, 
    query=query_string),
pool_size=5,
max_overflow=2,
pool_timeout=30,
pool_recycle=1800)

# uri = sqlalchemy.engine.url.make_url('mysql+pymysql://{user}:{password}@/{database}?unix_socket=/cloudsql/{connection_name}'.format(
#         user=db_user, password=db_password, database=db_name, connection_name=connection_name))

# db = sqlalchemy.create_engine("mysql+pymysql://root:webanalytics@127.0.0.1:33066/analytics")

# uri = sqlalchemy.engine.url.make_url('mysql+pymysql://root:webanalytics@127.0.0.1:3306/analytics')

# db_name_tes = "glanalytics"
     