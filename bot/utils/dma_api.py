import functools
import re
import textwrap

import aiohttp
from urllib import parse
from bs4 import BeautifulSoup
from loguru import logger

from bot.constants import DMA_API_URL, DMA_API_SEARCH_URL, DMA_TITLE_REGEX, DMA_SERIES_IDS, DMA_QUERY_REGEX


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


async def get_search_api(query_string: str = None, series_number: int = None):
    url_params = {}
    if query_string:
        url_params["query"] = f"{{{query_string}}}"

    if series_number:
        url_params["section"] = DMA_SERIES_IDS[series_number]

    request_url = f'{DMA_API_SEARCH_URL}?{parse.urlencode(url_params)}'
    
    results_parse = []
    try:
        async with aiohttp.ClientSession() as sess:
            response = await sess.get(request_url)
            response.raise_for_status()
            data = await response.json()

            results = data["results"]

            for item in results:
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
                    results_parse.append(article)

            results_parse = sorted(results_parse, key=lambda x: (x["series"], x["category"], x["digit"]))
    except Exception:
        logger.exception("Error fetching information from DMA")
    return results_parse


@get_api()
async def get_category(category, articles):
    items = [item for item in articles if item["category"] == str(category)]
    return sorted(items, key=lambda x: (x["series"], x["category"], x["digit"]))


async def get_article(number):
    articles = await get_search_api(query_string=str(number))
    return [
        item
        for item in articles
        if item["series"] == str(number)[0]
        and item["category"] == str(number)[1]
        and item["digit"] == str(number)[2]
    ]
