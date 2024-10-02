from flask import Flask, jsonify, request
import json
import datetime
from tensorflow.keras.models import load_model
import numpy as np
import requests

with open("data.json") as data:
    jsondata = json.load(data)

# Load the H5 model
model = load_model("model10plantrec.h5")

app = Flask(__name__)


@app.route("/")
def main():
    return jsonify({"message": "Connection success. This is crop reccomendation API."})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    N = float(data.get("n"))
    P = float(data.get("p"))
    K = float(data.get("k"))
    ph = float(data.get("ph"))
    lon = data.get("lon")
    lat = data.get("lat")
    weather = json.loads(
        requests.get(
            "https://api.openweathermap.org/data/2.5/weather?lat="
            + str(lat)
            + "&lon="
            + str(lon)
            + "&appid=64dd867de5e5d328aa7ee8d45c5271ad"
        ).text
    )
    temp = (float(weather["main"]["temp"]) - 32) * 5 / 9
    humid = float(weather["main"]["humidity"])
    location = weather["name"]
    rainfall = jsondata["rainfall"][datetime.datetime.now().strftime("%m")]

    feature_list = [N, P, K, temp, humid, ph, rainfall]
    singl_pred = np.array(feature_list).reshape(1, -1)

    prediction = model.predict(singl_pred)
    result_index = np.argmax(prediction, axis=1)[0]

    crop_arr = [
        "Arixtolochia acuminata",
        "Cassia Fistula",
        "Jengkol",
        "Cinamomum verum",
        "Klero Dendrum",
        "Melicope Pteleifolia",
        "Micromelum Minutum",
        "Mussaenda Frondosa",
        "Saga",
        "Uvaria",
    ]

    if result_index < len(crop_arr):
        result = crop_arr[result_index]
        return jsonify(
            {
                "crop": result,
                "description": jsondata["plant-description"][result]["description"],
                "location": location,
            }
        )
    else:
        return jsonify({"crop": "N/A"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
