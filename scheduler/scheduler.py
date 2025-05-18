import asyncio
import os

import pytz
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from app.scraper.scraper import parse_car_page
from app.dump_db import dump_postgres_db
from app.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

SCRAPE_TIME = os.getenv("SCRAPE_TIME", "12:00")
DUMP_TIME = os.getenv("DUMP_TIME", "11:00")
MAIN_PAGE = "https://auto.ria.com/car/used/"

timezone = pytz.timezone('Europe/Warsaw')
scheduler = BlockingScheduler(timezone=timezone)

scrape_hour, scrape_minute = map(int, SCRAPE_TIME.split(":"))
dump_hour, dump_minute = map(int, DUMP_TIME.split(":"))


@scheduler.scheduled_job("cron", hour=scrape_hour, minute=scrape_minute)
def daily_scraper_job():
    logger.info("Starting daily scraping job")
    asyncio.run(parse_car_page())
    logger.info("Scraping job completed")


@scheduler.scheduled_job("cron", hour=dump_hour, minute=dump_minute)
def daily_db_dump():
    logger.info("Starting daily DB dump")
    dump_postgres_db()
    logger.info("Dump DB finished")


logger.info("Scheduler started")
scheduler.start()
