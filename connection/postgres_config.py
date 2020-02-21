import sqlalchemy as sa


def dispose_engine(engine):
    engine.dispose()


def create_engine(schema):
    # engine+driver
    engine = sa.create_engine("postgresql+psycopg2://root:VMware1!@localhost:54320/postgres",
                              connect_args={'options': '-csearch_path={}'.format(schema)})
    return engine


def create_engine_config(schema, db_properties):
    # engine+driver
    engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        db_properties.user, db_properties.password, db_properties.hostname,
        db_properties.port, db_properties.db),
                              connect_args={'options': '-csearch_path={}'.format(schema)})
    return engine
