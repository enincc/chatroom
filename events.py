from flask import session
from flask_socketio import (
    emit,
    join_room,
    leave_room,
    SocketIO
)

socketio = SocketIO()


@socketio.on('join', namespace='/chat')
def join(data):
    room = data['room']
    join_room(room)
    session['room'] = room
    name = session.get('name')
    message = '----- 进入了房间 -----'.format(name)
    d = dict(
        user=name,
        message=message,
    )
    emit('status', d, room=room)


@socketio.on('send', namespace='/chat')
def send(data):
    room = session.get('room')
    name = session.get('name')
    message = data.get('message')
    d = dict(
        user=name,
        message=message,
    )
    emit('message', d, room=room)


@socketio.on('leave', namespace='/chat')
def leave(data):
    room = session.get('room')
    leave_room(room)
    name = session.get('name')
    d = dict(
        user=name,
        message='----- 离开了房间 -----',
    )
    emit('status', d, room=room)
