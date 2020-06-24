from flask import Flask, jsonify, render_template


app = Flask(__name__)
app.config.from_json('flask_config.json', silent=False)


@app.route("/sound_send", methods=["POST"])
def predict_language():
    return jsonify({"outcome": "SUCCESS"})


@app.route("/", methods=["GET"])
def default_route():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
