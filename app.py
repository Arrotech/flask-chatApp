# import time
# from flask import Flask, render_template, redirect, url_for
# from flask_socketio import SocketIO, send, join_room, leave_room
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField
# from wtforms.validators import Length, InputRequired, Email
# from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy import inspect
# from flask_login import login_required, login_user, UserMixin, LoginManager,\
#     logout_user, current_user


# app = Flask(__name__)

# app.config['SECRET_KEY'] = 'verysecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres20930988@localhost:5432/chat'  # noqa
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Bootstrap(app)
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# socketio = SocketIO(app, cors_allowed_origins="*")

# ROOMS = ["backend", "design", "marketting", "leadership", "general"]


# class User(UserMixin, db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(250), unique=True)
#     password = db.Column(db.String(250))

#     def __init__(self, username=None, email=None, password=None):
#         super().__init__()
#         self.username = username
#         self.email = email
#         if password:
#             self.password = generate_password_hash(password)

#     def as_dict(self):
#         return {c.key: getattr(self, c.key)
#                 for c in inspect(self).mapper.column_attrs}

#     def __repr__(self):
#         return "<User '{}'>".format(self.username)


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[
#                            InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('Password', validators=[
#                              InputRequired(), Length(min=8, max=250)])
#     remember = BooleanField('Remember me')


# class SignUpForm(FlaskForm):
#     username = StringField('Username', validators=[
#                            InputRequired(), Length(min=4, max=15)])
#     email = StringField('Email', validators=[
#                         InputRequired(), Email(message='Invalid email')])
#     password = PasswordField('Password', validators=[
#                              InputRequired(), Length(min=8, max=250)])


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# @app.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     return render_template('index.html',
#                            username=current_user.username,
#                            rooms=ROOMS)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
#                 login_user(user, remember=form.remember.data)
#                 return redirect(url_for('home'))
#         return '<h1>Invalid username or password</h1>'
#     return render_template('login.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignUpForm()

#     if form.validate_on_submit():
#         user = User(username=form.username.data,
#                     email=form.email.data, password=form.password.data)
#         db.session.add(user)
#         db.session.commit()

#         return '<h1>New user has been created</h1>'
#     return render_template('signup.html', form=form)


# @socketio.on('message')
# def on_message(data):
#     print(data)
#     msg = data['msg']
#     username = data['username']
#     room = data['room']

#     time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())

#     send({'msg': msg,
#           'username': username,
#           'time_stamp': time_stamp},
#          room=room)


# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send({'msg': username + " has joined the " +
#           room + " channel"}, room=room)


# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send({'msg': username + " has left the " +
#           room + " channel"}, room=room)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)
