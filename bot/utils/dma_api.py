import functools
import re
import textwrap

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger

from bot.constants import DMA_API_URL, DMA_TITLE_REGEX


def get_api():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(search):
            try:
                async with aiohttp.ClientSession() as sess:
                    response = await sess.get(DMA_API_URL)
                    response.raise_for_status()
                    data = await response.json()

                    articles = data["articles"]
                    articles_parse = []

                    for item in articles:
                        if re.search(DMA_TITLE_REGEX, item["name"]):
                            article = {}
                            # Article
                            number, name = item["name"].split(": ")
                            article["series"] = number[0]
                            article["category"] = number[1]
                            article["digit"] = number[2]
                            article["name"] = name
                            soup = BeautifulSoup(item["body"], "html.parser")

                            placeholder = f"... [continue reading](https://dis.gd/dma{number})"
                            article["text"] = textwrap.shorten(
                                soup.p.text, 800, placeholder=placeholder
                            )
                            articles_parse.append(article)
            except Exception:
                logger.exception("Error fetching information from DMA")
            return await func(search, articles_parse)

        return wrapped

    return wrapper


@get_api()
async def get_article(number, articles):
    return [
        item
        for item in articles
        if item["series"] == str(number)[0]
        and item["category"] == str(number)[1]
        and item["digit"] == str(number)[2]
    ]


@get_api()
async def get_series(series, articles):
    return [item for item in articles if item["series"] == str(series)]


@get_api()
async def get_category(category, articles):
    return [item for item in articles if item["category"] == str(category)]


@get_api()
async def search_term(term, articles):
    return [
        item
        for item in articles
        if term.lower() in item["text"].lower() or term.lower() in item["name"].lower()
    ]
