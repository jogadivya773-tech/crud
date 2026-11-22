from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["CRUD_Database"]
collection = db["Students"]

# CREATE
@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Data inserted successfully"})

# READ
@app.route('/students', methods=['GET'])
def read():
    students = list(collection.find({}, {"_id": 0}))
    return jsonify(students)

# UPDATE
@app.route('/update/<name>', methods=['PUT'])
def update(name):
    data = request.json
    result = collection.update_one(
        {"name": name},
        {"$set": data}
    )
    return jsonify({"message": "Update completed", "modified": result.modified_count})

# DELETE
@app.route('/delete/<name>', methods=['DELETE'])
def delete(name):
    result = collection.delete_one({"name": name})
    return jsonify({"message": "Delete completed", "deleted": result.deleted_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))