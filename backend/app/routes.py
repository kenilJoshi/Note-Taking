from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import bcrypt

main = Blueprint('main', __name__)

client = MongoClient("mongodb+srv://keniljoshi3:nDU34V7dV1lszVej@cluster0.m1f8s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Hackathon']
collection = db['User']

@main.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask Backend!"})

@main.route('/api/data', methods=['GET'])
def get_data():
    print(collection)
    data = list(collection.find({}, {"_id": 0}))  # Get all documents, excluding the _id field
    return jsonify({"data": data})

@main.route("/api/register", methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    username = data['username']
    password = data['password']

    if collection.find_one({"username": username}):
        return jsonify({"error": "User shoud be unique"}), 409
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = {
        "username": username,
        "password": hashed_password.decode('utf-8'),
    }

    collection.insert_one(user)
    return jsonify({"message": "User created successfully"}), 201


@main.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json()
    
    username = data['username']
    password = data['password']

    # Find the user by username
    user = collection.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404  # User not found
    
    # Compare the provided password with the hashed password in the database
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
    