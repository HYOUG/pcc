import discord
import asyncio
from discord.ext import commands, tasks
from modules.bot_functions import *
from modules.chat_effects import *
from random import randint, choice
from os import listdir, mkdir, getcwd
from os.path import getsize
from time import strftime
from shutil import copyfile
from hurry.filesize import size
from random import randint


class Loops(commands.Cog):
    """
    Loops : 
    - calc_event
    - change_status
    - save_data
    """

    def __init__(self, bot):
        self.bot = bot
        self.calc_event.start()
        self.change_status.start()
        self.save_data.start()
        self.stocks_evolution.start()
        self.loop_num_backup = 0
        self.loop_num_stocks = 0

    @tasks.loop(minutes=20)
    async def calc_event(self):
        """'Random calculation' event"""
        if randint(1, 5) == 1:
            a = randint(-10, 10)
            b = randint(-10, 10)
            c = randint(-10, 10)
            operator_1 = choice(["+", "-", "*"])
            operator_2 = choice(["+", "-", "*"])
            calc = f"{a} {operator_1} {b} {operator_2} {c}"
            result = eval(calc)
            chosen_guild = choice(self.bot.guilds)
            chosen_channel = choice(chosen_guild.text_channels)

            embed = discord.Embed(color=admin_color)
            embed.set_author(name=f"⏱️ Random Event")
            embed.add_field(name="Challenge", value=f"Le premier à résoudre ce calcul avant 20 secondes remporte une récompense :\n```{calc} = ?```")
            embed.set_footer(text=f"Random Event • {get_time()}", icon_url=self.bot.user.avater_url)
            random_event = await chosen_channel.send(embed=embed)
            print(f"[{get_time()}] : {yellow('[EVENT]')} {blue('Random Calc Event')} : {str(calc)} = {str(result)} {red('(' + chosen_channel.name + ')')}")

            def check(msg):
                return msg.channel == chosen_channel and int(msg.content) == result and is_registered(msg.author.id)

            try:
                answer = await self.bot.wait_for("message", check=check, timeout=20.0)
            except asyncio.TimeoutError:
                embed.clear_fields()
                embed.add_field(name="Challenge", value=f"```{calc} = {result}```", inline=False)
                embed.add_field(name="Timeout", value=":x: Personne n'a répondu avant la fin du timer (20 secs.)", inline=False)
                await random_event.edit(embed=embed)
            else:
                inventories = get_file("inventories")
                powers      = get_file("powers")
                reward      = choice(list(powers.keys()))
                inventories[str(answer.author.id)]["powers"].append(reward)
                update_file("inventories", inventories)

                embed.clear_fields()
                embed.add_field(name="Challenge", value=f"```{calc} = {result}```")
                embed.add_field(name="Reward", value=f"{answer.author.mention} a remporté le power-up : `{reward}`", inline=False)
                await random_event.edit(embed=embed)


    @tasks.loop(minutes=5)
    async def change_status(self):
        """'Change status' loop"""
        movies = open("data/metadata/movies.txt", "r").read().split("\n")
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{choice(movies)} | =help")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)


    @tasks.loop(hours=2)
    async def save_data(self):
        """'Save data and create backup' loop"""
        if self.loop_num_backup > 1:
            backup_folder = strftime("%d-%m-%Y_%H.%M.%S")
            mkdir(f"backup/{backup_folder}")
            for filename in listdir("./data"):
                if filename[:-5] in ["inventories", "cooldowns", "market"]:
                    copyfile(f"data/{filename}", f"backup/{backup_folder}/{filename}")

            save_size = 0
            backup_directory_size = 0
            
            for backup_directory in listdir("./backup"):
                for file in listdir(f"./backup/{backup_directory}"):
                    file_size = getsize(f"{getcwd()}\\backup\{backup_directory}\{file}")
                    if backup_directory == backup_folder:
                        save_size += file_size
                    backup_directory_size += file_size
            print(f"[{get_time()}] : {yellow('[BACKUP]')} backup/{backup_folder} {red(f'(SIZE (in bytes) > save : {size(save_size)}o | directory : {size(backup_directory_size)}o)')}")
        self.loop_num_backup += 1


    @tasks.loop(minutes=5)
    async def stocks_evolution(self):
        """'Make the stocks evolve loop"""
        if self.loop_num_stocks > 1:
            stocks = get_file("stocks")
            evolutions = []
            for share_key in list(stocks.keys()):
                evolution = randint(-100, 100)
                evolutions.append(evolution)
                stocks[share_key].append(stocks[share_key][-1] + evolution)
                if stocks[share_key][-1] < 0:
                    stocks[share_key][-1] = 0 
                if len(stocks[share_key]) >= 20:
                    stocks[share_key] = stocks[share_key][-20:]
            update_file("stocks", stocks)
            print(f"[{get_time()}] : {yellow('[STOCKS]')}")
        self.loop_num_stocks += 1


def setup(client):
    client.add_cog(Loops(client))
