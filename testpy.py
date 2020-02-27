from src.tools.helpers import *
prediction_output_array = [{'image': 'https://img.alicdn.com/bao/uploaded/i4/352469034/O1CN01Iwqd9C2GbcYRLuKTu_!!0-item_pic.jpg', 'predictions': ['running_shoe']}, {'image': 'https://img.alicdn.com/bao/uploaded/i1/352469034/TB2PLnbbpXXXXXcXpXXXXXXXXXX_!!352469034.jpg', 'predictions': ['jersey']}, {'image': 'https://img.alicdn.com/bao/uploaded/i4/352469034/O1CN019uBA9M2GbcdwnIGBP_!!0-item_pic.jpg', 'predictions': ['running_shoe']}, {'image': 'https://img.alicdn.com/bao/uploaded/i1/352469034/O1CN01e7m6b12GbcdybWLYR_!!0-item_pic.jpg', 'predictions': ['web_site']}]
detector_output_array = [{'image': 'https://img.alicdn.com/bao/uploaded/i1/352469034/TB2w5IvXVXXXXcQXXXXXXXXXXXX_!!352469034.jpg', 'predictions': ['person']}, {'image': 'https://img.alicdn.com/bao/uploaded/i1/352469034/TB2PLnbbpXXXXXcXpXXXXXXXXXX_!!352469034.jpg', 'predictions': ['person']}, {'image': 'https://img.alicdn.com/bao/uploaded/i1/352469034/O1CN01e7m6b12GbcdybWLYR_!!0-item_pic.jpg', 'predictions': ['person']}]

new_dicts = []
for dict1 in detector_output_array:
	for dict2 in prediction_output_array:
		if dict1['image'] == dict2['image']:
			print(dict1, dict2)
			new_dicts.append(mergeDict(dict1, dict2))
			detector_output_array.remove(dict1)
			prediction_output_array.remove(dict2)
if len(new_dicts) > 0:
	output_array = new_dicts.extend(detector_output_array.extend(prediction_output_array))
else:
	output_array = detector_output_array + prediction_output_array