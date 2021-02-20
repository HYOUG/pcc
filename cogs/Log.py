from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from emoji import demojize


class Log(commands.Cog):
    """
    Listeners : 
    - on_message
    - on_message_edit
    - on_message_delete
    """

    def __init__(self, bot):
        self.bot = bot
        self.send_log = yellow("[SEND]")                                             # generate the colored log categories
        self.edit_log = yellow("[EDIT]")
        self.del_log = yellow("[DELETE]")
        self.comands_list = get_commands_list()                                      # get the 'commands list' to filter messages

    @commands.Cog.listener(name = "on_message")
    async def on_message(self, message):
        """'on_message' event handler"""
        if not message.author.bot:
            if message.content.split(" ")[0] in self.comands_list:
                if is_registered(message.author.id) or message.content in ["=start", "=help"]:
                    ctx = await self.bot.get_context(message)
                    with ctx.typing():
                        await self.bot.process_commands(message)
                    print(demojize(f"[{get_time()}] : {self.send_log} {blue(str(message.author.name))} {message.content} {red(f'({message.channel})')}"))


    @commands.Cog.listener(name = "on_message_edit")
    async def on_message_edit(self, before, after):
        """'on_message_edit' event handler"""
        print(demojize(f"[{get_time()}] : {self.edit_log} {blue(str(before.author.name))} {after.content} {red(f'({after.channel})')}"))


    @commands.Cog.listener(name = "on_message_delete")
    async def on_message_delete(self, message):
        """'on_message_delete' event handler"""
        print(demojize(f"[{get_time()}] : {self.del_log} {blue(str(message.author.name))} {message.content} {red(f'({message.channel})')}"))


def setup(client):
    client.add_cog(Log(client))