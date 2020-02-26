from src.models.ImageTagging import ImageTagging
from src.tools.utils import get_datalake_conn, db_send_update_from_file, db_get_query_from_file
import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

execution_path = os.getcwd()

prediction = ImageTagging()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "src", "assets", "resnet50_weights_tf_dim_ordering_tf_kernels.h5"))
prediction.loadModel()

conn = get_datalake_conn()

# get valid image src data
result = db_send_update_from_file(conn, "src/data/SQL/get_image_url.sql")
img_src_array = [row[0] for row in result if row[0] is not None and len(row[0]) > 10]
for img_src in img_src_array:
	response = requests.get(img_src)
	image = Image.open(BytesIO(response.content))
	if image.mode != 'RGB':
		img_src_array.remove(img_src)

# predict image objects
output_array = prediction.predictMultipleImages(img_src_array, input_type="stream")
output_str_array, img_url_array = [], []
for image_src, image_content in zip(img_src_array, output_array):
	output = []
	for eachPrediction, eachProbability in zip(image_content['predictions'], image_content['percentage_probabilities']):
		if eachProbability > 50:
			output.append(eachPrediction)
	output = ', '.join(output)
	if len(output) > 1:
		print('图片中有：{}'.format(output))
		output = "'" + output + "'"

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
print(pd.read_sql_query(con = conn, sql = 'select * from image;'))
# print(db_get_query_from_file(conn, "src/data/SQL/check.sql"))
