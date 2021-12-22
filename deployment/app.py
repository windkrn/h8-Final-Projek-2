from re import split
import flask
import numpy as np
import pickle


model = pickle.load(open("model/model_classifier-svm_model.pkl", "rb"))
app = flask.Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    return(flask.render_template('main.html'))

if __name__ == '__main__':
    app.run()


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
     # ngambil nilai inputan dari form dibikin bentuk dict
    features = dict(flask.request.form)

    # karena fitur name itu kategori jadi kita encode
    features_Location = []
    for i in range(1, 50):
        if i == int(features['Location']):
            features_Location.append(1)
        else:
            features_Location.append(0)

    features_WindGustDir = []
    for i in range(1, 17):
        if i == int(features['WindGustDir']):
            features_WindGustDir.append(1)
        else:
            features_WindGustDir.append(0)

    features_WindDir9am = []
    for i in range(1, 17):
        if i == int(features['WindDir9am']):
            features_WindDir9am.append(1)
        else:
            features_WindDir9am.append(0)

    features_WindDir3pm = []
    for i in range(1, 17):
        if i == int(features['WindDir3pm']):
            features_WindDir3pm.append(1)
        else:
            features_WindDir3pm.append(0)

    int_features =  [float(features['MinTemp']),
                    float(features['MaxTemp']),
                    float(features['Rainfall']),
                    float(features['Evaporation']),
                    float(features['Sunshine']),
                    float(features['WindGustSpeed']),
                    float(features['WindSpeed9am']),
                    float(features['WindSpeed3pm']),
                    float(features['Humidity9am']),
                    float(features['Humidity3am']),
                    float(features['Pressure9am']),
                    float(features['Cloud9am']),
                    float(features['Cloud3pm']),
                    float(features['Temp9am']),
                    float(features['Temp3am']),
                    int(features['RainToday']),
                    int(features['Date'].split('-')[2]),
                    int(features['Date'].split('-')[1]),
                    int(features['Date'].split('-')[0])
                    ] + features_Location + features_WindGustDir + features_WindDir9am + features_WindDir3pm



    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = {0: 'Hujan', 1: 'Tidak hujan'}

    return flask.render_template('main.html', prediction_text='Prediksi cuaca : {}'.format(output[prediction[0]]))

if __name__ == "__main__":
    app.run(debug=True)