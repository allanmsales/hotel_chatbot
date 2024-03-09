from fastapi import FastAPI
from server.gunicorn_server import GunicornServer
from controller import chatbot

app = FastAPI(
    title="Hotel Chatbot",
    version="1.0",
    description="Chatbot to book rooms in a Hotel."
)

app.include_router(chatbot.router)

if __name__ == '__main__':
    options = {
        'bind': '{}:{}'.format('0.0.0.0', '8080'),
        'workers': 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'timeout': 600
    }

    GunicornServer(app, options).run()
