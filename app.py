from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://yogeshp:your_password@cluster0.0six4.mongodb.net/name_database?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['name_database']  # Ensure this matches the name of your database
names_collection = db['names']  # Ensure this matches the name of your collection

# Route for displaying the form and the list of names
@app.route('/')
def index():
    names = list(names_collection.find())
    return render_template('index.html', names=names)

# Route for adding a new name
@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name:
        names_collection.insert_one({"name": name})
    return redirect('/')

# Route for deleting a name
@app.route('/delete_name/<name_id>')
def delete_name(name_id):
    names_collection.delete_one({"_id": ObjectId(name_id)})
    return redirect('/')

# Route for editing a name
@app.route('/edit_name/<name_id>', methods=['GET', 'POST'])
def edit_name(name_id):
    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name:
            names_collection.update_one({"_id": ObjectId(name_id)}, {"$set": {"name": new_name}})
        return redirect('/')
    
    name = names_collection.find_one({"_id": ObjectId(name_id)})
    return render_template('edit.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
