import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle

app = Flask(__name__)
model = pickle.load(open('xgb_classifer.pkl','rb'))

def word_div_char(word):
  chars =[]
  for char in word:
    chars.append(char)
  return chars

vectorizer = pickle.load(open('vectorizer.pkl','rb'))

@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')
    #return render_template('index.html')



def transformation(password):
    parray = np.array([password])
    x_pred = vectorizer.transform(parray)
    return x_pred


@app.route('/predict',methods = ['POST'])
def predict():
    score = []
    rawdata = str(request.form['password'])
    transformed_pass = transformation(rawdata)
    prediction = model.predict(transformed_pass)
    if prediction[0] == 0:
      score.append('LOW')
    elif prediction[0] == 1:
      score.append("MEDIUM") 
    elif prediction[0] == 2:
      score.append("HIGH")
    else:
      score.append("NULL")

    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text=f'Your Password " {rawdata} " has strength of {score[0]}')

if __name__ == '__main__':
    app.run(debug=True) 
