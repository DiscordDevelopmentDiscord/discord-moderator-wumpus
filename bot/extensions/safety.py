from discord import Embed
from discord.colour import Colour
from discord.ext.commands import Cog
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from loguru import logger

from bot import DiscordModeratorWumpus
from bot.utils import safety_api
from bot.constants import SAFETY_CATEGORY_NAMES


class Safety(Cog):
    """Commands for fetching information from the Discord Moderator Academy"""

    def __init__(self, bot: DiscordModeratorWumpus) -> None:
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="safety",
        name="category",
        description="List the safety articles in a particular category.",
        options=[
            create_option(
                name="category",
                description="The category to be listed.",
                option_type=4,
                required=True,
                choices=[
                    create_choice(key, value) for (key, value) in SAFETY_CATEGORY_NAMES.items()
                ],
            )
        ],
    )
    async def _safety_category(self, ctx: SlashContext, number: int):
        if number in SAFETY_CATEGORY_NAMES:
            results = await safety_api.get_api(category=number)
            embed = Embed(colour=Colour.blurple(), description=f"*{SAFETY_CATEGORY_NAMES[number]}*")
            embed.set_author(name=f"Discord Safety Portal")
            for result in results:
                embed.add_field(
                    name=result["name"],
                    value=result["url"],
                    inline=False,
                )
            await ctx.send(embed=embed)
        else:
            logger.warning(f"Input of series {number} given by {ctx.author}")
            await ctx.send(content=f"Series {number} could not be found", hidden=True)

    @cog_ext.cog_subcommand(
        base="safety",
        name="search",
        description="Search within the contents of articles",
        options=[
            create_option(
                name="terms",
                description="Terms to search for within safety articles",
                option_type=3,
                required=True,
            )
        ],
    )
    async def _safety_search(self, ctx: SlashContext, terms: str):
        terms_safe = terms.replace("`", "")
        if len(terms_safe) == 0:
            terms_safe = " "
        embed = Embed(colour=Colour.blurple(), description=f"Search results for `{terms_safe}`")
        embed.set_author(name="Discord Safety Search")
        results = await safety_api.get_api(query_string=terms)
        for result in results:
            embed.add_field(
                name=result["name"],
                value=result["url"],
                inline=False,
            )
        await ctx.send(embed=embed)


def setup(bot: DiscordModeratorWumpus) -> None:
    bot.add_cog(Safety(bot))
