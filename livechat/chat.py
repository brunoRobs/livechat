import asyncio
import websockets

class Chat: 
    def __init__(self, host, port): 
        self.clients = set()
        self.websocket = websockets.serve(self._handler, host, port)

    async def _handler(self, websocket, path):
        self.clients.add(websocket)

        try:
            async for message in websocket:
                for client in self.clients:
                    await client.send(message)
        
        finally:
            self.clients.remove(websocket)

    def start(self): 
        asyncio.get_event_loop().run_until_complete(self.websocket)
        asyncio.get_event_loop().run_forever()