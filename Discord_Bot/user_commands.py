import discord
from discord.ext import commands
import requests
import json
import datetime
from discord.utils import get

# Функция для получения цитат с помощью API и HTTP-запроса
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")

    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' - ' + json_data[0]['a'] + '.'
    return(quote)

class User(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Команда inspire, которая выводит полученные от функции get_quote цитаты
    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        await ctx.send(quote)

    # Команда hello
    @commands.command()
    async def hello(self, ctx):
        author = ctx.message.author

        await ctx.send(f'{author.mention}' + ' Hello!')

    # Команда help
    @commands.command()

    async def help(self, ctx):
        emb = discord.Embed(title = 'Навигация по командам')

        emb.add_field(name='{}hello'.format('!'), value='Поздоровайтесь с ботой')
        emb.add_field(name='{}inspire'.format('!'),
                      value='Цитаты, которые принесут спокойствие в вашу жизнь')
        emb.add_field(name='{}clear'.format('!'), value = 'Очистка чата\n(только для администраторов)')
        emb.add_field(name='{}kick'.format('!'), value='Удаление участника с сервера\n(только для администраторов)')
        emb.add_field(name='{}ban'.format('!'), value='Ограничение доступа к серверу\n(только для администраторов)')
        emb.add_field(name='{}time'.format('!'), value='Вывод реального времени\n(только для администраторов)')
        emb.add_field(name='{}mute'.format('!'), value='Ограничение пользования чатом\n(только для администраторов)')
        emb.add_field(name='{}unmute'.format('!'), value='Отмена ограничения пользования чатом\n(только для администраторов)')
        emb.add_field(name='{}gratitude'.format('!'),
                      value='Благодарность за пользование в личном сообщении')
        emb.add_field(name='{}join'.format('!'), value='Подключение к голосовому чату')
        emb.add_field(name='{}leave'.format('!'), value='Отключение от голосового чата')
        emb.add_field(name='Вывод ободряющих сообщений',
                      value='Если вам станет грустно, поделитесь этим, и бот вас обязательно поддержит')

        await ctx.send(embed = emb)

    # Команда для отправки сообщения от бота в лс пользователя
    @commands.command()
    async def gratitude(self, ctx):
        await ctx.author.send('Спасибо за то, что пользуетесь ботом Рю!')

    # Команда time
    @commands.command()
    async def time(self, ctx):
        emb = discord.Embed(title='Время', description='Вы можете узнать текущее время',
                            colour=discord.Color.green(), url='https://time100.ru/')
        # Добавление имени пользователя
        #emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        # Добавление автора
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.set_thumbnail(url='https://i.pinimg.com/originals/8e/04/d6/8e04d62d3c4d1c9e514d2eb99a32c893.jpg')

        now_date = datetime.datetime.now()
        emb.add_field(name='Time', value='Time : {}'.format(now_date))
        await ctx.send(embed=emb)

    # Команда join - подключение бота к голосовому чату
    @commands.command()
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f'Бот присоединился к каналу: {channel}')

    # Команда leave - отключение от голосового чата
    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            voice = await channel.connect()

def setup(client: commands.Bot):
    client.add_cog(User(client))