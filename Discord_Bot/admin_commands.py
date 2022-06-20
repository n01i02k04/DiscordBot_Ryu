import discord
from discord.ext import commands

class Admin(commands.Cog):
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount : int):
        """Команда clear - очистка чата"""
        await ctx.channel.purge(limit = amount)

        await ctx.send(embed = discord.Embed(description=f':white_check_mark: Удалено {amount} сообщений',
                                             color=discord.Color.red()))

    @clear.error
    async def clear_error(self, ctx, error):
        """Обработка ошибок у команды clear"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, обязательно укажите аргумент!')

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        """Команда kick - удаление участника с сервера"""
        await ctx.channel.purge(limit = 1)

        await member.kick(reason = reason)

        await ctx.send(f'Пользователь {member.mention} был кикнут пользователем {ctx.author.mention}')

    @kick.error
    async def kick_error(self, ctx, error):
        """Обработка ошибок у команды kick"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        """Команда ban - ограничение доступа к серверу"""
        await ctx.channel.purge(limit = 1)

        await member.ban(reason = reason)
        await ctx.send(f'Пользователь {member.mention} был забанен пользователем {ctx.author.mention}')

    @ban.error
    async def ban_error(self, ctx, error):
        """Обработка ошибок у команды ban"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def mute(self, ctx, member: discord.Member):
        """Команда mute - ограничение пользования чатом"""
        await ctx.channel.purge(limit=1)

        mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

        await member.add_roles(mute_role)
        await ctx.send(f'Пользователь {member.mention} был замучен пользователем {ctx.author.mention}')

    @mute.error
    async def mute_error(self, ctx, error):
        """Обработка ошибок у команды mute"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unmute(self, ctx, member: discord.Member):
        """Команда unmute - отмена ограничения пользования чатом"""
        await ctx.channel.purge(limit=1)

        mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

        await member.remove_roles(mute_role)
        await ctx.send(f'Пользователь {member.mention} был размучен пользователем {ctx.author.mention}')

    @unmute.error
    async def unmute_error(self, ctx, error):
        """Обработка ошибок у команды unmute"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав!')

def setup(client: commands.Bot):
    client.add_cog(Admin(client))