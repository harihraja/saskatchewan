import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#
# Operator populates fact tables
# from staging tables
#
class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 conn_id="",
                 table="",
                 append=False,
                 sql="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.table = table
        self.append = append
        self.sql = sql

    def execute(self, context):
        # acquire hook
        db = PostgresHook(postgres_conn_id=self.conn_id)

        # clear table if not in append mode 
        if not self.append:
            self.log.info("Clearing data from destination table")
            db.run("DELETE FROM {}".format(self.table))
        
        # run sql updated with table name
        formatted_sql = self.sql.format(self.table)
        self.log.info("formatted_sql")
        db.run(formatted_sql)
