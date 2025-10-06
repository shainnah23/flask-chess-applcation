from flask import Blueprint,jsonify,request,send_from_directory
from app.models import Users
from app.db import db
import re
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

bcrypt = Bcrypt()


#create student bluprint
users_bp=Blueprint("users",__name__)

@users_bp.route("/add",methods=["POST"])
def add_users():
  data=request.get_json()

  name=data.get("name")
  email=data.get("email")
  password=data.get("password")

  if not name:
    return jsonify({"error":"Name is required"}),400
    
  if not email:
    return jsonify({"error":"Email is required"}),400

  email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

  if not re.match(email_regex,email):
    return jsonify({"error":"Invalid email address"})

  if not password:
    return jsonify({"error": "Name, email, and password are required"}), 400

  exists=Users.query.filter_by(email=email).first()

  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  
  new_users = Users(name=name, email=email, password=hashed_password)
  db.session.add(new_users)
  db.session.commit()

  return jsonify({
    "message":"Member added successfully",
    "member":{
      "id":new_users.id,
      "name":new_users.name,
      "email":new_users.email,
      "created_at":new_users.created_at
    }
  })

@users_bp.route("/login",methods=["POST"])
def login_users():
  data=request.get_json()

  email=data.get("email")
  password=data.get("password")

  if not email or not password:
    return jsonify({"message":"Email and password are required"}),400
  
  users=Users.query.filter_by(email=email).first()

  if not users:
    return jsonify({"message":"user not found"}),401
  
  check_password = bcrypt.check_password_hash(users.password, password)

  if not check_password:
    return jsonify({"message":"Invalid email or password"}),401
  

  access_token=create_access_token(
      identity={"id":f"{users.id}","name":users.name},
      expires_delta=timedelta(seconds=30)
    )

  return jsonify({ "token":access_token })