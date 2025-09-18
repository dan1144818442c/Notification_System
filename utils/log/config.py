import os

ELASTICSEARCH_WWW = os.getenv('ELASTICSEARCH_WWW', 'http')
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', 9200))
ELASTICSEARCH_URI = os.getenv("ELASTICSEARCH_URI",f"{ELASTICSEARCH_WWW}:"
                                                  f"//{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}/")