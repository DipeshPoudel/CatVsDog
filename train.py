import os
import pandas as pd
from tensorflow.keras import layers
from tensorflow.keras import Model
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from utilities.config import train_dir, image_height, image_width, image_channel, model_dir

image_height = int(image_height)
image_width = int(image_width)
image_channel = int(image_channel)
dir_path = os.path.dirname(os.path.realpath(__file__))

train_location = os.path.abspath(dir_path + train_dir)
model_location = os.path.abspath(dir_path + model_dir)
SAMPLE_SIZE = len([name for name in os.listdir(train_location)])
print("Number of images:", SAMPLE_SIZE)
IMAGE_SIZE = (image_width, image_height)

filenames = os.listdir(train_location)
categories = []
for filename in filenames:
    category = filename.split('.')[0]
    if category.lower() == 'dog':
        categories.append('dog')
    else:
        categories.append('cat')
df = pd.DataFrame({
    'filename': filenames,
    'label': categories
})
df['label'] = df['label'].astype(str)

train_df, valid_df = train_test_split(df, test_size=0.2)
train_datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rescale=1. / 255.,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_dataframe(
    train_df,
    train_location,
    x_col='filename',
    y_col='label',
    target_size=IMAGE_SIZE,
    class_mode='binary',
)

valid_generator = test_datagen.flow_from_dataframe(
    valid_df,
    train_dir,
    x_col='filename',
    y_col='label',
    target_size=IMAGE_SIZE,
    class_mode='binary'
)

# Our input feature map is 150x150x3: 150x150 for the image pixels, and 3 for
# the three color channels: R, G, and B
img_input = layers.Input(shape=(image_height, image_width, image_channel))

# First convolution extracts 16 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(16, 3, activation='relu')(img_input)
x = layers.MaxPooling2D(2)(x)

# Second convolution extracts 32 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(32, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)

# Third convolution extracts 64 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(64, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)
# Flatten feature map to a 1-dim tensor so we can add fully connected layers
x = layers.Flatten()(x)

# Create a fully connected layer with ReLU activation and 512 hidden units
x = layers.Dense(512, activation='relu')(x)

# Create output layer with a single node and sigmoid activation
output = layers.Dense(1, activation='sigmoid')(x)

# Create model:
# input = input feature map
# output = input feature map + stacked convolution/maxpooling layers + fully 
# connected layer + sigmoid output layer
model = Model(img_input, output)

model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['acc'])
history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,  # 2000 images = batch_size * steps
    epochs=15,
    validation_data=valid_generator,
    validation_steps=50,  # 1000 images = batch_size * steps
    verbose=1)

model_json = model.to_json()
with open("model/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save("model.h5")
