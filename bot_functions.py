from time import strftime
from json import loads, dumps
from discord import Embed
from discord.ext import commands
from chat_effects import default_color, error_color, warning_color, admin_color

"""Generics and usual bot's functions"""

def get_time() -> str:
    """Return a formated version of the time"""
    return strftime("%H:%M:%S")


def get_file(filename: str) -> dict:
    """Return the data from the JSON file desired"""
    return loads(open(f"data/gamedata/{filename}.json", "r", encoding="utf-8").read())


def is_registered(user_id: str) -> bool:
    """Return if the specified id is registered in the players database"""
    inv = get_file("inventories")
    return str(user_id) in list(inv.keys())


def is_bot_owner(ctx) -> bool:
    """Return if the author from the context is the bot owner"""
    return ctx.author.id == int(open("data/metadata/owner.id.txt", "r").read())


def gen_error(error_id: str, ctx) -> Embed:
    """Return a pre-made discord.Embed error message"""
    errors = get_file("errors")
    error = Embed(color=error_color)
    error.add_field(name="⚠️ " + errors[error_id]["title"], value=errors[error_id]['txt'])
    error = set_footer(error, ctx)
    return error


def set_footer(embed: Embed, ctx) -> Embed:
    """Set the discord.Embed's footer"""
    return embed.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.display_name} • {get_time()}")


def update_file(filename: str, variable_dict: dict) -> None:
    """Update the given file with the given data"""
    try:
        file = open(f"data/gamedata/{filename}.json", "w", encoding="utf-8")
        file.write(dumps(variable_dict, indent=3))
        file.close()
    except TypeError:
        print("TypeError")


def get_points(item_tier: str, item_float: float) -> tuple:
    """Return the 'tier_points' and the 'float_multiplicator' from the given item tier and item float"""
    POINTS_SCALE = {"S": 100, "A": 25, "B": 10, "C": 5, "D": 1}
    tier_points = POINTS_SCALE[item_tier]
    if 1.000 > item_float > 0.200:
        float_multiplicator = 1
    elif 0.199 > item_float > 0.100:
        float_multiplicator = 1.5
    elif 0.099 > item_float > 0.010:
        float_multiplicator = 5
    elif 0.009 > item_float > 0.000:
        float_multiplicator = 10
    return (tier_points, float_multiplicator)


async def target_parser(ctx, target: str) -> tuple:
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


def load_cogs(bot: commands.Bot, cog_name: str) -> None:
    """Load all coags"""
    bot.load_extension(f"cogs.{cog_name}")


def unload_cog(bot: commands.Bot, cog_name: str) -> None:
    """Unload a cog"""
    bot.unload_extension(f"cogs.{cog_name}")


def reload_cog(bot: commands.Bot, cog_name: str) -> None:
    """Reload a cog"""
    unload_cog(bot, cog_name)
    load_cogs(bot, cog_name)


def is_protected(target_id: str) -> bool:
    """Return whether or not the target is protected by a shield"""
    inventories = get_file("inventories")
    return inventories[target_id]["shield_active"]

def get_commands_list() -> list:
    """Return all of the commands and aliases in a list"""
    return open("data/metadata/commands.list.txt", "r").read().split(" ")

def get_commands_dict() -> dict:
    """Return all of the commands and aliases in a dictionary"""
    commands_dict = {}
    f =  open(f"data/metadata/commands.dict.txt", "r", encoding="utf-8").read()
    for command in f.split("\n"):
        commands_dict[command.split(":")[0]] = command.split(":")[1]
    return commands_dict            