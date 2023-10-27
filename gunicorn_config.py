# gunicorn_config.py

bind = '0.0.0.0:8000'  # Dirección y puerto en los que Gunicorn escuchará las solicitudes
workers = 4  # Número de trabajadores para gestionar las solicitudes (ajusta según tus recursos)
