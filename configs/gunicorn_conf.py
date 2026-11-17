"""Configuración de gunicorn para el API y el cronómetro.

Variables de entorno:
  BIND               dirección (host:puerto o unix:/ruta). Si no está, HOST:PORT (0.0.0.0:5000).
  WEB_CONCURRENCY    número de procesos. Si no está, WORKERS_PER_CORE (2) x núcleos.
  GUNICORN_THREADS   hilos por proceso (4).
  LOG_LEVEL          nivel de log (info).
"""
import multiprocessing
import os

workers_per_core = float(os.getenv("WORKERS_PER_CORE", "2"))
web_concurrency = os.getenv("WEB_CONCURRENCY")
if web_concurrency:
    workers = int(web_concurrency)
    assert workers > 0
else:
    workers = max(int(workers_per_core * multiprocessing.cpu_count()), 1)

bind = os.getenv("BIND") or "{}:{}".format(os.getenv("HOST", "0.0.0.0"), os.getenv("PORT", "5000"))

# meinheld ya no se mantiene: workers síncronos con hilos.
worker_class = "gthread"
threads = int(os.getenv("GUNICORN_THREADS", "4"))
# Cada proceso acepta solo las conexiones que puede atender: el resto espera en la cola del socket, compartida por
# todos los procesos. Con el valor por defecto (1000), un proceso ocupado acapara peticiones y sube la latencia.
worker_connections = int(os.getenv("GUNICORN_WORKER_CONNECTIONS", str(threads)))

loglevel = os.getenv("LOG_LEVEL", "info")
keepalive = 120
timeout = 120
graceful_timeout = 20
errorlog = "-"
accesslog = os.getenv("ACCESS_LOG") or None
capture_output = True

# gunicorn 26 abre un socket de control (gunicornc) en el HOME; no se usa y el HOME no existe en la imagen.
control_socket_disable = True
