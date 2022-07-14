from flask_app import app
from flask_app.config.mysqlconnection import  connectToMySQL
from flask_app.models import recipe, product, moment
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db='sweetys_bakery_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;" #this field "user_id" must always match what is in the query_data field in the session located in the dashboard route, this case.
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        # if len(result) < 1:
        #     return False -->don't need these previous 2 line; however, just kept them just in case.
        return cls(result[0]) #this was initially "return result" butchanged back to "return cls(result[0])".

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])   #this was initially "return result" butchanged back to "return cls(result[0])".

    @classmethod
    def get_user_with_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id" #this needs to be completed

    


    @staticmethod
    def validate_register(form_data):
        print("starting validation")
        is_valid = True
        if len(form_data["first_name"]) < 2:  #the first and last name fields must also contain a portion of if statement that requires that these fields be letters only and no integers. Add this in later.
            flash("First name must be present!")
            is_valid = False
        if len(form_data["last_name"]) < 2:
            flash("Last name must be present!")
            is_valid = False
        
        if len(form_data["email"]) < 1:
            flash("Email must be present!")
            is_valid = False
# test whether a field matches the pattern
        elif not EMAIL_REGEX.match(form_data["email"]): 
            flash("Please provide a valid email!")
            is_valid = False 

        if len(form_data["password"]) < 8:
            flash("Password must be at least 8 characters long!")
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash("Password and confirmation password must match!")
            is_valid = False
        return is_valid

    @staticmethod    
    def validate_login(form_data):
        is_valid = True 
        user_in_db = User.get_by_email(form_data)
            # user is not registered in the db
        if not user_in_db:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, form_data['password']):
            # if we get False after checking the password
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid
