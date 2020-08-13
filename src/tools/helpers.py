import re
import jieba
import jieba.posseg as pseg

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {}
   dict3['image'] = dict1['image']
   dict3['predictions'] = dict1['predictions'] + dict2['predictions']
 
   return dict3 

def getKeywordDict(data):
	keyword_dict = {}
	for i in data:
		label_nature = i[6]
		keyword_str = i[7]
		# print('keyword:', keyword)
		for keyword in list(set(re.split('\\s|，| |/', keyword_str))):
			if keyword not in ['2019年新款',' '] and bool(re.search('\\d+|包邮|质保|尺寸|儿童|男|女|可选', keyword)) is not True:
				keyword = re.sub(';|:|!|、','', keyword)
				if label_nature not in keyword_dict.keys():
					keyword_dict[label_nature] = keyword
				else:
					if keyword not in keyword_dict[label_nature]:
						keyword_dict[label_nature] = ' '.join([keyword_dict[label_nature], keyword])
		
		# print('label_nature:', label_nature, 'dict:', keyword_dict[label_nature])

	return keyword_dict

def compress_text(text: str):
	jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
	temp1 = list(jieba.cut(text, cut_all=False))

	char_list = [i for i in list(jieba.cut(text, cut_all=False)) if i != ' ']  # 把字符串转化列表自动按单个字符分词了
	# print(char_list)

	list1 = []
	list1.append(char_list[0])
	for char in char_list:
		if char not in list1:
			list1.append(char)

	return ''.join(list1)
