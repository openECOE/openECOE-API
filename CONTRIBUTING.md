# Configuración del entorno

## Requisitos
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Instalación

Para usarlo, primero se debe abrir el proyecto y abrir el contendor utilizando el comando de Visual Studio Code `Dev Containers: Reopen in Container`

> Si es la primera vez que se abre tardará más ya que se está creando el contenedor

Una vez creado, abrir una terminal y ejecutar el siguiente comando para crear el entorno virtual de python

```bash
poetry shell
```

Una vez creado el entorno virtual, instalar las dependencias

```bash
poetry install
```

Seleccionar el interprete de Python de Poetry utilizando el commando de Visual Studio Code `Python: Select Interpreter`, aparecerá una lista de opciones, seleccionar la siguiente:

```
Python 3.9.19 ('.venv': Poetry) ./venv/bin/python
```

> En caso de que no se haya seleccionado correctamente, reiniciar el editor y volver a abrir el contenedor

## Montar Bases de Datos

El proyecto requiere dos bases de datos, una de MySql y Redis. Para utilizarlas se va a lanzar estas dos en sus respectivos contenedores.

Para esto, se hace uso de la herramienta Docker Compose con el archivo [docker-compose.yml](./docker-compose.yml).

Desde fuera del contenedor abrir una terminal y ejecutar el comando desde la ruta base del proyecto

```bash
docker compose up
```

> Este comando creará tres contenedores, el contendor `api-1` no se usará y se podrá parar

## Lanzar API en modo desarrollo

Desde la pestaña de Visual Studio Code `Run and Debug (CTRL + Shift + D)` se lanzarán los tres componentes de la API (API, Chrono, Worker para Redis):
- Launch openECOE API
- Launch openECOE Chrono (Gunicorn)
- Launch worker

> Por defecto se lanzarán en los puertos 5000 (API) y 5001 (Chrono) 

Desde esta parte también se harán los lanzamientas para las migraciones de la base de datos.

## Construir imágenes de la API

Hay que tener en cuenta que por defecto el comando `docker compose up`, si no tienes descargada la imágen de la API la descargará de [Docker Hub](https://hub.docker.com/r/openecoe/api/tags).

En el caso de haber realizado cambios y querer tener estos actualizados en el contenedor habrá que construir la imágen de la API utilizando el script [build.sh](.docker/build.sh) o bien utilizando el comando manualmente:

```docker
docker build -t "openecoe/api:<NOMBRE_TAG>" .
```

> Es importante tener en cuenta el tag, ya que en [docker-compose.yml](./docker-compose.yml) se especifica que se va a usar el tag `latest`
