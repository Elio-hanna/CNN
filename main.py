import train_model
import load_trained_model
import os
import json

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from services.logging import *


class param(BaseModel):
    name: str
    learning_rate: Optional[float] = None
    batch: Optional[float] = None
    epchs: Optional[int] = None

app = FastAPI()

@app.post("/train_param/")
async def create_model(item: Optional[param] = None):
    """
    the user submit a json object that contain all the details needed to create and train a model
    :param item:
    :return:
    """
    if item is None:
        return {"name cannot be empty"}
    else:
        Model = train_model.train_model()
        if item.name is None:
            return {"name cannot be empty"}
        name = item.name
        learning_rate = item.learning_rate
        batch = item.batch
        epchs = item.epchs
        if learning_rate == 0 or learning_rate == None:
            learning_rate = 0.0001
        if batch == 0 or batch is None:
            batch = 64
        if epchs == 0 or epchs is None:
            epchs = 100
        parr = "learning rate: " + str(learning_rate) + " batch: " + str(batch) + " epochs: " + str(epchs) + " "
        try:
            Model.create_load_save(learning_rate=learning_rate, batch=batch, epchs=epchs, name=name)
            log.log(self=log,name= create_model.__name__, result= "Model saved " + name + ".h5", parm= parr)

        except Exception:
            log.log_error(self=log,name= create_model.__name__)
        return {"Model Trained and saved in": name}


@app.get("/train/{model_name}")
async def create_train_save(model_name):
    """
    Create a Model and train it then save it to a file given in param
    :param model_name: model name given by the user
    :return:  message
    """
    learning_rate = 0.0001
    batch = 64
    epchs = 100
    parr = "learning rate: " + str(learning_rate) + " batch: " + str(batch) + " epochs: " + str(epchs) + " "
    Model = train_model.train_model()
    try:
        Model.create_load_save(learning_rate=learning_rate, batch=batch, epchs=epchs, name=model_name)
        log.log(self=log,name= create_model.__name__, result= "Model saved " + model_name + ".h5", parm= parr)
    except:
        log.log_error(self=log,name= create_train_save.__name__)
    return {"Model Trained and saved in": model_name}


@app.get("/load")
async def load():
    """
    load all Models available in /assets/model
    :return: names
    """
    Model = load_trained_model.load_trained_model()
    result = ""
    for file in os.listdir("./assets/model"):
        if file.endswith(".h5"):
            Model.load_model(file)
            result += file + ", "

    log.log(self=log,name=load.__name__,result=result)
    return {"The loaded model are": result}


@app.post("/predict/")
async def predict(model: str, file: UploadFile = File(...)):
    """
    load the model specified and predict what is the image given by the user
    :param model: model name
    :param file: image given by the user
    :return: the prediction value
    """
    Model3 = load_trained_model.load_trained_model()
    try:
        prediction = Model3.load_image(model_name=model, file=file.file)
        parr = "model used: " + model +" "
        log.log(self=log,name= load.__name__,result= prediction,parm= parr)
    except Exception:
        log.log_error(self=log,name= predict.__name__)
    return {"Prediction": prediction}


@app.post("/predict_image/")
async def predict_image(model: str, file: UploadFile = File(...)):
    """
    load the model specified and predict what is the image given by the user
    :param model: model name
    :param file: image given by the user
    :return: the predicted image
    """
    Model3 = load_trained_model.load_trained_model()
    Model3.image(model_name=model, file=file.file)
    log.log(self=log,name= predict_image.__name__,result= "prediction as image", parm= "model used: " + model)
    path = './assets/img/test.jpeg'
    file_like = open(path, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpeg")


@app.get("/get_labels/{model_name}")
async def model_classes(model_name):
    """
    load a model and get all the classes
    :param model_name: name of the model given by the user
    :return: classes name in json object
    """
    Model = load_trained_model.load_trained_model()
    str2 = '{ '

    for i in range(0, 10):
        number = str(i)
        if i < 9:
            str2 += '"' + number + '"' + ":" + '"' + Model.predictions(i) + '"' + ", "
        else:
            str2 += '"' + number + '"' + ":" + '"' + Model.predictions(i) + '"' + '}'

    json_ob = json.loads(str2)
    return {"message": json_ob}