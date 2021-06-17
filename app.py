from flask import Flask

app = Flask(__name__)


@app.route("/")
def server_up():
    return "Server up"
