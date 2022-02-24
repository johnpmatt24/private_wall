# import the function that will return an instance of a connection
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import message
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)        # we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$') 
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.messages = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('private_wall_schema').query_db(query)
        # Create an empty list to append our instances
        users = []
        # Iterate over the db results and create instances
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('private_wall_schema').query_db( query, data )
    
    @classmethod
    def get_user(cls, data):
        query = "SELECT * from users where id = %(id)s";
        results = connectToMySQL('private_wall_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * from users where email = %(email)s";
        results = connectToMySQL('private_wall_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET password = %(password)s, created_at = NOW() WHERE email = %(email)s";
        return connectToMySQL('private_wall_schema').query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE from users where id = %(id)s"
        return connectToMySQL('private_wall_schema').query_db(query, data)
    
    
    @staticmethod
    def is_valid(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Password must contain at least one UPPERCASE LETTER, one LOWERCASE LETTER, ONE DIGIT, ONE SPECIAL CHARACTER eg '@', '&', '$' etc and have a MINIMUM of 8 CHAACTERS.")
            is_valid = False
        if user["confirmpassword"] != user["password"]:
            flash('Passwords do not match. Please Try again.')
            is_valid = False
        return is_valid
    