# openECOE-API
## How to contribute

If you want to contribute, you can [read the contributing guide](CONTRIBUTING.md).

## License
Copyright (c) 2019 Universidad Miguel Hernandez de Elche

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

## Requisitos y ejecución
* Python 3.15 (funciona desde la 3.12) y [Poetry](https://python-poetry.org/) 2: `poetry install --with dev`.
* MySQL 8 y Redis (o Valkey).
* Informes PDF con [WeasyPrint](https://weasyprint.org/): necesita Pango (en Debian/Ubuntu, `libpango-1.0-0`,
  `libpangoft2-1.0-0` y `libharfbuzz-subset0`).
* `flask_potion/` es una copia mantenida de Flask-Potion 0.16 (abandonada); ver [flask_potion/README.md](flask_potion/README.md).

La imagen Docker (`openecoe/api`, Python 3.15 sobre Debian 13, sin root) tiene tres procesos, cada uno con su comando:

| Proceso | Comando |
|---|---|
| API (por defecto, 0.0.0.0:5000) | `gunicorn -c configs/gunicorn_conf.py openecoe-api:app` |
| Cronómetro (un solo proceso) | `gunicorn -c configs/gunicorn_conf.py -w 1 --threads 100 openecoe-chrono:app` |
| Trabajos en segundo plano | `flask rq worker` |

Antes del API: `.docker/deploy/alembic.sh` (migraciones) y `.docker/deploy/first-run.sh` (organización y usuario
inicial). La imagen `openecoe/one-for-all` (repositorio [docker](https://github.com/openECOE/docker)) los lanza todos
juntos con nginx delante.

## Variables de entorno
### Variables de entorno para la conexión con la base de datos
* OPENECOE_DB_HOST: Dirección del servidor de la base de datos
* OPENECOE_DB_PORT: Puerto del servidor de la base de datos
* OPENECOE_DB_USER: Usuario de la base de datos
* OPENECOE_DB_PASSWORD: Contraseña del usuario de la base de datos
* OPENECOE_DB_NAME: Nombre de la base de datos
* OPENECOE_DB_PARAMS: Parámetros de la conexión, en la URL (por ejemplo, `?ssl_ca=/app/api/certs/global-bundle.pem` para RDS con TLS)

### Variables de entorno para la conexión con el servidor de Redis
* OPENECOE_REDIS_HOST: Dirección del servidor de Redis
* OPENECOE_REDIS_PORT: Puerto del servidor de Redis
* OPENECOE_REDIS_USER: Usuario del servidor de Redis
* OPENECOE_REDIS_PASSWORD: Contraseña del servidor de Redis
* OPENECOE_REDIS_DB: Base de datos de servidor de Redis
* OPENECOE_REDIS_TLS: Si se activa, se activa el protocolo TLS (True o False)

### Variables de entorno adicionales
* OPENECOE_SECRET: Clave para firmar las cookies de sesión. Obligatoria en producción (el valor por defecto es público)
* OPENECOE_CHRONO_URL: URL interna del cronómetro (por defecto, `http://localhost:5001`)
* OPENECOE_ARCHIVE_DIR: Directorio de los ficheros que generan los trabajos (exportaciones, informes). Por defecto, `archive` junto al código; en la imagen, `/tmp/openecoe-archive`
* OPENECOE_CHRONO_DIR: Directorio donde el cronómetro guarda su estado (configuración de cada ECOE y estado de rondas y cronómetros) para recuperarlo al arrancar. Por defecto, `/tmp`; para no perderlo al reiniciar, tiene que ser persistente (por ejemplo, un EFS)
* WEB_CONCURRENCY, GUNICORN_THREADS: Procesos e hilos por proceso de gunicorn (por defecto, 2 procesos por núcleo y 4 hilos)
* BCRYPT_LOG_ROUNDS: Número de rondas de encriptación de la contraseña
* DEBUG: Si se activa, se mostrarán los errores en la consola
* TESTING: Si se activa, se mostrarán los errores en la consola
* LOG_TO_STDOUT:  Si se activa, se mostrarán los errores en la consola STDOUT
* SQLALCHEMY_TRACK_MODIFICATIONS: Si se activa, se realiza seguimiento de las modificaciones de SQLAlchemy
* API_AUTH: Si se activa, se activa la autenticación de la API
* SQLALCHEMY_ECHO:  Si se activa, se mostrarán información de todas las consultas de SQLAlchemy en la consola


