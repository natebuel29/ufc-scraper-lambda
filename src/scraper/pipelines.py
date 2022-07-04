# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy

import mysql.connector


class UfcFutureFightScraperPipeline:
    def __init__(self):
        print("here in ufc future fight scraper pipeline")
        # temp DB creds that will be rotated out!!
        host = 'uu1744jdr5e80dc.cdxfj1ghajls.us-east-1.rds.amazonaws.com'
        user = 'mysqlAdmin'
        password = '5bc,cx^h=H8KbdN3x.mSd95jMmZmwK'
        database = 'thisisatest'
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
            """CREATE TABLE if not exists future_matchups(id INT AUTO_INCREMENT PRIMARY KEY,
            date_ TEXT,
            event_name TEXT,
            rf TEXT,
            bf TEXT,
            rwins INT,
            bwins INT,
            rloses INT,
            bloses INT,
            rslpm FLOAT,
            bslpm FLOAT,
            rstrac FLOAT,
            bstrac FLOAT,
            rsapm FLOAT,
            bsapm FLOAT,
            rstrd FLOAT,
            bstrd FLOAT,
            rtdav FLOAT,
            btdav FLOAT,
            rtdac FLOAT,
            btdac FLOAT,
            rtdd FLOAT,
            btdd FLOAT,
            rsubav FLOAT,
            bsubav FLOAT)"""
        )

    def process_item(self, item, spider):
        # skip db steps if there is no connection
        if self.con != None:
            sql = """
            INSERT INTO future_matchups (date_,event_name,rf,bf,rwins,bwins,rloses,bloses,rslpm,bslpm,rstrac,bstrac,rsapm,bsapm,rstrd,bstrd,rtdav,btdav,rtdac,btdac,rtdd,btdd,rsubav,bsubav)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            val = (
                item["date"],
                item["event_name"],
                item["rf"],
                item["bf"],
                item["rwins"],
                item["bwins"],
                item["rloses"],
                item["bloses"],
                item["rslpm"],
                item["bslpm"],
                item["rstrac"],
                item["bstrac"],
                item["rsapm"],
                item["bsapm"],
                item["rstrd"],
                item["bstrd"],
                item["rtdav"],
                item["btdav"],
                item["rtdac"],
                item["btdac"],
                item["rtdd"],
                item["btdd"],
                item["rsubav"],
                item["bsubav"],
            )

            self.cur.execute(sql, val)
            self.con.commit()

        return item
