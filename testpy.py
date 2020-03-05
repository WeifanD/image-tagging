from PIL import Image
import requests as req
from io import BytesIO
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
image_input = "https://pixl.decathlon.com.cn/p1567689/k$9fb681eb75df36f213f5be33eef25697/sq/RUN+SUPPORT+BREATHE.jpg"
response = req.get(image_input)
image_input = Image.open(BytesIO(response.content))
image_input = image_input.resize((224,224))