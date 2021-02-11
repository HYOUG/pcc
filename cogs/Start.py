import discord
from discord.ext import commands
from bot_functions import *
from chat_effects import *


class Start(commands.Cog):
    """
    Commands : 
    - start
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        """Create the author's game account"""
        if not is_registered(ctx.author.id):

            inventories = get_file("inventories")
            cooldowns = get_file("cooldowns")
            cooldowns[str(ctx.author.id)] = {"daily": 0, "spin": 0}
            inventories[str(ctx.author.id)] = {"balance": 0, "items": [], "powers": [], "shares":{},"shield_active": False}
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"🚩 Start")
            embed.add_field(name="Start", value=f"{ctx.author.mention}, votre compte a été créer !")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=gen_error("account_existing", ctx))


def setup(client):
    client.add_cog(Start(client))
