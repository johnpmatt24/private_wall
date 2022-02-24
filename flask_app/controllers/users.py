from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user, message
from flask_app.controllers import messages


@app.route("/")
def main():
    return redirect("/register")


@app.route("/register")
def register():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")




@app.route("/user/register", methods = ["POST"])
def registration():
    if user.User.is_valid(request.form):
        in_database = user.User.get_user_by_email(request.form)
        if in_database:
            flash("Email already taken")
            return redirect("/")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password" : pw_hash
        }
        user_id = user.User.save(data) #returns an id when we create/save a user
        session["user_id"] = user_id
        return redirect('/login')
    return redirect("/")





@app.route("/wall")
def wall():
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id" : session['user_id']
    }
    
    return render_template("wall.html", user = user.User.get_user(data), users = user.User.get_all(), messages = message.Message.get_user_messages(data))






@app.route("/user/login", methods = ["POST"])
def user_login():
    in_database = user.User.get_user_by_email(request.form)
    
    if not in_database:
        flash('Invalid Email/Password. Try Again')
    
    if not bcrypt.check_password_hash(in_database.password, request.form['password']):
        flash('Invalid Email/Password. Try Again')
        return redirect("/login")
    
    session['user_id'] = in_database.id
    return redirect("/wall")

