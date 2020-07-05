from flask import Flask, jsonify, render_template, make_response, request

app = Flask(__name__)
app.config.from_json('flask_config.json', silent=False)


@app.route("/sound_analyze", methods=["POST"])
def predict_language():
    print(request.files)
    return make_response(jsonify({'language': 'Spanish'}), 200)


@app.route("/", methods=["GET"])
def default_route():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
