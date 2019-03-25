from keras.models import Sequential
from keras.models import load_model as load
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization, Activation
import sys

model = None

persons = []


def predict(input):
    if model is None:
        raise Exception("Model is not loaded")

    return model.predict(input)


def load_model(path):
    global model
    model = load(path)


def train_model(data, labels):
    if labels.shape[-1] != 1:
        raise Exception(
            "Lables shape is wrong got %s expected (None, 1)" % str(labels.shape))

    callbacks = [ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=4),
                 ModelCheckpoint(
                     monitor='val_loss', filepath='./FakeTestModel.h5', save_best_only=True),
                 EarlyStopping(monitor='val_loss', min_delta=0.05)]

    shape = (300, 300, 3)

    global model
    model = Sequential()

    # First ConvBlock
    model.add(Conv2D(32, (3, 3), padding='same',
                     activation='relu', input_shape=shape))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D((2, 2)))  # 150x150

    # Second ConvBlcok with Batch normallization
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D((2, 2)))  # 75x75

    # Thrid ConvBlock with Batch normalization
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D((2, 2)))  # 37x37

    # Forth ConvBlock
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D((2, 2)))  # 18x18

    # Last ConvBlock with Batch normalization
    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D((2, 2)))  # 9x9

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='softmax'))

    model.compile('rmsprop', loss='binary_crossentropy', metrics=['acc'])
    model.fit(data, labels, batch_size=32, epochs=20,
              callbacks=callbacks, validation_split=.2)
