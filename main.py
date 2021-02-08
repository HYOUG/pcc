#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by "HYOUG"

                                                                                    # importations :
import discord                                                                      # discord : manage the bot's actions
from os import listdir, chdir, path, system                                         # os : manage env. and files
from discord.ext import commands                                                    # discord.ext : load cogs
from botFunctions import *                                                          # botFunctions : usuals bot's functions
from chatEffects import *                                                           # chat effects : create color effects on displayed text

                                                                                    # environment setup :
abspath = path.abspath(__file__)                                                    # set the working directory to the main's one
dname = path.dirname(abspath)                                                       # //
chdir(dname)                                                                        # //
system("cls")                                                                       # clear the console
system("title Pop culture Collectibles")                                            # set the console's title to 'Pop culture Collectibles'

                                                                                    # bot's setup :
token = open("data/bot.token.txt", "r").read()                                      # get the bot's token from 'bot.token.txt"
description = open("data/description.txt", "r").read()                              # get the bot's description from 'description.txt'                                                              
bot = commands.Bot(command_prefix="=",                                              # set the bot prefix to '='
                   description=description,                                         # set the bot's description 
                   case_insensitive=True)                                           # make the bot case insensitive
bot.remove_command("help")                                                          # remove the default help command


                                                                                    # variables :
commands_list = []                                                                  # declare the 'commands list'
commands_dict = {}                                                                  # declare the 'commands dict'

                                                                                    # events handlers :
@bot.event
async def on_ready():                                                               # on_ready event
    print("-"*85)                                                                   # initiate the 'bot's authetication' block
    print(f"Logged in as :    {yellow(bot.user.name)}")                             # display the bot's name
    print(f"ID :              {yellow(bot.user.id)}")                               # display the bot's ID
    print("-"*85)                                                                   # separate 'bot's authentication header' to the 'commands block'
    for filename in listdir("./cogs"):                                              # cogs importation by looking all files in 'cogs' folder
        if filename.endswith(".py"):                                                # check if the file is a python file
            bot.load_extension(f"cogs.{filename[:-3]}")                             # load the coag
            cog = bot.get_cog(filename[:-3])                                        # get the cog obj. (in order to get commands from it)
            cog_methods = cog.get_commands() + cog.get_listeners()                  # get commands from the cog obj.
            cog_line = f"{yellow(filename[:-3])} : "                                # create the 'cog line', start with the cog name, the 'category'          
            for method in cog_methods:                                              # iterate all the cogs methods
                if isinstance(method, commands.Command):                            # check if the 'method' is a 'command'
                    commands_list.append(method.name)                               # add the command to the 'commands list'
                    commands_dict[method.name] = method.name                        # add the command to the 'commands dict'
                    if method != cog_methods[-1]:                                   # check if the command isn't the last method from the actual cog
                        cog_line += f"{red(method.name)}, "                         # add the command name to the 'cog line' (generic format)
                    else:                                                           # else
                        cog_line += red(method.name)                                # add the command name to the 'cog line' (last one format)
                    for aliases in method.aliases:                                  # iterate the command's aliases
                        commands_list.append(aliases)                               # add the command's aliases to the 'commands list'
                        commands_dict[aliases] = method.name                        # add the command's aliases to the 'commands dict'
                elif isinstance(method, tuple):                                     # check if the 'method' is a 'listener'
                    if method != cog_methods[-1]:                                   # check if the command isn't the last method from the actual cog
                        cog_line += f"{red(method[0])}, "                           # add the listener name to the 'cog line' (generic format)
                    else:                                                           # else
                        cog_line += red(method[0])                                  # add the listener name to the 'cog line' (last one format)
            print(cog_line)                                                         # print cogs then commands and listeners from it  
    print("-" * 85 + "\n")                                                          # close the 'commands and listeners block'
    print("Commands log :\n")

    f = open("data/commands.list.txt", "w")                                         # tell the cogs the 'commands list' by a file, no other way found at the moment
    f.write(" ".join(commands_list))                                                # //
    f.close()                                                                       # //

    update_file("commands.dict.json", commands_dict)

    bot.owner_id = open("data/owner.id.txt").read()


bot.run(token)                                                                      # launch the bot


"""TODO
Rework powers
Add items (?)
give item command
Upgrade the README
get_points from item_id and item_float not item_tier
"""
