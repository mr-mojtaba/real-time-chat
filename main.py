# Need to install ( pip install flask )
from flask import Flask, render_template, request, redirect, url_for, session

# Need to install ( pip install flask flask-socketio )
from flask_socketio import SocketIO, emit

# Standard python library
from werkzeug.security import generate_password_hash, check_password_hash

# Creating a web application.
app = Flask(__name__)

# Creating communication with the server for messages in real-time.
socketio = SocketIO(app)

users = {}


# ---------- Functions ----------

# To specify the link to register and authorized methods.
@app.route("/register", methods=['Get', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username in users:
            error = "This username already exists!"
        elif password != confirm_password:
            error = "Passwords do not match!"
        else:
            users[username] = {
                'username': username,
                'password': generate_password_hash(password)
            }
            print(users)
            return redirect(url_for('login'))
        print(error)
        return render_template('register.html', error=error)
    return render_template('register.html')


# To specify the link to login and authorized methods.
@app.route("/login", methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        error = "The username or password is incorrect!"
        print("error!")
        return render_template('login.html', error=error)
    return render_template('login.html')


# To specify the link to logout and authorized methods.
@app.route("/logout")
def logout():
    # Deleting the username from the session.
    session.pop('username', None)
    return redirect(url_for('index'))


# To specify the link to index and authorized methods.
@app.route("/")
def index():
    if "username" in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))


@socketio.on('message')
def handle_message(message):
    emit('message', {'username': session['username'], 'message': message}, broadcast=True)


if __name__ == '__main__':
    app.secret_key = '8MLn5jxy7c3ouKrk4DCe5ALMrg29'
    socketio.run(app, debug=True)
