import uvicorn
from fastapi import FastAPI
from api.api_v1 import api

app = FastAPI()
app.include_router(api.router, prefix='/api')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8001, reload=True, log_level="debug", access_log=True)
