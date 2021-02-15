import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *


class UserInfo(commands.Cog):
    """
    Commands : 
    - inventory
    - balance
    - points
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, target: str = None):
        """Display the target's inventory (the author if target is not specified)"""
        target_found, target = await target_parser(ctx, target)
        if target_found:
            if is_registered(target.id):
                inventories = get_file("inventories")
                items = get_file("items")
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"📦 Inventaire de {target.name}")

                if inventories[str(target.id)]["items"]:
                    name_column  = ""
                    tier_column  = ""
                    float_column = ""

                    for item in inventories[str(target.id)]["items"]:
                        name_column += f"• **{items[item['id']]['name']}** `{item['id']}` \n"
                        tier_column += f" *{items[item['id']]['tier']}* \n"
                        showed_float = str(item["float"])
                        for i in range(5 - len(str(item["float"]))):
                            showed_float += "0"
                        float_column += f" __{showed_float}__ • **{item['points']}**\n"
                    embed.add_field(name = "Item (ID)",      value=name_column)
                    embed.add_field(name = "Tier",           value=tier_column)
                    embed.add_field(name = "Float • Points", value=float_column)
                else:
                    embed.add_field(name = "Inventory",      value="`Vous n'avez pas d'items'`", inline=False)

                if inventories[str(target.id)]["powers"]:
                    powers = get_file("powers")
                    powers_column = ""
                    for power in inventories[str(target.id)]["powers"]:
                        powers_column += f"• **{powers[power]['name']}** `{power}`\n"
                    embed.add_field(name="Power-Ups", value=powers_column, inline=False)
                else:
                    embed.add_field(name="Power-Ups", value="`Vous n'avez pas de power-ups`", inline=False)

                if inventories[str(ctx.author.id)]["shares"]:
                    share_column = ""
                    for key in inventories[str(ctx.author.id)]["shares"].keys():
                        share_column += f"• $**{key.upper()}** : `{inventories[str(ctx.author.id)]['shares'][key]}`\n"
                    embed.add_field(name="Actions", value=share_column, inline=False)
                else:
                    embed.add_field(name="Actions • Quantité", value="Vous n'avez pas d'actions")

                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_player", ctx)
        else:
            await gen_error("invalid_synthax", ctx)


    @commands.command(aliases=["bal"])
    async def balance(self, ctx, target: str = None):
        """Display the target's balance (the author if target is not specified)"""
        target_found, target = await target_parser(ctx, target)
        if target_found:
            if is_registered(target.id):
                inventories = get_file("inventories")
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"💰 Bourse de {target.name}")
                embed.add_field(name="Bourse", value=f"`{inventories[str(target.id)]['balance']}` **PO** (pièces d'or)")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_player", ctx)
        else:
            await gen_error("invalid_synthax", ctx)
            

    @commands.command(aliases=["pts", "score"])
    async def points(self, ctx, target: str = None):
        """Display the target's points (the author if target is not specified)"""
        target_found, target = await target_parser(ctx, target)
        if target_found:
            if is_registered(target.id):
                inventories = get_file("inventories")
                player_points = 0
                for item in inventories[str(ctx.author.id)]["items"]:
                    player_points += item["points"]
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"⭐ Points de {target.name}")
                embed.add_field(name="Points", value=f"`{player_points}` points")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_player", ctx)
        else:
            await gen_error("invalid_synthax", ctx)


def setup(client):
    client.add_cog(UserInfo(client))
