import os
import signal

import fastapi
import uvicorn

from .utils import write_devteamtask_json

app = fastapi.FastAPI()


def callback(request: fastapi.Request):
    access_token = request.query_params.get("access_token")
    refresh_token = request.query_params.get("refresh_token")

    if access_token is not None and refresh_token is not None:
        write_devteamtask_json("access_token", access_token)
        write_devteamtask_json("refresh_token", refresh_token)

        # Shutting down server
        os.kill(os.getpid(), signal.SIGTERM)

        print("Successfully authenticated")

    return fastapi.Response(status_code=200, content="Server shutting down...")


app.add_api_route("/callback", callback, methods=["GET"])


def start_server():
    from socket import AF_INET, SOCK_STREAM, socket

    def is_port_in_use(port):
        with socket(AF_INET, SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0

    port = 8008

    while is_port_in_use(port):
        port += 1

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="critical")
