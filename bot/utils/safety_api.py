import aiohttp
from urllib import parse
from loguru import logger
from discord_slash.context import SlashContext

from bot.constants import SAFETY_API_ENDPOINT, SAFETY_IDS


def key_sort(article_id: int):
    try:
        category_index = SAFETY_IDS.index(article_id)
    except ValueError:
        category_index = 2000  # Number which shall never be reached in articles
    return category_index


async def get_api(ctx: SlashContext, query_string: str = None, category: int = None):
    url_params = {}
    if query_string:
        url_params["query"] = f"{{{query_string}}}"

    if category:
        url_params["section"] = category

    request_url = f"{SAFETY_API_ENDPOINT}?{parse.urlencode(url_params)}"

    try:
        async with aiohttp.ClientSession() as sess:
            response = await sess.get(request_url)
            response.raise_for_status()
            data = await response.json()

            results = data["results"]
            for result in results:
                result["url"] = f"https://discord.com/safety/{result['id']}"

            results_parse = sorted(results, key=lambda x: key_sort(x["id"]))

    except Exception:
        logger.exception("Error in Safety API Request")
        await ctx.send(
            "Couldn't load search results from the Safety Portal, please contact the devs"
        )
        return True

    return results_parse
