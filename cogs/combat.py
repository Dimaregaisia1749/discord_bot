import discord
from discord.ext import commands
from discord import app_commands
from data.users import User
from data import db_session
from asyncio import sleep
from random import randint

class Zone():
    def __init__(self, name, lvl, reward_exp, reward_coins, damage, armor, max_hp, punishment, command):
        self.name = name
        self.lvl = lvl
        self.reward_exp = reward_exp
        self.reward_coins = reward_coins
        self.damage = damage
        self.armor = armor
        self.max_hp = max_hp
        self.punishment = punishment
        self.command = command

class CombatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.zones = [Zone(name="⛪️Деревня", lvl=0, reward_exp=50, reward_coins=4,
                           damage=5, armor=0, max_hp=100, punishment=0, command="village"),
                      Zone(name="🏜Пустыня", lvl=10, reward_exp=150, reward_coins=15,
                           damage=30, armor=5, max_hp=500, punishment=10, command="desert"),
                      Zone(name="🗻Горы", lvl=100, reward_exp=500, reward_coins=50,
                           damage=120, armor=75, max_hp=1000, punishment=100, command="mountains")]

    @app_commands.command(name='areas', description='Вывести все зоны')
    async def areas(self, ctx: discord.Interaction):
        embeds = []
        for i in self.zones:
            embed = discord.Embed(title=i.name,
                                 color=discord.Colour.random())
            lines = {"🔒Необходимый уровень:": i.lvl,
                     "⭐Награды опыта:": i.reward_exp,
                     "📀Награды монет:": i.reward_coins,
                     "💪Атака противника:": i.damage,
                     "🔰Броня противника:": i.armor,
                     "💗Хп противника:": i.max_hp,
                     "🚫Наказание в монетах за проигрыш:": i.punishment,
                     "⚫Команда:": i.command}
            for i in lines:
                embed.add_field(name=i, value=lines[i])
            embeds.append(embed)

        await ctx.response.send_message(embeds=embeds)
    
    @app_commands.command(name='fight', description='Сразиться с противниками')
    @app_commands.describe(location_name="Команда локации")
    async def fight(self, ctx: discord.Interaction, location_name: str):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.user_id == ctx.user.id).first()
        if user:
            if location_name in [i.command for i in self.zones]:
                for i in [i for i in self.zones]:
                    if i.command == location_name:
                        location = i
                        break
                embed = discord.Embed(title=f"{user.name} in {location_name}",
                                    color=discord.Colour.red())
                user_hp = f"💗Хп: {user.max_hp} / {user.max_hp}"
                user_dmg = f"💪Базовый урон: {user.base_damage}"
                user_crit = f"💢Шанс крита: {user.crit_chance}"
                user_crit_chance = f"💥Крит урон: {user.crit_damage}"
                user_armor = f"🔰Броня: {user.armor}"
                reward = f"Награда: {location.reward_coins}📀, {location.reward_exp}⭐"
                enemy_hp = f"💗Хп: {location.max_hp} / {location.max_hp}"
                enemy_dmg = f"💪Базовый урон: {location.damage}"
                enemy_armor = f"🔰Броня: {location.armor}"
                first_list = [user_hp, user_dmg, user_crit,
                              user_crit_chance, user_armor, reward]
                second_list = [enemy_hp, enemy_dmg, enemy_armor]
                embed.add_field(name="Твои характеристики", value='\n'.join(
                    first_list), inline=True)
                embed.add_field(name="Характеристики противника", value='\n'.join(
                    second_list), inline=True)
                embed.set_thumbnail(
                    url="https://tenor.com/view/binguscombat-bingus-gif-26533508")
                await ctx.response.send_message(embed=embed)
                message = await ctx.channel.fetch_message(ctx.channel.last_message_id)
                damage_to_user = 0
                damage_to_enemy = 0
                damage_log = ["", ""]
                while (user.max_hp - damage_to_user) >= 0 and (location.max_hp - damage_to_enemy) > 0:
                    await sleep(2)
                    if randint(0, 100) <= user.crit_chance:
                        damage = int(user.base_damage * user.crit_damage / 100) - location.armor
                    else:
                        damage = user.base_damage
                    damage_log[0] = f"🔵{user.name} нанес урон({damage})"
                    damage = location.damage - user.armor
                    damage_to_user += damage
                    damage_log[1] = f"🔴Противник нанес урон({damage})"
                    await ctx.channel.send('\n'.join(damage_log))
                    embed = discord.Embed(title=f"{user.name} in {location_name}",
                                          color=discord.Colour.red())
                    user_hp = f"💗Хп: {max((user.max_hp - damage_to_user), 0)} / {user.max_hp}"
                    user_dmg = f"💪Базовый урон: {user.base_damage}"
                    user_crit = f"💢Шанс крита: {user.crit_chance}%"
                    user_crit_chance = f"💥Крит урон: {user.crit_damage}%"
                    user_armor = f"🔰Броня: {user.armor}"
                    reward = f"Награда: {location.reward_coins}📀, {location.reward_exp}⭐"
                    enemy_hp = f"💗Хп: {max((location.max_hp - damage_to_enemy), 0)} / {location.max_hp}"
                    enemy_dmg = f"💪Базовый урон: {location.damage}"
                    enemy_armor = f"🔰Броня: {location.armor}"
                    first_list = [user_hp, user_dmg, user_crit,
                                user_crit_chance, user_armor, reward]
                    second_list = [enemy_hp, enemy_dmg, enemy_armor]
                    embed.add_field(name="Твои характеристики", value='\n'.join(
                        first_list), inline=True)
                    embed.add_field(name="Характеристики противника", value='\n'.join(
                        second_list), inline=True)
                    embed.set_thumbnail(
                        url="https://media.discordapp.net/attachments/708047219093143752/1063168058539114546/Rasstrel.gif")
                    await message.edit(embed=embed)
                if (user.max_hp - damage_to_user) >= 0:
                    await ctx.channel.send(f"{user.name} победил и получил {location.reward_coins}📀, {location.reward_exp}⭐")
                    await ctx.channel.send("https://media.discordapp.net/attachments/806157869040140290/1096470872501539047/ezgif-3-9a2abc027f.gif")
                    user.coins += location.reward_coins
                    user.expirience += location.reward_exp
                else:
                    await ctx.channel.send(f"{user.name} проиграл и потерял {location.punishment}📀")
                    await ctx.channel.send("https://media.discordapp.net/attachments/806157869040140290/1096470852398239835/ezgif-3-2a0fc07043.gif")
                    user.expirience -= location.punishment
                user.base_damage = 10 + await lvl_write(user.expirience) * 2
                user.max_hp = 100 + await lvl_write(user.expirience) * 20
                db_sess.commit()
            else:
                await ctx.response.send_message(content="Такой локации не существует, вызовите areas чтобы просмотреть все локации")
        else:
            await ctx.response.send_message(content="Аккаунта не существует")
    



async def setup(bot):
    await bot.add_cog(CombatCommands(bot), guilds=[discord.Object(id=806157869040140288)])
    #await bot.add_cog(BaseCommands(bot))


async def lvl_write(exp):
    exp_list = [i * 75 + 50 for i in range(100)]
    for i in range(len(exp_list)):
        if exp < exp_list[i]:
            return i
    return len(exp_list)
