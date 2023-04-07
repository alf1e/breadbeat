import discord
from discord import app_commands
import aiocron
import aiohttp

import breadcord
from breadcord.module import ModuleCog


class BreadBeat(breadcord.module.ModuleCog):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name)

        self.client = aiohttp.ClientSession()
        self.module_settings = self.bot.settings.breadbeat
        self.aio_cron = aiocron.crontab(self.module_settings.heartbeat_crontab.value, func=self.heartbeat)
        self.aio_cron.start()

    async def cog_unload(self):
        await self.client.close()
        self.aio_cron.stop()

    async def heartbeat(self):
        await self.client.get(self.module_settings.heartbeat_url.value)
        self.logger.debug(f'Heartbeat sent to {self.module_settings.heartbeat_url.value}')


async def setup(bot: breadcord.Bot):
    await bot.add_cog(BreadBeat("breadbeat"))
