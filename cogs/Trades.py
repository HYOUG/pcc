import discord
import asyncio
from discord.ext import commands
from botFunctions import *
from chatEffects import *
from time import time


class Trades(commands.Cog):
    """Commands : trade, give, pay"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trade(self, ctx, trader_2: discord.Member):
        """Initiate a trade with the specified user"""
        global last_input
        global trader_id
        global trader2_id
        trader_id = ""
        trader2_id = ""
        seller_id = ""
        trader_1 = ctx.author
        id_key_1 = str(trader_1.id)
        trader_id = id_key_1
        id_key_2 = str(trader_2.id)
        trader2_id = id_key_2
        trade_finished = False
        timeout = False
        new_valid_input = False
        cancel = False
        in_list = []
        out_list = []
        scale = {"S": 100, "A": 25, "B": 10, "C": 5, "D": 1}

        if is_registered(trader_2.id):
            if trader_2.id != ctx.author.id:

                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"Trade [{trader_1.name} ↔ {trader_2.name}]")
                embed.add_field(name="Initialisation", value=f"Vous avez initialisé un échage avec {trader_2.mention} avec succès")
                embed.add_field(name="📥 IN - Items que vous receverez", value="`Vide`", inline=False)
                embed.add_field(name=f"📤 OUT - Items que {trader_2.name} recevera", value="`Vide`", inline=False)
                embed = set_footer(embed, ctx)

                trade = await ctx.send(embed=embed)
                await trade.add_reaction("✅")
                await trade.add_reaction("❌")

                inventories = get_file("inventories")
                items = get_file("items")

                trade_start = time()

                while not trade_finished:

                    try:

                        msg = await self.bot.wait_for("message", check=check1, timeout=3.0)

                        if msg.content.startswith("+in "):
                            for item_input in msg.content.split(" ")[1:]:
                                item_dic = {"id": item_input.split(":")[0],
                                            "float": float(item_input.split(":")[1])}

                                for item in inventories[id_key_2]:
                                    if item_dic == item:
                                        inventories[id_key_1]["items"].append(inventories[id_key_2]["items"].pop(
                                            inventories[id_key_2]["items"].index(item_dic)))
                                        in_list.append(f"`{item_dic['id']}:{item_dic['float']}`")
                                        break
                            new_valid_input = True
                            await msg.add_reaction("✅")

                        elif msg.content.startswith("+out "):
                            for item_input in msg.content.split(" ")[1:]:
                                item_dic = {"id": item_input.split(":")[0],
                                            "float": float(item_input.split(":")[1])}
                                for item in inventories[id_key_1]:
                                    if item_dic == item:
                                        inventories[id_key_2]["items"].append(inventories[id_key_1]["items"].pop(
                                            inventories[id_key_1]["items"].index(item_dic)))
                                        out_list.append(f"`{item_dic['id']}:{item_dic['float']}`")
                                        break
                            new_valid_input = True
                            await msg.add_reaction("✅")

                        elif msg.content.startswith("-in "):
                            for item_input in msg.content.split(" ")[1:]:
                                try:
                                    item_dic = {"id": item_input.split(":")[0],
                                                "float": float(item_input.split(":")[1])}
                                    inventories[id_key_2]["items"].append(inventories[id_key_1]["items"].pop(
                                        inventories[id_key_1]["items"].index(item_dic)))
                                    del in_list[in_list.index(f"`{item_dic['id']}:{item_dic['float']}`")]
                                    new_valid_input = True
                                    await msg.add_reaction("✅")
                                except:
                                    await msg.add_reaction("❌")

                        elif msg.content.startswith("-out "):
                            for item_input in msg.content.split(" ")[1:]:
                                try:
                                    item_dic = {"id": item_input.split(":")[0],
                                                "float": float(item_input.split(":")[1])}
                                    inventories[id_key_1]["items"].append(inventories[id_key_2]["items"].pop(
                                        inventories[id_key_2]["items"].index(item_dic)))
                                    del out_list[in_list.index(f"`{item_dic['id']}:{item_dic['float']}`")]
                                    new_valid_input = True
                                    await msg.add_reaction("✅")
                                except:
                                    await msg.add_reaction("❌")

                        else:
                            await msg.add_reaction("❌")

                        await msg.delete(delay=1)

                    # timeout
                    except asyncio.TimeoutError:
                        new_valid_input = False
                        if time() > trade_start + 180:
                            trade_finished = True
                            timeout = True
                            embed.clear_fields()
                            embed.add_field(name="Timeout", value=":no_entry_sign: Le trade a mis trop de temps (+180 secs) pour se conclure, il a été annulé")
                            await trade.edit(embed=embed)

                    # update the trade
                    if new_valid_input == True and timeout == False:
                        new_valid_input = False
                        embed.remove_field(2)
                        embed.remove_field(1)
                        if len(in_list) >= 2:
                            in_field = ", ".join(in_list)
                        if len(out_list) >= 2:
                            out_field = ", ".join(out_list)
                        if len(in_list) == 1:
                            in_field = in_list[0]
                        if len(out_list) == 1:
                            out_field = out_list[0]
                        if len(in_list) == 0:
                            in_field = "`Vide`"
                        if len(out_list) == 0:
                            out_field = "`Vide`"
                        embed.add_field(name="📥 IN - Items que vous receverez", value=in_field, inline=False)
                        embed.add_field(name=f"📤 OUT - Items que {trader_2.name} recevera", value=out_field, inline=False)
                        await trade.edit(embed=embed)

                    # check la confirmation ou l'annulation
                    updt_trade = self.bot.get(self.bot.cached_messages, id=trade.id)

                    for reaction in updt_trade.reactions:

                        async for reaction_user in reaction.users():

                            # étape 3
                            if reaction.emoji == "✅" and str(reaction_user.id) == id_key_1 and not timeout and not cancel:

                                embed.add_field(name="Confirmation", value=f"{trader_2.mention} confirmez l'échange avec :white_check_mark: (60 sec.)")
                                await trade.edit(embed=embed)

                                # get the confirmation from the 2nd trader
                                try:
                                    await self.bot.wait_for("reaction_add", check=check2, timeout=60.0)  # final confirmation from trader n°2
                                    update_file("inventories.json", inventories)
                                    embed.clear_fields()
                                    embed.add_field(name="Conclusion", value=f":white_check_mark: L'échange a été effectué :\n{trader_1.mention} a reçu : {in_field}\n{trader_2.mention} a reçu : {out_field}")
                                    await trade.edit(embed=embed)
                                    trade_finished = True

                                # timeout
                                except asyncio.TimeoutError:
                                    timeout = True
                                    embed.clear_fields()
                                    embed.add_field(name="Timeout",
                                                    value=":no_entry_sign: Le trade a mis trop de temps (+180 secs) pour se conclure, il a été annulé")
                                    await trade.edit(embed=embed)
                                    trade_finished = True

                            if reaction.emoji == "❌" and str(
                                    reaction_user.id) == id_key_1 and not timeout and not cancel:
                                trade_finished = True
                                cancel = True
                                embed.clear_fields()
                                embed.add_field(name="Annulation",
                                                value=f":no_entry_sign: Le trade a été annulé par {trader_1.mention}")
                                await trade.edit(embed=embed)

                            if trade_finished:
                                break

                        if trade_finished:
                            break
            else:
                await ctx.send(embed=gen_error("self_trade", ctx))
        else:
            await ctx.send(embed=gen_error("missing_account", ctx))


    @commands.command()
    async def give(self, item_id: str, item_float: float):
        pass


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
                            update_file("inventories.json", inventories)

                            embed = discord.Embed(color=default_color)
                            embed.set_author(name=f"💳 Payment | {ctx.author.name} to {target.name}")
                            embed.add_field(name="Payment",
                                            value=f"{ctx.author.mention} : -`{pay_sum}` ({inventories[str(ctx.author.id)]['balance']})\n"
                                                  f"{target.mention} : +`{pay_sum}` ({inventories[str(target.id)]['balance']})")
                            embed = set_footer(embed, ctx)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(embed=gen_error("missin_money", ctx))
                    else:
                        await ctx.send(embed=gen_error("incorrect_value", ctx))
                except ValueError:
                    await ctx.send(embed=gen_error("incorrect_value", ctx))
            else:
                await ctx.send(embed=gen_error("self_trade", ctx))
        else:
            await ctx.send(embed=gen_error("missing_account", ctx))


def setup(client):
    client.add_cog(Trades(client))
