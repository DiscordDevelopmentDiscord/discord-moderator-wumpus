from discord.ext.commands import Cog
from discord import Member, Message
from loguru import logger

from bot import Bot
from bot.constants import AUTOROLE_CONFIG


class AutoRole(Cog):
    """Automatic role assignment for DMD/MMC members."""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.guild.id not in AUTOROLE_CONFIG:
            return

        if not member.bot:
            logger.info(f"User {member} joined, applying roles.")
            await self.add_roles(member)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None:
            return

        if message.guild.id not in AUTOROLE_CONFIG:
            return

        member = message.author
        guild = message.guild
        role_ids = [role.id for role in member.roles]
        role_config = AUTOROLE_CONFIG[guild.id]

        has_job_role = (
            role_config["MODERATOR"] in role_ids or role_config["DISCORD"] in member.roles
        )
        is_roled = role_config["MEMBER"] in role_ids and has_job_role

        if not member.pending and not is_roled:
            await self.add_roles(member)

    async def add_roles(self, member: Member) -> None:
        role_config = AUTOROLE_CONFIG[member.guild.id]
        guild = member.guild

        member_role = guild.get_role(role_config["MEMBER"])
        moderator_role = guild.get_role(role_config["MODERATOR"])
        discord_role = guild.get_role(role_config["DISCORD"])

        if member.public_flags.staff:
            await member.add_roles(member_role, discord_role)
            logger.info(f"Gave member + Discord roles to {member}")
        else:
            await member.add_roles(member_role, moderator_role)
            logger.info(f"Gave member + Moderator roles to {member}")


def setup(bot: Bot):
    bot.add_cog(AutoRole(bot))
