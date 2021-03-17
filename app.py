import time
from flask import Flask, render_template
from flask_socketio import SocketIO, send, join_room, leave_room


app = Flask(__name__)

app.config['SECRET_KEY'] = 'verysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

ROOMS = ["backend", "design", "marketting", "leadership", "general"]


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', username='arrotech', rooms=ROOMS)


@socketio.on('message')
def on_message(data):
    print(data)
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
    username = data['username']
    room = data['room']
    join_room(room)
    send({'msg': username + " has joined the " +
          room + " channel"}, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({'msg': username + " has left the " +
          room + " channel"}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
