from discord import Intents, Status
from discord.ext import commands
from discord_slash import SlashCommand
from loguru import logger


class Bot(commands.Bot):
    async def on_ready(self):
        logger.info(f"Logged in as {self.user} on {len(self.guilds)} guilds.")


bot = Bot(
    command_prefix="!",
    intents=Intents.all(),
    help_command=None,
)

slash = SlashCommand(
    bot, sync_commands=True, sync_on_cog_reload=True, delete_from_unused_guilds=True
)
