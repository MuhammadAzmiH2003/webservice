from flask import Flask
from markupsafe import escape
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask import jsonify
import base64

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#from argon2 import PasswordHasher

#from datetime import datetime
#from datetime import timedelta
#from datetime import timezone

#from flask_jwt_extended import create_access_token
#from flask_jwt_extended import current_user
#from flask_jwt_extended import get_jwt_identity
#from flask_jwt_extended import jwt_required
#from flask_jwt_extended import JWTManager


# Pastikan db.create_all() ditempatkan sebelum pembuatan aplikasi Flask


# Pastikan db.create_all() ditempatkan sebelum pembuatan aplikasi Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflask.db'
db = SQLAlchemy(app)
#db.create_all()  # Buat tabel sebelum mendefinisikan model

# Define the User model setelah tabel dibuat
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

@app.route("/user", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    if request.method == 'POST':
        dataDict = request.get_json()  # Get JSON data from the request
        if not all(key in dataDict for key in ['email', 'name']):
            return jsonify({"message": "Email and Name are required"}), 400
        
        email = dataDict["email"]
        name = dataDict["name"]
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Successfully created user"}), 200

    elif request.method == 'PUT':
        dataDict = request.get_json()
        if not all(key in dataDict for key in ['id', 'email', 'name']):
            return jsonify({"message": "ID, Email, and Name are required"}), 400
        
        id = dataDict["id"]
        email = dataDict["email"]
        name = dataDict["name"]
        
        row = User.query.get(id)
        if row:
            row.email = email
            row.name = name
            db.session.commit()
            return jsonify({"message": "Successfully updated user"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    elif request.method == 'DELETE':
        dataDict = request.get_json()
        if 'id' not in dataDict:
            return jsonify({"message": "ID is required"}), 400
        
        id = dataDict["id"]
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Successfully deleted user"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    else:  # GET
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({"id": user.id, "email": user.email, "name": user.name})
        return jsonify(user_list), 200




# @app.route("/")
# def hello_world():
#     return {
#             "message":"Hellow"
#             },200

# @app.route('/hello')
# def hello():
#     return {
#             "message":"Hello, world!"
#             },200
    
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return {
#             "message":f"Hello, {username}!"
#             },200

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'

# from flask import request

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Lakukan sesuatu dengan file yang diunggah di sini
        # Misalnya, menyimpannya di server atau melakukan proses lainnya
        # Di sini kita hanya mengembalikan respons bahwa file telah diunggah dengan sukses
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    # Definisikan ekstensi file yang diizinkan di sini
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


if __name__ == '__main__':
    app.run()