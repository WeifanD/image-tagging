from sqlalchemy import *
from src.tools.utils import *
from src.tools.helpers import *
from jinjasql import JinjaSql
import pandas as pd
import traceback
import sys
import os
import re
import json
import pickle
import jieba
import jieba.posseg as psg
import random
import numpy as np

titles = ['产品解析','好在哪里','设计亮点']
filename = "test.jsonl"

conn = get_datalake_conn()

result = db_send_update_from_file(conn, "src/data/SQL/get_image_content.sql")
data = [i for i in result]
keyword_dict = getKeywordDict(data)

file = open(filename, "w", encoding='utf-8')
lst_of_dicts = []
for i, item in enumerate(data):
	lst = []
	# tmall_id = item[0]
	model_code = item[1]
	weblabel = item[2]
	benefits = item[3]
	catchline = item[4]
	tmall_cat_lvl3_name = item[6]

	keyword = keyword_dict[tmall_cat_lvl3_name].split(' ')
	weblabel = re.split('- |\+', weblabel)[0]
	weblabel = re.sub('Essential 4 mm', '', weblabel)
	product_name = '迪卡侬' + random.choice(keyword) + weblabel

	for i in list(range(3)):
		title = titles[i%3]
		print(model_code, i)
		if i%3 in (0,2):
			# print('the length of benefits is {}'.format(len(benefits)))
			if len(benefits) > 30 and len(re.findall('\\d', benefits)) < 5:
				benefits = benefits.replace('|', '')
				benefits = benefits.replace('.', '。')
				benefits = benefits.replace('：', '，')
				if i%3 == 0:
					string = benefits
				elif i%3 == 2:
					n = min(4,len(keyword))
					string = '，'.join(np.random.choice(keyword, n, replace=False)) + '。' + benefits.split('。')[0] + '。'
			else:
				string = 'None'
		else:
			string = catchline.replace('|','')
		print(string)
		if len(string) > 0:
			dict = {'model_code': model_code, 'product_name': product_name, 'title': title, 'text': string}
		lst.append(dict)
		file.write(json.dumps(lst, ensure_ascii=False) + "\n")
		lst_of_dicts.append(dict)
file.close()

output = pd.DataFrame(lst_of_dicts)
# print(output)
output.to_sql('d_content_text', con=conn, if_exists='replace', index=False, schema='bi')
db_send_update_from_file(conn, "src/data/SQL/update_content.sql")