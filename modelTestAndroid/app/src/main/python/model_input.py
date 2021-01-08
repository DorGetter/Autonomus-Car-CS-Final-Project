import numpy as np
import base64
import io
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image

import cv2


def img_preprocess(img):
    print('before process ',img.shape)
    img = img[60:135,:,:]
    print('before process 2',img.shape)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    print('before process 3',img.shape)

    img = cv2.GaussianBlur(img,  (3, 3), 0)
    print('before process 4',img.shape)
    img = cv2.resize(img, (200, 66))
    print('before process 5',img.shape)

    img = img/255
    return img


def main(data):
    decoded_data = base64.b64decode(data)
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

    print('main 2 ',img.shape)

    image1 = img_preprocess(img)
    print('after process', image1.shape)

    image1 = np.array([image1])
    print(type(image1))
    return image1