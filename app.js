from flask import Flask, render_template, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://yogeshp:j22nsWPUUN0uKj9L@cluster0.0six4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['name_database']  # Create or access the database
names_collection = db['names']  # Create or access the collection

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

if __name__ == '__main__':
    app.run(debug=True)
