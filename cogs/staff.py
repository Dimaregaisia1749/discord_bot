import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import random


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gifs = [
            "https://media.discordapp.net/attachments/431125949128507403/1082724710640529489/ezgif.com-resize.gif",
            "https://media.discordapp.net/attachments/806157869040140290/1052679473641816145/bb.gif",
            "https://tenor.com/view/bonk-funny-cat-bonk-bonk-bonk-bonk-bonk-bonk-bonk-cat-funny-hammer-gif-22703304",
            "https://media.discordapp.net/attachments/708047219093143752/1068532466534592582/suetolog.gif",
            "https://media.discordapp.net/attachments/708047219093143752/1063168058539114546/Rasstrel.gif",
            "https://media.discordapp.net/attachments/708047219093143752/1049662213369106482/MOLU.gif",
            "https://cdn.discordapp.com/attachments/806157869040140290/1051131918957154344/hapi.gif",
            "https://media.discordapp.net/attachments/721328686254653460/1071117580422631494/ezgif.com-gif-maker_7.gif",
            "https://tenor.com/view/man-standing-gif-20655812",
            "https://tenor.com/view/jackpot-syava-gif-25689977",
            "https://tenor.com/view/kitty-cat-sandwich-cats-sandwich-gif-26112528",
            "https://media.discordapp.net/attachments/777609425534976020/842461023809699861/image0-7.gif",
            "https://media.discordapp.net/attachments/888409520236265514/890595554571202610/3x.gif",
            "https://media.discordapp.net/attachments/777609425534976020/1004248003546206268/image0-2-1.gif",
            "https://cdn.discordapp.com/attachments/777609425534976020/1088825888205967440/20220819_103235.gif"
            ]

    @app_commands.command(name='randint', description='Рандомное число')
    @app_commands.describe(min_int="Нижняя планка", max_int="Верхняя планка")
    async def randint(self, ctx: discord.Interaction, min_int: int, max_int: int):
        if min_int >= max_int:
            await ctx.response.send_message(f"Первое число должно быть меньше второго")
        else:
            num = random.randint(int(min_int), int(max_int))
            await ctx.response.send_message(num)
        
    @app_commands.command(name='randgif', description='Рандомная гифка')
    async def randgif(self, ctx: discord.Interaction):
        gif = self.gifs[random.randint(0, len(self.gifs) - 1)]
        await ctx.response.send_message(gif)
    
    @app_commands.command(name='delete_messages', description='Удалить последние сообщения')
    @app_commands.describe(x="Количество сообщений(максимум 10)")
    async def delete_messages(self, ctx: discord.Interaction, x: int):
        if x > 10:
            await ctx.response.send_message(f"Можно удалить максимум 10 сообщений за раз")
        else:
            await ctx.response.send_message(f"Удалено {x} сообщений")
            await ctx.channel.purge(limit=x + 1)

    @app_commands.command(name='embed')
    async def embed(self, ctx: discord.Interaction, title: str, field: str):
        embed = discord.Embed(title=title, description=field,color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/777609425534976020/1088825888205967440/20220819_103235.gif")
        await ctx.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(Staff(bot), guilds=[discord.Object(id=806157869040140288)])
    #await bot.add_cog(Staff(bot))
