import discord
import asyncio
from discord.ext import commands
from botFunctions import *
from chatEffects import *


class Market(commands.Cog):
    """Commands : market, buy, sell, remove_offer"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def market(self, ctx):
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
        embed.set_author(name=f"⚖️ Market")
        embed.add_field(name="Item (ID)", value=item_field)
        embed.add_field(name="Float • Tier", value=float_field)
        embed.add_field(name="Price • Seller", value=price_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command()
    async def buy(self, ctx, offer_num: int):
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
                    embed.set_author(name=f"⚖️ Buy")
                    embed.add_field(name="Success",
                                    value=f":white_check_mark: {ctx.author.mention}, you successfully bought **{items[item_bought['id']]['name']}** (`{item_bought['id']}`) : __{items[item_bought['id']]['tier']}__ for `{price}` PO (pièces d'or)")
                    embed = set_footer(embed, ctx)
                    await ctx.send(embed=embed)

                    embed = discord.Embed(color=default_color)
                    embed.set_author(name=f"📯 Notification")
                    embed.add_field(name="Success",
                                    value=f":white_check_mark: {seller.mention}, you successfully sold **{items[item_bought['id']]['name']}** (`{item_bought['id']}`) to {ctx.author.mention} for `{price}` PO (pièces d'or)")
                    embed.set_footer(icon_url=seller.avatar_url, text=f"{seller} • {get_time()}")
                    await seller.send(embed=embed)

                    update_file("inventories.json", inventories)
                    update_file("market.json", market)

                else:
                    await ctx.send(embed=gen_error("missing_money", ctx))
            else:
                await ctx.send(embed=gen_error("self_trade", ctx))
        else:
            await ctx.send(embed=gen_error("incorrect_value", ctx))


    @commands.command()
    async def sell(self, ctx, item_id: str, item_float: float, price: int):
        offer_ended = False

        def check_market(reaction, user):
            return user.id == ctx.author.id and reaction.emoji in ["✅", "❌"]

        id_key = str(ctx.author.id)
        inventories = get_file("inventories")
        items = get_file("items")
        tier_points, multiplicator = get_points(items[item_id]["tier"][0], float(item_float))
        target_dic = {"id": item_id, "float": float(item_float), "points": tier_points * multiplicator}

        if target_dic in inventories[id_key]["items"]:
            if 0 < price < 1000000000:

                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"⚖️ Sell")
                embed.add_field(name="Offer",
                                value=f"`{item_id}:{item_float}` for `{price}` PO (pièces d'or)")
                embed.add_field(name="Confirmation",
                                value=f"{ctx.author.mention}, confirm your offer with :white_check_mark: or cancel it with :x:",
                                inline=False)
                embed = set_footer(embed, ctx)
                confirmation = await ctx.send(embed=embed)

                await confirmation.add_reaction("✅")
                await confirmation.add_reaction("❌")

                try:
                    await self.bot.wait_for("reaction_add", check=check_market, timeout=30.0)
                    updt_confirmation = self.bot.get(self.bot.cached_messages, id=confirmation.id)

                    for reaction in updt_confirmation.reactions:
                        async for reaction_user in reaction.users():
                            if reaction.emoji == "❌" and reaction_user.id == ctx.author.id:
                                cancel = discord.Embed(color=0xE62020)
                                cancel.set_author(name=f"⚖️ Market add")
                                cancel.add_field(name="Cancelled", value=f":x: {ctx.author.mention}, the trade have been cancelled")
                                cancel.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name} • {get_time()}")
                                await confirmation.edit(embed=cancel)
                                offer_ended = True
                                break

                            if reaction.emoji == "✅" and reaction_user.id == ctx.author.id:
                                market = get_file("market")

                                market["offers"].append(
                                    {"seller": ctx.author.id, "id": item_id, "float": item_float,
                                     "price": price})

                                inventories[id_key]["items"].remove(target_dic)

                                market_file = open("market.json", "w")
                                inventories_file = open("inventories.json", "w")
                                market_file.write(dumps(market, indent=3))
                                inventories_file.write(dumps(inventories, indent=3))
                                market_file.close()
                                inventories_file.close()

                                success = discord.Embed(color=default_color)
                                success.set_author(name=f"⚖️ Market add")
                                success.add_field(name="Success",
                                                  value=f":white_check_mark: {ctx.author.mention}, you're offer have been created")
                                success.set_footer(icon_url=ctx.author.avatar_url,
                                                   text=f"{ctx.author.name} • {get_time()}")
                                await confirmation.edit(embed=success)
                                offer_ended = True
                                break

                        if offer_ended:
                            break

                except asyncio.TimeoutError:
                    timeout = discord.Embed(color=0xE62020)
                    timeout.set_author(name=f"⚖️ Market add")
                    timeout.add_field(name="Timeout",
                                      value=f":x: {ctx.author.mention}, the trade have been cancelled")
                    timeout.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name} • {get_time()}")
                    await confirmation.edit(embed=timeout)

            else:
                await ctx.send(embed=gen_error("incorrect_value", ctx))
        else:
            await ctx.send(embed=gen_error("missing_item", ctx))


    @commands.command()
    async def remove_offer(self, ctx, offer_num: int):
        market = get_file("market")

        if market["offers"][offer_num - 1]["seller"] == ctx.author.id:

            inventories = get_file("inventories")
            offer = market["offers"].pop(offer_num - 1)
            del offer["seller"]
            del offer["price"]
            inventories[str(ctx.author.id)]["items"] += offer

            update_file("market.json", market)
            update_file("inventories.json", inventories)

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"⚖️ Market")
            embed.add_field(name="Remove offer",
                            value=f":white_check_mark: {ctx.author.mention}, you successfully remove your offer for `{offer['id']}:{offer['float']}`.")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            ctx.send(embed=gen_error("missing_permissions", ctx))


def setup(client):
    client.add_cog(Market(client))
