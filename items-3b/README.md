# Items 3B

## Descripción
Items 3B es una aplicación FastAPI para gestionar productos e inventarios. Este proyecto incluye APIs para crear y obtener productos, actualizar inventarios, y crear órdenes.

## Estructura del Proyecto
```bash
items_3b/
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── settings/
├── tests/
├── poetry.lock
├── pyproject.toml
├── README.md
└── test.db
```

## Requisitos Previos
- [Docker](https://www.docker.com/products/docker-desktop) instalado en tu máquina.

## Instrucciones para Construir y Ejecutar con Docker

### 1. Clonar el Repositorio
Descarga y descomprime el archivo zip con el proyecto.

### 2. Construir la Imagen Docker
Navega al directorio del proyecto en tu terminal y ejecuta el siguiente comando para construir la imagen Docker:

```bash
docker build -t items3b .
```
### 3. Ejecutar el Contenedor Docker
Una vez que la imagen Docker haya sido construida con éxito, ejecuta el siguiente comando para iniciar el contenedor Docker:

```bash
docker run -p 8000:8000 --name 3b_contenedor items3b uvicorn items_3b.app.main:app --host 0.0.0.0 --port 8000
```
### 4. Ejecutar el proyecto desde la terminal
Usa el siguiente comando.
```bash
poetry run uvicorn items_3b.app.main:app --reload
```           
### 5. Acceder a la Aplicación con Swagger
Abre tu navegador web y visita http://localhost:8000/docs para acceder a la aplicación.

### 6. Acceder a la Aplicación con Postman
Puedes acceder a probar los endpoints con Postman a través del siguiente link. Además de que contiene la documentación.
[Postman Collection](https://www.postman.com/lilamargo/workspace/tests/request/18289752-248abb2e-7bfb-4c7d-a745-946869bc2ffd?tab=overview)

## Endpoints Principales
Crear Producto
```bash
POST /api/products
```
Obtener Productos
```bash
GET /api/products
```
Actualizar Inventario
```bash
PATCH /api/inventories/product/{product_id}
```
Obtener Inventarios
```bash
GET /api/inventories
```
Crear Orden
```bash
POST /orders
```
## Tests
Para ejecutar los tests, asegúrate de que tienes todas las dependencias instaladas y ejecuta los siguientes comandos en tu entorno de desarrollo local:
```bash
python -m unittest items_3b.tests.test_main   
```
## Contacto
Si tienes alguna pregunta, por favor contactame a:

email: liliana.martinezgo@gmail.com
linkedin: https://www.linkedin.com/in/liliana-martinez-240490/
🦄💜