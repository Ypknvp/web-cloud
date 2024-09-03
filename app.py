from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)

# Correct MongoDB connection string
uri = "mongodb+srv://yogeshp:j22nsWPUUN0uKj9L@cluster0.0six4.mongodb.net/myDatabase?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['myDatabase']  # Replace 'myDatabase' with your actual database name
collection = db['names']

# Display names and form
@app.route('/')
def index():
    names = collection.find()
    return render_template('index.html', names=names)

# Add a new name
@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name:
        collection.insert_one({'name': name})
    return redirect(url_for('index'))

# Edit a name
@app.route('/edit_name/<id>', methods=['GET', 'POST'])
def edit_name(id):
    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name:
            collection.update_one({'_id': ObjectId(id)}, {"$set": {'name': new_name}})
        return redirect(url_for('index'))
    name = collection.find_one({'_id': ObjectId(id)})
    return render_template('edit.html', name=name)

# Delete a name
@app.route('/delete_name/<id>', methods=['GET'])
def delete_name(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
