from discord import Embed
from discord.colour import Colour
from discord.ext.commands import Cog
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from bot import DiscordModeratorWumpus
from bot.utils import timestamp_validity

from datetime import datetime, timedelta
import dateutil.tz
from calendar import month_name


class Timestamp(Cog):
    """Commands for creating timestamps"""

    def __init__(self, bot: DiscordModeratorWumpus) -> None:
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="timestamp",
        name="make",
        description="Returns embeddable timestamp",
        options=[
            create_option(
                name="year",
                description="Year of date",
                option_type=4,
                required=True,
            ),
            create_option(
                name="month",
                description="Month of date",
                option_type=4,
                required=True,
                choices=[
                    create_choice(1, "January"),
                    create_choice(2, "February"),
                    create_choice(3, "March"),
                    create_choice(4, "April"),
                    create_choice(5, "May"),
                    create_choice(6, "June"),
                    create_choice(7, "July"),
                    create_choice(8, "August"),
                    create_choice(9, "September"),
                    create_choice(10, "October"),
                    create_choice(11, "November"),
                    create_choice(12, "December"),
                ]
            ),
            create_option(
                name="day",
                description="Day of date",
                option_type=4,
                required=True,
            ),
            create_option(
                name="hour",
                description="Hour of time in 24 hour format",
                option_type=4,
                required=True,
            ),
            create_option(
                name="minute",
                description="Minute of time",
                option_type=4,
                required=True,
            ),
            create_option(
                name="utc",
                description="UTC offset, defaults to 0, range -12 -> 14",
                option_type=4,
                required=False,
            ),
            create_option(
                name="tag",
                description="Tag for format, defaults to short date/time",
                option_type=3,
                required=False,
                choices=[
                    create_choice("t", "Short Time"),
                    create_choice("T", "Long Time"),
                    create_choice("d", "Short Date"),
                    create_choice("D", "Long Time"),
                    create_choice("f", "Short Date/Time"),
                    create_choice("F", "Long Date/Time"),
                    create_choice("R", "Relative Time"),

                ]
            )
        ],
    )
    async def _timestamp_make(self, ctx: SlashContext, year: int, month: int, day: int, hour: int, minute: int, utc: int = 0, tag: str = "f"):
        validity_check = timestamp_validity.make_data_validity(year, month, day, hour, minute, utc)

        if len(validity_check) == 0:
            dt = datetime(year, month, day, hour, minute, 0, 0, tzinfo=dateutil.tz.tzoffset(None, 3600 * utc))
            ts = int(dt.timestamp())
            embed = Embed(title="Timestamp Created", color=Colour.blurple())
            embed.add_field(name="Output", value=f"<t:{ts}:{tag}>")
            embed.add_field(name="Copyable", value=f"\<t:{ts}:{tag}\>")
            await ctx.send(embed=embed, hidden=True)

        else:
            embed = Embed(colour=Colour.blurple(), title="Timestamp Error")
            for error in validity_check:
                extra = ""

                if error["name"] == "day":
                    extra = f" for {month_name[month]}"
                    if month == 2:
                        extra += f" {year}"

                embed.add_field(
                    name="Field Error",
                    value=f'You inputted {error["input"]} for field `{error["name"]}`. Field must be between '
                          f'{error["min"]} and {error["max"]} inclusively{extra}.',
                    inline=False,
                )
            await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_subcommand(
        base="timestamp",
        name="now",
        description="Returns the current date and time in UTC and your timezone",
    )
    async def _timestamp_now(self, ctx: SlashContext):
        time = datetime.utcnow()
        embed = Embed(title="Current Time", color=Colour.blurple())
        embed.add_field(name="UTC Time", value=time.strftime("%A, %B %d, %Y %-I:%M %p"), inline=False)
        embed.add_field(name="Local Time", value=f"<t:{int(time.timestamp())}:F>", inline=False)
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_subcommand(
        base="timestamp",
        name="relative",
        description="Returns a timestamp relative to current time",
        options=[
            create_option(
                name="days",
                description="Days relative to now, +- 730500 days inclusively",
                option_type=4,
                required=False,
            ),
            create_option(
                name="hours",
                description="Hours relative to now, += 23 hours inclusively",
                option_type=4,
                required=False,
            ),
            create_option(
                name="minutes",
                description="Minutes relative to now, +- 59 minutes inclusively",
                option_type=4,
                required=False,
            ),
            create_option(
                name="tag",
                description="Tag for format, defaults to short date/time",
                option_type=3,
                required=False,
                choices=[
                    create_choice("t", "Short Time"),
                    create_choice("T", "Long Time"),
                    create_choice("d", "Short Date"),
                    create_choice("D", "Long Time"),
                    create_choice("f", "Short Date/Time"),
                    create_choice("F", "Long Date/Time"),
                    create_choice("R", "Relative Time"),

                ]
            )
        ]
    )
    async def _timestamp_relative(self, ctx: SlashContext, days: int = 0, hours: int = 0, minutes: int = 0, tag: str = "f"):
        validity_check = timestamp_validity.relative_data_validity(days, hours, minutes)
        if len(validity_check) == 0:
            time = datetime.utcnow()
            td = timedelta(days=days, hours=hours, minutes=minutes)
            time = time + td
            ts = int(time.timestamp())
            embed = Embed(title="Relative Time", color=Colour.blurple(), description=f"Time shifted by {td}")
            embed.add_field(name="Output", value=f"<t:{ts}:{tag}>", inline=False)
            embed.add_field(name="Copyable", value=f"\<t:{ts}:{tag}\>", inline=False)
            await ctx.send(embed=embed, hidden=True)

        else:
            embed = Embed(colour=Colour.blurple(), title="Timestamp Error")
            for error in validity_check:
                embed.add_field(
                    name="Field Error",
                    value=f'You inputted {error["input"]} for field `{error["name"]}`. Field must be within '
                          f'the range +-{error["range"]}.',
                    inline=False,
                )
            await ctx.send(embed=embed, hidden=True)


def setup(bot: DiscordModeratorWumpus) -> None:
    bot.add_cog(Timestamp(bot))
