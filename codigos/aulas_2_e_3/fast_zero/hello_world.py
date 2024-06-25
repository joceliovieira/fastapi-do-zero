from fastapi import FastAPI
from http import HTTPStatus
from fast_zero.schemas import Message
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_model=Message)
def read_root():
    return {"message": "Olá, planeta."}


@app.get(
    "/hw_html",
    response_class=HTMLResponse,
    status_code=HTTPStatus.OK,
    name="Hello World HTML",
)
def hello_world_html():
    return """
  <html>
    <head>
      <title> Nosso olá mundo!</title>
    </head>
    <body>
      <h1> Olá Mundo </h1>
    </body>
  </html>"""
