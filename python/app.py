from flask import Flask, jsonify
from routes.item_routes import bp

app = Flask(__name__)
app.register_blueprint(bp)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
