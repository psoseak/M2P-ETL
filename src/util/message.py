import logging


def initialize():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s  - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def log_stack_trace(encountered_exception, file_name, line_number):
    msg = 'Logging Stack Trace: {encountered_exception}. ' \
          'Error in {file_name} at Line {line_number}' \
        .format(encountered_exception=encountered_exception,
                file_name=file_name,
                line_number=line_number
                )

    initialize()
    logging.debug(msg)


def error_conn(db_properties, db_type):
    msg = 'Failed to connect to {type}: {hostname}:{port}, {db}'.format(
        type=db_type,
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    initialize()
    logging.warning(msg)


def warn_db_not_found(db_properties):
    msg = 'Database not found: {hostname}:{port}, {db}'.format(
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    initialize()
    logging.warning(msg)


def info_db_created(db_properties):
    msg = 'Successfully created database: {hostname}:{port}, {db}'.format(
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    initialize()
    logging.info(msg)


def warning_no_schema(db_properties):
    msg = 'Warning no schema [{schema}] at {hostname}:{port}, {db}'.format(
        schema=db_properties.schema,
        hostname=db_properties.hostname,
        port=db_properties.port,
        db=db_properties.db
    )
    initialize()
    logging.warning(msg)

    msg = 'Creating new schema [{schema}]'.format(
        schema=db_properties.schema
    )
    logging.info(msg)


def info_extraction_database_empty(db_name):
    msg = 'Extracting empty database: {db}'.format(
        db=db_name
    )
    initialize()
    logging.warning(msg)


def info_extraction_collection_empty(collection_name):
    msg = 'Extracting empty collection: {collection}'.format(
        collection=collection_name
    )
    initialize()
    logging.info(msg)


def info_start():
    initialize()
    logging.info('Preparing to migrate.....')


def info_database_connected():
    initialize()

    logging.info('Connected to all database successfully.')
    logging.info('Starting to migrate......')


def info_migrated_completed():
    initialize()

    logging.info('Migrated database successfully. :)')
