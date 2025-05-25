# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
    if 'email' in session:
        return db.reversibleEncrypt('decrypt', session['email'])
    return 'Unknown'

@app.route('/login')
def login():
    return render_template('login.html',user=getUser())

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result = db.authenticate(email, password)

    # Track failed login attempts in session
    if 'failed_attempts' not in session:
        session['failed_attempts'] = 0

    # Use authenticate method from db
    if result.get('success') == 1:
        user = result.get('user', {})
        session['email'] = db.reversibleEncrypt('encrypt', email)
        return json.dumps({'success': True})
    else:
        session['failed_attempts'] += 1
        return json.dumps({'success': 0, 'fail_count': session['failed_attempts']})


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    user = getUser()
    emit('status', {'user': user, 'msg': user + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')

@socketio.on('text', namespace='/chat')
def text(message):
    user = getUser()
    emit('message', {'user': user, 'msg': message['msg']}, room='main')

@socketio.on('left', namespace='/chat')
def left(message):
    user = getUser()
    leave_room('main')
    emit('status', {'user': user, 'msg': user + ' has left the room.', 'style': 'color:gray;text-align: left;width: 100%;'}, room='main')
    
#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
    x = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
    return render_template('home.html',user=getUser(), fun_fact = x)


@app.route('/piano')
def piano():
	return render_template('piano.html',user=getUser())

@app.route('/projects')
def projects():
	return render_template('projects.html',user=getUser())


@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data,user=getUser())


@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
   if request.method == 'POST':
        # Retrieve data from form
        name = request.form.get('name')
        email = request.form.get('email')
        comment = request.form.get('comment')
        
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='master',
            password='master',
            port=3306,
            database='db',
            charset='utf8mb4'
        )
        cursor = cnx.cursor()

        query = "INSERT INTO feedback (name, email, comment) VALUES (%s, %s, %s);"
        cursor.execute(query, (name, email, comment))  # Pass the parameters as a tuple

        # Commit the transaction to save data in the database
        cnx.commit()  # Ensure the data is saved to the database

        # Retrieve all feedback, ordered by comment_id (the primary key)
        feedback_query = "SELECT name, email, comment FROM feedback ORDER BY comment_id DESC;"
        cursor.execute(feedback_query)
        feedback = cursor.fetchall()
        cursor.close()
        cnx.close()
        # Render feedback page
        return render_template('processfeedback.html', feedback=feedback)
   
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

