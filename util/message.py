import logging


def error_conn(db_properties):
    msg = "Failed to connect to: {hostname}:{port}, {db}".format(
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    logging.critical(msg)


def warning_no_schema(db_properties, schema):
    msg = "Warning no schema [{schema}] at {hostname}:{port}, {db}".format(
        schema=schema,
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    logging.warning(msg)
