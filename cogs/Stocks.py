import discord
from discord.ext.commands.core import command
import matplotlib.pyplot as plt
from discord.ext import commands
from botFunctions import *
from os import getcwd
from chatEffects import *

class Stocks(commands.Cog):
    """Commands : stocks"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["charts"])
    async def chart(self, ctx, share="*"):
        stocks = get_file("stocks")
        if share in list(stocks.keys()):
            plt.plot(range(20), stocks[share])
            plt.ylabel("valeur (PO)")
            plt.savefig("./data/chart.png")
            chart = discord.File(f"data/chart.png", filename=f"chart.png")

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"📈 Courbe : {share}")
            embed.add_field(name="Valeur", value=f"**{share}** : `{stocks[share][-1]}`")
            embed.set_image(url="attachment://chart.png")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed, file=chart)
            plt.clf()

        elif share == "*":
            values_field = ""
            for share_key in list(stocks.keys()):
                plt.plot(range(20), stocks[share_key])
                values_field += f"**{share_key}** : `{stocks[share_key][-1]}` PO\n"
            plt.ylabel("valeur (PO)")
            plt.savefig("./data/chart.png")
            chart = discord.File(f"data/chart.png", filename=f"chart.png")

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"📈 Courbes")
            embed.add_field(name="Valeurs", value=values_field)
            embed.set_image(url="attachment://chart.png")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed, file=chart)
            plt.clf()

        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))

        
    @commands.command(aliases=["stocks"])
    async def shares(self, ctx):
        stocks = get_file("stocks")
        shares = list(stocks.keys())
        embed = discord.Embed(color=default_color)
        embed.set_author(name="📈 Actions")
        shares_field = ""
        for share in shares:
            shares_field += f"• **{share}** : `{stocks[share][-1]}` PO\n"
        embed.add_field(name="Actions disponibles", value=shares_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command()
    async def invest(self, ctx, share, qtty=1):
        stocks      = get_file("stocks")
        inventories = get_file("inventories")
        if share in list(stocks.keys()):
            if 1 <= qtty <= 1000:
                if inventories[str(ctx.author.id)]["balance"] >= qtty * (stocks[share][-1] * 1.05):
                    inventories[str(ctx.author.id)]["balance"] -= qtty * (stocks[share][-1] * 1.05)
                    if share in list(inventories[str(ctx.author.id)]["shares"].keys()):
                        inventories[str(ctx.author.id)]["shares"][share] += qtty
                    else:
                        inventories[str(ctx.author.id)]["shares"][share] = qtty
                    update_file("stocks.json", stocks)
                    update_file("inventories.json", inventories)
                else:
                    await ctx.send(embed=gen_error("invalid_synthax", ctx))
            else:
                await ctx.send(embed=gen_error("invalid_synthax", ctx))
        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))

def setup(client):
    client.add_cog(Stocks(client))
