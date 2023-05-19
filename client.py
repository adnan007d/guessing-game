import asyncio
import socketio
import sys

sio = socketio.AsyncClient()


# This a utility function to get input from the user asynchronously
# So if any other user wins the game will disconnect
async def ainput(string: str) -> str:
    await asyncio.to_thread(sys.stdout.write, f"{string}")
    sys.stdout.flush()
    return (await asyncio.to_thread(sys.stdin.readline)).rstrip("\n")


@sio.event
async def connect():
    print("connection established")
    await sio.emit("start")


@sio.event
async def guess(data):
    global pending_input
    print(data["message"])
    guess = await ainput("Enter the number: ")
    await sio.emit("guess", {"guess": guess})


@sio.event
async def result(data):
    print(data["message"])
    await sio.disconnect()


@sio.event
async def winner(data):
    print(data["message"])
    await sio.disconnect()


@sio.event
async def disconnect():
    print("disconnected from server")


async def main():
    await sio.connect("http://localhost:6969")
    await sio.wait()
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
