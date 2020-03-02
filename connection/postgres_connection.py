import sqlalchemy as sa


def dispose_engine(engine):
    engine.dispose()


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
