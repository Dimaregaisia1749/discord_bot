import discord
from discord.ext import commands
from discord import app_commands
from discord.ui.view import View
from discord.app_commands import Choice
import random
from data.users import User
from data import db_session


class BaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='start', description='Начать путешествие')
    @app_commands.describe(nickname="Никнейм")
    async def start(self, ctx: discord.Interaction, nickname: str):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        if user == None:
            user = User()
            user.name = nickname
            user.user_id = ctx.user.id
            user.avatar_link = "https://cdn.discordapp.com/attachments/777609425534976020/1088825888205967440/20220819_103235.gif"
            user.expirience = 0
            user.coins = 0
            user.tesseracts = 0
            user.rank = "None"
            db_sess.add(user)
            db_sess.commit()
            await ctx.response.send_message(content="Профиль успешно создан✅")
        else:
            await ctx.response.send_message(content="Профиль уже создан")

    @app_commands.command(name='change_avatar', description='Изменить аватарку профиля')
    @app_commands.describe(link="Ссылка на пнг/гиф")
    async def change_avatar(self, ctx: discord.Interaction, link: str):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        if user:
            user.avatar_link = link
            db_sess.commit()
            await ctx.response.send_message(content="Автарка изменена")
        else:
            await ctx.response.send_message(content="Профиля не существует⛔, создайте его с помощью команды /start")

    @app_commands.command(name='help', description='Справка по командам')
    async def help(self, ctx: discord.Interaction):
        base = discord.Embed(title="Базовые комады",
                             color=discord.Colour.random())
        base_commands = {"/start": "Создать профиль",
                         "/change_avatar": "Изменить аватар профиля",
                         "/change_name": "Изменить имя профиля",
                         "/del_acc": "Удалить профиль",
                         "/info": "Вывести сведения о профиле",
                         "/start": "Создать профиль"}
        combat = discord.Embed(title="Команды сражений",
                               color=discord.Colour.random())
        combat_commands = {"/start": "Создать профиль",
                           "/change_avatar": "Измнить аватар профиля",
                           "/del_acc": "Удалить профиль",
                           "/info": "Вывести сведения о профиле",
                           "/start": "Создать профиль"}
        economy = discord.Embed(title="Команды экономики",
                                color=discord.Colour.random())
        economy_commands = {"/start": "Создать профиль",
                            "/change_avatar": "Измнить аватар профиля",
                            "/del_acc": "Удалить профиль",
                            "/info": "Вывести сведения о профиле",
                            "/start": "Создать профиль"}
        for i in base_commands:
            base.add_field(name=i, value=base_commands[i])
        for i in combat_commands:
            combat.add_field(name=i, value=combat_commands[i])
        for i in economy_commands:
            economy.add_field(name=i, value=economy_commands[i])
        embed_list = [base, combat, economy]
        await ctx.response.send_message(embeds=embed_list)

    @app_commands.command(name='leader_table', description='Таблица лидеров')
    async def leader_table(self, ctx: discord.Interaction):
        db_sess = db_session.create_session()
        users = db_sess.query(User).order_by(User.expirience).all()[::-1]
        embed = discord.Embed(title="💣Таблица лидеров💣", description="Лучшие игроки по опыту",
                              color=discord.Colour.random())
        for i in range(len(users)):
            if i < 3:
                number = str(i + 1) + (3 - i) * '😈'
            else:
                number = str(i + 1)
            embed.add_field(name=f"{number}: {users[i].name} : {users[i].expirience} опыта", value="", inline=False)
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name='exp_plus', description='Добавить опыт')
    @app_commands.describe(exp="Експа")
    async def exp_plus(self, ctx: discord.Interaction, exp: int):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        user.expirience += exp
        db_sess.commit()
        if user:
            await ctx.response.send_message(content=f"Добавлено {exp} опыта")

    @app_commands.command(name='del_acc', description='БЕЗВОЗРАТНОЕ УДАЛЕНИЕ АККАУНТА❌❌❌')
    async def del_acc(self, ctx: discord.Interaction):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        if user:
            db_sess.delete(user)
            db_sess.commit()
            await ctx.response.send_message(content="Аккаунт успешно удален")
        else:
            await ctx.response.send_message(content="Аккаунта не существует")
    
    @app_commands.command(name='change_name', description='Изменение имени')
    @app_commands.describe(nickname="Новое имя")
    async def change_name(self, ctx: discord.Interaction, nickname: str):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        if user:
            user.name = nickname
            db_sess.commit()
            await ctx.response.send_message(content="Имя изменено")
        else:
            await ctx.response.send_message(content="Аккаунта не существует")

    @app_commands.command(name='info', description='Информация о профиле')
    async def player_info(self, ctx: discord.Interaction):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        if user:
            embed = discord.Embed(title=user.name, description="Ваш профиль",
                                  color=discord.Colour.blurple())
            exp = f"⭐Опыт: {await exp_write(user.expirience)}"
            lvl = f"📍Уровень: {await lvl_write(user.expirience)}"
            coins = f"📀Монеты: {user.coins}"
            tesseracts = f"🔳Тессеракты: {user.tesseracts}"
            first_list = [exp, lvl]
            second_list = [" ", coins, tesseracts]
            embed.add_field(name="Статы📊", value='\n'.join(
                first_list), inline=True)
            embed.add_field(name="", value='\n'.join(
                second_list), inline=True)
            embed.set_thumbnail(url=user.avatar_link)
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.response.send_message(content="Профиля не существует⛔, создайте его с помощью команды /start")


async def lvl_write(exp):
    exp_list = [i * 50 + 100 for i in range(100)]
    for i in range(len(exp_list)):
        if exp < exp_list[i]:
            return i
    return len(exp_list)


async def exp_write(exp):
    exp_list = [i * 50 + 100 for i in range(100)]
    for i in range(len(exp_list)):
        if exp < exp_list[i]:
            return f"{exp}/{exp_list[i]}"
    return f"{exp}/∞"


async def setup(bot):
    await bot.add_cog(BaseCommands(bot), guilds=[discord.Object(id=806157869040140288)])
    #await bot.add_cog(BaseCommands(bot))
