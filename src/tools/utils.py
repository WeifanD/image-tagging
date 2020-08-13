from sqlalchemy import *
from jinjasql import JinjaSql
import pandas as pd
# import boto3
import traceback
import sys
import os

def get_redshift_conn(env):
    user_name = os.environ.get('redshift_user')
    password = os.environ.get('redshift_pwd')
    if env == 'PROD':
        engine = create_engine('postgresql://' + user_name + ':' + password + '@192.168.112.18:5539/dvdbredshift02') \
                 .execution_options(autocommit=True)
    else :
        engine = create_engine('postgresql://' + user_name + ':' + password + '@bgda.dvredshift02.oxatech.net:5439/dvdbredshift02') \
                 .execution_options(autocommit=True)
            
    conn = engine.connect()
    return conn

def get_datalake_conn():
    user_name = os.environ.get('datalake_user')
    password = os.environ.get('datalake_pwd')
    engine = create_engine('postgresql://' + user_name + ':' + password + '@10.50.8.227:60906/dw') \
        .execution_options(autocommit=True)
    conn = engine.connect()
    return conn

def db_get_query_from_file(conn, sql_file, params = {}) :
    j = JinjaSql()
    f = open(sql_file, 'r')
    template = f.read().replace('}}', ' | sqlsafe }}')
    f.close()
    query = j.prepare_query(template, params)[0]
    return pd.read_sql_query(con = conn, sql = query)

def db_send_update_from_file(conn, sql_file, params = {}) :
    j = JinjaSql()
    f = open(sql_file, 'r',encoding='UTF-8')
    # f = open(sql_file, 'r')
    template = f.read().replace('}}', ' | sqlsafe }}')
    f.close()
    query = j.prepare_query(template, params)[0]
    # print(query)
    return conn.execute(query)

def get_sql_query_from_file(conn, sql_file, params = {}) :
    j = JinjaSql()
    f = open(sql_file, 'r')
    template = f.read().replace('}}', ' | sqlsafe }}')
    f.close()
    query = j.prepare_query(template, params)[0]
    # print(query)

def get_S3_info(env) :
    s3_credentials = os.environ.get('AWS_ACCESS_KEY_ID')    
    s3_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')  
    if env == 'PROD' :
        s3_bucket = "s3://CN-PR/chinabi-pr/GUESS_YOU_LIKE/IN/"
    else :
        s3_bucket = "s3://preprod.datamining/"
    return s3_credentials, s3_access_key, s3_bucket


def get_s3_bucket(s3_credentials, s3_access_key, s3_bucket):
    s3 = boto3.resource('s3', aws_access_key_id = s3_credentials, aws_secret_access_key = s3_access_key)
    bucket = s3.Bucket(s3_bucket)
    return bucket


def unload_on_S3(img_path, bucket):

    from io import BytesIO

    in_memory_file = BytesIO()
    img.imwrite(in_memory_file)
    obj = bucket.Object(img_path)
    obj.upload_fileobj(in_memory_file)


def unload_table_on_S3(conn, table_name, s3_path, s3_credentials, s3_access_key) :
  
    params = {'table_name' : table_name,
              's3_path' : s3_path,
              's3_credentials' : s3_credentials,
              's3_access_key' : s3_access_key}
  
    db_send_update_from_file(conn, "src/data/SQL/copy.sql", params)


def unload_table_on_local(conn, table_name, ftp_path) :

    pd.read_sql_table(table_name, con=conn, schema='bi').to_csv(ftp_path, index=False)


def unload_table_on_ftp(conn, table_name) :

    params = {'table_name' : table_name
              }

    db_send_update_from_file(conn, "src/data/SQL/copy.sql", params)


