from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# Registration & login page 
@app.route('/')
def login_reg_page():
    if 'id' in session:
        return redirect('/success')
    return render_template('index.html')


# Route to registration & return if user input errors
@app.route('/register', methods=['POST'])
def register():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
    }
    if not User.validate_register(data):
        flash("*Registration information is incomplete or not meeting data requirements, please try again", "register_errors")
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    del data['confirm_password']
    print(data)
    user_id = User.create_user(data)
    session['id'] = user_id
    return redirect('/success')


# Route to login page if user input errors
@app.route('/login', methods=['POST'])
def login():
    verify_user = User.get_by_email({'email': request.form['email']})
    if not verify_user:
        flash("*User email is not recongnized", "login_errors")
        return redirect('/')
    if not bcrypt.check_password_hash(verify_user.password, request.form['password']):
        flash("*Password incorrect", "login_errors")
        return redirect('/')
    session['id'] = verify_user.id
    return redirect('/success')


# Route to sucessful login page
@app.route('/success')
def success():
    if 'id' not in session:
        return redirect('/')
    logged_in_user = User.get_one({'id': session['id']})
    return render_template('success.html', user=logged_in_user)


# Route back to registaiton page after logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out', 'logout')
    return redirect('/')