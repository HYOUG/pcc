from os import name
import discord
from discord.ext import commands
from botFunctions import *
from chatEffects import *


class GameInfo(commands.Cog):
    """Commands : help, items, powers, players, statistics, get_points"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, command: str = "*"):
        """Give a general help or a specified one"""
        if command == "*":
            help_data = get_file("help")
            target = self.bot.get_user(ctx.author.id)

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"❔ Aide")
            for help_line in help_data.keys():
                embed.add_field(name=f"🔹 {help_data[help_line]['title']}", value=help_data[help_line]["desc"], inline=False)
            embed = set_footer(embed, ctx)
            await target.send(embed=embed)

        elif command in get_commands_list():
            help_data = get_file("help")
            target = self.bot.get_user(ctx.author.id)
            commands_dict = get_commands_dict()

            embed = discord.Embed(color=default_color)
            embed.set_author(name=f"❔ Aide")
            embed.add_field(name=f"🔹 {help_data[commands_dict[command]]['title']}", value=help_data[commands_dict[command]]['desc'])
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))


    @commands.command()
    async def items(self, ctx):
        """Display the list of all game items"""
        embed = discord.Embed(color=default_color)
        embed.set_author(name=f"📜 Liste des items")
        embed.add_field(name="Informations",
                        value=f"✅ {ctx.author.mention}, la liste des items va vous être envoyée. "
                              f"La liste peut prendre du temps à se générer.\n\n"
                              f":warning: À cause de la charte graphique il se peut que certaines colonnes"
                              f"soit décalées par rapport aux autres")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)

        name_column = ""
        tier_column = ""
        from_column = ""

        items = get_file("items")
        items_keys = list(items.keys())
        item_index = 0
        page = 1
        finished = False

        embed = discord.Embed(color=default_color)
        embed.add_field(name="Nom (ID)", value="*")
        embed.add_field(name="Tier", value="*")
        embed.add_field(name="Source", value="*")

        while not finished:

            while len(embed.fields[0].value) +                                                                     \
                  len(f"{items[items_keys[item_index]]['name']} ({items_keys[item_index]})\n") <= 1024 and         \
                  len(embed.fields[1].value) + len(f"*{items[items_keys[item_index]]['tier']}*\n") <= 1024 and     \
                  len(embed.fields[2].value) + len(f"__{items[items_keys[item_index]]['from']}__\n") <= 1024:

                embed.set_author(name=f"📜 Liste des items | Page n°{page}")
                name_column += f"**{items[items_keys[item_index]]['name']}** `{items_keys[item_index]}`\n"
                tier_column += f"*{items[items_keys[item_index]]['tier']}*\n"
                from_column += f"__{items[items_keys[item_index]]['from']}__\n"

                embed.clear_fields()

                embed.add_field(name="Nom (ID)", value=name_column)
                embed.add_field(name="Tier", value=tier_column)
                embed.add_field(name="Source", value=from_column)
                embed = set_footer(embed, ctx)

                if item_index == len(items_keys) - 1:
                    finished = True
                    await ctx.author.send(embed=embed)
                item_index += 1

            await ctx.author.send(embed=embed)
            embed.clear_fields()

            embed.add_field(name="Name (ID)", value="*")
            embed.add_field(name="Tier", value="*")
            embed.add_field(name="Source", value="*")

            name_column = ""
            tier_column = ""
            from_column = ""

            if item_index == len(items_keys) - 1:
                finished = True

            page += 1


    @commands.command()
    async def powers(self, ctx):
        """Display the list of all game powers"""
        powers = get_file("powers")
        name_column = ""
        id_column = ""
        desc_column = ""

        for power in powers.items():
            name_column += f"**{power[1]['name']}**\n"
            id_column += f"{power[0]}\n"
            desc_column += f"*{power[1]['desc']}*\n"

        embed = discord.Embed(color=default_color)
        embed.set_author(name="⚡ Liste des pouvoirs")
        embed.add_field(name="Nom", value=f"**{name_column}**")
        embed.add_field(name="ID", value=f"*{id_column}*")
        embed.add_field(name="Description", value=f"{desc_column}")
        embed = set_footer(embed, ctx)

        await ctx.send(embed=embed)


    @commands.command()
    async def players(self, ctx):
        """Display the list of all game players"""
        inventories = get_file("inventories")
        players_field = ""

        if list(inventories.keys()):
            for player_id in inventories.keys():
                players_field += f"• <@{player_id}>\n"
        else:
            players_field = "🍂 `Il n'y pas encore encore de joueurs...` 🕸️"

        embed = discord.Embed(color=default_color)
        embed.set_author(name=f"👥 Liste des joueurs")
        embed.add_field(name="Players", value=players_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["stats"])
    async def statistics(self, ctx):
        """Display some bot's statistics"""
        stats = get_file("stats")
        inventories = get_file("inventories")

        game_field = ""
        game_field += f"**spin** exécuté : `{stats['spin']}` *fois*\n"
        game_field += f"**daily** exécuté : `{stats['daily']}` *fois*\n"
        game_field += f"**trade** exécuté : `{stats['trade']}` *fois*\n"
        game_field += f"**pay** exécuté : `{stats['pay']}` *fois*"

        money_qtty = 0
        points_qtty = 0
        items_qtty = 0
        for player in inventories.keys():
            money_qtty += inventories[player]["balance"]
        for player in inventories.keys():
            items_qtty += len(inventories[player]["items"])
            for item in inventories[player]["items"]:
                points_qtty += item["points"]

        qtty_field = f"**argent** : `{money_qtty}` PO (pièces d'or)\n"             \
                     f"**items** : `{items_qtty}` items\n"                        \
                     f"**points** : `{points_qtty}` points"

        bot_field = f"nombre de **joueurs** : `{len(list(inventories.keys()))}`\n"         \
                    f"nombre de **servers** : `{len(self.bot.guilds)}`\n"                  \
                    f"**ID** propriétaire : `{open('./data/owner.id.txt', 'r').read()}`\n" \
                    f"**latence** : `{self.bot.latency}` secs."

        embed = discord.Embed(color=default_color)
        embed.set_author(name=f"📊 Statistics")
        embed.add_field(name="Commandes", value=game_field, inline=False)
        embed.add_field(name="Volumes", value=qtty_field, inline=False)
        embed.add_field(name="Bot",      value=bot_field,  inline=False)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command()
    async def get_points(self, ctx, item_id: str, item_float: float):
        items = get_file("items")
        if item_id in list(items.keys()) and 0 <= item_float <= 1:
            item_tier = items[item_id]["tier"]
            tier_points, float_multiplicator = get_points(item_tier, item_float)
            embed = discord.Embed(color=default_color)
            embed.set_author(name="❔ Obtenir points d'item")
            embed.add_field(name="Points calculation",
                            value=f"**Points de tier** : `{tier_points} pts`\n"                          \
                                  f"**Multiplicateur du float** : `x{float_multiplicator}`"              \
                                  f"**Points de l'items** : `{tier_points * float_multiplicator} pts`")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=gen_error("invalid_synthax", ctx))




def setup(client):
    client.add_cog(GameInfo(client))