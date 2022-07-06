 # Introduction
 ufc-scraper-lambda is an AWS Lambda built using the Serverless framework and Scrapy to scrap past and future UFC data from [ufcstats](http://ufcstats.com/). The scraped data is commited to an AWS RDS database to be used by the Flask app [ufc-event-predictor](https://github.com/natebuel29/ufc-event-predictor) to predict future UFC events using various Machine Learning algorithms. 
 
 # Lambda Functions
 ### Future Fight Scraper

The future fight scraper scraps data for future UFC events. This data will be **fed** to various ML models to predict UFC events. The scraper runs every Monday and Friday at 6:00 UTC.

## PLANNED FUNCTIONS

`Future Fight Reaper` - Cleans up past UFC events from future_matchups DB table

`Previous Event Result Scraper` - Scraps and randomizes the previous UFC event and commits the data to the past_matchups DB table
