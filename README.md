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

// ENGLISH //

# OS Project: Distributed Microservices Ecosystem

This project represents the final assignment for the **Operating Systems** course. It consists of a distributed hybrid architecture that integrates a production environment in the cloud (Google Cloud Platform) with a local backup and visualization environment (WSL2/Docker Desktop).

The ecosystem is designed based on the principles of containers, resource isolation, data persistence, and optimization through concurrency.

---

## Prerequisites and Installation

Before starting, ensure you have the following installed:
* **Docker Desktop** with the **WSL2** engine enabled.

* A **Linux (Ubuntu/Kali)** instance running WSL2.

* SSH access to a **Google Cloud Platform** instance.

### Variable Configuration
Before running `docker compose`, you must update your Cloud server's IP address in the following files:
1. `local-backup/backup_script.py` -> Variable `CLOUD_IP`.

2. `local/frontend/main.py` -> Variable `CLOUD_IP`.

---

## System Architecture

The system is divided into three main components distributed across two logical nodes:

### A. Cloud Environment (GCP - Virtual Machine)
1. **Container 1: Master Database & Proxy**

- **Engine:** MySQL 8.0.

- **Network Abstraction:** Nginx configured as a TCP Reverse Proxy (`stream` module) to manage access to port 3306.

- **Persistence:** Use of *Docker Volumes* to ensure data persistence across container restarts.

- **Automation:** Deployment using `init.sql` for automatic configuration of tables and users.

### B. Local Environment (WSL2 / Docker Desktop)
2. **Container 2: Backup Worker**

- **Technology:** Python 3.11-slim.

- **Function:** Synchronization agent that performs incremental replication of the cloud database to a local volume every 10 minutes.

- **Operating Systems:** Implementation of scheduled tasks and background process management.

3. **Container 3: Frontend & API Gateway**

- **Technology:** FastAPI (Python).

- **Resource Restrictions:** Strict hardware limitation to 2 vCPUs and 2 GB of RAM.

- **Functionality:** Web interface for querying real-time data from the cloud and processing external data concurrently (`AsyncIO`).

---

## Cloud Infrastructure Deployment

To automatically replicate the cloud environment, follow these steps:

### 1. File Preparation
Ensure that the `docker-compose.yml`, `nginx.conf`, and `init.sql` files are in the same directory within the VM.

### 2. Environment Setup
Run the orchestration command. This command will create the virtual network, persistence volumes, and run the initialization scripts:

```bash
sudo docker-compose up -d
```

### 3. Automatic Verification
To confirm that the operating system has correctly deployed the services and that the database has processed the startup script, run:

```bash
sudo docker exec -it db_master mysql -u operator_cloud -p -e "USE monitoring_system; SELECT * FROM sensors;"
```

---

## Deploying the Local Environment (WSL2)

To automatically replicate the local environment, follow these steps:

### 1. File Preparation
Ensure you have the `backup_script.py`, `docker-compose.yml`, and `Dockerfile` files in the local-backup folder.

### 2. Execution
Navigate to the local-backup folder and run:

```bash
docker compose up -d --build
```

### 3. Synchronization Monitoring

To audit the status of the replicas in real time:

```bash
docker logs -f backup_worker
```

## Justification of the chosen model: Concurrency

We chose Concurrency with AsyncIO because the Frontend tasks (querying an external API and querying the cloud database) are I/O-bound tasks (limited by network input/output). We don't need parallelism (multiprocessing) because the processor isn't performing heavy calculations, but rather waiting for network responses. AsyncIO allows the Operating System to handle hundreds of these waits in a single thread without blocking the interface.

## Evidence of the project's operation

<p align="center"> 
<img src="img/Evidencia1.png" alt="Deployment of the container on the web" width="700"/>
</p>

<p align="center"> 
<img src="img/Evidencia2.png" alt="Result of the deployment on the web" width="700"/>
</p>

<p align="center"> 
<img src="img/Evidencia3.png" alt="Initial data loaded into the database" width="700"/>
</p>

<p align="center"> 
<img src="img/Evidencia5.png" alt="Deployment of the container locally" width="700"/>
</p>

<p align="center"> 
<img src="img/Evidence5.png" alt="Result of the backup performed" width="700"/>
</p>

<p align="center"> 
<img src="img/Evidencia6.png" alt=" Fronted running." width="700"/>
</p>

<p align="center"> 
<img src="img/Evidencia7.png" alt="Query to the external API and the database" width="700"/>
</p>
