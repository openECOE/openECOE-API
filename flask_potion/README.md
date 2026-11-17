# flask_potion (copia mantenida en openECOE-API)

Copia de [Flask-Potion 0.16.0](https://github.com/biosustain/potion) (licencia MIT, en `LICENSE`), en la que se
basa toda la API REST de openECOE (`app/api/`). El proyecto original está archivado desde 2019 y no funciona con
Flask 3, Werkzeug 3, Flask-SQLAlchemy 3 ni SQLAlchemy 2, así que se mantiene aquí con los cambios mínimos.
El código de la aplicación la sigue importando igual (`from flask_potion import ...`).

## Cambios respecto a la 0.16.0

- Fuera `contrib/mongoengine` y `contrib/peewee` (no se usan).
- `__init__.py`: `werkzeug.wrappers.BaseResponse` ya no existe (se usa `Response`); `functools.wraps` en vez de
  `six.wraps`.
- `utils.py` (`route_from`): sin `_app_ctx_stack` ni `_request_ctx_stack` (eliminados en Flask 3); el adaptador de
  URL se pide con `current_app.create_url_adapter()`. `urllib.parse.urlsplit` en vez de `werkzeug.urls.url_parse`.
- `reference.py`: fuera el import de `_app_ctx_stack`.
- `fields.py` y `natural_keys.py`: `"\/"` pasa a `"\\/"` (misma cadena; Python 3.12+ avisa de la secuencia inválida).
- `contrib/alchemy/manager.py`:
  - `Pagination` se importa de `flask_sqlalchemy.pagination`; la sesión, de `current_app.extensions["sqlalchemy"]`
    (`get_state` ya no existe).
  - Para elegir entre `has()` y `any()` se mira `relationship.property.uselist` en vez de la clase interna
    `ScalarObjectAttributeImpl`.
  - Sin `reset_joinpoint()` (eliminado en SQLAlchemy 2).
  - `create()`: si a un objeto nuevo se le asigna una relación con otro que ya está en la sesión, se añade a la
    sesión antes de las señales `before_create`. Es lo que hacía SQLAlchemy 1.x por su cuenta (`cascade_backrefs`,
    eliminado en la 2.0) y de lo que dependen señales de openECOE como el recálculo del orden de las preguntas.

Dependencias que necesita (en `pyproject.toml`): `jsonschema`, `rfc3339-validator` (para que el formato `date-time`
se siga validando), `aniso8601` y `six`.
