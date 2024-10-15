from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)


@app.route("/")
def hello_microsoft():
    return "Hello Microsoft!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
