import discord
from discord.ext import commands
import requests
import json
import datetime
from discord.utils import get

def get_quote():
    """Функция для получения цитат с помощью API и HTTP-запроса"""
    response = requests.get("https://zenquotes.io/api/random")

    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' - ' + json_data[0]['a'] + '.'
    return quote

class User(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def inspire(self, ctx):
        """Команда inspire, которая выводит полученные от функции get_quote цитаты"""
        quote = get_quote()
        await ctx.send(quote)

    @commands.command()
    async def hello(self, ctx):
        """Команда hello"""
        author = ctx.message.author

        await ctx.send(f'{author.mention}' + ' Hello!')

    @commands.command()
    async def help(self, ctx):
        """Команда help"""
        emb = discord.Embed(title = 'Навигация по командам')

        emb.add_field(name='{}hello'.format('!'), value='Поздоровайтесь с ботой')
        emb.add_field(name='{}inspire'.format('!'),
                      value='Цитаты, которые принесут спокойствие в вашу жизнь')
        emb.add_field(name='{}clear'.format('!'), value = 'Очистка чата\n(только для администраторов)')
        emb.add_field(name='{}kick'.format('!'), value='Удаление участника с сервера\n(только для администраторов)')
        emb.add_field(name='{}ban'.format('!'), value='Ограничение доступа к серверу\n(только для администраторов)')
        emb.add_field(name='{}time'.format('!'), value='Вывод реального времени\n(только для администраторов)')
        emb.add_field(name='{}mute'.format('!'), value='Ограничение пользования чатом\n(только для администраторов)')
        emb.add_field(name='{}unmute'.format('!'),
                      value='Отмена ограничения пользования чатом\n(только для администраторов)')
        emb.add_field(name='{}gratitude'.format('!'),
                      value='Благодарность за пользование в личном сообщении')
        emb.add_field(name='{}join'.format('!'), value='Подключение к голосовому чату')
        emb.add_field(name='{}leave'.format('!'), value='Отключение от голосового чата')
        emb.add_field(name='Вывод ободряющих сообщений',
                      value='Если вам станет грустно, поделитесь этим, и бот вас обязательно поддержит')

        await ctx.send(embed = emb)

    @commands.command()
    async def gratitude(self, ctx):
        """Команда для отправки сообщения от бота в лс пользователя"""
        await ctx.author.send('Спасибо за то, что пользуетесь ботом Рю!')

    @commands.command()
    async def time(self, ctx):
        """Команда time"""
        emb = discord.Embed(title='Время', description='Вы можете узнать текущее время',
                            colour=discord.Color.green(), url='https://time100.ru/')
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.set_thumbnail(url='https://i.pinimg.com/originals/8e/04/d6/8e04d62d3c4d1c9e514d2eb99a32c893.jpg')

        now_date = datetime.datetime.now()
        emb.add_field(name='Time', value='Time : {}'.format(now_date))
        await ctx.send(embed=emb)

    @commands.command()
    async def join(self, ctx):
        """Команда join - подключение бота к голосовому чату"""
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f'Бот присоединился к каналу: {channel}')

    @commands.command()
    async def leave(self, ctx):
        """Команда leave - отключение от голосового чата"""
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            voice = await channel.connect()

def setup(client: commands.Bot):
    client.add_cog(User(client))