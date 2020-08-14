import numpy as np
from flask import Flask, jsonify, render_template, make_response, request
import requests

from webapp.backend.predict import preprocess

app = Flask(__name__)
app.config.from_json('flask_config.json', silent=False)

language_list = ["Chinese", "English", "German", "Polish", "Russian"]


@app.route("/sound_analyze", methods=["POST"])
def predict_language():
    request.files['audio'].save('audio.wav')
    spectrogram: np.ndarray = preprocess(request.files['audio'])
    spectrogram: np.ndarray = spectrogram.reshape((1, spectrogram.shape[0], spectrogram.shape[1], 1))
    input_json: dict = {"instances": spectrogram.tolist()}
    response: requests.Response = requests.post("http://localhost:8501/v1/models/voice_model:predict", json=input_json)
    language_index: int = int(np.argmax((response.json()['predictions'][0])))
    return make_response(jsonify({'language': language_list[language_index]}), 200)


@app.route("/", methods=["GET"])
def default_route():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host='0.0.0.0', ssl_context=('certificate.crt', 'privateKey.key'))
