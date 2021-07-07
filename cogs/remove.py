from discord.ext import commands
import sqlite3

class Remove(commands.Cog):
    def __init(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def remove(self, ctx):
        pass

    @remove.command()
    async def channel(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                sql = (f"UPDATE main SET channel_id = ? WHERE guild_id = {ctx.guild.id}")
                val = (None,)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                await ctx.channel.send(f"Channel has been cleared, announcements will no longer be posted.")
                
    @remove.command()
    async def team(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                sql = (f"UPDATE main SET team_name = ? WHERE guild_id = {ctx.guild.id}")
                val = (None,)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                await ctx.channel.send(f"Team has been cleared, announcements will no longer be posted.")
                
    @remove.command()
    async def time(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                sql = (f"UPDATE main SET announce_time = ? WHERE guild_id = {ctx.guild.id}")
                val = (None,)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                await ctx.channel.send(f"Announcement Time has been cleared, announcements will no longer be posted.")
    
    @remove.command()
    async def role(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                sql = (f"UPDATE main SET role_id = ? WHERE guild_id = {ctx.guild.id}")
                val = (None,)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                await ctx.channel.send(f"Role has been cleared, this role will no longer be pinged.")



def setup(bot):
    bot.add_cog(Remove(bot))