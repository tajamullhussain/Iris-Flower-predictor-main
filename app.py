from flask import Flask, render_template, request
import joblib
import numpy as np
import os
import sys
import traceback

app = Flask(__name__)

model = None

def load_model():
    global model
    if model is None:
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
            model = joblib.load(model_path)
            print("Iris model loaded successfully on Vercel!")
        except Exception as e:
            print("MODEL LOAD FAILED:", str(e), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            model = None  
    return model

try:
    print("App starting... imports OK")
except Exception as e:
    print("STARTUP CRASH:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    loaded_model = load_model()
    if loaded_model is None:
        return render_template('index.html', prediction_text="Error: Model could not be loaded. Contact admin.")

    try:
        float_features = [float(x) for x in request.form.values()]
        features = [np.array(float_features)]
        
        prediction = loaded_model.predict(features)
        
        flower_names = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
        result = flower_names[int(prediction[0])]
        
        return render_template('index.html', prediction_text=f'Predicted Flower: {result}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Prediction error: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)