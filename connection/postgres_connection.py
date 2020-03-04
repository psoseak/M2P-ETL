import sys
import os
import sqlalchemy as sa
import psycopg2
import util as log


def dispose_engine(engine):
    engine.dispose()


class PostgresConnection:
    def __init__(self, db_properties):
        self.db_properties = db_properties

    def get_db_properties(self):
        return self.db_properties

    def check_connection(self):
        try:
            conn = psycopg2.connect(database=self.db_properties.db,
                                    user=self.db_properties.user,
                                    password=self.db_properties.password,
                                    host=self.db_properties.hostname,
                                    port=self.db_properties.port,
                                    connect_timeout=5)
            conn.close()
            return True
        except sa.exc.SQLAlchemyError as err:
            exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.message.log_stack_trace(err, file_name, exc_tb.tb_lineno)

    def create_engine_config(self):
        if self.db_properties.schema is not None:
            # engine+driver
            engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                self.db_properties.user,
                self.db_properties.password,
                self.db_properties.hostname,
                self.db_properties.port,
                self.db_properties.db), \
                connect_args={'options': '-csearch_path={}'.format(self.db_properties.schema)})
        else:
            engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                self.db_properties.user, self.db_properties.password, self.db_properties.hostname,
                self.db_properties.port, self.db_properties.db))

        try:
            engine.connect()
            return engine
        except sa.exc.SQLAlchemyError as err:
            log.message.error_conn(self.db_properties, 'destination')
            exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.message.log_stack_trace(err, file_name, exc_tb.tb_lineno)
