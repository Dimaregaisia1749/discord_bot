import discord
import logging
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, Context
import os
from data import db_session
from dotenv import load_dotenv
from data import db_session
import datetime

load_dotenv(dotenv_path="token.env")

TOKEN = os.getenv('TOKEN')
#proxy = "http://proxy.volgatech.net:3128/"

db_session.global_init("db/blogs.db")

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

            
class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.all(),
                         application_id=1087358256416051325)
        
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            if message.author.name in ("70 JlETHNN TTЕHCNOHEP", "dimaregaisia"):
                await message.add_reaction("💀")
            if message.author.name == "DоctorMaki":
                await message.add_reaction("🍺")                
    
    async def setup_hook(self) -> None:
        for i in os.listdir('cogs'):
            if i[-3:] == '.py':
                await self.load_extension(f"cogs.{i[:-3]}")
        await self.tree.sync(guild=discord.Object(id=806157869040140288))


#client = BotClient(intents=intents, proxy=proxy)
bot = BotClient()
bot.run(TOKEN)

