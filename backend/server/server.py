# MUST BE FIRST
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit, join_room
from flask_compress import Compress


app = Flask(__name__)
Compress(app)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    ping_interval=25,
    ping_timeout=60,
)

@app.route("/")
def home():
    return {"status": "ok", "message": "WebXR backend running 🚀"}

@socketio.on("join")
def on_join(room):
    join_room(room)
    print(f"👥 User joined room: {room}")
    emit("ready", room=room, include_self=False)

@socketio.on("offer")
def on_offer(data):
    print("📡 Received offer → forwarding")
    emit("offer", data["description"], room=data["room"], include_self=False)

@socketio.on("answer")
def on_answer(data):
    print("📡 Received answer → forwarding")
    emit("answer", data["description"], room=data["room"], include_self=False)

@socketio.on("candidate")
def on_candidate(data):
    print("🌐 Received ICE candidate → forwarding")
    emit("candidate", data["candidate"], room=data["room"], include_self=False)


# Do NOT run socketio.run() here.
# Gunicorn will load "app", and the worker class will handle WebSockets.

if __name__ != "__main__":
    # this lets gunicorn import app without running socketio.run()
    pass

