from src.tools.utils import *
from src.tools.helpers import *
from jinjasql import JinjaSql
import json
import numpy as np

class TextGeneration:
	"""
	"""

	def __init__(self):
		self.conn = get_datalake_conn()
		self.filename = ''
		self.titles = ['设计亮点','好在哪里','产品解析']
		pass

	def get_universe(self):
		db_send_update_from_file(self.conn, "../data/SQL/get_universe.sql")

	def generate_text(self, universe_id):
		print('{} running'.format(universe_id))

		self.params = {'universe_id': universe_id}
		result = db_send_update_from_file(self.conn, "../data/SQL/get_image_content.sql", self.params)
		data = [i for i in result]
		keyword_dict = getKeywordDict(data)
		if len(keyword_dict) > 0:

			file = open(self.filename, "w", encoding='utf-8')
			lst_of_dicts = []
			for i, item in enumerate(data):
				lst = []
				# tmall_id = item[0]
				model_code = item[1]
				weblabel = item[2]
				benefits = item[3]
				catchline = item[4]
				tmall_cat_lvl3_name = item[6]

				if tmall_cat_lvl3_name in keyword_dict.keys():
					keyword = keyword_dict[tmall_cat_lvl3_name].split(' ')
					weblabel = re.split('- |\+|\s|-', weblabel)[0]
					weblabel = re.sub('Essential 4 mm', '', weblabel)
					product_name = item[-1]
					# jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
					# seg_list = list(jieba.cut(product_name, cut_all=False))
					# product_name = compress_text(product_name).strip()

					for i in list(range(3)):
						title = self.titles[i%3]
						# print(model_code, i)
						if i%3 in (0,2):
							# print('the length of benefits is {}'.format(len(benefits)))
							benefits_splits = [re.sub(';|:|!|,','', i) for i in re.split(r'\.|\||。|，|\\', benefits)]
							benefits = '，'.join([i for i in benefits_splits if len(i) > 4
																					and bool(re.search('[\u4e00-\u9fff]+', i))
																					and not bool(re.search('\\d', i))])
							if len(benefits) > 25 and len(re.findall('\\d', benefits)) < 5:
								if i%3 == 0:
									string = '，'.join(benefits.split('，')[:4]) + '。'
								elif i%3 == 2:
									n = min(4,len(keyword))
									# print(np.random.choice(keyword, n, replace=False))
									string = '，'.join(np.random.choice(keyword, n, replace=False)) + '。' + '，'.join(benefits.split('，')[-2:]) + '。'
									string = string.replace('。。', '。')
							else:
								string = 'None'
						else:
							if len(catchline) > 20:
								string = catchline.replace('|','')
							else:
								string = 'None'
						# print(i, string)
						if len(string) > 0:
							dict = {'model_code': model_code, 'product_name': product_name, 'title': title, 'text': string}
						lst.append(dict)
						file.write(json.dumps(lst, ensure_ascii=False) + "\n")
						lst_of_dicts.append(dict)
			file.close()

			output = pd.DataFrame(lst_of_dicts)

			return output


	def update_content(self, universe_id):
		print('generate text...')
		output = self.generate_text(universe_id)
		
		print('create table...')
		db_send_update_from_file(self.conn, "../data/SQL/create_text_table.sql")
		output.to_sql('d_content_text', con=self.conn, if_exists='replace', index=False, schema='bi')

		print('Update content...')
		db_send_update_from_file(self.conn, "../data/SQL/update_content.sql", self.params)