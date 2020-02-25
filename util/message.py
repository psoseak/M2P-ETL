import logging
from logging.handlers import RotatingFileHandler


def initialize():
    log_file = 'app.log'
    log_formatter = logging.Formatter('%(asctime)s - %(message)s')
    log_handler = RotatingFileHandler(log_file, mode='w', maxBytes=5 * 1024 * 1024,
                                      backupCount=2, encoding=None, delay=0)
    log_handler.setFormatter(log_formatter)

    app_log = logging.getLogger('root')
    app_log.addHandler(log_handler)

    return app_log


def error_conn(db_properties):
    msg = "Failed to connect to: {hostname}:{port}, {db}".format(
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    app_log = initialize()
    app_log.critical(msg)


def warning_no_schema(db_properties, schema):
    msg = "Warning no schema [{schema}] at {hostname}:{port}, {db}".format(
        schema=schema,
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    app_log = initialize()
    app_log.warning(msg)
