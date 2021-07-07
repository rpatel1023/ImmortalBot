from discord.ext import commands
import discord
import sqlite3

class Setup(commands.Cog):
    def __init(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def setup(self, ctx):
        pass

    @setup.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    
    @setup.command()
    async def team(self, ctx, *, team):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT team_name FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, team_name) VALUES(?,?)")
                val = (ctx.guild.id, team)
                await ctx.send(f"Team has been set to **{team_name}**")
            elif result is not None:
                sql = ("UPDATE main SET team_name = ? WHERE guild_id = ?")
                val = (team, ctx.guild.id)
                await ctx.send(f"Team has been set to **{team}**")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command()
    async def time(self, ctx, time):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT announce_time FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, annouce_time) VALUES(?,?)")
                val = (ctx.guild.id, time)
                await ctx.send(f"Announce Time has been set to **{time} UTC**")
            elif result is not None:
                sql = ("UPDATE main SET announce_time = ? WHERE guild_id = ?")
                val = (time, ctx.guild.id)
                await ctx.send(f"Announce Time has been set to **{time} UTC**")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command()
    async def role(self, ctx, role):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT role_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, role_id) VALUES(?,?)")
                val = (ctx.guild.id, role)
                await ctx.send(f"Role has been set to {role}")
            elif result is not None:
                sql = ("UPDATE main SET role_id = ? WHERE guild_id = ?")
                val = (role, ctx.guild.id)
                await ctx.send(f"Role has been set to {role}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_messages:
                await ctx.send("Missing argument. Try -setup channel <#channel>")
    
    @team.error
    async def team_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_messages:
                await ctx.send("Missing argument. Try -setup team <team_name>")

    @time.error
    async def time_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_messages:
                await ctx.send("Missing argument. Try -setup time <announce_time>")
    
    @role.error
    async def channel_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_messages:
                await ctx.send("Missing argument. Try -setup role <role>")

def setup(bot):
    bot.add_cog(Setup(bot))