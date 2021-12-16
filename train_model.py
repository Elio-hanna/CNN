from __future__ import print_function
from tensorflow import keras
from tensorflow.keras import layers
from fastapi import HTTPException
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D


class train_model:

    def create_load_save(self, learning_rate, batch, epchs, name: str):
        """
        Create a model and train it then save it to a specific place by a name given by the users
        :param learning_rate:
        :param batch:
        :param epchs:
        :param name: name of the model to be saved as.
        :return:
        """
        try:
            # Loads the CIFAR dataset
            (x_train, y_train), (x_test, y_test) = cifar10.load_data()
            # Format our training data by Normalizing and changing data type
            x_train = x_train.astype('float32')
            x_test = x_test.astype('float32')
            x_train /= 255
            x_test /= 255
            # Now we one hot encode outputs
            y_train = keras.utils.to_categorical(y_train, num_classes=10)
            y_test = keras.utils.to_categorical(y_test, num_classes=10)
        except Exception:
            raise HTTPException(status_code=303, detail="can't load CIFAR dataset ")

        try:
            model = Sequential()
            # Padding = 'same'  results in padding the input such that
            # the output has the same length as the original input
            model.add(Conv2D(32, (3, 3), padding='same',
                             input_shape=x_train.shape[1:]))
            model.add(Activation('relu'))
            model.add(Conv2D(32, (3, 3)))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))

            model.add(Conv2D(64, (3, 3), padding='same'))
            model.add(Activation('relu'))
            model.add(Conv2D(64, (3, 3)))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))

            model.add(Flatten())
            model.add(Dense(512))
            model.add(Activation('relu'))
            model.add(Dropout(0.5))
            model.add(Dense(10))
            model.add(Activation('softmax'))

            # initiate RMSprop optimizer and configure some parameters
            opt = keras.optimizers.RMSprop(lr=learning_rate, decay=1e-6)

            # Let's create our model
            model.compile(loss='categorical_crossentropy',
                          optimizer=opt,
                          metrics=['accuracy'])

        except Exception:
            raise HTTPException(status_code=303, detail="can't create and compile the model ")
        try:
            # train the model
            model.fit(x_train, y_train, epochs=epchs, batch_size=int(batch), 
                    validation_data=(x_test, y_test))

        except Exception as ex:
            raise HTTPException(status_code=303, detail="can't train the model " )

        try:
            model.save("./assets/model/" + name + ".h5")
        except Exception:
            raise HTTPException(status_code=303, detail="model can't be saved to: " + name)
