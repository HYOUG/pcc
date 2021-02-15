import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from modules.bot_functions import *
from modules.chat_effects import *


class Market(commands.Cog):
    """
    Commands : 
    - market
    - buy
    - sell
    - remove_offer
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def market(self, ctx):
        """Display the market's offers"""
        offers = get_file("market")["offers"]
        items = get_file("items")

        item_field = ":black_small_square:\n"
        float_field = ":black_small_square:\n"
        price_field = ":black_small_square:\n"
        offer_number = 1

        if len(offers) != 0:
            for offer in offers:
                item_field += f"• [{offer_number}] **{items[str(offer['id'])]['name']}** ({offer['id']}) \n"
                float_field += f" __{offer['float']}__ • *{items[str(offer['id'])]['tier']}* \n"
                price_field += f" {offer['price']} • {self.bot.get_user(offer['seller']).mention} \n"
                offer_number += 1
        else:
            item_field += "`The market is empty`"

        embed = discord.Embed(color=default_color)
        embed.set_author(name=f"⚖️ Marché")
        embed.add_field(name="[#] Item (ID)", value=item_field)
        embed.add_field(name="Float • Tier", value=float_field)
        embed.add_field(name="Prix • Vendeur", value=price_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command()
    async def buy(self, ctx, offer_num: int = 1):
        """Buy a market's offer specified by it's name"""
        market = get_file("market")
        if offer_num % 1 == 0 and 1 <= offer_num <= (len(market["offers"])):
            if market["offers"][offer_num - 1]["seller"] != ctx.author.id:
                inventories = get_file("inventories")
                if inventories[str(ctx.author.id)]["balance"] >= market["offers"][offer_num - 1]["price"]:
                    items = get_file("items")

                    item_bought = market["offers"].pop(offer_num - 1)
                    price = item_bought["price"]
                    seller = self.bot.get_user(item_bought["seller"])
                    del item_bought["seller"]
                    del item_bought["price"]

                    inventories[str(ctx.author.id)]["items"].append(item_bought)
                    inventories[str(ctx.author.id)]["balance"] -= price
                    inventories[str(seller.id)]["balance"] += price

                    embed = discord.Embed(color=default_color)
                    embed.set_author(name=f"⚖️ Marché")
                    embed.add_field(name="Achat",
                                    value=f"{ctx.author.mention}, vous avez acheté avec succès **{items[item_bought['id']]['name']}** (`{item_bought['id']}`) pour `{price}` PO (pièces d'or) à {seller.mention}")
                    embed = set_footer(embed, ctx)
                    await ctx.send(embed=embed)

                    embed = discord.Embed(color=default_color)
                    embed.set_author(name="📯 Notification")
                    embed.add_field(name="Vente",
                                    value=f"{seller.mention}, vous avez vendu **{items[item_bought['id']]['name']}** à {ctx.author.mention} pour `{price}` PO (pièces d'or)")
                    embed = set_footer(embed, ctx)
                    await seller.send(embed=embed)

                    update_file("inventories", inventories)
                    update_file("market", market)

                else:
                    await gen_error("missing_money", ctx)
            else:
                await gen_error("self_trade", ctx)
        else:
            await gen_error("incorrect_value", ctx)


    @commands.command()
    async def sell(self, ctx, item_id: str, item_float: float, price: int):
        """Create a market's offer usin the item ID, the item float and the price"""
        offer_ended = False

        def check_market(reaction, user):
            return user.id == ctx.author.id and reaction.emoji in ["✅", "❌"]

        id_key = str(ctx.author.id)
        inventories = get_file("inventories")
        items = get_file("items")
        tier_points, multiplicator = get_points(items[item_id]["tier"][0], item_float)
        item_points = tier_points * multiplicator
        target_dic = {"id": item_id, "float": float(item_float), "points": item_points}

        if target_dic in inventories[id_key]["items"]:
            if 0 < price < 1000000000:

                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"⚖️ Marché")
                embed.add_field(name="Offre",
                                value=f"`{item_id}:{item_float}` pour `{price}` PO (pièces d'or)")
                embed.add_field(name="Confirmation",
                                value=f"{ctx.author.mention}, confirmez votre offre avec :white_check_mark: ou annulez la avec :x:",
                                inline=False)
                embed = set_footer(embed, ctx)
                confirmation = await ctx.send(embed=embed)

                await confirmation.add_reaction("✅")
                await confirmation.add_reaction("❌")

                try:
                    await self.bot.wait_for("reaction_add", check=check_market, timeout=30.0)
                    updt_confirmation = get(self.bot.cached_messages, id=confirmation.id)

                    for reaction in updt_confirmation.reactions:
                        async for reaction_user in reaction.users():
                            if reaction.emoji == "❌" and reaction_user.id == ctx.author.id:
                                await confirmation.edit(embed=gen_error("trade_canceled"))
                                offer_ended = True
                                break

                            if reaction.emoji == "✅" and reaction_user.id == ctx.author.id:
                                market = get_file("market")
                                market["offers"].append({"seller": ctx.author.id, "id": item_id, "float": item_float, "points":item_points, "price": price})
                                inventories[id_key]["items"].remove(target_dic)

                                update_file("inventories", inventories)
                                update_file("market", market)

                                success = discord.Embed(color=default_color)
                                success.set_author(name=f"⚖️ Marché")
                                success.add_field(name="Succès",
                                                  value=f"{ctx.author.mention}, votre offre a été créée")
                                success = set_footer(success, ctx)
                                await confirmation.edit(embed=success)
                                offer_ended = True
                                break

                        if offer_ended:
                            break

                except asyncio.TimeoutError:
                    await confirmation.edit(embed=gen_error("trade_canceled", ctx))
            else:
                await gen_error("incorrect_value", ctx)
        else:
            await gen_error("missing_item", ctx)


    @commands.command()
    async def remove_offer(self, ctx, offer_num: int = 1):
        """Remove one of yours market's offer"""
        market = get_file("market")

        if market["offers"][offer_num - 1]["seller"] == ctx.author.id:

            inventories = get_file("inventories")
            offer = market["offers"].pop(offer_num - 1)
            del offer["seller"]
            del offer["price"]
            inventories[str(ctx.author.id)]["items"] += offer

            update_file("market", market)
            update_file("inventories", inventories)

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"⚖️ Marché")
            embed.add_field(name="Retrait d'offre",
                            value=f"{ctx.author.mention}, vous avez retiré votre offre du marché : `{offer['id']}:{offer['float']}`.")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            gen_error("missing_permissions", ctx)


def setup(client):
    client.add_cog(Market(client))
