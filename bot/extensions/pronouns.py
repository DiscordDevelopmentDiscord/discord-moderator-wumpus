import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from loguru import logger

from bot.constants import PRONOUN_OPTIONS, GUILDS_PRONOUN_ROLES


class Pronouns(commands.Cog):
    """Manage pronoun roles."""

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="pronouns",
        name="add",
        description="Add a pronoun role",
        options=[
            create_option(
                name="pronoun",
                description="The pronoun to add",
                option_type=3,
                required=True,
                choices=PRONOUN_OPTIONS,
            )
        ],
    )
    async def pronoun_roles_add(self, ctx: SlashContext, pronoun: str):
        role = ctx.guild.get_role(GUILDS_PRONOUN_ROLES[ctx.guild.id][pronoun])

        logger.info(f"Adding {role} to {ctx.author}")

        await ctx.author.add_roles(role, reason="Pronouns Command")
        await ctx.send(":tada: Pronouns updated!", hidden=True)

    @cog_ext.cog_subcommand(
        base="pronouns",
        name="remove",
        description="Remove a pronoun role",
        options=[
            create_option(
                name="pronoun",
                description="The pronoun to add",
                option_type=3,
                required=True,
                choices=PRONOUN_OPTIONS,
            )
        ],
    )
    async def pronoun_roles_remove(self, ctx: SlashContext, pronoun: str):
        role = ctx.guild.get_role(GUILDS_PRONOUN_ROLES[ctx.guild.id][pronoun])

        await ctx.author.remove_roles(role, reason="Pronouns Command")

        logger.info(f"Removing {role} to {ctx.author}")
        await ctx.send("Pronouns updated! :tada:", hidden=True)

    @cog_ext.cog_subcommand(
        base="pronouns", name="about", description="Information on pronouns"
    )
    async def pronoun_roles_about(self, ctx: SlashContext):
        pronouns = "\n".join(["• " + pronoun["name"] for pronoun in PRONOUN_OPTIONS])

        embed = discord.Embed(
            title="Pronoun roles",
            description=f"Available pronouns are:\n{pronouns}",
            color=0xEB459E,
        )

        embed.set_footer(text="Update your pronouns with the /pronouns commands.")
        await ctx.send(embed=embed, hidden=True)


def setup(bot):
    bot.add_cog(Pronouns(bot))
