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
	    keyword = i[7]
	    for keyword in list(set(keyword.split(' '))):
	        if label_nature not in keyword_dict.keys():
	            keyword_dict[label_nature] = keyword
	        else:
	            if keyword not in keyword_dict[label_nature] and \
	                    True not in [i in keyword for i in ['咨询客服', '教学视频']]:
	                keyword_dict[label_nature] = ' '.join([keyword_dict[label_nature], keyword])

	return keyword_dict
