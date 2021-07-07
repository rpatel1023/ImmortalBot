from discord.ext import commands, tasks
import discord
import requests_cache
import asyncio
from liquipediapy import dota
from datetime import datetime
from datetime import timedelta
import sqlite3

dota_obj = dota("ImmortalBot 1.0")
requests_cache.install_cache(expire_after=3600)
url = "https://liquipedia.net/dota2/Special:Stream/twitch/"



class MatchFetching(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkAnnounceTimes.start()
        

    @tasks.loop(minutes=1)
    async def checkAnnounceTimes(self):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM main")
        for row in cursor:
            current_time = datetime.utcnow()
            stripped_time = current_time.strftime("%H:%M")
            if row[3] is None:
                continue
            row3 = list(row[3])
            if len(row3) < 5:
                row3 = "0" + str(row[3])
            else:
                row3 = str(row[3])
            # print(row3)
            
            # print(stripped_time)
            if row3 == stripped_time:
                await self.fetchMatches(row)


    
    async def fetchMatches(self, row):

        #get json of all games from liquipedia
        games = dota_obj.get_upcoming_and_ongoing_games()
        
        print("fetching games")

            
        upcoming_matches = []
        # filter all matches for specific team
        matches = self.getMatches(games, row[1].lower())
        for series in matches:
            match_datetime = datetime.strptime(series['start_time'], "%B %d, %Y - %H:%M %Z")
            current_time = datetime.utcnow()

            # compare current time with match time
            # if match is <24 hrs away, add it to embed
            diff = match_datetime - current_time
            if diff < timedelta(hours=24):
                countdown = "https://www.timeanddate.com/countdown/generic?p0=769&iso=" + match_datetime.strftime("%Y") + match_datetime.strftime("%m") + match_datetime.strftime("%d") + "T" + match_datetime.strftime("%H") + match_datetime.strftime("%M")
                upcoming_matches.append(series)
                embed = discord.Embed()
                embed.set_footer(text="Data sourced from Liquipedia.net", icon_url="https://liquipedia.net/commons/extensions/TeamLiquidIntegration/resources/pagelogo/liquipedia_icon_menu.png")

                if series['twitch_channel'] == None:
                    embed.add_field(name=series['team1'] + " vs. " + series['team2'], value="Format: " + series['format'] + "\nStart Time: " + series['start_time'] + "\nTournament: " + series['tournament'] + "\nStream: None" + "\nCountdown: [Link]({})".format(countdown), inline=False)
                else: 
                    embed.add_field(name=series['team1'] + " vs. " + series['team2'], value="Format: " + series['format'] + "\nStart Time: " + series['start_time'] + "\nTournament: " + series['tournament'] + "\nStream: [Link]({})".format(url + str(series['twitch_channel'])) + "\nCountdown: [Link]({})".format(countdown), inline=False)                    
        channel = await self.bot.fetch_channel(row[2])
        if len(upcoming_matches) > 0:
            if row[4] is not None:
                await channel.send(content=f"Hey {row[4]}! **{row[1]}** has the following matches coming up",embed=embed)
            elif row[4] is None:
                await channel.send(embed=embed)
    

    def getMatches(self, games, team_name):
        team_matches = []
        #remove all duplicates and find all matches that match a certain team name
        for series in games:
            if series['team1'].lower() == team_name or series['team2'].lower() == team_name:
                team_matches.append(series)
        unique_stuff = {each['start_time'] : each for each in team_matches}.values()
        team_matches.clear()
        return unique_stuff




    @commands.group(invoke_without_command=True)
    async def view(self, ctx):
        pass
        # await ctx.send("```Available View commands:   \nview team \nview channel \nview time (in UTC) \nview role```")
    
    @view.command()
    async def channel(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result[0] is not None:
                await ctx.send(f"Channel is <#{result[0]}>")
            elif result[0] is None:
                await ctx.send("Channel not set. Please use -setup channel")
            cursor.close()
            db.close()
    
    @view.command()
    async def team(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT team_name FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result[0] is not None:
                await ctx.send(f"Team Name is **{result[0]}**")
            elif result[0] is None:
                await ctx.send("Team Name not set. Please use -setup team")
            cursor.close()
            db.close()

    @view.command()
    async def time(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT announce_time FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result[0] is not None:
                await ctx.send(f"Announcement Time is **{result[0]} UTC**")
            elif result[0] is None:
                await ctx.send("Announcement Time not set. Please use -setup time")
            cursor.close()
            db.close()


    @view.command()
    async def role(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT role_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result[0] is not None:
                await ctx.send(f"Role is {result[0]}")
            elif result[0] is None:
                await ctx.send("Role not set. Please use -setup role")
            cursor.close()
            db.close()
    
    @commands.command(name='games')
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def getGamesCommand(self, ctx, *, teamname):
        games = dota_obj.get_upcoming_and_ongoing_games()
        matches = self.getMatches(games, teamname.lower())
        embed = None
        for series in matches:
            match_datetime = datetime.strptime(series['start_time'], "%B %d, %Y - %H:%M %Z")
            countdown = "https://www.timeanddate.com/countdown/generic?p0=769&iso=" + match_datetime.strftime("%Y") + match_datetime.strftime("%m") + match_datetime.strftime("%d") + "T" + match_datetime.strftime("%H") + match_datetime.strftime("%M")
            
            embed = discord.Embed()
            embed.set_footer(text="Data sourced from Liquipedia.net", icon_url="https://liquipedia.net/commons/extensions/TeamLiquidIntegration/resources/pagelogo/liquipedia_icon_menu.png")

            if series['twitch_channel'] == None:
                embed.add_field(name=series['team1'] + " vs. " + series['team2'], value="Format: " + series['format'] + "\nStart Time: " + series['start_time'] + "\nTournament: " + series['tournament'] + "\nStream: None" + "\nCountdown: [Link]({})".format(countdown), inline=False)
            else: 
                embed.add_field(name=series['team1'] + " vs. " + series['team2'], value="Format: " + series['format'] + "\nStart Time: " + series['start_time'] + "\nTournament: " + series['tournament'] + "\nStream: [Link]({})".format(url + str(series['twitch_channel'])) + "\nCountdown: [Link]({})".format(countdown), inline=False)                    
        if embed is None:
            await ctx.send("**" + teamname + "** has no upcoming matches on Liquipedia.")
        else:
            await ctx.send(content="Upcoming Matches for **" + teamname + "**:", embed=embed)

    @getGamesCommand.error
    async def getGamesCmd_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await asyncio.sleep(error.retry_after)        
            await ctx.reinvoke()
def setup(bot):
    bot.add_cog(MatchFetching(bot))
