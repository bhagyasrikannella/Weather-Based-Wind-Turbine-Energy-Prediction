from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load model
model_path = "wind_model.sav"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        wind_speed = float(data.get("wind_speed", 0))
        theoretical_power = float(data.get("theoretical_power", 0))

        input_features = np.array([[wind_speed]])  # model expects 1 feature
        prediction = model.predict(input_features)[0]
        prediction = round(prediction, 2)

        return jsonify({"prediction": prediction})
    except Exception as e:
        print("Error in /predict:", e)
        prediction = round(wind_speed * theoretical_power * 0.5, 2)
        return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)
