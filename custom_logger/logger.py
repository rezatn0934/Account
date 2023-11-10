import logging.config
import structlog

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%S.%fZ")
pre_chain = [
    structlog.stdlib.add_log_level,
    structlog.processors.StackInfoRenderer(),
]


def setup_logger():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": structlog.processors.JSONRenderer(),
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "elastic": {
                    "level": "INFO",
                    "class": "custom_logger.log_handler.ElasticHandler",
                    'formatter': 'plain'
                },
            },
            "loggers": {
                "elastic_logger": {
                    "handlers": ["elastic"],
                    "level": "INFO",
                    "propagate": True,
                },
            },
        }
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )
