import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
import matplotlib.pyplot as plt
from discord.ext import commands


class Stocks(commands.Cog):
    """
    Commands : 
    - chart
    - stocks
    - invest
    - cashout
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["charts"])
    async def chart(self, ctx, share: str = "*"):
        """Display the specified share's chart specified or all of them"""
        stocks = get_file("stocks")
        embed = discord.Embed(color=default_color)

        if share in stocks.keys or share == "*":
            if share in stocks:
                plt.plot(range(20), stocks[share])
                embed.set_author(name=f"📈 Courbe : {share}")
                embed.add_field(name="Valeur", value=f"**{share}** : `{stocks[share][-1]}`")

            elif share == "*":
                values_field = ""
                for share_key in stocks:
                    plt.plot(range(20), stocks[share_key])
                    values_field += f"**{share_key}** : `{stocks[share_key][-1]}` PO\n"
                embed.set_author(name=f"📈 Courbes")
                embed.add_field(name="Valeurs", value=values_field)

            plt.grid(True)
            plt.ylabel("valeur (PO)")
            plt.savefig("./assets/chart.png")

            chart = discord.File("assets/chart.png", filename=f"chart.png")
            embed.set_image(url="attachment://chart.png")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed, file=chart)
            plt.clf()
        else:
            await gen_error("invalid_synthax", ctx)

        
    @commands.command(aliases=["shares"])
    async def stocks(self, ctx):
        """List of all of the stocks avaibles"""
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
    async def invest(self, ctx, share: str = "or", qtty: int = 1):
        """Buy the speficied quantity of the specified share"""
        stocks = get_file("stocks")
        if share in stocks:
            if 1 <= qtty <= 1000:
                inventories = get_file("inventories")
                if inventories[str(ctx.author.id)]["balance"] >= qtty * (stocks[share][-1] * 1.05):
                    inventories[str(ctx.author.id)]["balance"] -= qtty * (stocks[share][-1] * 1.05)
                    if share in inventories[str(ctx.author.id)]["shares"]:
                        inventories[str(ctx.author.id)]["shares"][share] += qtty
                    else:
                        inventories[str(ctx.author.id)]["shares"][share] = qtty
                    update_file("stocks", stocks)
                    update_file("inventories", inventories)

                    embed = discord.Embed(color=default_color)
                    embed.set_author(name="📈 Investissement")
                    embed.add_field(name="Achat", value=f"Vous avez acheté `{qtty}` action(s) `{share}`")
                    embed = set_footer(embed, ctx)
                    await ctx.send(embed=embed)
                else:
                    await gen_error("missing_money", ctx)
            else:
                await gen_error("invalid_synthax", ctx)
        else:
            await gen_error("invalid_synthax", ctx)

    
    @commands.command()
    async def cashout(self, ctx, share: str = "or", qtty: int = 1):
        """Sell back the specified quantity of the specified share"""
        inventories = get_file("inventories")
        if share in inventories[str(ctx.author.id)]["shares"]:
            if qtty <= inventories[str(ctx.author.id)]["shares"][share]:
                stocks = get_file("stocks")
                inventories[str(ctx.author.id)]["shares"][share] -= qtty
                inventories[str(ctx.author.id)]["balance"] += qtty * stocks[share][-1]
                if inventories[str(ctx.author.id)]["shares"][share] == 0:
                   del inventories[str(ctx.author.id)]["shares"][share]
                update_file("inventories", inventories)

                embed = discord.Embed(color=default_color)
                embed.set_author(name="📈 Retrait")
                embed.add_field(name="Vente",
                                value=f"Vous avez vendu `{qtty}` action(s) `{share}` pour `{qtty * stocks[share][-1]}` (pièces d'or)")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("incorrect_value", ctx)
        else:
            await gen_error("missing_share", ctx)


def setup(client):
    client.add_cog(Stocks(client))
