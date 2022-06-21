from inspect import BoundArguments
from re import match
import scrapy
import numpy as np
from scraper.util import normalize_results


class UfcFutureFightSpider(scrapy.Spider):
    name = "ufc_future_fights"
    start_urls = ["http://ufcstats.com/statistics/events/upcoming?page=all"]
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "ufc_stats_scraper.pipelines.UfcFutureFightScraperPipeline": 300,
    #     }
    # }

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
        # TODO: Add error logic for a future_fight with a fighter who is missing data

        future_fight_matrix = np.reshape(matchup_stats[0:45], (15, 3))
        print(future_fight_matrix)
        rf = fighter_names[0]
        bf = fighter_names[1]

        rwins = int(future_fight_matrix[0][1].split("-")[0])
        bwins = int(future_fight_matrix[0][2].split("-")[0])

        rloses = int(future_fight_matrix[0][1].split("-")[1])
        bloses = int(future_fight_matrix[0][2].split("-")[1])

        print(rwins)
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
        }
