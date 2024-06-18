from fastapi import FastAPI

app = FastAPI()


@app.get('/laris')
def read_root():
    return {'message': 'Hello, World!'}
