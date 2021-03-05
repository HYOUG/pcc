import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *


class GameInfo(commands.Cog):
    """
    Commands : 
    - help
    - items
    - powers
    - players
    - statistics
    - get_points
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, target: str = "*"):
        """Give a general help or a specified one"""
        help = get_file("help_draft")
        if target == "*" or target in help.keys() or ("=" + target) in get_commands_list():            
            embed = discord.Embed(color=default_color)
            author_value = "❔ Aide"

            if target == "*":
                for key in help.keys():
                    embed.add_field(name=help[key]["display_name"],
                                    value=f"`=help {key}`", inline=True)

            elif target in help.keys():
                author_value += f" | {help[target]['display_name']}"
                help_lines = list(help[target].keys())
                help_lines.remove("display_name")
                for key in help_lines:
                    embed.add_field(name=f"🔹 {help[target][key]['title']}",
                                    value=f"{help[target][key]['desc']}", inline=False)

            elif ("=" + target) in get_commands_list():
                commands_dict = get_commands_dict()
                default_cmd_name = commands_dict[target]
                for category in list(help.keys()):
                    try:
                        embed.add_field(name=f"🔹 {help[category][default_cmd_name]['title']}",
                                        value=help[category][default_cmd_name]['desc'])
                    except KeyError:
                        pass
                
            embed.set_author(name=author_value)
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await gen_error("invalid_synthax", ctx)


    @commands.command()
    async def items(self, ctx):
        """Display the list of all game items"""
        embed = discord.Embed(color=default_color)
        embed.set_author(name="📜 Liste des items")

        if ctx.message.channel.type == discord.ChannelType.text:
            info_field = f"{ctx.author.mention}, la liste des items va vous être envoyée en DM. "        \
                         "La liste peut prendre du temps à se générer.\n\n"                              \
                         ":warning: À cause de la charte graphique il se peut que certaines colonnes "   \
                         "soit décalées par rapport aux autres"
        
        else:
            info_field = f":warning: {ctx.author.mention}, à cause de la charte graphique il se peut que certaines colonnes "   \
                         "soit décalées par rapport aux autres"

        embed.add_field(name="Informations", value=info_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)

        name_column = ""
        tier_column = ""
        from_column = ""

        items = dict(sorted(get_file("items").items(), key = lambda item: item[1]["name"]))
        item_index = 0
        page = 1
        finished = False

        embed = discord.Embed(color=default_color)
        embed.add_field(name="Nom (ID)", value="*")
        embed.add_field(name="Tier", value="*")
        embed.add_field(name="Source", value="*")
        
        for item_key in list(items.keys()):
            if len(embed) <= 6000 and                                                                         \
               len(embed.fields[0].value) + len(f"**{items[item_key]['name']}** ({item_key})\n") < 1024 and   \
               len(embed.fields[1].value) + len(f"***{items[item_key]['tier']}***\n") < 1024 and              \
               len(embed.fields[2].value) + len(f"**__{items[item_key]['from']}__**\n") < 1024:
                   
                embed.set_author(name=f"📜 Liste des items | Page n°{page}")
                name_column += f"**{items[item_key]['name']}** ({item_key})\n"
                tier_column += f"***{items[item_key]['tier']}***\n"
                from_column += f"**__{items[item_key]['from']}__**\n"

                embed.clear_fields()

                embed.add_field(name="Nom (ID)", value=name_column)
                embed.add_field(name="Tier", value=tier_column)
                embed.add_field(name="Source", value=from_column)
                embed = set_footer(embed, ctx)
                   
            else:
                await ctx.author.send(embed=embed)
                
                embed.clear_fields()
                embed.add_field(name="Name (ID)", value="*")
                embed.add_field(name="Tier", value="*")
                embed.add_field(name="Source", value="*")

                name_column = ""
                tier_column = ""
                from_column = ""
                page += 1
                
        await ctx.author.send(embed=embed)


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
        embed.set_author(name="⚡ Liste des power-ups")
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
        embed.set_author(name="👥 Liste des joueurs")
        embed.add_field(name="Players", value=players_field)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["stats"])
    async def statistics(self, ctx):
        """Display some bot's statistics"""
        stats = get_file("statistics")
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

        qtty_field = f"**argent** : `{money_qtty}` PO (pièces d'or)\n"  \
                     f"**items** : `{items_qtty}` items\n"              \
                     f"**points** : `{points_qtty}` points"

        bot_field = f"nombre de **joueurs** : `{len(list(inventories.keys()))}`\n"         \
                    f"nombre de **servers** : `{len(self.bot.guilds)}`\n"                  \
                    f"**ID** propriétaire : `{open('data/metadata/owner.id.txt', 'r').read()}`\n" \
                    f"**latence** : `{self.bot.latency}` secs."

        embed = discord.Embed(color=default_color)
        embed.set_author(name="📊 Statistiques")
        embed.add_field(name="Commandes", value=game_field, inline=False)
        embed.add_field(name="Volumes", value=qtty_field, inline=False)
        embed.add_field(name="Bot", value=bot_field,  inline=False)
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command()
    async def get_points(self, ctx, item_id: str, item_float: float):
        """Display the points (score) of the give item (ID, float)"""
        items = get_file("items")
        if item_id in items and 0 <= item_float <= 1:
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
            await gen_error("invalid_synthax", ctx)




def setup(client):
    client.add_cog(GameInfo(client))
