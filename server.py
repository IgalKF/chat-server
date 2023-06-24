import asyncio
import websockets.server
import rsa

clients = []
public_keys = []

async def handler(client: websockets.server.WebSocketServerProtocol, path: str) -> None:
    clients.append(client)
    await client.send("Logging in to chat ..")

    # Generate keys and retry on failure
    while True:
        try:
            private_key, public_key = rsa.rsa().generate_keys()
            break
        except:
            print("retry..")

    # Greet a user with their private key.
    await client.send(f"Welcome, your private key is: {private_key}")

    # send the new user all the logged in public keys
    for u, k in public_keys:
        await client.send(f'{u} logged in. Their public key is: ' + k)

    # messages from user to user.
    while True:
        try:
            message = await client.recv()
        except:
            print(f'{client.host} couldn\'t send a message')
            clients.remove(client)
            break
        print(message)

        # If the message was sent by the user.
        if ":" in message:
            user, mid, mtype, m = tuple(message.split(':'))
        else:
            public_keys.append((message, public_key))

        # Broadcast the message to all the connected clients
        for connected_client in clients:
            if connected_client.open:
                if ":" in message:
                    await connected_client.send(f'{user}: {m}')
                else:
                    await connected_client.send(f'{message} logged in. Their public key is: ' + public_key)
            else:
                # Remove client if disconnected
                clients.remove(connected_client)


async def main():
    async with websockets.serve(handler, "localhost", 12345):
        await asyncio.Future()  # Run on a thread


if __name__ == "__main__":
    asyncio.run(main())
