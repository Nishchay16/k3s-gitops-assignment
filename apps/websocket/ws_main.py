apiVersion: v1
kind: ConfigMap
metadata:
  name: ws-code
data:
  ws_main.py: |
    from fastapi import FastAPI, WebSocket

    app = FastAPI()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
