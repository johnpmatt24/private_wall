from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 


class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.sender = data['sender']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        # None can represent a currently empty space for a single User dictionary to be placed here, as a Tweet is made by ONE User. We want a User instance and all their attributes to be placed here, so something like data['...'] will not work as we have to make the User instance ourselves.
        self.creator = None
        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('private_wall_schema').query_db(query)
        # Create an empty list to append our instances
        messages = []
        # Iterate over the db results and create instances
        for message in results:
            messages.append( cls(message) )
        return messages
    
    
    
    
    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* from users LEFT JOIN messages on users.id = messages.sender_id LEFT JOIN users as users2 on users2.id = messages.receiver_id where users2.id = %(id)s;" # as key word: the new column has to be an attribute in the __init__ function
        results = connectToMySQL('private_wall_schema').query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages
    
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO messages ( content , sender_id, receiver_id, created_at, updated_at ) VALUES ( %(content)s , %(sender_id)s, %(receiver_id)s, NOW() , NOW() );" # will return id can also be called create
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('private_wall_schema').query_db( query, data ) 
    
    @classmethod
    def get_message(cls, data):
        query = "SELECT * from messages where id = %(id)s;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)
        return cls(results[0])
    
    
    @classmethod
    def update_message(cls, data):
        query = "UPDATE messages SET content = %(content)s, created_at = NOW(), updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('private_wall_schema').query_db(query, data)
    
    
    @classmethod
    def delete(cls, data):
        query = "DELETE from messages where id = %(id)s;"
        return connectToMySQL('private_wall_schema').query_db(query, data)
    
    
    
    
    
    
    
    # @classmethod
    # def get_all_messages_with_creator(cls):
    #     # Get all messages, and their one associated User that created it
    #     query = "SELECT * FROM messages JOIN users ON messages.user_id = users.id;"
    #     results = connectToMySQL('private_wall_schema').query_db(query)
    #     all_messages = []
    #     for row in results:
    #         # Create a Tweet class instance from the information from each db row
    #         one_message = cls(row)
    #         # Prepare to make a User class instance, looking at the class in models/user.py
    #         one_message_user_info = {
    #             # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
    #             "id": row['users.id'], 
    #             "first_name": row['first_name'],
    #             "last_name": row["last_name"],
    #             "email": row['email'],
    #             "password": row['password'],
    #             "created_at": row['users.created_at'],
    #             "updated_at": row['users.updated_at']
    #         }
    #         # Create the User class instance that's in the user.py model file
    #         author = user.User(one_message_user_info)
    #         # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
    #         one_message.creator = author
    #         # Append the Tweet containing the associated User to your list of tweets
    #         all_messages.append(one_message)
    #     return all_messages