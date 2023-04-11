from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

load_dotenv()  # cargamos las variables desde el archivo .env

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")  # obtenemos la variable de entorno de postgres url
connection = psycopg2.connect(database=os.environ.get("DATABASE_NAME") ,
                              host=os.environ.get("DATABASE_HOST"),
                              port=os.environ.get("DATABASE_PORT"),
                              user=os.environ.get("DATABASE_USER"),
                              password=os.environ.get("DATABASE_PASS"))

@app.get("/api/hello")
def hello_world():
    return "hello world", 200

@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["nombre"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Habitacion {name} creada."}, 201