import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from modules.bot_functions import *
from modules.chat_effects import *


class Account(commands.Cog):
    """
    Commands : 
    - start
    - delete_account
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
            inventories[str(ctx.author.id)] = {"balance": 0,
                                               "items": [],
                                               "packs": {},
                                               "powers": [],
                                               "shares":{},
                                               "shield_active": False}
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

            embed = discord.Embed(color=default_color)
            embed.set_author(name="🚩 Inscription")
            embed.add_field(name="Start", value=f"{ctx.author.mention}, votre compte a été créer !")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await gen_error("account_existing", ctx)

    
    @commands.command(aliases=["delete account", "ragequit"])
    async def delete_account(self, ctx):
        """Delete the author's account"""
        confirmation_text = "Vous êtes sur le point de supprimer définitivement votre         \
                            compte de jeu. Vos items, packs, actions et power-ups seront      \
                            également définitivement supprimés. Vous ne serez jamais          \
                            remboursé et vos possessions ne seront pas réstaurées.\n          \
                            Confirmez cette action en ajoutant une réction "


        embed = discord.Embed(color=warning_color)
        embed.set_author(name="🗑️ Supprimer son compte")
        embed.add_field(name="Confirmation", value=confirmation_text)
        embed = set_footer(embed)
        confirmation = await ctx.send(embed=embed)

        await confirmation.add_reaction("✅")

        check = lambda reaction, user: reaction.emoji == "✅" and user.id == ctx.author.id

        try:
            reaction = await self.bot.wait_for("reaction", check=check, timeout=10.0)
        
        except asyncio.TimeoutError:
            pass




def setup(client):
    client.add_cog(Account(client))
