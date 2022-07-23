from src.db.mysql_connect import get_mysql_connection
import pendulum
import logging


def handler(event, context):
    logging.info(
        f"Kicking off {context.function_name} with Lambda Request ID {context.aws_request_id}")
    con = get_mysql_connection()
    cur = con.cursor()
    current_date = pendulum.now().format("YYYY-MM-DD")
    logging.info(
        f"Deleting entries in future_matchups where date is older than {current_date}")
    sql_delete = "DELETE * FROM future_matchups WHERE date_ < %s;"
    sql_date = (current_date,)
    cur.execute(sql_delete, sql_date)
