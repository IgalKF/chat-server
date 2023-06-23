import asyncio
import websockets.server
import rsa

clients = []


async def handler(client: websockets.server.WebSocketServerProtocol, path: str) -> None:
    clients.append(client)
    await client.send("Logging in to chat ..")
    while True:
        try:
            private_key, public_key = rsa.rsa().generate_keys()
            break
        except:
            print("retry..")
    await client.send(f"Welcome, your private key is: {private_key}")
    while True:
        try:
            message = await client.recv()
        except:
            print(f'{client.host} couldn\'t send a message')
        print(message)
        if ":" in message:
            user, mid, mtype, m = tuple(message.split(':'))
        
        for connected_client in clients:
            if connected_client.open:
                if ":" in message:
                    await connected_client.send(f'{user}: {m}')
                else:
                    await connected_client.send(f'{message} logged in. Their public key is: ' + public_key)
            else:
                clients.remove(connected_client)


async def main():
    async with websockets.serve(handler, "localhost", 12345):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
