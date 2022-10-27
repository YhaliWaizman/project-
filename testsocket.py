import asyncio
from click import command
import psutil
import os

from pygame import QUIT

HOST = "192.168.1.14"
PORT = 11111


def SendProcs() -> bin:
    processes = []
    for proc in psutil.process_iter():
        processes.append(f"{proc.pid}\t{proc.name()}")
    data = "\n".join(processes)
    return data.encode()


def WriteProcs() -> None:
    with open("testfile.txt", 'w') as file:
        for proc in psutil.process_iter():
            file.write(f"{proc.pid}\t{proc.name()}")


async def run_client() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)

    writer.write(b"connected")
    await writer.drain()
    countdown = 10

    while True:
        data = await reader.read(2048)
        if not data:
            raise Exception("Bye Bye!")

        data = data.decode()
        print(f"recieved: {data}")
        try:
            command, pid = " ".split(data)
            if (command == "KILL"):
                writer.write(b"heheded")
                await writer.drain()
                os.kill(pid)
        except:
            continue

        if command != QUIT:
            await asyncio.sleep(3)
            """
            writer.write(SendProcs())
            await writer.drain()
            """
            WriteProcs()
            countdown -= 1
        else:
            writer.write(b"quit")
            await writer.drain()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
