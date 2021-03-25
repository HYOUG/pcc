#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by HYOUG
                                                                    
from os import listdir, chdir, path, system
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *

abspath = path.abspath(__file__)                                                    # set up the env. : working dir. and console appearence
dname = path.dirname(abspath)
chdir(dname)
system("cls")
system("title Pop culture Collectibles")

token = open("data/metadata/bot.token.txt", "r").read()                             # set up the bot obj. : token, desc., prefix, etc
description = open("data/metadata/description.txt", "r").read()
bot = commands.Bot(command_prefix="=",
                   description=description,
                   case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():                                                               # on_ready event
    commands_list = []                                                              # local variables
    commands_dict = {}
    bot_is_ready = False
    if not bot_is_ready:                                                            # check if the bot have been ran once
        bot_is_ready = True
        
        print("=" * 45)                                                             # login header : display name and ID
        print(f"Logged in as :    {yellow(bot.user.name)}")
        print(f"ID :              {yellow(bot.user.id)}")
        print("=" * 45)

        for filename in listdir("./cogs"):                                          # load cogs by iterating all the .py files
            if filename.endswith(".py"):                                            # in the 'cogs' folder. Fetch all the commands,
                bot.load_extension(f"cogs.{filename[:-3]}")                         # aliases and listeners.
                cog = bot.get_cog(filename[:-3])
                cog_methods = cog.get_commands() + cog.get_listeners()
                for method in cog_methods:
                    if isinstance(method, commands.Command):
                        commands_list.append(f"={method.name}")
                        commands_dict[method.name] = method.name
                        for aliases in method.aliases:
                            commands_list.append(f"={aliases}")
                            commands_dict[aliases] = method.name
                print(yellow(filename[:-3]), end="")
                print(" " + "-"*(37 - len(filename[:-3])) + blue('[READY]'))
        print("=" * 45 + "\n")
        print("Commands log :\n")

        f = open("data/metadata/commands.list.txt", "w")                            # tell the cogs the 'commands list' by a file, no other way found at the moment
        commands_list += ["+in", "-in", "+out", "-out"]
        f.write("\n".join(commands_list))
        f.close()                                                                   

        f = open("data/metadata/commands.dict.txt", "w")                            # tell the cogs the 'commands dict' by a file, no other way found at the moment
        commands_str = [f"{key}:{value}" for (key, value) in commands_dict.items()]
        f.write("\n".join(commands_str))
        f.close()

        bot.owner_id = open("data/metadata/owner.id.txt", "r").read()               # get the owner's ID by reading the 'owner.id.txt' file


@bot.event
async def on_message(message):                                                      # on_message event
    pass                                                                            # delete/edit the default function to prevent the bot
                                                                                    # to process messages from here instand of the cog listener


bot.run(token)                                                                      # run the bot


"""
TODO
- Rework powers
- Add items (?)
- get_points from item_id and item_float not item_tier
- PEP8 (PEP8.org)
- Errors handling
- Get rid of commands.dict and commands.list
- Rework errors meaning
- create a pagination system for the embed's character limts (inventory, market)
- add images to README
- create a requirements.txt and look for other standarts, examples, badges (?)
- packs and box
- help examples
- remove/change stocks (?)
- finish check_embed()
"""