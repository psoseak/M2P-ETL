import sys
import os
import sqlalchemy as sa
import util as log
import psycopg2

class PostgresConnection:
    def __init__(self, db_properties):
        self.db_properties = db_properties

    def get_db_properties(self):
        return self.db_properties

    def dispose_engine(self, engine):
        engine.dispose()

    def check_connection(self):
        try:
            conn = psycopg2.connect(database=self.db_properties.db, user=self.db_properties.user,
                                    password=self.db_properties.password, host=self.db_properties.hostname,
                                    port=self.db_properties.port, connect_timeout=5)
            conn.close()
            return True
        except Exception as caught_exception:
            exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.message.log_stack_trace(caught_exception, fname, exc_tb.tb_lineno)
            return False

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
        except sa.exc.SQLAlchemyError as caught_exception:
            log.message.error_conn(self.db_properties, 'destination')
            exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.message.log_stack_trace(caught_exception, fname, exc_tb.tb_lineno)
            return None
