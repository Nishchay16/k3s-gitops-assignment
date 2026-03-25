apiVersion: v1
kind: ConfigMap
metadata:
  name: http-code
data:
  main.py: |
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/hello")
    def hello():
        return {"message": "Hello from HTTP Service"}
