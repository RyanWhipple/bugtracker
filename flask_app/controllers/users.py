from flask import render_template, redirect, session, flash, request
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Homepage for Login and Registration
@app.route('/')
def home():
    if 'user_id' in session:
        print("user_id in session == True")
        user    = session.user_id
    else:
        print("user_id in session == False")
        user    = None
    return render_template('index.html', user=user)

# Register
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }

    session['user_id'] = User.save(data)
    
    return redirect("/bugs")


# Update Account
@app.route('/user/<int:user_id>/update', methods=['POST'])
def update(user_id):
    if not User.validate_update(request.form):
        return redirect('/')

    data = {
        'id'            : session['user_id'],
        'first_name'    : request.form['first_name'],
        'last_name'     : request.form['last_name'],
        'email'         : request.form['email'],
    }

    User.update(data)
    
    return redirect("/bugs")


# Login
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/bugs")

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Display a User and All Their Bugs and Updates
@app.route('/users/<int:user_id>')
def user(user_id):
    if 'user_id' not in session:
        return redirect('/')
     
    # Get User Data
    data = {
        'id'    :   session['user_id']
    }
    user = User.get_by_id(data)

    return render_template(
        'user.html',
        user=user,
        )