def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {}
   dict3['image'] = dict1['image']
   dict3['predictions'] = dict1['predictions'] + dict2['predictions']
 
   return dict3 
