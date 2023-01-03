from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import requests
from bs4 import BeautifulSoup

ca = certifi.where()

client = MongoClient("mongodb://sparta:sparta@ac-wqtlhrl-shard-00-00.7frjr12.mongodb.net:27017,ac-wqtlhrl-shard-00-01.7frjr12.mongodb.net:27017,ac-wqtlhrl-shard-00-02.7frjr12.mongodb.net:27017/?ssl=true&replicaSet=atlas-hiv7s7-shard-0&authSource=admin&retryWrites=true&w=majority", tlsCAFile=ca)

db = client.AnimeProject

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('indext.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    username_recieve = request.form['username_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')
    rating = soup.select_one('.score > .score-label').text

    image = og_image['content']
    title = og_title['content']
    desc = og_description['content']

    doc = {
        'username':username_recieve,
        'image':image,
        'title':title,
        'description':desc,
        'star':star_receive,
        'comment':comment_receive,
        'rate':rating
    }

    db.myanime.insert_one(doc)

    return jsonify({'msg':'DATA TERSIMPAN!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.myanime.find({},{'_id': False}))
    return jsonify({'movies':movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)