import discord
from os import system
from discord.ext import commands
from botFunctions import *
from chatEffects import *
from json import dumps


class Admin(commands.Cog):
    """Commands : admin_off, admin_reboot, admin_reload_cog, admin_give, admin_remove, admin_reset, admin_add_item, admin_skip"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["=off", "=shutdown"])
    @commands.check(is_bot_owner)
    async def admin_off(self, ctx):
        """Shutdown the bot"""
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🛑 Extinction", value=f"{ctx.author.mention}, Pop culture Collectibles va bientôt se déconnecter !")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        await self.bot.logout()                                                     # logout the bot
        print("-"*85)                                                               # log system
        print(red("Pop culture Collectibles se deconnecte..."))                     # //
        print("-"*85 + "\n")                                                        # //


    @commands.command(aliases = ["=reboot", "=reload"])
    @commands.check(is_bot_owner)
    async def admin_reboot(self, ctx):
        """Reboot the bot"""
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔁 Reboot", value=f"{ctx.author.mention}, Pop culture Collectibles va bientôt se reboot !")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        print("-"*85)                                                               # log system
        print(red("Pop culture Collectibles se relance..."))                        # //
        print("-"*85 + "\n")                                                        # //
        system("python main.py")                                                    # re-launching the main script


    @commands.command(aliases = ["=reloadcog"])
    @commands.check(is_bot_owner)
    async def admin_reload_cog(self, ctx, cog_name: str):
        """Reload the specified cog"""
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔁 Reloading cog", value=f"{ctx.author.mention}, le cog {cog_name} va vientôt se reload")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        reload_cog(self.bot, cog_name)


    @commands.command(aliases = ["=generate", "=gen"])
    @commands.check(is_bot_owner)
    async def admin_generate(self, ctx, target: discord.Member, item_id: str, item_float: float):
        """Generate the specified item (item_id, item_float) to the given member"""
        inventories = get_file("inventories")
        items = get_file("items")

        if item_id in list(items.keys()):

            inventories[str(target.id)]["items"].append({"id": item_id, "float": item_float})
            inventories_file = open("inventories.json", "w")
            inventories_file.write(dumps(inventories, indent=3))
            inventories_file.close()

            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="➕ Give (ADMIN)", value=f"`{ctx.author.mention}, {item_id}:{item_float}` a été procuré avec succès à : {target.mention}")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=gen_error("missing_item", ctx))


    @commands.command(aliases=["=remove"])
    @commands.check(is_bot_owner)
    async def admin_remove(self, ctx, target: discord.Member, item_id: str, item_float: float):
        """Remove the specified item (item_id, item_float) to the given member"""
        inventories = get_file("inventories")
        dic_target = {"id": item_id, "float": item_float}
        try:
            inventories[str(target.id)]["items"].remove(dic_target)
            inventories_file = open("inventories.json", "w")
            inventories_file.write(dumps(inventories, indent=3))
            inventories_file.close()

            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="➖ Remove", value=f"{ctx.author.mention}, `{item_id}:{item_float}` have been removed from {target.mention}'s inventory.")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(color=error_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="➖ Remove", value=f"{ctx.author.mention}, `{item_id}:{item_float}` have not been founded in the {target.mention}'s inventory")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)


    @commands.command(aliases=["=reset"])
    @commands.check(is_bot_owner)
    async def admin_reset(self, ctx, target: discord.Member):
        """Reset the account of the given user"""
        id_key = str(target.id)

        inventories = get_file("inventories")
        cooldowns = get_file("cooldowns")
        del inventories[id_key]
        del cooldowns[id_key]
        update_file("inventories.json", inventories)
        update_file("cooldowns.json", cooldowns)

        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="♻️ Reset", value=f"{ctx.author.mention}, the profile of {target.mention} have been reset.")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["=additem"])
    @commands.check(is_bot_owner)
    async def admin_add_item(self, ctx, *item_infos: tuple):
        """Add a new item from the given item_infos"""
        items = get_file("items")
        item_infos = "".join(item_infos)
        item_id, item_name, item_from, item_desc, item_tier, item_image = item_infos.split(",")
        items[item_id] = {"name": item_name, "from": item_from, "description": item_desc, "tier": item_tier, "image": item_image}
        items_file = open("list_items.json", "w", encoding="utf-8")
        items_file.write(dumps(items, indent=3))
        items_file.close()

        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="➕ Add item", value=f"{ctx.author.mention}, item **{item_name}** ({item_id}) added !")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["=skip"])
    @commands.check(is_bot_owner)
    async def admin_skip(self, ctx, target: discord.Member, category: str):
        """Skip the target's category cooldown"""
        cooldowns = get_file("cooldowns")

        if category in list(cooldowns[str(target.id)].keys()):
            cooldowns[str(target.id)][target] = 0
            update_file("cooldowns.json", cooldowns)
            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="⏩ Cooldown skip", value=f"{ctx.author.mention}, le cooldown `{category}` de {target.mention} a été réinitialisé")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))



def setup(client):
    client.add_cog(Admin(client))
