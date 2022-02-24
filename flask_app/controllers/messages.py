from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import message, user
from flask_app.controllers import users


@app.route('/send/message', methods = ["POST"])
def send_message():
    data = {
        "sender_id": request.form["sender_id"],   #sender_id and receiver_id will be hidden inputs
        "receiver_id": request.form['receiver_id'],
        "content" : request.form['content']
    }
    message.Message.save(data)
    return redirect("/wall")


@app.route("/delete/message/<int:id>")
def delete_message(id):
    data = {
        "id" : id
    }
    
    message.Message.delete(data)
    return redirect("/wall")