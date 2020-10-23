import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from utilities.config import  image_height, image_width
def make_prediction(image_file_path):
    model = tf.keras.models.load_model('model.h5')
    image_path = image_file_path
    image = tf.keras.preprocessing.image.load_img(image_path,target_size=[int(image_height),int(image_width)])
    input_arr = keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to a batch.
    prediction = model.predict(input_arr)
    if int(prediction[0][0])==1:
        result='Dog'
    else:
        result='Cat'
    return result