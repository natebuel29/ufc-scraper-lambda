# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class UfcFutureFightScraperPipeline:
    def __init__(self):
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        database = os.environ.get("DB_DATABASE")
        if host != None and user != None and password != None and database != None:
            self.con = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            self.cur = self.con.cursor()
            self.create_table()
        else:
            self.con = None
            self.cur = None

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE if not exists future_fights(id INT AUTO_INCREMENT PRIMARY KEY,
            fighter_1 TEXT,
            fighter_2 TEXT,
            date_ TEXT,
            bout TEXT,
            location_ TEXT,
            event_name TEXT)"""
        )

    def process_item(self, item, spider):
        # skip db steps if there is no connection
        if self.con != None:
            sql = """ INSERT IGNORE INTO future_fights (fighter_1,fighter_2,date_,bout,location_,event_name) VALUES (%s,%s,%s,%s,%s,%s)
            """
            val = (
                item["fighter_1"],
                item["fighter_2"],
                item["date"],
                item["bout"],
                item["location"],
                item["event_name"],
            )

            self.cur.execute(sql, val)
            self.con.commit()

        return item
