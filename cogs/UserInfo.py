import discord
from botFunctions import *
from chatEffects import *
from discord.ext import commands


class UserInfo(commands.Cog):
    """Commands : inventory, balance, points"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, target=None):
        """Display the target's inventory (the author if target is not specified)"""
        target_found, target = await target_parser(ctx, target)

        if target_found:
            if is_registered(target.id):

                inventories = get_file("inventories")
                items       = get_file("items")
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"📦 {target.name}'s Inventory")

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
                    embed.add_field(name = "Inventory",      value="`You have no items`", inline=False)

                if inventories[str(target.id)]["powers"]:
                    powers = get_file("powers")
                    powers_column = ""
                    for power in inventories[str(target.id)]["powers"]:
                        powers_column += f"• **{powers[power]['name']}** `{power}`\n"
                    embed.add_field(name="Power-Ups", value=powers_column, inline=False)
                else:
                    embed.add_field(name="Power-Ups", value="`You have no power-ups`", inline=False)

                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)

            else:
                await ctx.send(embed=gen_error("missing_player", ctx))
        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))


    @commands.command(aliases=["bal"])
    async def balance(self, ctx, target=None):
        """Display the target's balance (the author if target is not specified)"""
        target_found, target = await target_parser(ctx, target)

        if target_found:
            if is_registered(target.id):

                inventories = get_file("inventories")
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"💰 {target.name}'s Balance")
                embed.add_field(name="Bourse", value=f"`{inventories[str(target.id)]['balance']}` **PO** (pièces d'or)")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)

            else:
                await ctx.send(embed=gen_error("missing_player", ctx))
        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))
            

    @commands.command(aliases=["pts"])
    async def points(self, ctx, target=None):
        """Display the target's points (the author if target is not specified)"""
        target_found, target = await target_parser(ctx, target)

        if target_found:
            if is_registered(target.id):

                inventories = get_file("inventories")
                player_points = 0
                for item in inventories[str(ctx.author.id)]["items"]:
                    player_points += item["points"]
                embed = discord.Embed(color=default_color)
                embed.set_author(name=f"⭐ {target.name}'s points")
                embed.add_field(name="Points", value=f"`{player_points}` points")
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)

            else:
                await ctx.send(embed=gen_error("missing_player", ctx))
        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))


def setup(client):
    client.add_cog(UserInfo(client))
