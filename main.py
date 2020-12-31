import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
# dict_keys(['hits', 'nbHits', 'page', 'nbPages', 'hitsPerPage', 'ex
# haustiveNbHits', 'query', 'params', 'processingTimeMS'])

req_new = requests.get(new).json()['hits']
req_pop = requests.get(popular).json()['hits']

app = Flask("DayNine")

@app.route("/")
def home():
  word = request.args.get('order_by', 'popular')
  if word:
    fromDb = db.get(word)
    if fromDb:
      news = fromDb
    else:
      if word == "popular":
        news = req_pop
      elif word == "new":
        news = req_new
    db[word] = news
    results = db[word]
  return render_template("index.html", word = word, results = results)


@app.route("/<id>")
def detail(id):
  detail_request = requests.get(make_detail_url(id)).json()
  return render_template("detail.html", result = detail_request)

app.run(host="0.0.0.0")