import os
import discord
from discord.ext import commands
import random
from settings_local import token
from Discord_Bot.List_words.list_words import sad_words, words_encouragement

client = commands.Bot(command_prefix='!')
client.remove_command('help')

# Вывод статуса бота в консоль при подключении на сервер
@client.event
async def on_ready():
    print('Бот подключен под именем {0.user}'.format(client))

    #Статус бота
    await client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))

# Вывод ободряющих фраз для пользователя в случае отправки грустного слова
@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(words_encouragement))

# Вывод ошибки о неизвестной команде в чат
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.mention}, данной команды не существует.**', color=0x0c0c0c))


for filename in os.listdir('./Discord_Bot'):
    if filename.endswith('.py'):
        client.load_extension(f'Discord_Bot.{filename[:-3]}')

client.run(token)