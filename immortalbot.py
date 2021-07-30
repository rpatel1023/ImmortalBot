from discord.ext.commands import Bot
import discord
from config import CLIENT_TOKEN




intents = discord.Intents.default()
intents.members=True
intents.presences = True
bot = Bot(command_prefix='-', intents=intents)
bot.remove_command('help')



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="Dota 2 | -help"))

@bot.event
async def on_guild_join(guild):
    log_channel = bot.get_channel(channel_id)
    embed = discord.Embed(title=guild.name)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Guild ID", value=guild.id)
    embed.add_field(name="Members", value=guild.member_count)
    
    await log_channel.send(content="New Guild Added!", embed=embed)

    bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
    await bot_entry[0].user.send("""
    Hello! Thanks for inviting ImmortalBot to your server.
    \n ImmortalBot is a simple Discord bot for scraping pro matches from Liquipedia and sends notifications on upcoming matches.
    \nIn your server, use `-help` to look over the various commands. Set up a team, channel, and time (in UTC) to begin listening.
    \nPlease be sure to copy team names **exactly as they appear on Liquipedia**.
    \nIf you have any trouble, try using `-help`
    """)



@bot.group(invoke_without_command=True)
async def help(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        embed = discord.Embed(title="Help", description="Use -help <command> for extended information for a command.\n\nTo start listening, assign a channel, team, and time for your server.\nOptionally, you can add a role to be notified when matches are posted.")
        embed.add_field(name="-setup", value="\nchannel\nteam\ntime\nrole\n`ex. -setup channel #notifications`", inline=False)
        embed.add_field(name="-remove", value="\nchannel\nteam\ntime\nrole\n`ex. -remove channel`", inline=False)
        embed.add_field(name="-view", value="\nchannel\nteam\ntime\nrole\n`ex. -view channel`",inline=False)
        embed.add_field(name="-games", value="`ex. -games Team Secret`",inline=False)
        await ctx.send(embed=embed)

@help.command()
async def setup(ctx):
    await ctx.send("""
    ```
    Setup
    -setup channel <#channel>       [Assigns a channel to post match announcements]
    -setup team <team_name>         [Assigns the pro team to track matches. Copy name as it appears on Liquipedia]
    -setup time <announce_time>     [Set the time (UTC) for the bot to post announcements for upcoming matches]
    -setup role <role>              [Set a role to be notified when the bot posts new announcements]```
    """)

@help.command()
async def remove(ctx):
    await ctx.send("""
    ```
    Remove
    -remove channel                 [Removes the channel to post match announcements]
    -remove team                    [Removes the pro team to track matches]
    -remove time                    [Removes the time (UTC) for the bot to post announcements for upcoming matches]
    -remove role                    [Removes the role to be notified when the bot posts new announcements]```
    """)

@help.command()
async def view(ctx):
    await ctx.send("""
    ```
    View
    -view channel                   [Shows the current channel to post match announcements]
    -view team                      [Shows the current pro team to track matches]
    -view time                      [Shows the current time (UTC) for the bot to post announcements for upcoming matches]
    -view role                      [Shows the current role to be notified when the bot posts new announcements]```
    """)

@help.command()
async def games(ctx):
    await ctx.send("""
    ```
    Games 
    -games [team_name]             [Shows the upcoming matches for a given team name]
    
    Copy team names EXACTLY as they appear on Liquipedia to ensure the query is correct.```
    """)


bot.load_extension("cogs.matchfetching")
bot.load_extension("cogs.setup")
bot.load_extension("cogs.remove")
bot.run(CLIENT_TOKEN)
