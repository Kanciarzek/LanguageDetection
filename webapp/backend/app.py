from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.config.from_json('flask_config.json', silent=False)
print("dupa")


@app.route("/upload", methods=["POST"])
def predict_language():
    raw_wave = flask.requests.get_data()
    print(raw_wave)
    return jsonify({"outcome":"SUCCESS"}) 

@app.route("/", methods=["GET", "POST"])
def default_route():
    print("tutej")
    return jsonify({"outcome" : "FAIL"})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)