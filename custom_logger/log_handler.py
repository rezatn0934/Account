import logging
import time
from config.config import settings
from elasticsearch import Elasticsearch


class ElasticHandler(logging.Handler):
    """
    Custom logging handler for sending log records to Elasticsearch.

    This handler sends log records to Elasticsearch with a specified index name and timestamp.

    Attributes:
        es (Elasticsearch): Elasticsearch client instance for log storage.
        sender (LogSender): Log sender instance for writing log records.

    Methods:
        emit(self, record):
            Emit a log record to Elasticsearch.

    Example Usage:
        To use this custom logging handler, add it to your Django logging configuration.
        It sends log records to Elasticsearch with the specified index name and timestamp.

    Note:
        - If there is an exception during log emission, it is handled, and the error is logged.
        - The Elasticsearch host and port are configured from Django settings.

    See the Elasticsearch Python client documentation for more details on usage.
    """

    def __init__(self):
        super().__init__()
        self.es = Elasticsearch(f'http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}')

    def emit(self, record):
        try:
            index_name = f'log_{time.strftime("%Y_%m_%d")}'
            self.es.index(index=index_name, document=record.msg)

        except Exception:
            self.handleError(record)
