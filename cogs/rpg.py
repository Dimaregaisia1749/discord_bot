import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import random
from data.users import User
from data import db_session


class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='start', description='Начать путешествие')
    @app_commands.describe(nickname="Никнейм")
    async def start(self, ctx: discord.Interaction, nickname: str):
        user = User()
        user.name = nickname
        user.user_id = ctx.user.id
        user.avatar_link = "https://cdn.discordapp.com/attachments/777609425534976020/1088825888205967440/20220819_103235.gif"
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        view = discord.ui.View()
        button = discord.ui.Button(label="продолжить")
        view.add_item(button)
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        embed = discord.Embed(title=user.name, description="Ваш профиль",
                              color=discord.Colour.random())
        embed.set_thumbnail(url=user.avatar_link)
        await ctx.response.send_message(view=view, embed=embed)


async def setup(bot):
    await bot.add_cog(RPG(bot), guilds=[discord.Object(id=806157869040140288)])
    #await bot.add_cog(RPG(bot))
