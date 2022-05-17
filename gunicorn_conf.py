from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/ar/python/nlpguide_rest_api/gunicorn.sock'

# Worker Options 
workers = cpu_count() + 1
workers_class = 'uvicorn.workers.UvicornWorker'


# Logging Options 
loglevel = 'debug'
accesslog = '/home/ar/python/nlpguide_rest_api/access_log'
errorlog = '/home/ar/python/nlpguide_rest_api/error_log'
