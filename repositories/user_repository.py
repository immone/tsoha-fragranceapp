import os
from entities.db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

class UserRepository:
    def register(self, name, password, role):
        hash_value = generate_password_hash(password)
        try:
            sql = """INSERT INTO users (name, password, role)
                         VALUES (:name, :password, :role)"""
            db.session.execute(text(sql), {"name": name, "password": hash_value, "role": role})
            db.session.commit()
        except:
            return False
        return self.login(name, password)


    def login(self, name, password):
        query = "SELECT password, id, role FROM users WHERE name=:name"
        response = db.session.execute(text(query), {"name":name})
        user = response.fetchone()

        if not user or not check_password_hash(user[0], password):
            return False

        session["user_id"] = user[1]
        session["user_name"] = name
        session["user_role"] = user[2]
        session["csrf_token"] = os.urandom(16).hex()

        return True

    def get_user(self):
        return session.get("user_id", 0)

    def logout_user(self):
        del session["user_id"]
        del session["user_name"]
        del session["user_role"]

    def require_role(self, role):
        if role > session.get("user_role", 0):
            abort(403)

    def check_csrf(self):
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

user_repository = UserRepository()