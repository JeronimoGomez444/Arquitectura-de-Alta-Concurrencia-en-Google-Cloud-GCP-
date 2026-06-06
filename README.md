# Proyecto-SO: Ecosistema de Microservicios Distribuidos

Este proyecto representa el trabajo final para la asignatura de **Sistemas Operativos**. Consiste en una arquitectura híbrida distribuida que integra un entorno productivo en la nube (Google Cloud Platform) con un entorno de respaldo y visualización local (WSL2/Docker Desktop).

El ecosistema está diseñado bajo principios de contenedores, aislamiento de recursos, persistencia de datos y optimización mediante concurrencia.

---

## Requisitos Previos e Instalación

Antes de iniciar, asegúrese de tener instalado:
* **Docker Desktop** con el motor de **WSL2** activado.
* Una instancia de **Linux (Ubuntu/Kali)** en WSL2.
* Acceso SSH a una instancia de **Google Cloud Platform**.

### Configuración de Variables
Antes de ejecutar `docker compose`, debe actualizar la dirección IP de su servidor Cloud en los siguientes archivos:
1. `local-backup/backup_script.py` -> Variable `CLOUD_IP`.
2. `local/frontend/main.py` -> Variable `CLOUD_IP`.

---

## Arquitectura del Sistema

El sistema se divide en tres componentes principales distribuidos en dos nodos lógicos:

### A. Entorno Cloud (GCP - Máquina Virtual)
1. **Contenedor 1: Master Database & Proxy**
   - **Motor:** MySQL 8.0.
   - **Abstracción de Red:** Nginx configurado como Proxy Inverso TCP (módulo `stream`) para gestionar el acceso al puerto 3306.
   - **Persistencia:** Uso de *Docker Volumes* para garantizar que los datos sobrevivan a reinicios del contenedor.
   - **Automatización:** Despliegue mediante `init.sql` para auto-configuración de tablas y usuarios.

### B. Entorno Local (WSL2 / Docker Desktop)
2. **Contenedor 2: Backup Worker**
   - **Tecnología:** Python 3.11-slim.
   - **Función:** Agente de sincronización que realiza una réplica incremental de la base de datos de la nube hacia un volumen local cada 10 minutos.
   - **Sistemas Operativos:** Implementación de tareas programadas y gestión de procesos en segundo plano.

3. **Contenedor 3: Frontend & API Gateway**
   - **Tecnología:** FastAPI (Python).
   - **Restricción de Recursos:** Limitación estricta de hardware a 2 vCPUs y 2 GB de RAM.
   - **Funcionalidad:** Interfaz web para consultar datos en tiempo real de la nube y procesamiento de datos externos mediante concurrencia (`AsyncIO`).

---

## Despliegue de la Infraestructura Cloud

Para replicar el entorno de la nube de forma automática, siga estos pasos:

### 1. Preparación de Archivos
Asegúrese de contar con los archivos `docker-compose.yml`, `nginx.conf` e `init.sql` en el mismo directorio dentro de la VM.

### 2. Ejecución del Entorno
Ejecute el comando de orquestación. Este comando creará la red virtual, los volúmenes de persistencia y ejecutará los scripts de inicialización:

```bash
sudo docker-compose up -d
```

### 3. Verificación Automática
Para confirmar que el Sistema Operativo ha desplegado correctamente los servicios y que la base de datos ha procesado el script de inicio, ejecute:

```bash
sudo docker exec -it db_master mysql -u operador_cloud -p -e "USE sistema_monitoreo; SELECT * FROM sensores;"
```

---

## Despliegue del Entorno Local (WSL2)

Para replicar el entorno local de forma automática, siga estos pasos:

### 1. Preparación de Archivos
Asegúrese de contar con los archivos `backup_script.py`, `docker-compose.yml` e `Dockerfile` en la carpeta local-backup.

### 2. Ejecución
Navegue a la carpeta local-backup y ejecute:

```bash
docker compose up -d --build
```

### 3. Monitoreo de Sincronización

Para auditar el estado de las réplicas en tiempo real:

```bash
docker logs -f backup_worker
```

## Justificación del modelo elegido: Concurrencia 

Elegimos Concurrencia con AsyncIO porque las tareas del Frontend (consultar una API externa y consultar la base de datos en la nube) son tareas I/O-Bound (limitadas por la entrada/salida de red). No necesitamos paralelismo (Multiprocessing) porque el procesador no está haciendo cálculos pesados, sino esperando respuestas de red, AsyncIO permite que el Sistema Operativo maneje cientos de estas esperas en un solo hilo sin bloquear la interfaz.

## Evidencias del funcionamiento del proyecto

<p align="center">
  <img src="img/Evidencia1.png" alt="Despliegue del contenedor en la web" width="700"/>
</p>

<p align="center">
  <img src="img/Evidencia2.png" alt="Resultado del despliegue en la web" width="700"/>
</p>

<p align="center">
  <img src="img/Evidencia3.png" alt="Datos iniciales cargados en la base de datos" width="700"/>
</p>

<p align="center">
  <img src="img/Evidencia5.png" alt=" Despliegue del contenedor en local" width="700"/>
</p>

<p align="center">
  <img src="img/Evidencia5.png" alt="Resultado del backup realizado" width="700"/>
</p>

<p align="center">
  <img src="img/Evidencia6.png" alt=" Fronted en ejecución." width="700"/>
</p>

<p align="center">
  <img src="img/Evidencia7.png" alt="Consulta al API externa y a la base de datos" width="700"/>
</p>

