from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

# MongoDB Atlas connection
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['test']  # Replace 'test' with your database name
collection = db['names']

@app.route('/')
def index():
    names = collection.find()
    return render_template('index.html', names=names)

@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form['name']
    collection.insert_one({'name': name})
    return redirect(url_for('index'))

@app.route('/delete_name/<name_id>')
def delete_name(name_id):
    collection.delete_one({'_id': ObjectId(name_id)})
    return redirect(url_for('index'))

@app.route('/edit_name/<name_id>', methods=['POST'])
def edit_name(name_id):
    new_name = request.form['name']
    collection.update_one({'_id': ObjectId(name_id)}, {'$set': {'name': new_name}})
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
