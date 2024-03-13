from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from server.gunicorn_server import GunicornServer
from controller import chatbot

app = FastAPI(
    title="Hotel Chatbot",
    version="1.0",
    description="Chatbot to book rooms in a Hotel."
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(chatbot.router)

if __name__ == '__main__':
    options = {
        'bind': '{}:{}'.format('0.0.0.0', '8080'),
        'workers': 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'timeout': 600
    }

    GunicornServer(app, options).run()
