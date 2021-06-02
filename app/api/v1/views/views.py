import time
from flask import render_template, redirect, url_for
from flask_socketio import send, join_room, leave_room, emit
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from app.api.v1 import chat_v1
from app.extensions import socketio
from app.api.v1.forms.forms import LoginForm, SignUpForm
from app.api.v1.models.models import User, ChatHistory
from app.extensions import db, login_manager

ROOMS = ["backend", "design", "marketting", "leadership", "general"]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@chat_v1.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('index.html',
                           username=current_user.username,
                           rooms=ROOMS)


@chat_v1.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('chat_v1.home'))
        return render_template('login.html',
                               form=form,
                               message='Invalid Username or Password')
    return render_template('login.html', form=form)


@chat_v1.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat_v1.home'))


@chat_v1.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('chat_v1.login'))
    return render_template('signup.html', form=form)


@socketio.on('message')
def on_message(data):
    message = ChatHistory(username=data['username'], room=data['room'], message=data['msg'])
    db.session.add(message)
    db.session.commit()
    msg = data['msg']
    username = data['username']
    room = data['room']

    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())

    send({'msg': msg,
          'username': username,
          'time_stamp': time_stamp},
         room=room)


@socketio.on('join')
def on_join(data):
    messages = ChatHistory.query.filter_by(room=data['room'])
    chat_history = []
    for message in messages:
        chat_history.append(message.as_dict())
    username = data['username']
    room = data['room']
    join_room(room)
    send({'msg': username + " has joined the " +
          room + " channel"}, room=room)
    emit('joined', chat_history)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({'msg': username + " has left the " +
          room + " channel"}, room=room)
