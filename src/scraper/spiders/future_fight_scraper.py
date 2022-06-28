from inspect import BoundArguments
from re import match
import scrapy
import numpy as np
from scraper.util import *


class UfcFutureFightSpider(scrapy.Spider):
    SLPM_STRING = "Strikes Landed per Min. (SLpM)"

    name = "ufc_future_fights"
    start_urls = ["http://ufcstats.com/statistics/events/upcoming?page=all"]
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "ufc_stats_scraper.pipelines.UfcFutureFightScraperPipeline": 300,

    def parse(self, response):
        future_event_links = response.css("a.b-link::attr(href)").getall()
        yield from response.follow_all(future_event_links, self.parse_future_events)

    def parse_future_events(self, response):
        future_matchups = response.css("a.b-link::attr(data-link)").getall()
        event_context = normalize_results(
            response.css("li.b-list__box-list-item::text").getall()
        )
        yield from response.follow_all(
            future_matchups,
            self.parse_future_matchups,
            cb_kwargs={"event_context": event_context},
        )

    def trim_stats_array(self, stats_array):
        slpm_index = None
        for i in range(len(stats_array)):
            content = stats_array[i]
            if content == self.SLPM_STRING:
                slpm_index = i
                break

        return stats_array[slpm_index:]

    def parse_future_matchups(self, response, event_context):
        date = event_context[0]
        location = event_context[1]
        event_name = normalize_results(
            response.css("h2.b-content__title a.b-link::text").getall()
        )[0]
        fighter_names = normalize_results(
            response.css("a.b-fight-details__table-header-link::text").getall()
        )
        matchup_stats = response.css(
            'td.b-fight-details__table-col p.b-fight-details__table-text::text').getall()
        matchup_stats = normalize_results(matchup_stats)

        rwins = int(matchup_stats[1].split("-")[0])
        bwins = int(matchup_stats[2].split("-")[0])
        rloses = int(matchup_stats[1].split("-")[1])
        bloses = int(matchup_stats[2].split("-")[1])

        matchup_stats = self.trim_stats_array(matchup_stats)
        future_fight_matrix = np.reshape(matchup_stats[0:24], (8, 3))
        rf = fighter_names[0]
        bf = fighter_names[1]

        rslpm = float(future_fight_matrix[0][1])
        bslpm = float(future_fight_matrix[0][2])

        rstrac = int(null_check(
            future_fight_matrix[1][1]).replace("%", "")) / 100
        bstrac = int(null_check(
            future_fight_matrix[1][1]).replace("%", "")) / 100

        rsapm = float(future_fight_matrix[2][1])
        bsapm = float(future_fight_matrix[2][2])

        rstrd = int(null_check(
            future_fight_matrix[3][1]).replace("%", "")) / 100
        bstrd = int(null_check(
            future_fight_matrix[3][2]).replace("%", "")) / 100

        rtdav = float(future_fight_matrix[4][1])
        btdav = float(future_fight_matrix[4][2])

        rtdac = int(null_check(
            future_fight_matrix[5][1]).replace("%", "")) / 100
        btdac = int(null_check(
            future_fight_matrix[5][2]).replace("%", "")) / 100

        rtdd = int(null_check(
            future_fight_matrix[6][1]).replace("%", "")) / 100
        btdd = int(null_check(
            future_fight_matrix[6][2]).replace("%", "")) / 100

        rsubav = float(future_fight_matrix[7][1])
        bsubav = float(future_fight_matrix[7][2])

        bout = normalize_results(
            response.css("i.b-fight-details__fight-title::text").getall()
        )[0]

        yield {
            "rf": rf,
            "bf": bf,
            "date": date,
            "bout": bout,
            "location": location,
            "event_name": event_name,
            "rwins": rwins,
            "bwins": bwins,
            "rloses": rloses,
            "bloses": bloses,
            "rslpm": rslpm,
            "bslpm": bslpm,
            "rstrac": rstrac,
            "bstrac": bstrac,
            "rsapm": rsapm,
            "bsapm": bsapm,
            "rstrd": rstrd,
            "bstrd": bstrd,
            "rtdav": rtdav,
            "btdav": btdav,
            "rtdac": rtdac,
            "btdac": btdac,
            "rtdd": rtdd,
            "btdd": btdd,
            "rsubav": rsubav,
            "bsubav": bsubav,
        }
