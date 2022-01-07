from flask import Flask
from werkzeug.wrappers import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to ReviewSense API!</p>"

# Gives all the aspects
@app.route("/restaurant/<restaurant_name>", methods=['GET']) 
def restaurant(restaurant_name):
    # return json of <aspect, polarity score> else 404
    return None

# Specific feature, which may not be in the pre-set options
@app.route("/restaurant/<restaurant_name>/feature/")
def restaurant_and_feature(restaurant_name, feature):
    args = request.args
    feature_name = args['feature_name']
    feature_corpus = args['corpus']
    # return polarity score for given feature else 404 if restaurant not in database
