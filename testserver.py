import asyncio

HOST = "192.168.1.14"
PORT = 11111


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = None
    while data != b"quit":
        data = await reader.read(4096)
        msg = data.decode()
        addr, port = writer.get_extra_info("peername")
        print(f"message from {addr} from port {port}: {msg}")
        writer.write(data)
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def run_server() -> None:
    server = await asyncio.start_server(handle, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
