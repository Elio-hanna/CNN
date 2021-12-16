import numpy as np
from fastapi import HTTPException
from tensorflow import keras
from PIL import Image, ImageDraw, ImageOps


class load_trained_model:

    def predictions(self, res):
        """
        take result of the prediction by the model and assign the name of the prediction
        :return: prediction as string
        """
        try:
            res = int(res)
            predict = ["airplane", "automobile", " bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
            return str(predict[res])
        except Exception:
            raise HTTPException(status_code=404, detail="Error in the predictions")

    def load_model(self, name):
        """
        Load a model given by user or by the program
        :return: loaded model
        """
        try:
            classifier = keras.models.load_model('./assets/model/' + name)
            return classifier
        except Exception as ex:
            raise HTTPException(status_code=404, detail="can't load model")


    def load_image(self, model_name, file):
        """
        load an image given by the user and a model and return the prediction
        :param file: image given by the user
        :param model_name: model to be loaded
        :return:
        """
        try:
            model = load_trained_model()
            img = Image.open(file, "r").convert('RGB')
            input_im = np.array(img)
            input_im = input_im.reshape(1, 32, 32, 3)
            classifier = model.load_model(name=model_name)
            res = str(classifier.predict_classes(input_im, 1, verbose=0)[0])
            prediction = model.predictions(res)

            return prediction
        except Exception:
            raise HTTPException(status_code=303, detail="Error loading image or model")

    def draw_test(self, prediction, input_im):
        try:
            img = ImageOps.fit(input_im, (300, 300), Image.ANTIALIAS)
            draw = ImageDraw.Draw(img)
            draw.text((5, 5), prediction, fill="red", align="left")
            img.save(r"./assets/img/test.jpeg")
        except Exception:
            raise HTTPException(status_code=500, detail="can't save the prediction")

    def image(self, model_name, file):
        """
        load an image given by the user and a model and return the prediction
        :param file: image given by the user
        :param model_name: model to be loaded
        :return:
        """
        try:
            model = load_trained_model()
            res = model.load_image(model_name=model_name, file=file)
            img = Image.open(file, "r").convert('RGB')
            model.draw_test(prediction=res, input_im=img)
        except Exception:
            raise HTTPException(status_code=303, detail="Error in the function image")
