from src.models.ImageTagging import ImageTagging
from src.tools.utils import get_datalake_conn, db_send_update_from_file, db_get_query_from_file
from src.tools.helpers import *
import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime



execution_path = os.getcwd()
conn = get_datalake_conn()

prediction = ImageTagging()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "src", "assets", "resnet50_weights_tf_dim_ordering_tf_kernels.h5"))
prediction.loadModel(type = "prediction")

detector = ImageTagging()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "src", "assets", "resnet50_coco.h5"))
# detector.setModelPath("C:/Users/Blair/Documents/Decathlon/assets/detection/resnet50_coco_best_v2.0.1.h5")
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

# img_src_array = ["https://pixl.decathlon.com.cn/p1419332/k$e37913992216a3924a68912d40e50785/sq/.jpg"]
# recognize image objects
detector_output_array = detector.detectCustomObjectsFromImage(sent_images_array=img_src_array, custom_objects=custom)
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),'detection finished')

prediction_output_array = prediction.predictMultipleImages(img_src_array, input_type="stream")
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'prediction finished')

prediction_face_array = prediction.predictFace(img_src_array)
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),'face prediction finished')

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
		print(dict1,dict2)
		if dict1['image'] == dict2['image'] and dict1 in prediction_face_array and dict2 in output_array:
			new_dicts.append(mergeDict(dict1, dict2))
			prediction_face_array.remove(dict1)
			output_array.remove(dict2)
if len(new_dicts) > 0:
	output_array = new_dicts + prediction_face_array + output_array
else:
	output_array = prediction_face_array + output_array

print(output_array)

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
db_send_update_from_file(conn, "src/data/SQL/create_image_table.sql")
for json in df_json:
	try:
		db_send_update_from_file(conn, "src/data/SQL/insert_image_data.sql", json)
	except:
		continue
# print(pd.read_sql_query(con = conn, sql = 'select * from bi.d_content_img;'))
# db_send_update_from_file(conn, "src/data/SQL/update_content_img.sql")
