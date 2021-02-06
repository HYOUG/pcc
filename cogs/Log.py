from discord.ext import commands
from botFunctions import *
from chatEffects import *
from emoji import demojize


class Log(commands.Cog):
    """Listeners : on_message, on_message_edit, on_message_delete"""

    def __init__(self, bot):
        self.bot = bot
        self.sendLog = yellow("[SEND]")                                             # declare the log category 'send'
        self.editLog = yellow("[EDIT]")                                             # declare the log category 'edit'
        self.deleteLog = yellow("[DELETE]")                                         # declare the log category 'delete'
        self.commandList = get_commands_list()                                      # get the 'commands list' 

    @commands.Cog.listener(name = "on_message")
    async def on_message(self, message):
        """'on_message' event handler"""
        if not message.author.bot:
            if message.content.split(" ")[0][1:] in self.commandList:
                if is_registered(message.author.id) or message.content in ["=start", "=help"]:
                    print(demojize(f"[{get_time()}] : {self.sendLog} {blue(str(message.author.name))} {message.content} {red(f'({message.channel})')}"))

 
    @commands.Cog.listener(name = "on_message_edit")
    async def on_message_edit(self, before, after):
        """'on_message_edit' event handler"""
        print(demojize(f"[{get_time()}] : {self.editLog} {blue(str(before.author.name))} {after.content} {red(f'({after.channel})')}"))


    @commands.Cog.listener(name = "on_message_delete")
    async def on_message_delete(self, message):
        """'on_message_delete' event handler"""
        print(demojize(f"[{get_time()}] : {self.deleteLog} {blue(str(message.author.name))} {message.content} {red(f'({message.channel})')}"))


def setup(client):
    client.add_cog(Log(client))