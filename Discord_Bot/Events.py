import discord
import random
from discord.ext import commands
from Discord_Bot.List_words.list_words import sad_words, words_encouragement

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Вывод статуса бота в консоль при подключении на сервер"""
        print('Бот подключен под именем {0.user}'.format(self.client))

        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Вывод ободряющих фраз для пользователя в случае отправки грустного слова"""
        msg = message.content.lower()

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(words_encouragement))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Вывод ошибки о неизвестной команде в чат"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данной команды не существует.',
                                                 color=0x0c0c0c))

def setup(client):
    client.add_cog(Events(client))