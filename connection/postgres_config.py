import sqlalchemy as sa
import util as log


def dispose_engine(engine):
    engine.dispose()


def check_schema_exist(db_properties):
    engine = create_engine_config(db_properties)
    if engine is not None:
        # Read
        sql_query = "SELECT COUNT(schema_name) FROM information_schema.schemata WHERE schema_name = '{}'".format(db_properties.schema)
        result = engine.execute(sql_query).scalar()
        if result == 0:
            # schema does not exist
            # create schema
            sql_query = "CREATE SCHEMA IF NOT EXISTS {}".format(db_properties.schema)
            engine.execute(sql_query)
            log.message.warning_no_schema(db_properties)


def create_engine_config(db_properties):
    engine = None
    if db_properties.schema is not None:
        # engine+driver
        engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            db_properties.user, db_properties.password, db_properties.hostname,
            db_properties.port, db_properties.db),
                                  connect_args={'options': '-csearch_path={}'.format(db_properties.schema)})
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
