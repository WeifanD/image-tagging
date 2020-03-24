import numpy as np
from tensorflow.python.keras.preprocessing import image
from PIL import Image
import requests as req
from io import BytesIO
from src.models.keras_retinanet.models.resnet import resnet50_retinanet
from src.models.image import *
import face_recognition
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


from tensorflow.python.keras.layers import Input, Conv2D, MaxPool2D, Activation, concatenate, Dropout
from tensorflow.python.keras.layers import GlobalAvgPool2D, GlobalMaxPool2D
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.models import Sequential


class ImageTagging:
    """
            This is the image prediction class in the ImageAI library. It provides support for 4 different models which are:
             ResNet, SqueezeNet, DenseNet and Inception V3. After instantiating this class, you can set it's properties and
             make image predictions using it's pre-defined functions.

             The following functions are required to be called before a prediction can be made
             * setModelPath()
             * At least of of the following and it must correspond to the model set in the setModelPath()
              [setModelTypeAsSqueezeNet(), setModelTypeAsResNet(), setModelTypeAsDenseNet, setModelTypeAsInceptionV3]
             * loadModel() [This must be called once only before making a prediction]

             Once the above functions have been called, you can call the predictImage() function of the prediction instance
             object at anytime to predict an image.
    """

    def __init__(self):
        self.__modelType = ""
        self.modelPath = ""
        self.__modelPathAdded = True
        self.__modelLoaded = False
        self.__model_collection = []
        self.__input_image_size = 224
        self.__input_image_min = 1333
        self.__input_image_max = 800

        self.numbers_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
                   7: 'truck', 8: 'boat', 9: 'traffic_light', 10: 'fire_hydrant', 11: 'stop_sign', 12: 'parking_meter',
                   13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant',
                   21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie',
                   28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports_ball', 33: 'kite',
                   34: 'baseball_bat', 35: 'baseball_glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis_racket',
                   39: 'bottle', 40: 'wine_glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
                   46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot_dog',
                   53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted_plant', 59: 'bed',
                   60: 'dining_table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
                   67: 'cell_phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator',
                   73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy_bear', 78: 'hair_dryer',
                   79: 'toothbrush'}


    def setModelPath(self, model_path):
        """
        'setModelPath()' function is required and is used to set the file path to the model adopted from the list of the
        available 4 model types. The model path must correspond to the model type set for the prediction instance object.

        :param model_path:
        :return:
        """
        self.modelPath = model_path


    def setModelTypeAsResNet(self):
        """
         'setModelTypeAsResNet()' is used to set the model type to the ResNet model
                for the prediction instance object .
        :return:
        """
        self.__modelType = "resnet"

    def setModelTypeAsDenseNet(self):
        """
         'setModelTypeAsDenseNet()' is used to set the model type to the DenseNet model
                for the prediction instance object .
        :return:
        """
        self.__modelType = "densenet"

    def setModelTypeAsInceptionV3(self):
        """
         'setModelTypeAsInceptionV3()' is used to set the model type to the InceptionV3 model
                for the prediction instance object .
        :return:
        """
        self.__modelType = "inceptionv3"

    def setModelTypeAsRetinaNet(self):
        """
        'setModelTypeAsRetinaNet()' is used to set the model type to the RetinaNet model
        for the object detection instance instance object .
        :return:
        """
        self.__modelType = "retinanet"

    def loadModel(self, speed="normal", type = "prediction"):
        """
        'loadModel()' function is used to load the model structure into the program from the file path defined
        in the setModelPath() function. This function receives an optional value which is "prediction_speed".
        The value is used to reduce the time it takes to predict an image, down to about 50% of the normal time,
        with just slight changes or drop in prediction accuracy, depending on the nature of the image.
        * prediction_speed (optional); Acceptable values are "normal", "fast", "faster" and "fastest"

        :param prediction_speed :
        :return:
        """

        if (type == "prediction"):
            if(speed=="normal"):
                self.__input_image_size = 224
            elif(speed=="fast"):
                self.__input_image_size = 160
            elif(speed=="faster"):
                self.__input_image_size = 120
            elif (speed == "fastest"):
                self.__input_image_size = 100

            if (self.__modelLoaded == False):

                image_input = Input(shape=(self.__input_image_size, self.__input_image_size, 3))

                if(self.__modelType == "" ):
                    raise ValueError("You must set a valid model type before loading the model.")


                elif(self.__modelType == "resnet"):
                    import numpy as np
                    from tensorflow.python.keras.preprocessing import image
                    from .ResNet.resnet50 import ResNet50
                    from .imagenet_utils import preprocess_input, decode_predictions
                    try:
                        model = ResNet50(model_path=self.modelPath, model_input=image_input)
                        self.__model_collection.append(model)
                        self.__modelLoaded = True
                    except:
                        raise ValueError("You have specified an incorrect path to the ResNet model file.")
        else:
            if (self.__modelType == "retinanet"):
                if (speed == "normal"):
                    self.__input_image_min = 800
                    self.__input_image_max = 1333
                elif (speed == "fast"):
                    self.__input_image_min = 400
                    self.__input_image_max = 700
                elif (speed == "faster"):
                    self.__input_image_min = 300
                    self.__input_image_max = 500
                elif (speed == "fastest"):
                    self.__input_image_min = 200
                    self.__input_image_max = 350
                elif (speed == "flash"):
                    self.__input_image_min = 100
                    self.__input_image_max = 250
            elif (self.__modelType == "yolov3"):
                if (speed == "normal"):
                    self.__yolo_model_image_size = (416, 416)
                elif (speed == "fast"):
                    self.__yolo_model_image_size = (320, 320)
                elif (speed == "faster"):
                    self.__yolo_model_image_size = (208, 208)
                elif (speed == "fastest"):
                    self.__yolo_model_image_size = (128, 128)
                elif (speed == "flash"):
                    self.__yolo_model_image_size = (96, 96)
            elif (self.__modelType == "tinyyolov3"):
                if (speed == "normal"):
                    self.__yolo_model_image_size = (832, 832)
                elif (speed == "fast"):
                    self.__yolo_model_image_size = (576, 576)
                elif (speed == "faster"):
                    self.__yolo_model_image_size = (416, 416)
                elif (speed == "fastest"):
                    self.__yolo_model_image_size = (320, 320)
                elif (speed == "flash"):
                    self.__yolo_model_image_size = (272, 272)

            if (self.__modelLoaded == False):
                if (self.__modelType == ""):
                    raise ValueError("You must set a valid model type before loading the model.")
                elif (self.__modelType == "retinanet"):
                    model = resnet50_retinanet(num_classes=80)
                    model.load_weights(self.modelPath)
                    self.__model_collection.append(model)
                    self.__modelLoaded = True




            
    def predictImage(self, image_input, result_count=5, input_type="file" ):
        """
        'predictImage()' function is used to predict a given image by receiving the following arguments:
            * input_type (optional) , the type of input to be parsed. Acceptable values are "file", "array" and "stream"
            * image_input , file path/numpy array/image file stream of the image.
            * result_count (optional) , the number of predictions to be sent which must be whole numbers between
                1 and 1000. The default is 5.

        This function returns 2 arrays namely 'prediction_results' and 'prediction_probabilities'. The 'prediction_results'
        contains possible objects classes arranged in descending of their percentage probabilities. The 'prediction_probabilities'
        contains the percentage probability of each object class. The position of each object class in the 'prediction_results'
        array corresponds with the positions of the percentage possibilities in the 'prediction_probabilities' array.


        :param input_type:
        :param image_input:
        :param result_count:
        :return prediction_results, prediction_probabilities:
        """
        prediction_results = []
        prediction_probabilities = []
        if (self.__modelLoaded == False):
            raise ValueError("You must call the loadModel() function before making predictions.")

        else:

            model = self.__model_collection[0]

            from .imagenet_utils import preprocess_input, decode_predictions
            if (input_type == "file"):
                try:
                    image_to_predict = image.load_img(image_input, target_size=(self.__input_image_size, self.__input_image_size))
                    image_to_predict = image.img_to_array(image_to_predict, data_format="channels_last")
                    image_to_predict = np.expand_dims(image_to_predict, axis=0)

                    image_to_predict = preprocess_input(image_to_predict)
                except:
                    raise ValueError("You have set a path to an invalid image file.")
            elif (input_type == "array"):
                try:
                    image_input = Image.fromarray(np.uint8(image_input))
                    image_input = image_input.resize((self.__input_image_size, self.__input_image_size))
                    image_input = np.expand_dims(image_input, axis=0)
                    image_to_predict = image_input.copy()
                    image_to_predict = np.asarray(image_to_predict, dtype=np.float64)
                    image_to_predict = preprocess_input(image_to_predict)
                except:
                    raise ValueError("You have parsed in a wrong numpy array for the image")
            elif (input_type == "stream"):
                try:
                    response = req.get(image_input)
                    image_input = Image.open(BytesIO(response.content))
                    image_input = image_input.convert(mode='RGB') ## ensure image shape (1,224,224,3)
                    image_input = image_input.resize((self.__input_image_size, self.__input_image_size))
                    image_input = np.expand_dims(image_input, axis=0)
                    image_to_predict = image_input.copy()
                    image_to_predict = np.asarray(image_to_predict, dtype=np.float64)
                    image_to_predict = preprocess_input(image_to_predict)
                except:
                    raise ValueError("You have parsed in a wrong stream for the image")

            prediction = model.predict(x=image_to_predict, steps=1)

            try:
                predictiondata = decode_predictions(prediction, top=int(result_count))

                for results in predictiondata:
                    countdown = 0
                    for result in results:
                        countdown += 1
                        prediction_results.append(str(result[1]))
                        prediction_probabilities.append(result[2] * 100)
            except:
                raise ValueError("An error occured! Try again.")

            return prediction_results, prediction_probabilities

    def predictMultipleImages(self, sent_images_array, result_count_per_image=2, input_type="stream"):
        """
                'predictMultipleImages()' function is used to predict more than one image by receiving the following arguments:
                    * input_type , the type of inputs contained in the parsed array. Acceptable values are "file", "array" and "stream"
                    * sent_images_array , an array of image file paths, image numpy array or image file stream
                    * result_count_per_image (optionally) , the number of predictions to be sent per image, which must be whole numbers between
                        1 and 1000. The default is 2.

                This function returns an array of dictionaries, with each dictionary containing 2 arrays namely 'prediction_results' and 'prediction_probabilities'. The 'prediction_results'
                contains possible objects classes arranged in descending of their percentage probabilities. The 'prediction_probabilities'
                contains the percentage probability of each object class. The position of each object class in the 'prediction_results'
                array corresponds with the positions of the percentage possibilities in the 'prediction_probabilities' array.


                :param input_type:
                :param sent_images_array:
                :param result_count_per_image:
                :return output_array:
                """

        output_array = []

        for image_input in sent_images_array:
     
            image_src = image_input
            prediction_results = []
            prediction_probabilities = []
            if (self.__modelLoaded == False):
                raise ValueError("You must call the loadModel() function before making predictions.")

            else:

                model = self.__model_collection[0]

                from .imagenet_utils import preprocess_input, decode_predictions
                
                try:
                    response = req.get(image_input)
                    image_input = Image.open(BytesIO(response.content))
                    image_input = image_input.convert(mode='RGB') ## ensure image shape (1,224,224,3)
                    image_input = image_input.resize((self.__input_image_size, self.__input_image_size))
                    image_input = np.expand_dims(image_input, axis=0)
                    image_to_predict = image_input.copy()
                    image_to_predict = np.asarray(image_to_predict, dtype=np.float64)
                    image_to_predict = preprocess_input(image_to_predict)
                except:
                    raise ValueError("You have parsed in a wrong stream for the image")

                prediction = model.predict(x=image_to_predict, steps=1)

                try:
                    predictiondata = decode_predictions(prediction, top=int(result_count_per_image))

                    for results in predictiondata:
                        countdown = 0
                        for result in results:
                            if result[2] * 100 > 70:
                                countdown += 1
                                prediction_results.append(str(result[1]))
                                # prediction_probabilities.append(result[2] * 100)
                except:
                    raise ValueError("An error occured! Try again.")

                if len(prediction_results) > 0:
                    each_image_details = {}
                    each_image_details["image"] = image_src
                    each_image_details["predictions"] = prediction_results
                    # each_image_details["percentage_probabilities"] = prediction_probabilities
                    output_array.append(each_image_details)
        
        print('predicted {} images with objects'.format(length(output_array)))
        return output_array


    def CustomObjects(self, person=False, bicycle=False, car=False, motorcycle=False, airplane=False,
                      bus=False, train=False, truck=False, boat=False, traffic_light=False, fire_hydrant=False, stop_sign=False,
                      parking_meter=False, bench=False, bird=False, cat=False, dog=False, horse=False, sheep=False, cow=False, elephant=False, bear=False, zebra=False,
                      giraffe=False, backpack=False, umbrella=False, handbag=False, tie=False, suitcase=False, frisbee=False, skis=False, snowboard=False,
                      sports_ball=False, kite=False, baseball_bat=False, baseball_glove=False, skateboard=False, surfboard=False, tennis_racket=False,
                      bottle=False, wine_glass=False, cup=False, fork=False, knife=False, spoon=False, bowl=False, banana=False, apple=False, sandwich=False, orange=False,
                      broccoli=False, carrot=False, hot_dog=False, pizza=False, donut=False, cake=False, chair=False, couch=False, potted_plant=False, bed=False,
                      dining_table=False, toilet=False, tv=False, laptop=False, mouse=False, remote=False, keyboard=False, cell_phone=False, microwave=False,
                      oven=False, toaster=False, sink=False, refrigerator=False, book=False, clock=False, vase=False, scissors=False, teddy_bear=False, hair_dryer=False,
                      toothbrush=False):


        custom_objects_dict = {}
        input_values = [person, bicycle, car, motorcycle, airplane,
                      bus, train, truck, boat, traffic_light, fire_hydrant, stop_sign,
                      parking_meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra,
                      giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard,
                      sports_ball, kite, baseball_bat, baseball_glove, skateboard, surfboard, tennis_racket,
                      bottle, wine_glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange,
                      broccoli, carrot, hot_dog, pizza, donut, cake, chair, couch, potted_plant, bed,
                      dining_table, toilet, tv, laptop, mouse, remote, keyboard, cell_phone, microwave,
                      oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy_bear, hair_dryer,
                      toothbrush]
        actual_labels = ["person", "bicycle", "car", "motorcycle", "airplane",
                      "bus", "train", "truck", "boat", "traffic_light", "fire_hydrant", "stop_sign",
                      "parking_meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
                      "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
                      "sports_ball", "kite", "baseball_bat", "baseball_glove", "skateboard", "surfboard", "tennis_racket",
                      "bottle", "wine_glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
                      "broccoli", "carrot", "hot_dog", "pizza", "donut", "cake", "chair", "couch", "potted_plant", "bed",
                      "dining_table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell_phone", "microwave",
                      "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy_bear", "hair_dryer",
                      "toothbrush"]

        for input_value, actual_label in zip(input_values, actual_labels):
            # print(input_value, actual_label)
            if(input_value == True):
                custom_objects_dict[actual_label] = "valid"
            else:
                custom_objects_dict[actual_label] = "invalid"

        return custom_objects_dict


    def detectCustomObjectsFromImage(self, custom_objects=None, sent_images_array="", minimum_percentage_probability = 70):

        if (self.__modelLoaded == False):
            raise ValueError("You must call the loadModel() function before making object detection.")
        elif (self.__modelLoaded == True):
            if (self.__modelType == "retinanet"):
                
                output_array = []
                for image_input in sent_images_array:
                    image_src = image_input
                    prediction_results, prediction_probabilities = [], []

                    output_objects_array = []
                    detected_objects_image_array = []

                    def read_image_src(img_src):
                        response = req.get(img_src)
                        img = Image.open(BytesIO(response.content)) # Bug: "IOError: cannot identify image file" with some JPG images
                        # print('one image loaded.')
                        # image = np.asarray(Image.open(path).convert('RGB'))
                        image = np.asarray(img.convert('RGB'))
                        return image[:, :, ::-1].copy()

                    image = read_image_src(image_input)

                    detected_copy = image.copy()
                    detected_copy = cv2.cvtColor(detected_copy, cv2.COLOR_BGR2RGB)

                    detected_copy2 = image.copy()
                    detected_copy2 = cv2.cvtColor(detected_copy2, cv2.COLOR_BGR2RGB)

                    image = preprocess_image(image)
                    image, scale = resize_image(image, min_side=self.__input_image_min, max_side=self.__input_image_max)

                    model = self.__model_collection[0]

                    _, _, detections = model.predict_on_batch(np.expand_dims(image, axis=0)) 


                    predicted_numbers = np.argmax(detections[0, :, 4:], axis=1)

                    scores = detections[0, np.arange(detections.shape[1]), 4 + predicted_numbers]

                    detections[0, :, :4] /= scale

                    min_probability = minimum_percentage_probability / 100
                    counting = 0

                    for index, (label, score), in enumerate(zip(predicted_numbers, scores)):
                        if score < min_probability:
                            continue


                        if(custom_objects != None):
                            check_name = self.numbers_to_names[label]
                            if (custom_objects[check_name] == "invalid"):
                                continue

                        counting += 1

                        detection_details = detections[0, index, :4].astype(int)

                        prediction_results.append(self.numbers_to_names[label])
                        prediction_probabilities.append(str(round(score,2)))

                    if len(prediction_results) > 0:
                        each_image_details = {}
                        each_image_details["image"] = image_src
                        each_image_details["predictions"] = prediction_results
                        # each_image_details["percentage_probabilities"] = prediction_probabilities
                        output_array.append(each_image_details)

                print('detected {} images with person'.format(len(output_array)))

                return output_array

    def predictFace(self, sent_images_array):
        def load_image_file(img_src, mode = 'RGB'):

            response = req.get(img_src)
            im = Image.open(BytesIO(response.content))
            width, height = im.size
            if mode:
                im = im.convert(mode)
            return np.array(im), width, height
        
        def _trim_css_to_bounds_self(css, image_shape):

            return max(css[3], 0), max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0])

        def face_locations_self(img, number_of_times_to_upsample=1, model="hog"):
            if model == "cnn":
                return [_trim_css_to_bounds_self(face_recognition.api._rect_to_css(face.rect), img.shape) for face in face_recognition.api._raw_face_locations(img, number_of_times_to_upsample, "cnn")]
            else:
                return [_trim_css_to_bounds_self(face_recognition.api._rect_to_css(face), img.shape) for face in face_recognition.api._raw_face_locations(img, number_of_times_to_upsample, model)]
        output_array = []
        for input_image_src in sent_images_array:
            image, width, height = load_image_file(input_image_src)

            face_locations = face_locations_self(image)
            if len(face_locations) > 0:
                output_array.append({"image":input_image_src, "predictions":['face']})

        print('detected {} images with face'.format(length(output_array)))

        return output_array
