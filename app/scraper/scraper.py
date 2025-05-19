import asyncio
import math
import re

from typing import Optional

import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Car

from app.logger import get_logger

logger = get_logger(__name__)

ODOMETER_PATTERN = r"(\d+)(тис\.?)?"


def parse_odometer(text: str) -> int:
    """
    Parse odometer reading from string.

    :param text: Parsed odometer text from page in "тис.".
    :return: Odometer value as an integer.
    """
    if not text:
        logger.warning("Odometer text is empty")
        return 0
    text = text.lower().replace(" ", "")
    match = re.search(ODOMETER_PATTERN, text)
    if not match:
        logger.warning("Odometer text does not match")
        return 0
    odometer_number = int(match.group(1))
    if match.group(2):
        return odometer_number * 1000
    return odometer_number


def format_phone(number: str) -> str:
    """
    Format phone number to +380xxxxxxxxx format.

    :param number: Raw parsed phone number.
    :return: Formatted phone number.
    """
    digits = "".join(filter(str.isdigit, number))
    if digits.startswith('0'):
        digits = digits[1:]
    return "+380" + digits


async def get_content_with_playwright(url: str, find_phone: bool = False) -> str:
    """
    Fetch page content with Playwright. If find_phone is True, click buttons to reveal phone.

    :param url: URL of the page to fetch.
    :param find_phone: Whether to interact with page to reveal phone.
    :return: HTML content of the page.
    """
    async with async_playwright() as p:
        logger.info(f"Starting playwright browser for url {url}")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        if find_phone:
            logger.info("Looking for phone number")
            # Accept cookies if the popup appears
            try:
                await page.wait_for_selector('button.fc-cta-consent', timeout=5000)
                await page.click('button.fc-cta-consent')
                logger.info("Cookie consent accepted.")
            except Exception as e:
                logger.warning(f"Consent button not found: {e}")

            try:
                await page.wait_for_selector('a.size14.phone_show_link.link-dotted.mhide', timeout=5000)
                await page.click('a.size14.phone_show_link.link-dotted.mhide')
                logger.info("Clicked the phone reveal link.")
            except Exception as e:
                logger.warning(f"Phone reveal link not found: {e}")

            card_html = await page.content()
            await browser.close()
            return card_html

        html = await page.content()
        await browser.close()
    return html


async def count_page_offers(session: aiohttp.ClientSession, url: str) -> Optional[int]:
    """
    Retrieve the total number of pages of offers from the given URL.

    :param session: Session object.
    :param url: URL of the page to scrape.
    :return: Number of pages.
    """
    html = await get_content_with_playwright(url)
    soup = BeautifulSoup(html, "html.parser")
    offers_div = soup.find("div", class_="quantity-offer")
    total_amount_span = offers_div.find("span")
    total_amount_str = total_amount_span.get_text(strip=True) if total_amount_span else None

    if total_amount_str:
        try:
            amount = int(total_amount_str.replace(" ", ""))
            pages = math.ceil(amount / 100)
            return pages
        except ValueError as e:
            logger.error(f"Failed to parse offer count: {e}")
    return None


async def insert_car_data(db: Session, car_data: dict) -> bool:
    """
    Insert car data into the database if it doesn't already exist.
    Checks for existing records by VIN or URL before insertion.

    :param db: Database session.
    :param car_data: Car data dictionary.
    :return: True if inserted successfully, False otherwise.
    """

    if not car_data.get("url") or not car_data.get("car_vin"):
        logger.error("Missing required fields: url or car_vin")
        return False

    existing_car = db.query(Car).filter(
        (Car.car_vin == car_data.get("car_vin")) |
        (Car.url == car_data.get("url"))
    ).first()

    if existing_car:
        logger.warning(f"Car already exists in DB: {car_data.get('car_vin') or car_data.get('url')}")
        return False

    try:
        car = Car(**car_data)
        db.add(car)
        db.commit()
        logger.info(f"Saved car: {car.url}")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError while saving car: {e}")
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while saving car: {e}")
        return False


async def fetch_html(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch raw HTML content for a given URL.

    :param session: HTTP session.
    :param url: URL to fetch.
    :return: HTML content of the page.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }
    try:
        async with session.get(url, headers=headers) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Failed to fetch html: {e}")
        raise


async def parse_car_page():
    """
    Main function to parse car from the specified URL.
    Fetches pages, extracts car details, and inserts data into the database.
    """
    async with aiohttp.ClientSession() as session:
        start_url = ("https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search"
                     "&categories.main.id=1&country.import.usa.not=-1&price.currency=1"
                     "&abroad.not=0&custom.not=1&page=1&size=100")

        total_pages = await count_page_offers(session, start_url)
        if not total_pages:
            logger.error("Unable to determine total pages")
            return

        logger.info(f"Total pages to process: {total_pages}")

        for page_num in range(1, total_pages + 1):
            page_url = start_url.replace("page=1", f"page={page_num}")
            logger.info(f"Processing page {page_num}: {page_url}")
            page_html = await fetch_html(session, page_url)
            soup = BeautifulSoup(page_html, 'html.parser')
            cards = soup.find_all("section", class_="ticket-item")

            for car in cards:
                try:
                    link = car.find('div', class_='content-bar').find('a', class_='m-link-ticket').get('href')
                    card_html = await get_content_with_playwright(link, True)
                    card_soup = BeautifulSoup(card_html, "html.parser")

                    title = card_soup.find("h1", class_="head")
                    title = title.get_text(strip=True) if title else None

                    # price_str = card_soup.find("div", class_="price_value")
                    # price_str = price_str.get_text(strip=True).split("$")[0] if price_str else None
                    # price = int(price_str.replace(" ", "")) if price_str and "грн" not in price_str else None
                    price_str = card_soup.find("div", class_="price_value")
                    if price_str:
                        price_text = price_str.get_text(strip=True)
                        price_digits = re.search(r"(\d[\d\s]*)", price_text)
                        if price_digits:
                            price_cleaned = price_digits.group(1).replace(" ", "")
                            try:
                                price = int(price_cleaned)
                            except ValueError:
                                logger.warning(f"Could not parse price: {price_text}")
                                price = None
                        else:
                            price = None
                    else:
                        price = None

                    odometer_div = card_soup.find("div", class_="base-information")
                    odometer = parse_odometer(odometer_div.get_text(strip=True)) if odometer_div else None

                    username_div = card_soup.find("div", class_="seller_info_name bold")
                    username_tag = username_div.find("a") if username_div else None
                    username = username_div.get_text(strip=True) if username_tag else None

                    phone_span = card_soup.find("span", class_="phone bold")
                    phone_number = phone_span.get_text(strip=True) if phone_span else None
                    phone_number = format_phone(phone_number) if phone_number else None

                    photo_div = card_soup.find("div", id="photosBlock")
                    first_img = photo_div.find("img") if photo_div else None
                    first_img_url = first_img.get("src") if first_img and first_img.has_attr("src") else None

                    images_count = len(card_soup.find_all("div", class_="photo-620x465"))

                    state_span = card_soup.find("span", class_="state-num ua")
                    cur_number = state_span.contents[0].get_text(strip=True) if state_span else None
                    cur_number = cur_number.replace(" ", "") if cur_number else None

                    vin_span = card_soup.find("span", attrs={"class": ["vin-code", "label-vin"]})
                    vin_number = vin_span.get_text(strip=True) if vin_span else None

                    car_data = {
                        "url": link,
                        "title": title,
                        "price_usd": price,
                        "odometer": odometer,
                        "username": username,
                        "phone_number": phone_number,
                        "images_count": images_count,
                        "image_url": first_img_url,
                        "car_number": cur_number,
                        "car_vin": vin_number,
                    }

                    db = SessionLocal()
                    await insert_car_data(db, car_data)
                    db.close()
                except Exception as e:
                    logger.error(f"Error parsing card: {e}")


if __name__ == "__main__":
    asyncio.run(parse_car_page())
