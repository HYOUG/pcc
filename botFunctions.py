from time import strftime
from json import loads, dumps
from discord import Embed
from discord.ext import commands
from chatEffects import default_color, error_color, warning_color, admin_color


def get_time():
    """Return a formated version of the time"""
    return strftime("%H:%M:%S")


def get_file(file: str):
    """Return the data from the JSON file desired"""
    return loads(open(f"data/{file}.json", "r", encoding="utf-8").read())


def is_registered(user_id: str):
    """Return if the specified id is registered in the players database"""
    inv = get_file("inventories")
    return str(user_id) in list(inv.keys())


def check1(msg):
    global trader_id
    return str(msg.author.id) == str(trader_id)


def check2(reaction, user):
    global trader2_id
    return str(user.id) == trader2_id and str(reaction) == "✅"


def is_bot_owner(ctx):
    """Return if the author from the context is the bot owner"""
    return ctx.author.id == int(open("data/owner.id.txt", "r").read())


def gen_error(error_id: str, ctx):
    """Return a pre-made discord.Embed error message"""
    errors = get_file("errors")
    error = Embed(color=error_color)
    error.add_field(name="⚠️ " + errors[error_id]["title"], value=errors[error_id]['txt'])
    error.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name} • {get_time()}")
    return error


def set_footer(embed, ctx):
    """Set the discord.Embed's footer"""
    return embed.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.display_name} • {get_time()}")


def update_file(filename: str, variable_dict: dict):
    """Update the given file with the given data"""
    file = open(f"data/{filename}", "w", encoding="utf-8")
    file.write(dumps(variable_dict, indent=3))
    file.close()


def get_points(item_tier: str, item_float: float):
    """Return the 'tier_points' and the 'float_multiplicator' from the given item tier and item float"""
    points_scale = {"S": 100, "A": 25, "B": 10, "C": 5, "D": 1}
    tier_points = points_scale[item_tier]
    if 1.000 > item_float > 0.200:
        float_multiplicator = 1
    elif 0.199 > item_float > 0.100:
        float_multiplicator = 1.5
    elif 0.099 > item_float > 0.010:
        float_multiplicator = 5
    elif 0.009 > item_float > 0.000:
        float_multiplicator = 10
    return tier_points, float_multiplicator


async def target_parser(ctx, target):
    """Return whether or not the 'target' is valid"""
    if target is None:
        target = ctx.author
        target_found = True
    else:
        try:
            target = await commands.MemberConverter().convert(ctx, target)
            target_found = True
        except commands.BadArgument:
            target_found = False
    return (target_found, target)


def load_cogs(bot, cog_name):
    """Load all coags"""
    bot.load_extension(f"cogs.{cog_name}")


def unload_cog(bot, cog_name):
    """Unload a cog"""
    bot.unload_extension(f"cogs.{cog_name}")


def reload_cog(bot, cog_name):
    """Reload a cog"""
    unload_cog(bot, cog_name)
    load_cogs(bot, cog_name)


def is_protected(target_id):
    """Return whether or not the target is protected by a shield"""
    inventories = get_file("inventories")
    return inventories[target_id]["shield_active"]

def get_commands_list():
    """Return all of the commands and aliases list"""
    return open("data/commands.list.txt", "r").read().split(" ")

def get_commands_dict():
    return loads(open(f"data/commands.dict.json", "r", encoding="utf-8").read())