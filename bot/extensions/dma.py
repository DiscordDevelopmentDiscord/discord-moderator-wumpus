from discord import Embed
from discord.colour import Colour
from discord.ext.commands import Cog
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option

from bot import DiscordModeratorWumpus
from bot.constants import DMA_CATEGORY_NAMES, DMA_SERIES_NAMES
from bot.utils import dma_api


def article_to_name(articles):
    names = []
    for a in articles:
        names.append(f'{a["series"]}{a["category"]}{a["digit"]}: {a["name"]}')
    return names


def article_to_url(articles):
    urls = []
    for u in articles:
        urls.append(f"https://dis.gd/dma{u['series']}{u['category']}{u['digit']}")
    return urls


class DMA(Cog):
    """Commands for fetching information from the Discord Moderator Academy"""

    def __init__(self, bot: DiscordModeratorWumpus) -> None:
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="dma",
        name="article",
        description="Search for a specific DMA article",
        options=[
            create_option(
                name="number",
                description="The number of the article",
                option_type=4,
                required=True,
            )
        ],
    )
    async def _dma_article(self, ctx: SlashContext, number: int):
        try:
            results = await dma_api.get_article(number)
            embed = Embed(
                title=article_to_name(results)[0],
                colour=Colour.blurple(),
                url=article_to_url(results)[0],
                description=results[0]["text"],
            )
            embed.set_author(name="Discord Moderator Academy")
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(content=f"Article {number} could not be found", hidden=True)

    @cog_ext.cog_subcommand(
        base="dma",
        name="series",
        description="List the articles in a specific series",
        options=[
            create_option(
                name="number",
                description="The series (Nxx) number",
                option_type=4,
                required=True,
            )
        ],
    )
    async def _dma_series(self, ctx: SlashContext, number: int):
        if number in [1, 2, 3, 4, 5]:
            results = await dma_api.get_series(number)
            embed = Embed(colour=Colour.blurple(), description=f"*{DMA_SERIES_NAMES[number]}*")
            embed.set_author(name=f"Discord Moderator Academy: Series {number}")
            for result in results:
                embed.add_field(
                    name=article_to_name([result])[0],
                    value=article_to_url([result])[0],
                    inline=False,
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send(content=f"Series {number} could not be found", hidden=True)

    @cog_ext.cog_subcommand(
        base="dma",
        name="category",
        description="List the articles in a specific category",
        options=[
            create_option(
                name="number",
                description="The category (xNx) number",
                option_type=4,
                required=True,
            )
        ],
    )
    async def _dma_category(self, ctx: SlashContext, number: int):
        if number in [0, 1, 2, 3, 4, 5]:
            results = await dma_api.get_category(number)
            embed = Embed(colour=Colour.blurple(), description=f"*{DMA_CATEGORY_NAMES[number]}*")
            embed.set_author(name=f"Discord Moderator Academy: Category {number}")
            for result in results:
                embed.add_field(
                    name=article_to_name([result])[0],
                    value=article_to_url([result])[0],
                    inline=False,
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send(content="Needs a valid number between 0 and 5", hidden=True)

    @cog_ext.cog_subcommand(
        base="dma",
        name="search",
        description="Search within the contents of articles",
        options=[
            create_option(
                name="terms",
                description="Terms to search for within DMA articles",
                option_type=3,
                required=True,
            )
        ],
    )
    async def _dma_search(self, ctx: SlashContext, terms: str):
        embed = Embed(colour=Colour.blurple(), description=f"Search results for `{terms}`")
        embed.set_author(name="DMA Search")
        for result in await dma_api.search_term(terms):
            embed.add_field(
                name=article_to_name([result])[0],
                value=article_to_url([result])[0],
                inline=False,
            )
        await ctx.send(embed=embed)


def setup(bot: DiscordModeratorWumpus) -> None:
    bot.add_cog(DMA(bot))
