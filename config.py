class Config:
    # Flask settings
    SECRET_KEY = 'your_secret_key'
    DEBUG = True

    # Elasticsearch settings
    ELASTICSEARCH_HOST = 'localhost'
    ELASTICSEARCH_PORT = 9200
    ELASTICSEARCH_USER = 'elastic'
    ELASTICSEARCH_PASSWORD = 'rFhi70ABm*VHOI843IfP'
    ELASTICSEARCH_SCHEME = 'https'
    ELASTICSEARCH_VERIFY_CERTS = False

    @staticmethod
    def get_elasticsearch_url():
        return f"{Config.ELASTICSEARCH_SCHEME}://{Config.ELASTICSEARCH_HOST}:{Config.ELASTICSEARCH_PORT}"
