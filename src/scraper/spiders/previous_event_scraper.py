import scrapy
import numpy as np
from src.scraper.util import *
from src.db.mysql_connect import get_mysql_connection
import random
import logging


class UfcPreviousEventScraper(scrapy.Spider):
    name = "ufc_previous_event"
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "src.scraper.pipelines.UfcPreviousEventScraperPipeline": 300,
        }
    }

    def parse(self, response):
        previous_event_link = response.css(
            "tr.b-statistics__table-row a::attr(href)").getall()[1]
        print(previous_event_link)
        yield response.follow(previous_event_link, self.parse_previous_event)

    def parse_previous_event(self, response):
        previous_matchups = response.css(
            "table.b-fight-details__table tbody tr::attr(data-link)").getall()

        yield from response.follow_all(
            previous_matchups,
            self.parse_previous_matchups
        )

    def parse_previous_matchups(self, response):
        # scrap the winner
        results = {}

        fighter_results = normalize_results(
            response.css(
                "section a.b-fight-details__person-link ::text").getall()
        )
        chance = random.uniform(0, 1)
        r_labels = ["rwins", "rloses", "rslpm", "rstrac",
                    "rsapm", "rstrd", "rtdav", "rtdac", "rtdd", "rsubav"]
        b_labels = ["bwins", "bloses", "bslpm", "bstrac",
                    "bsapm", "bstrd", "btdav", "btdac", "btdd", "bsubav"]
        if chance < 0.65:
            rf = fighter_results[0]
            bf = fighter_results[1]

            rf_index = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
            bf_index = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
        else:
            rf = fighter_results[1]
            bf = fighter_results[0]
            rf_index = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
            bf_index = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
        results["rf"] = rf
        results["bf"] = bf

        winner_results = normalize_results(response.css(
            "section div.b-fight-details__person i.b-fight-details__person-status ::text").getall())
        if winner_results[0] == "D":
            return
        else:
            winner = 1 if winner_results[0] == "W" else 0
            results["winner"] = winner

        con = get_mysql_connection()
        cur = con.cursor()
        try:
            sql = f"SELECT * FROM future_matchups where rf = '{rf}' AND bf='{bf}';"
            cur.execute(sql)

            fight_stats = cur.fetchall()[0]

            for i in range(0, len(r_labels)):
                r_label = r_labels[i]
                r_i = rf_index[i]
                r_value = fight_stats[r_i]
                b_label = b_labels[i]
                b_i = bf_index[i]
                b_value = fight_stats[b_i]

                results[r_label] = r_value
                results[b_label] = b_value
        except:
            logging.error(
                "Failed to scrap previous event - perhaps there wasn't an event last week")
            return

        return results
