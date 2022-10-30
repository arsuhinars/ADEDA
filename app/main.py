from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get('/')
def index():
    return JSONResponse({'hello': 'world', 'pi': 3.34, 'happy': True})
