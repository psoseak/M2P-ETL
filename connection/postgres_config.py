import sqlalchemy as sa


def dispose_engine(engine):
    engine.dispose()


def create_engine(schema):
    # engine+driver
    engine = sa.create_engine("postgresql+psycopg2://root:VMware1!@localhost:54320/postgres",
                              connect_args={'options': '-csearch_path={}'.format(schema)})
    return engine