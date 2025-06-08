import flask

app = flask.Flask(__name__)

print("started!")

@app.route("/")
def index():
    return "Hello world!"

app.run()