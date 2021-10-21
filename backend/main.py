from flask import Flask, jsonify, render_template
from flask import request
from flask_cors import CORS

from recommender import make_recommendation
import requests


app = Flask(__name__, template_folder="./")
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def get_movie():
    # searchTerms = ['horror', 'tomcruise', 'jamescameron', 'blood boat romance magic']
    genre = request.args.get("genre").replace(" ", "")
    actor = request.args.get("actor").replace(" ", "")
    director = request.args.get("director").replace(" ", "")
    keywords = request.args.get("keywords").replace(" ", "").split(",")
    keywords = " ".join(keywords)
    searchTerms = [genre, actor, director, keywords]
    print("HELLo", searchTerms)
    res = make_recommendation(searchTerms=searchTerms)
    res2 = [{"name": i[0], "id": i[1]} for i in res]
    print(res2)
    return jsonify({"movies": res2})
    # return res2
    # return "Web App with Python Flask!"


# @app.route("/get")
# def get_from_api():
#     query = request.args.get("msg")
#     genre = request.args.get("genre").replace(" ", "") + " "
#     actor = request.args.get("actor").replace(" ", "") + " "
#     director = request.args.get("director").replace(" ", "") + " "
#     keywords = request.args.get("keywords").replace(" ", "") + " "
#     temp = genre + actor + director + keywords
#     print(query)

#     url = (
#         "https://uitxgusnt5.execute-api.us-west-1.amazonaws.com/production/get?msg="
#         + query
#     )
#     print(url)
#     try:
#         response = requests.get(url)
#         return response.text
#     except Exception as e:
#         print(e)


app.run(debug=True)
