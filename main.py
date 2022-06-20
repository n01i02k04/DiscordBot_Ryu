import os
from discord.ext import commands
from settings_local import token

client = commands.Bot(command_prefix='!')
client.remove_command('help')

for filename in os.listdir('./Discord_Bot'):
    if filename.endswith('.py'):
        client.load_extension(f'Discord_Bot.{filename[:-3]}')

client.run(token)