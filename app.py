from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection URI
uri = "mongodb+srv://yogeshp:your_password@cluster0.0six4.mongodb.net/name_database?retryWrites=true&w=majority"

# Initialize MongoDB client and database
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['name_database']  # Make sure this matches your database name
names_collection = db['names']  # Make sure this matches your collection name

# Route for displaying the form and the list of names
@app.route('/')
def index():
    try:
        names = list(names_collection.find())
        return render_template('index.html', names=names)
    except Exception as e:
        print(f"Error fetching names: {e}")
        return f"Error fetching names: {e}"

# Route for adding a new name
@app.route('/add_name', methods=['POST'])
def add_name():
    try:
        name = request.form.get('name')
        if name:
            names_collection.insert_one({"name": name})
        return redirect('/')
    except Exception as e:
        print(f"Error adding name: {e}")
        return f"Error adding name: {e}"

# Route for deleting a name
@app.route('/delete_name/<name_id>')
def delete_name(name_id):
    try:
        names_collection.delete_one({"_id": ObjectId(name_id)})
        return redirect('/')
    except Exception as e:
        print(f"Error deleting name: {e}")
        return f"Error deleting name: {e}"

# Route for editing a name
@app.route('/edit_name/<name_id>', methods=['GET', 'POST'])
def edit_name(name_id):
    if request.method == 'POST':
        try:
            new_name = request.form.get('name')
            if new_name:
                names_collection.update_one({"_id": ObjectId(name_id)}, {"$set": {"name": new_name}})
            return redirect('/')
        except Exception as e:
            print(f"Error updating name: {e}")
            return f"Error updating name: {e}"

    try:
        name = names_collection.find_one({"_id": ObjectId(name_id)})
        return render_template('edit.html', name=name)
    except Exception as e:
        print(f"Error fetching name for edit: {e}")
        return f"Error fetching name for edit: {e}"

if __name__ == '__main__':
    app.run(debug=True)
