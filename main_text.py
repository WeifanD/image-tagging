from sqlalchemy import *
from src.tools.utils import get_datalake_conn
from jinjasql import JinjaSql
import pandas as pd
# import boto3
import traceback
import sys
import os
import re

titles = ['产品解析','设计亮点','功能特性','好在哪里']
filename = "test.jsonl"

conn = get_datalake_conn()

query = 'select distinct tmall_id, benefits, model_code from smartdata_pro.d_product_info \
	where benefits is not null and \
	tmall_id in (SELECT distinct tmall_id FROM smartdata_pro.d_product_online_rate \
		where tmall_sale_status = 'onsale');'
data = [i for i in conn.execute(query)]

file = open(filename, "w")
lst_of_dicts = []
for i, item in enumerate(data):
	lst = []
	tmall_id = item[0]
	string = item[1]
	model_code = item[2]
	if len(string) > 40 and re.search('\\d', string) is None:
		string = string.replace('|','')
		desc = '#' + titles[i%4] + '#' + string
		dict = {'tmall_id': tmall_id, 'model_code':model_code, 'desc': desc}
		lst.append(dict)
		file.write(json.dumps(lst, ensure_ascii=False) + "\n")
	lst_of_dicts.append(dict)
file.close()
output = pd.DataFrame(lst_of_dicts)
output.to_sql('b_item_content', con=conn, if_exists='replace', index=False, schema='bi')
