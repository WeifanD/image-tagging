import numpy as np
from tensorflow.python.keras.preprocessing import image
from PIL import Image
import requests as req
from io import BytesIO
from src.models.keras_retinanet.models.resnet import resnet50_retinanet
from src.models.image import *
from PIL import ImageFile
from src.models.imagenet_utils import preprocess_input, decode_predictions
ImageFile.LOAD_TRUNCATED_IMAGES = True

image_input = 'https://img.alicdn.com/bao/uploaded/i1/352469034/O1CN01BPcfTD2GbcducIaxT_!!352469034.png'
response = req.get(image_input)
image_input = Image.open(BytesIO(response.content))
image_input = image_input.convert(mode='RGB')
image_input = image_input.resize((224,224))
image_input = np.expand_dims(image_input, axis=0)
print(image_input.shape)
image_to_predict = image_input.copy()
print(image_to_predict.shape)
image_to_predict = np.asarray(image_to_predict, dtype=np.float64)
print(image_to_predict.shape)
image_to_predict = preprocess_input(image_to_predict)
print(image_to_predict.shape)