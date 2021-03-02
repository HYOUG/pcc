import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from modules.bot_functions import *
from modules.chat_effects import *
from time import time


class Trades(commands.Cog):
    """
    Commands :
    - trade
    - give
    - pay
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trade(self, ctx, target: discord.Member):
        """Initiate a trade with the specified target"""
        if is_registered(target.id):
            if target.id != ctx.author.id:
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"💱 Échange entre {ctx.author.name} et {target.name}")
                embed.add_field(name="Initialisation", value=f"Vous avez initialisé un échange avec {target.mention} avec succès")
                embed.add_field(name="📥 IN - Items que vous receverez", value="`Vide`", inline=False)
                embed.add_field(name=f"📤 OUT - Items que {target.name} recevera", value="`Vide`", inline=False)
                embed = set_footer(embed, ctx)
                trade = await ctx.send(embed=embed)

                await trade.add_reaction("✅")
                await trade.add_reaction("❌")

                trade_finished = False
                trade_canceled = False
                trade_start = time()
                in_list = []
                out_list = []
                inventories = get_file("inventories")
                check_input = lambda message: message.content.split(" ")[0] in ["+in", "-in", "+out", "-out"]
                check_react = lambda reaction, user: user.id in [ctx.author.id, target.id] and reaction.emoji in ["✅", "❌"]

                while not trade_finished:
                    try:
                        new_input = await self.bot.wait_for("message", check=check_input, timeout=2.0)
                        await new_input.add_reaction("✅")
                        await new_input.delete(delay=1.0)

                        if new_input.content.startswith("+in"):
                            for new_item in new_input.content.split(" ")[1:]:
                                item_id, item_float = new_item.split(":")
                                for item in inventories[str(target.id)]["items"]:
                                    if item_id == item["id"] and float(item_float) == float(item["float"]):
                                        item_transfer = inventories[str(target.id)]["items"].pop(inventories[str(target.id)]["items"].index(item))
                                        inventories[str(ctx.author.id)]["items"].append(item_transfer)
                                        in_list.append(new_item)

                        elif new_input.content.startswith("-in"):
                            for new_item in new_input.content.split(" ")[1:]:
                                item_id, item_float = new_item.split(":")
                                for item in inventories[str(ctx.author.id)]["items"]:
                                    if item_id == item["id"] and float(item_float) == float(item["float"]):
                                        item_transfer = inventories[str(ctx.author.id)]["items"].pop(inventories[str(ctx.author.id)]["items"].index(item))
                                        inventories[str(target.id)]["items"].append(item_transfer)
                                        in_list.remove(new_item)
                                

                        elif new_input.content.startswith("+out"):
                            for new_item in new_input.content.split(" ")[1:]:
                                item_id, item_float = new_item.split(":")
                                for item in inventories[str(ctx.author.id)]["items"]:
                                    if item_id == item["id"] and float(item_float) == float(item["float"]):
                                        item_transfer = inventories[str(ctx.author.id)]["items"].pop(inventories[str(ctx.author.id)]["items"].index(item))
                                        inventories[str(target.id)]["items"].append(item_transfer)
                                        out_list.append(new_item)

                        elif new_input.content.startswith("-out"):
                            for new_item in new_input.content.split(" ")[1:]:
                                item_id, item_float = new_item.split(":")
                                for item in inventories[str(target.id)]["items"]:
                                    if item_id == item["id"] and float(item_float) == float(item["float"]):
                                        item_transfer = inventories[str(target.id)]["items"].pop(inventories[str(target.id)]["items"].index(item))
                                        inventories[str(ctx.author.id)]["items"].append(item_transfer)
                                        out_list.remove(new_item)


                        if len(in_list) == 0:
                            in_field = "`Vide`"
                        elif len(in_list) == 1:
                            in_field = f"`{in_list[0]}`"
                        elif len(in_list) >= 2:
                            in_field = "`" + "`, `".join(in_list) + "`"
                    
                        if len(out_list) == 0:
                            out_field = "`Vide`"
                        elif len(out_list) == 1:
                            out_field = f"`{out_list[0]}`"
                        elif len(out_list) >= 2:
                            out_field = "`" + "`, `".join(out_list) + "`"

                        embed.remove_field(2)
                        embed.remove_field(1)
                        embed.add_field(name="📥 IN - Items que vous receverez", value=in_field, inline=False)
                        embed.add_field(name=f"📤 OUT - Items que {target.name} recevera", value=out_field, inline=False)
                        await trade.edit(embed=embed)

                    except asyncio.TimeoutError:
                        pass

                    trade_reactions = get(self.bot.cached_messages, id=trade.id).reactions
                    for reaction in trade_reactions:
                        async for reaction_author in reaction.users():
                            if reaction.emoji == "✅" and reaction_author == ctx.author:
                                trade_finished = True
                            if reaction.emoji == "❌" and reaction_author == ctx.author:
                                trade_finished = True
                                trade_canceled = True

                    if time() >= trade_start + 60:
                        trade_finished = True
                        trade_canceled = True

                if not trade_canceled:
                    author_confirmed = False
                    trader_confirmed = False
                    confirmation_finished = False
                    confimation_canceled = False
                    confimation_start = time()

                    for reaction in get(self.bot.cached_messages, id=trade.id).reactions:
                        async for reaction_author in reaction.users():
                            await reaction.remove(reaction_author)

                    await trade.add_reaction("✅")
                    await trade.add_reaction("❌")
                    
                    embed.add_field(name="Confirmation", value=f"{target.mention} et {ctx.author.mention} confirmez l'échange avec :white_check_mark: (60 sec.)")
                    await trade.edit(embed=embed)

                    while not confirmation_finished:
                        try:
                            new_reaction, reaction_author = await self.bot.wait_for("reaction_add", check=check_react, timeout=2.0)

                            if new_reaction.emoji == "✅":
                                if reaction_author.id == ctx.author.id:
                                    author_confirmed = True
                                elif reaction_author.id == target.id:
                                    trader_confirmed = True
                                if author_confirmed and trader_confirmed:
                                    confirmation_finished = True

                            elif new_reaction.emoji == "❌":
                                confimation_canceled = True

                        except asyncio.TimeoutError:
                            pass

                        if time() >= confimation_start + 60:
                            confirmation_finished = True
                            confimation_canceled = True

                    if not confimation_canceled:
                        update_file("inventories", inventories)
                        embed.clear_fields()
                        embed.add_field(name="Conclusion", value=f"L'échange a été effectué :\nVous avez reçu : {in_field}\n{target.mention} a reçu : {out_field}")
                        await trade.edit(embed=embed)

                    elif confimation_canceled:
                        await trade.edit(embed=gen_error("trade_canceled", ctx))
                elif trade_canceled:
                    await trade.edit(embed=gen_error("trade_canceled", ctx))
            else:
                await gen_error("self_trade", ctx)
        else:
            await gen_error("missing_player", ctx)


    @commands.command()
    async def give(self, ctx, target: discord.Member, item_id: str, item_float: float):
        """Give the specified item to the specified user"""
        if is_registered(target.id):
            inventories = get_file("inventories")
            item_found = False
            for item in inventories[str(target.id)]["items"]:
                if item["id"] == item_id and item["float"] == item_float:
                    item_found = True
                    inventories[str(ctx.author.id)]["items"].append(item)
                    inventories[str(target.id)]["items"].remove(item)
                    break
            if item_found:
                embed = discord.Embed(color=default_color)
                embed.set_author(name="🎁 Don")
                embed.add_field(name="Transaction", value=f"{ctx.author.mention}, vous avez donné `{item_id}:{item_float}` à {target.mention}")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_item", ctx)
        else:
            await gen_error("missing_player", ctx)


    @commands.command()
    async def pay(self, ctx, target: discord.Member, pay_sum: int):
        """Give to the specified user the specified sum of PO"""
        if is_registered(ctx.author.id) and is_registered(target.id):
            if target.id != ctx.author.id:
                try:
                    pay_sum = int(pay_sum)
                    if pay_sum > 0:
                        inventories = get_file("inventories")
                        if inventories[str(ctx.author.id)]["balance"] >= pay_sum:

                            inventories[str(ctx.author.id)]["balance"] -= pay_sum
                            inventories[str(target.id)]["balance"] += pay_sum
                            update_file("inventories", inventories)

                            embed = discord.Embed(color=default_color)
                            embed.set_author(name=f"💳 Paiement | {ctx.author.name} to {target.name}")
                            embed.add_field(name="Transaction",
                                            value=f"{ctx.author.mention} : -`{pay_sum}` ({inventories[str(ctx.author.id)]['balance']})\n"
                                                  f"{target.mention} : +`{pay_sum}` ({inventories[str(target.id)]['balance']})")
                            embed = set_footer(embed, ctx)
                            await ctx.send(embed=embed)
                        else:
                            await gen_error("missin_money", ctx)
                    else:
                        await gen_error("incorrect_value", ctx)
                except ValueError:
                    await gen_error("incorrect_value", ctx)
            else:
                await gen_error("self_trade", ctx)
        else:
            await gen_error("missing_account", ctx)


def setup(client):
    client.add_cog(Trades(client))
