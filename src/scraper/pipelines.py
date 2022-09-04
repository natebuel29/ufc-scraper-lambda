# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import logging
from src.db.mysql_connect import get_mysql_connection


class UfcFutureFightScraperPipeline:
    def __init__(self):
        logging.info("initializing UfcFutureFightScraperPipeline")
        self.con = get_mysql_connection()
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE if not exists future_matchups(fight_id varchar(64) PRIMARY KEY,
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
            REPLACE INTO future_matchups (fight_id,date_,event_name,rf,bf,rwins,bwins,rloses,bloses,rslpm,bslpm,rstrac,bstrac,rsapm,bsapm,rstrd,bstrd,rtdav,btdav,rtdac,btdac,rtdd,btdd,rsubav,bsubav)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            val = (
                # .encode('ascii') converts the string to binary
                hashlib.sha224(
                    f"{item['rf']}+{item['bf']}+{item['rwins']}+{item['bwins']}".encode('ascii')).hexdigest(),
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


class UfcPreviousEventScraperPipeline:
    def __init__(self):
        logging.info("initializing UfcFutureFightScraperPipeline")
        self.con = get_mysql_connection()
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE if not exists past_matchups(id INT AUTO_INCREMENT PRIMARY KEY,
            rf TEXT,
            bf TEXT,
            winner INT,
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
            INSERT INTO past_matchups (rf,bf,winner,rwins,bwins,rloses,bloses,rslpm,bslpm,rstrac,bstrac,rsapm,bsapm,rstrd,bstrd,rtdav,btdav,rtdac,btdac,rtdd,btdd,rsubav,bsubav)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            val = (
                item["rf"],
                item["bf"],
                item["winner"],
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
