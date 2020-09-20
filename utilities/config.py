import os
from configparser import ConfigParser

file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
try:
    config = ConfigParser()
    config.read(os.path.abspath(file_path+'/config/config.ini'))
    train_dir = config.get('data', 'train_dir')
    image_height = config.get('image_size', 'image_height')
    image_width = config.get('image_size', 'image_width')
    image_channel = config.get('image_size', 'channel')
    model_dir = config.get('model','model_dir')
except Exception as e:
    raise RuntimeError("Could Not Load the config information") from e
