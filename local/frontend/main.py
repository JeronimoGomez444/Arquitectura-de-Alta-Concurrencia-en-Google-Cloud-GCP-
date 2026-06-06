from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import mysql.connector
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configuración de la Nube (GCP)
CLOUD_IP = "34.173.115.30"
DB_CONFIG = {
    "host": CLOUD_IP,
    "user": "operador_cloud",
    "password": "proyecto123so",
    "database": "sistema_monitoreo"
}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}
    )

# BOTÓN 1: API Externa con AsyncIO (I/O-Bound)
@app.get("/api-externa")
async def get_weather():
    # Usamos httpx (asíncrono) para no bloquear el bucle de eventos del SO
    async with httpx.AsyncClient() as client:
        # Consultamos el clima de Manizales (ejemplo)
        response = await client.get("https://api.open-meteo.com/v1/forecast?latitude=5.06&longitude=-75.51&current_weather=true")
        return response.json()

# BOTÓN 2: Consulta a la Nube (Container 1)
@app.get("/datos-nube")
async def get_cloud_data():
    try:
        # Esta es una tarea I/O-Bound (espera de red)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sensores ORDER BY timestamp DESC LIMIT 5")
        data = cursor.fetchall()
        conn.close()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}