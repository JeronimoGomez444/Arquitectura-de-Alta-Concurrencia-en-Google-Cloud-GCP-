import mysql.connector
import json
import time
import os

# Configuración
CLOUD_IP = "34.173.115.30"
DB_CONFIG = {
    "host": CLOUD_IP,
    "user": "operador_cloud",
    "password": "proyecto123so",
    "database": "sistema_monitoreo"
}

def fetch_and_backup():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Consultamos los datos de la nube
        cursor.execute("SELECT * FROM sensores")
        data = cursor.fetchall()
        
        # Guardamos en un JSON dentro del volumen local
        file_path = "/data/backup_sensores.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4, default=str)
            
        print(f"[{time.ctime()}] Backup exitoso. {len(data)} registros guardados.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[{time.ctime()}] Error en el backup: {e}")

if __name__ == "__main__":
    print("Iniciando Worker de Backup...")
    while True:
        fetch_and_backup()
        # Esperar 10 minutos (600 segundos) según el requerimiento
        time.sleep(600)