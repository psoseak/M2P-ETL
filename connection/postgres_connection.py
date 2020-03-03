import sqlalchemy as sa
import util as log


class PostgresConnection:
    def __init__(self, db_properties):
        self.db_properties = db_properties

    def get_db_properties(self):
        return self.db_properties

    def dispose_engine(self, engine):
        engine.dispose()

    def create_engine_config(self):
        engine = None
        if self.db_properties.schema is not None:
            # engine+driver
            engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                self.db_properties.user, self.db_properties.password, self.db_properties.hostname,
                self.db_properties.port, self.db_properties.db),
                connect_args={'options': '-csearch_path={}'.format(self.db_properties.schema)})
        else:
            engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                self.db_properties.user, self.db_properties.password, self.db_properties.hostname,
                self.db_properties.port, self.db_properties.db))

        try:
            engine.connect()
            return engine
        except sa.exc.SQLAlchemyError:
            log.message.error_conn(self)
            return None
