#  validate and authenticate the user 

from flask import jsonify,Blueprint,request
from app.models import Users
from app.db import db
import re

users_bp=Blueprint("users",__name__)

@users_bp.route("/add",methods=["POST"])
def add_users():
    print("Add user was hit")
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
    
    exists=Users.query.filter_by(email=email).first()

    if exists:
        return jsonify({"error":"Email in use"}),400

 
    
    new_user=Users(name=name,email=email,password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message":"member added",
        "student":{
            "id":new_user.id,
            "name":new_user.name,
            "email":new_user.email,
            "created_at":new_user.created_at
        }
    }),201