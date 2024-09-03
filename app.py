from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection string
uri = "mongodb+srv://yogeshp:your_password@cluster0.xxxxx.mongodb.net/myDatabase?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

# Database and collection
db = client['myDatabase']  # Replace 'myDatabase' with your actual database name
collection = db['names']   # Replace 'names' with your collection name

# Display names and form
@app.route('/')
def index():
    try:
        names = collection.find()
        return render_template('index.html', names=names)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Error fetching data."

# Add a new name
@app.route('/add_name', methods=['POST'])
def add_name():
    name = request.form.get('name')
    if name:
        try:
            collection.insert_one({'name': name})
        except Exception as e:
            print(f"Error inserting data: {e}")
    return redirect(url_for('index'))

# Edit a name
@app.route('/edit_name/<id>', methods=['GET', 'POST'])
def edit_name(id):
    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name:
            try:
                collection.update_one({'_id': ObjectId(id)}, {"$set": {'name': new_name}})
            except Exception as e:
                print(f"Error updating data: {e}")
        return redirect(url_for('index'))
    try:
        name = collection.find_one({'_id': ObjectId(id)})
        return render_template('edit.html', name=name)
    except Exception as e:
        print(f"Error fetching data for editing: {e}")
        return "Error fetching data."

# Delete a name
@app.route('/delete_name/<id>', methods=['GET'])
def delete_name(id):
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(f"Error deleting data: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

