# openECOE-API
## License
Copyright (c) 2019 Universidad Miguel Hernandez de Elche

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

## Variables de entorno
### Variables de entorno para la conexión con la base de datos
* OPENECOE_DB_HOST: Dirección del servidor de la base de datos
* OPENECOE_DB_PORT: Puerto del servidor de la base de datos
* OPENECOE_DB_USER: Usuario de la base de datos
* OPENECOE_DB_PASSWORD: Contraseña del usuario de la base de datos
* OPENECOE_DB_NAME: Nombre de la base de datos

### Variables de entorno para la conexión con el servidor de Redis
* OPENECOE_REDIS_HOST: Dirección del servidor de Redis
* OPENECOE_REDIS_PORT: Puerto del servidor de Redis
* OPENECOE_REDIS_PASSWORD: Contraseña del servidor de Redis
* OPENECOE_REDIS_DB: Base de datos de servidor de Redis

### Variables de entorno adicionales
* BCRYPT_LOG_ROUNDS: Número de rondas de encriptación de la contraseña
* DEBUG: Si se activa, se mostrarán los errores en la consola
* TESTING: Si se activa, se mostrarán los errores en la consola
* LOG_TO_STDOUT:  Si se activa, se mostrarán los errores en la consola STDOUT
* SQLALCHEMY_TRACK_MODIFICATIONS: Si se activa, se realiza seguimiento de las modificaciones de SQLAlchemy
* API_AUTH: Si se activa, se activa la autenticación de la API
* SQLALCHEMY_ECHO:  Si se activa, se mostrarán información de todas las consultas de SQLAlchemy en la consola


