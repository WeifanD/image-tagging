from sqlalchemy import *
from jinjasql import JinjaSql
import pandas as pd
# import boto3
import traceback
import sys
import os
json = {"Col1":"'https:\/\/pixl.decathlon.com.cn\/p1147396\/k$30b0326156d8ac616e556f9f2af2c49b\/sq\/SODE+HOOK.jpg'","Col2":"'web_site'"}
j = JinjaSql()
f = open("src/data/SQL/insert_image_output.sql", 'r',encoding='UTF-8')
# f = open(sql_file, 'r')
template = f.read().replace('}}', ' | sqlsafe }}')
# template = f.read()
f.close()
query = j.prepare_query(template, json)[0]
print(query)