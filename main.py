from src.models.ImageTagging import ImageTagging
from src.tools.utils import get_datalake_conn, db_send_update_from_file, db_get_query_from_file
from src.tools.helpers import *
import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO


execution_path = os.getcwd()
conn = get_datalake_conn()

prediction = ImageTagging()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "src", "assets", "resnet50_weights_tf_dim_ordering_tf_kernels.h5"))
prediction.loadModel(type = "prediction")

detector = ImageTagging()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "src", "assets", "resnet50_coco.h5"))
detector.loadModel(type = "detection")

custom = detector.CustomObjects(person=True)

# get valid image src data
result = db_send_update_from_file(conn, "src/data/SQL/get_image_url.sql")
img_src_array = [row[0] for row in result if row[0] is not None and len(row[0]) > 10]
#print(img_src_array)
for img_src in img_src_array:
	response = requests.get(img_src)
	image = Image.open(BytesIO(response.content))
	if image.mode != 'RGB':
		img_src_array.remove(img_src)
print('valid images {} '.format(len(img_src_array)))

# recognize image objects
prediction_output_array = prediction.predictMultipleImages(img_src_array, input_type="stream")
prediction_face_array = prediction.predictFace(img_src_array)
detector_output_array = detector.detectCustomObjectsFromImage(sent_images_array=img_src_array, custom_objects=custom)
# prediction_output_array = [{'image': 'https://img.alicdn.com/bao/uploaded/i4/352469034/O1CN01Ze33zj2GbcZ8QX9B1_!!352469034.jpg', 'predictions': ['punching_bag']}, {'image': 'https://img.alicdn.com/bao/uploaded/i4/352469034/O1CN01Iwqd9C2GbcYRLuKTu_!!0-item_pic.jpg', 'predictions': ['running_shoe']}]
# detector_output_array = [{'image': 'https://img.alicdn.com/bao/uploaded/i1/352469034/TB2w5IvXVXXXXcQXXXXXXXXXXXX_!!352469034.jpg', 'predictions': ['person']}]

new_dicts = []
for dict1 in detector_output_array:
	for dict2 in prediction_output_array:
		if dict1['image'] == dict2['image']:
			new_dicts.append(mergeDict(dict1, dict2))
			detector_output_array.remove(dict1)
			prediction_output_array.remove(dict2)
if len(new_dicts) > 0:
#        print(new_dicts, detector_output_array, prediction_output_array)
        output_array = new_dicts + detector_output_array + prediction_output_array
else:
	output_array = detector_output_array + prediction_output_array

new_dicts = []
for dict1 in prediction_face_array:
	for dict2 in output_array:
		if dict1['image'] == dict2['image']:
			new_dicts.append(mergeDict(dict1, dict2))
			prediction_face_array.remove(dict1)
			output_array.remove(dict2)
if len(new_dicts) > 0:
	output_array = new_dicts + prediction_face_array + output_array
else:
	output_array = prediction_face_array + output_array

#print(output_array)

# convert list output to string type
output_str_array, img_url_array = [], []
for item in output_array:
	if len(item) > 1:
		output = "'" + ',  '.join(item['predictions']) + "'"
		image_src = "'" + item['image'] + "'"

		img_url_array.append(image_src)
		output_str_array.append(output)

df_insert = pd.DataFrame({'Col1':img_url_array, 'Col2':output_str_array})
import json
df_json = json.loads(df_insert.to_json(orient='records'))

# load image output data
db_send_update_from_file(conn, "src/data/SQL/create_image_tmp_table.sql")
for json in df_json:
	print(json)
	db_send_update_from_file(conn, "src/data/SQL/insert_image_output.sql", json)
print(pd.read_sql_query(con = conn, sql = 'select * from smartdata_pro.image;'))
# print(db_get_query_from_file(conn, "src/data/SQL/check.sql"))
