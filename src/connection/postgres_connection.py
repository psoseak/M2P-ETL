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
            conn = psycopg2.connect(user=self.db_properties.user,
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

    def check_database_exist(self):
        try:
            # tries to connect to the database
            conn = psycopg2.connect(user=self.db_properties.user,
                                    password=self.db_properties.password,
                                    host=self.db_properties.hostname,
                                    port=self.db_properties.port,
                                    database=self.db_properties.db,
                                    connect_timeout=5)
        except psycopg2.OperationalError as err:
            log.message.warn_db_not_found(self.db_properties)
            engine = sa.create_engine("postgresql+psycopg2://{}:{}@{}:{}".format(
                self.db_properties.user,
                self.db_properties.password,
                self.db_properties.hostname,
                self.db_properties.port))

            conn = engine.connect()
            # cannot run inside a transaction block;
            # need to set the isolation_level as AUTOCOMMIT
            conn = conn.execution_options(isolation_level="AUTOCOMMIT")
            sql_query = "CREATE DATABASE {db}".format(
                db=self.db_properties.db
            )
            conn.execute(sql_query)
            log.message.info_db_created(self.db_properties)

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
