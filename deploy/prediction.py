from keras.models import load_model
import cv2
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras import backend as K

#Main processing for the prediction
def get_splited_hist(img):
    
    scaler = MinMaxScaler()
    
    b,g,r = cv2.split(img)

    hist_b = cv2.calcHist([b],[0],None,[256],[0,256])
    hist_g = cv2.calcHist([g],[0],None,[256],[0,256])
    hist_r = cv2.calcHist([r],[0],None,[256],[0,256])

    hist_data = hist_b.flatten() + hist_g.flatten() + hist_r.flatten()

    return scaler.fit_transform(hist_data.reshape(-1,1)).flatten()

#Get the model and runs the prediction
def get_prediction(filename):

    model = load_model('best_model.h5')

    image = None

    if ('numpy' in str(type(filename))):

        image = np.copy(filename)

    else:

        image = cv2.imread('to_predict/'+filename)

    hist_data = get_splited_hist(image)
    image = image/255.0
    arr = [np.asarray([image]),np.asarray([hist_data])]
    prediction = model.predict(arr)[0][0]

    label = ''

    if (prediction<0.5):

        prediction = 1-prediction

    acc = str(prediction)

    K.clear_session()

    if (prediction>0.5):

        label = 'Tree'

    else:

        label = 'Soil'

    return label, acc

