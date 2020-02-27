import sqlalchemy as sa
import util as log


def dispose_engine(engine):
    engine.dispose()


def check_schema_exist(schema, db_properties):
    # Set none to create an engine not pointing to any schema
    engine = create_engine_config(None, db_properties)
    if engine is not None:
        # Read
        sql_query = "SELECT COUNT(schema_name) FROM information_schema.schemata WHERE schema_name = '{}'".format(schema)
        result = engine.execute(sql_query).scalar()
        print(result)
        if result == 0:
            # schema does not exist
            # create schema
            sql_query = "CREATE SCHEMA IF NOT EXISTS {}".format(schema)
            engine.execute(sql_query)
            log.message.warning_no_schema(db_properties, schema)


def create_engine_config(schema, db_properties):
    engine = None
    if schema is not None:
        # engine+driver
        engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            db_properties.user, db_properties.password, db_properties.hostname,
            db_properties.port, db_properties.db),
                                  connect_args={'options': '-csearch_path={}'.format(schema)})
    else:
        engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            db_properties.user, db_properties.password, db_properties.hostname,
            db_properties.port, db_properties.db))

    try:
        engine.connect()
        return engine
    except sa.exc.SQLAlchemyError:
        log.message.error_conn(db_properties)
        return None
