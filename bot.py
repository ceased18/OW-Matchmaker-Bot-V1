import discord
from discord.ext import commands
from bot_data_functions import *
from bot_matchmake_functions import *
import asyncio

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)
# global game_in_progress
# game_in_progress = False

global msg
global response

vip_list = ["176510548702134273", "176095065670811649", "338591837465870336",
            "452697846345367562", "464328777975988246", "306878726027739137"]


## Cameron, Michael, Tony, Panda


@client.event
async def on_ready():
    ''' Prints a message when the bot is ready.
    '''
    loadPlayerData()
    print("bot is ready")


'''
@client.event
async def on_message(message):
        if str(message.guild.id) == "651200164169777154":
                pass
        else:
                await client.process_commands(message)
'''


@client.command()
async def vip(ctx):
    global vip_list
    if str(ctx.message.author.id) == "176510548702134273":
        vip_list.append(str(ctx.message.mentions[0].id))


@client.command()
async def bitches(ctx):
    if str(ctx.message.author.id) in vip_list:
        member_list = []
        for member in ctx.guild.members:
            member_list.append(member.name + '#' + member.discriminator + ", " + str(member.id))
        await ctx.send('\n'.join(member_list))


@client.command(aliases=["btag", "tag", "register"])
async def battletag(ctx, btag):
    if setBtag(btag, str(ctx.message.author), ctx.message.author.id):
        await ctx.send(ctx.message.author.mention +
                       ", your battletag has been saved. " +
                       "Data will be automatically updated.")
        await update(ctx)
    else:
        await ctx.send(ctx.message.author.mention +
                       ", something went wrong.")


@client.command()
async def update(ctx):
    ''' Updates the player data based off their in game profile.
    '''
    await ctx.send("This may take a while and will pause all " +
                   "other commands. Please be patient and do not spam it.")

    if pullSR(str(ctx.message.author), ctx.message.author.id):
        await ctx.send(ctx.message.author.mention +
                       ", success! Your data has been imported." +
                       " If you are not placed or not public, data" +
                       " will not be overwritten.")
    else:
        await ctx.send(ctx.message.author.mention +
                       ", something went wrong. Is your profile " +
                       "public and have you completed any placements?")


@client.command(aliases=["pugs"])
async def schedule(ctx, time, metric):
    ''' Schedules a pug event some time in the future. Format: .schedule <time> <metric: s/m/h>
        ex:  .schedule 1 h         <-- poll for pugs in 1 hour

    '''
    if str(ctx.message.author.id) in vip_list:
        try:
            await ctx.message.delete()
        except:
            pass
        sleep_timer = 0

        if metric.lower()[0] == "s":
            sleep_timer = int(time)
        elif metric.lower()[0] == "m":
            sleep_timer = int(time) * 60
        elif metric.lower()[0] == "h":
            sleep_timer = int(time) * 60 * 60

        for i in ctx.message.guild.roles:
            if str(i) == "Beta Testers":
                role = i

        if ctx.message.guild.id == 964959897328447559:
            schedule_channel = client.get_channel(966334011037351936)
            poll = await schedule_channel.send(role.mention +
                                               ", react if you're down " +
                                               "for pugs in " + time + metric)
        else:
            poll = await ctx.send("React if you're down for pugs in "
                                  + time + metric)

        check = '✅'
        await poll.add_reaction(check)

        await asyncio.sleep(sleep_timer)

        try:
            cache_poll = await ctx.fetch_message(poll.id)

            num_puggers = 0
            for reaction in cache_poll.reactions:
                if str(reaction) == check:
                    num_puggers = reaction.count - 1

            if num_puggers > 12:
                try:
                    await ctx.send(role.mention +
                                   " the time for pugs is upon us!")
                except:
                    await ctx.send("It's pugs time!")
            else:
                await ctx.send("Not enough people responded." +
                               " Please get at least " +
                               str(12 - num_puggers) + " more.")
        except:
            await ctx.send("A scheduling error occured. "
                           "Was the original message deleted?")


##@client.event
##async def on_message(message):
##    channel = message.channel
##    mystr = message.content
##    sender = str(message.author)
##    await client.process_commands(message)


@client.command()
async def avoid(ctx):
    ''' Avoids a player from being on your team.
    '''
    # await ctx.message.delete()
    await ctx.send("Player has been avoided in queue. " +
                   "Note that regular matchmaking time may be " +
                   "extended. Players have a max of 3 avoid " +
                   "slots, any new avoids will replace the oldest one.")


@client.command()
async def resetavoid(ctx):
    ''' Resets your current avoid slots.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send("All avoids have been deleted and reset. ")


@client.command()
async def highlyavoided(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(
        "<@297127857665343489>,<@230096485289689089>\nWARNING: You have been avoided multiple times by a considerable number of players. " +
        "Please speak to an organizer before your next queue " +
        "as this may result in longer queue times or the inability to queue at all " +
        "while attempting to find a match")


@client.command(aliases=["mtt"])
# @commands.has_role('BotMaster')
async def move_to_teams(ctx):
    ''' Moves people on teams to their respective team channel.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    if str(ctx.message.author.id) in vip_list:
        ## ## Private Gauntlet Beta channel IDs
        if ctx.message.guild.id == 964959897328447559:
            draft_channel = client.get_channel(964959897794007060)
            channel1 = client.get_channel(965077932013940786)
            channel2 = client.get_channel(965077947138576394)

        pdata = loadPlayerData()
        team1 = get_t1_id(pdata)
        team2 = get_t2_id(pdata)
        sender = ctx.message.author
        num_moved = 0
        for member in draft_channel.members:
            if member.id in team1:
                await member.move_to(channel1)
                num_moved += 1
            elif member.id in team2:
                await member.move_to(channel2)
                num_moved += 1
        await ctx.send("{} users moved.".format(num_moved),
                       delete_after=3)


@client.command(aliases=["mtd"])
# @commands.has_role('BotMaster')
async def move_to_draft(ctx):
    ''' Moves all users from the team channels to the draft channel.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    if str(ctx.message.author.id) in vip_list:
        ## ## Private Gauntlet Beta channel IDs
        if ctx.message.guild.id == 964959897328447559:
            draft_channel = client.get_channel(964959897794007060)
            channel1 = client.get_channel(965077932013940786)
            channel2 = client.get_channel(965077947138576394)

        num_moved = 0
        for member in channel1.members:
            await member.move_to(draft_channel)
            num_moved += 1
        for member in channel2.members:
            await member.move_to(draft_channel)
            num_moved += 1
        await ctx.send("{} users moved.".format(num_moved),
                       delete_after=3)


@client.command()
async def captains(ctx):
    ''' Picks two users at random from draft channel.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    ## ## Private Gauntlet Beta channel IDs
    if ctx.message.guild.id == 964959897328447559:
        draft_channel = client.get_channel(964959897794007060)
        channel1 = client.get_channel(965077932013940786)
        channel2 = client.get_channel(965077947138576394)

    i = random.randint(0, len(draft_channel.members))
    j = random.randint(0, len(draft_channel.members))
    while i == j:
        j = random.randint(0, len(draft_channel.members))
    await ctx.send(draft_channel.members[i].mention + " " +
                   draft_channel.members[j].mention +
                   " are your captains.")


# @client.command()
# async def team(ctx):
#     ''' Reminds the sender what team they're on.
#     '''
#     try:
#         await ctx.message.delete()
#     except:
#         pass
#     sender = str(ctx.message.author)
#     team = getPlayerTeam(sender)
#     if team == "-1":
#         await ctx.send(ctx.message.author.mention +
#                        ", you're not on a team.", delete_after=15)
#     else:
#         await ctx.send(ctx.message.author.mention +
#                        ", you're on team " + str(team), delete_after=15)


async def map_embed(ctx, maplist):
    embed_msg = discord.Embed(title="Maps",
                              description="Please vote for your favorite map.", color=0xBE2596)
    # embed_msg.set_thumbnail(url="https://i.imgur.com/4yg6YMW.jpeg")
    embed_msg.add_field(name="Map 1", value=maplist[0])
    embed_msg.add_field(name="Map 2", value=maplist[1])
    embed_msg.add_field(name="Map 3", value=maplist[2])
    return embed_msg


@client.command(aliases=["randomMap", "randommap", "maps", "randommaps"])
async def map(ctx, map_num=3):
    ''' Sends a random map.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    if map_num > len(mapList) or map_num < 1:
        await ctx.send("Invalid number of maps.")
        return 0
    maps = []
    while len(maps) < map_num:
        map_to_add = randomMap()
        if map_to_add not in maps:
            maps.append(map_to_add)
    poll = await ctx.send(embed=await map_embed(ctx, maps))
    reacts = ['1️⃣', '2️⃣', '3️⃣']
    for emoji in reacts:
        await poll.add_reaction(emoji)




@client.command()
async def mention(ctx):
    ''' Mentions whoever used the command.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    sleep_timer = random.randint(1, 120)
    print(sleep_timer)
    await asyncio.sleep(sleep_timer)
    await ctx.send(ctx.message.author.mention, delete_after=10)


@client.command()
async def commands(ctx):
    ''' Prints working commands.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    string1 = """To input your SR, please use the following commands:
        \n.tank SR\n.dps SR\n.support SR
        \nTo see your SR, use .sr
        \nTo queue for a role, use .q role\nTo see the current queue, use .q
        \nTo see what you are queued for, use .status
        \nTo see the roles needed to make a match, use .roles
        \nTo begin matchmaking, use .mm
        \nTo report the winning team, use.win 1/2
        \nIn case of a tie, use .win 0"""
    """
    \nTo move users to team channels after matchmaking, use .mtt
    \nTo move users from team channels back to draft, use .mtd
    """
    await ctx.send(string1)


@client.command(aliases=["matchmake"])
async def mm(ctx):
    ''' Makes a match based on users queued. If not enough players
            are queued prints an error message.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    # global game_in_progress
    mylist = getAllPlayerData()
    matchList = matchmake(mylist)
    if matchList[0] != -1:
        await ctx.send(printTeams(matchList))
        await map(ctx, 3)
    else:
        await ctx.send("Error encountered. Are enough players queued?")


# @client.command(aliases=["w"])
# async def win(ctx, team_num):
#     ''' Calls adjust to add or subtract player SR.
#     '''
#     global game_in_progress
#     if (team_num == "0" or team_num == "1" or team_num == "2") \
#             and game_in_progress:
#         adjust(int(team_num))
#         if team_num != "0":
#             await ctx.send("Congrats Team " +
#                            team_num)
#         else:
#             await ctx.send("My algorithm is so good, " +
#                            "the teams were perfectly balanced.")
#         # clearQueue()
#         await client.change_presence(activity=discord.Game(name=""))
#         game_in_progress = False
#     else:
#         if game_in_progress:
#             await ctx.send("Please enter a valid team.")
#         else:
#             await ctx.send("No game in progress.")


@client.command(aliases=["supp"])
async def support(ctx, SR):
    ''' Updates the sender's profile with the new support data.
    '''
    sender = str(ctx.message.author)
    discord_id = ctx.message.author.id
    if setSupport(SR, sender, discord_id):
        await ctx.send(ctx.message.author.mention +
                       ", your support SR has been updated.")
    elif int(SR) <= 1000:
        await ctx.send(ctx.message.author.mention +
                       ", please rank up and try again.")
    else:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.")


@client.command(aliases=["dps"])
async def damage(ctx, SR):
    ''' Updates the sender's profile with the new dps data.
    '''
    sender = str(ctx.message.author)
    discord_id = ctx.message.author.id
    if setDamage(SR, sender, discord_id):
        await ctx.send(ctx.message.author.mention +
                       ", your dps SR has been updated.")
    elif int(SR) <= 1000:
        await ctx.send(ctx.message.author.mention +
                       ", please rank up and try again.")
    else:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.")


@client.command()
async def tank(ctx, SR):
    ''' Updates the sender's profile with the new tank data.
    '''
    sender = str(ctx.message.author)
    discord_id = ctx.message.author.id
    if (not SR.isalpha()) and setTank(SR, sender, discord_id):
        await ctx.send(ctx.message.author.mention +
                       ", your tank SR has been updated.", delete_after=15)
    elif int(SR) <= 1000:
        await ctx.send(ctx.message.author.mention +
                       ", please rank up and try again.", delete_after=15)
    else:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.", delete_after=15)


@client.command(aliases=["q", "queuecheck", "qc"])
async def queue(ctx, role="none"):
    ''' If no args passed, prints the queue. Else it updates the
            sender's data to place them in the queue for what role
            they want.
    '''
    if role == "none":
        await ctx.send(ctx.message.author.mention
                       + "\n" + printQueue()
                       )
    elif role == "clear":
        clearQueue()
        await ctx.send("The queue has been emptied.")
    elif role == "fill":
        roles_needed = []
        if suppQueued() != 0:
            roles_needed.append("support")
        if tankQueued() != 0:
            roles_needed.append("tank")
        if dpsQueued() != 0:
            roles_needed.append("dps")
        if len(roles_needed) == 0:
            roles_needed = ["tank", "support", "dps"]

        rand = random.randint(0, len(roles_needed) - 1)
        sender = str(ctx.message.author)
        message = (queueFor(roles_needed[rand], sender))
        await ctx.send(ctx.message.author.mention + ", " +
                       message)
        await roles(ctx, 10)

    else:
        sender = str(ctx.message.author)
        message = (queueFor(role, sender))
        await ctx.send(ctx.message.author.mention + ", " +
                       message)
        await roles(ctx, 10)


@client.command(aliases=["role"])
async def roles(ctx, timer=25):
    ''' Prints out the roles needed to matchmake.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    message = "Roles Needed:\n"
    if tankQueued() != 0:
        message = message + (tankQueued() + " tanks.\n")
    if dpsQueued() != 0:
        message = message + (dpsQueued() + " dps.\n")
    if suppQueued() != 0:
        message = message + (suppQueued() + " supports.\n")
    if message == "Roles Needed:\n":
        message = "All roles filled."
    await ctx.send(message, delete_after=timer)


@client.command(aliases=["l", "leavequeue", "lq"])
async def leave(ctx):
    ''' Leaves the queue.
    '''
    sender = str(ctx.message.author)
    message = deQueue(sender)
    await roles(ctx, 10)


@client.command(aliases=["SR"])
async def sr(ctx):
    ''' Prints out the player's saved SR values.
    '''
    try:
        sender = str(ctx.message.author)
        sr = printPlayerData(sender)
        await ctx.send(sr)
    except:
        await ctx.send("Error 404: SR doesn't exist", delete_after=25)


@client.command()
async def status(ctx):
    ''' Prints what the sender is queued for.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    sender = str(ctx.message.author)
    status = printQueueData(sender)
    await ctx.send(ctx.message.author.mention + status, delete_after=25)


##@client.command(aliases=["allsr"])
##async def allSR(ctx):
##        ''' Prints out all the saved SR data.
##        '''
##        try:
##                sr = printAllPlayerData()
##                await ctx.send(sr)
##        except:
##                await ctx.send("Error 404: SR doesn't exist")


@client.command()
async def clear(ctx, amount=5):
    ''' Removes a specified amount of messages.
    '''
    # await ctx.message.delete()
    if amount > 0:
        await ctx.channel.purge(limit=amount)


@client.command(aliases=["flip"])
async def coin(ctx):
    ''' Flips a coin.
    '''
    result = random.randint(0, 1)
    if result == 0:
        await ctx.send("Heads!")
    else:
        await ctx.send("Tails!")


@client.command(aliases=["dick", "size"])
async def dicksize(ctx):
    ''' Randomly assigns a number in inches.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    i = random.randint(321, 987)
    if str(ctx.message.author) == "Panda#3239":
        i = 100
        message = str(i / 100) + " nautical mile dick."
    elif str(ctx.message.author) == "Timmy#3426":
        i += 30
        message = str(i / 100) + " inch dick."
    elif str(ctx.message.author) == "Twang#8757":
        i -= 321
        message = str(i / 100) + " inch dick."
    elif str(ctx.message.author) == "Duncanator02#5596":
        i += 350
        message = str(i / 100) + " inch dick."
    elif str(ctx.message.author) == "Archangel#0346":
        i += 1250
        message = str(i / 100) + " inch dick."
    elif str(ctx.message.author) == "ZypherLuna#9125":
        i += 321
        message = str(i / 100) + " inch dick."
    elif str(ctx.message.author) == "BubbLeS#4835":
        message = "dick beyond human comprehension."
    else:
        message = str(i / 100) + " inch dick."
    ##                await ctx.send(ctx.message.author.mention +
    ##                               " has a massive dick.")
    # else:
    await ctx.send(ctx.message.author.mention + " has a "
                   + message)


@client.command(aliases=["bi", "pan"])
async def gay(ctx):
    ''' Randomly assigns the user a sexuality. Not always random.
    '''
    try:
        await ctx.message.delete()
    except:
        pass
    i = random.randint(0, 100)
    if str(ctx.message.author) == "aries#0402":
        await ctx.send(ctx.message.author.mention + " is a mercy main.")
    elif str(ctx.message.author) == "Panda#3239":
        await ctx.send(ctx.message.author.mention + " is bi.")
    elif str(ctx.message.author) == "StodgyMeteor#8420":
        await ctx.send(ctx.message.author.mention + " is a bad torb.")
    else:
        if (i % 11) == 0:
            await ctx.send(ctx.message.author.mention +
                           " is gay.")
        elif (i % 11) == 1:
            await ctx.send(ctx.message.author.mention +
                           " is straight.")
        elif (i % 11) == 2:
            await ctx.send(ctx.message.author.mention +
                           " is asexual.")
        elif (i % 11) == 3:
            await ctx.send(ctx.message.author.mention +
                           " is bi.")
        elif (i % 11) == 4:
            await ctx.send(ctx.message.author.mention +
                           " is closeted :0.")
        elif (i % 10) == 5:
            await ctx.send(ctx.message.author.mention +
                           " just came out!")
        elif (i % 11) == 6:
            await ctx.send(ctx.message.author.mention +
                           " is pan.")
        elif (i % 11) == 7:
            await ctx.send(ctx.message.author.mention +
                           " is sexy af.")
        elif (i % 11) == 8:
            await ctx.send(ctx.message.author.mention +
                           " will probably die alone :(")
        elif (i % 11) == 9:
            await ctx.send(ctx.message.author.mention +
                           " Error 404: Sexuality not found.")
        elif (i % 11) == 10:
            await ctx.send(ctx.message.author.mention +
                           " is a furry.")


client.run("token")