import discord
from discord.ext import commands

class Admin(commands.Cog):
    # Команда clear - очистка чата
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit = amount)

        await ctx.send(embed = discord.Embed(description=f':white_check_mark: Удалено {amount} сообщений',
                                             color=discord.Color.red()))

    # Обработка ошибок у команды clear
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, обязательно укажите аргумент!')

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    # Команда kick - удаление участника с сервера
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await ctx.channel.purge(limit = 1)

        await member.kick(reason = reason)

        await ctx.send(f'Пользователь {member.mention} был кикнут пользователем {ctx.author.mention}')

    # Обработка ошибок у команды kick
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    # Команда ban - ограничение доступа к серверу
    @commands.command()
    @commands.has_permissions(administrator = True)

    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await ctx.channel.purge(limit = 1)

        await member.ban(reason = reason)
        await ctx.send(f'Пользователь {member.mention} был забанен пользователем {ctx.author.mention}')

    # Обработка ошибок у команды ban
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    # Команда mute - ограничение пользования чатом
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def mute(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)

        mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

        await member.add_roles(mute_role)
        await ctx.send(f'Пользователь {member.mention} был замучен пользователем {ctx.author.mention}')

    # Обработка ошибок у команды mute
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    # Команда unmute - отмена ограничения пользования чатом
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unmute(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)

        mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

        await member.remove_roles(mute_role)
        await ctx.send(f'Пользователь {member.mention} был размучен пользователем {ctx.author.mention}')

    # Обработка ошибок у команды unmute
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

def setup(client: commands.Bot):
    client.add_cog(Admin(client))