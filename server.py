from aiohttp import web
import socketio
import random


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

number: int = 0

# Stores the sid of the player who is currently playing
players: list[str] = []


@sio.event
async def connect(sid, environ):
    print("connect ", sid)
    players.append(sid)


@sio.event
async def guess(sid, data):
    global number
    guess = data["guess"]

    if not guess.isdigit():
        await sio.emit("guess", {"message": "not a number"}, room=sid)

    guess = int(guess)

    if guess == number:
        await sio.emit("winner", {"message": "You Won!"}, room=sid)
        await sio.emit("result", {"message": f"Player {players.index(sid) + 1} won!"})
    elif number < guess:
        await sio.emit("guess", {"message": "lower"}, room=sid)
    else:
        await sio.emit("guess", {"message": "higher"}, room=sid)


@sio.event
def disconnect(sid):
    players.remove(sid)
    print("disconnect ", sid)


@sio.event
async def start(sid):
    print("Game started for ", sid)
    await sio.emit("guess", {"message": "Guess the number"}, room=sid)


if __name__ == "__main__":
    number = random.randint(1, 20)
    print(number)
    web.run_app(app, port=6969)
