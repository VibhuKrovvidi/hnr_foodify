from flask import Flask
from werkzeug.wrappers import request
from data_processing import process_for_restaurant

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to ReviewSense API!</p>"

# Returns polarity score for all default aspects
@app.route("/restaurant/<restaurant_name>", methods=['GET']) 
def restaurant(restaurant_name):
    # return json of <aspect, polarity score> else 404
    process_for_restaurant(restaurant_name=restaurant_name)
    return None

# Specific feature, which may not be in the pre-set options
@app.route("/restaurant/<restaurant_name>/feature/")
def restaurant_and_feature(restaurant_name, feature):
    args = request.args
    # fetch feature specifics from the request body
    current_corpus = {
        args['feature_name']: args['corpus']
    }
    # return polarity score for given feature else 404 if restaurant not in database
    process_for_restaurant(restaurant_name=restaurant_name, current_corpus=current_corpus)
    return None