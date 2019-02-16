import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import colorsys
import json
import aiohttp
import random




Forbidden= discord.Embed(title="Permission Denied", description="1) Please check whether you have permission to perform this action or not. \n2) Please check whether my role has permission to perform this action in this channel or not. \n3) Please check my role position.", color=0x00ff00)
client = commands.Bot(description="Bot prefix is *", command_prefix=commands.when_mentioned_or("*" ), pm_help = True)

GIPHY_API_KEY = "dc6zaTOxFJmzC"


async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='for *help', type=2))
        await asyncio.sleep(20)
        await client.change_presence(game=discord.Game(name=str(len(set(client.get_all_members())))+' users', type=3))
        await asyncio.sleep(20)
        await client.change_presence(game=discord.Game(name=str(len(client.servers))+' servers', type=3))
        await asyncio.sleep(20)

@client.event
async def on_ready():
     print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
     print('the bot is ready')
     print('.......')
     print('created by dp and bluebird')
     client.loop.create_task(status_task())

def is_owner(ctx):
     return ctx.message.author.id in ["455322915471097857","429301779981795338"]



@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='member')
    await client.add_roles(member, role)
    print("In our server" + member.name + " just joined")
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Welcome user')
    embed.add_field(name = '__Welcome to Our Server__',value ='**Hope you will be active here. Check Our server rules and never try to break any rules. ',inline = False)
    embed.set_image(url = 'https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif')
    await client.send_message(member,embed=embed)
    for channel in member.server.channels:
        if channel.name == 'server-welcome':
            embed = discord.Embed(title=f'Welcome {member.name} to {member.server.name}', description='Do not forget to check rules and never try to break any one of them', color = 0x36393E)
            embed.add_field(name='__Thanks for joining__', value='**Hope you will be active here.**', inline=True)
            embed.set_thumbnail(url='https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif')
            embed.add_field(name='__Join position__', value='{}'.format(str(member.server.member_count)), inline=True)
            embed.add_field(name='Time of joining', value=member.joined_at)
            await asyncio.sleep(0.4)
            await client.send_message(channel, embed=embed)
        


@client.command(pass_context = True)
async def ping(ctx):
    if ctx.message.author.bot:
      return
    else:
      channel = ctx.message.channel
      t1 = time.perf_counter()
      await client.send_typing(channel)
      t2 = time.perf_counter()
      await client.say("Pong: {}ms".format(round((t2-t1)*2000)))

@client.command(pass_context=True)
async def jointest(ctx):
    member = ctx.message.author
    for channel in member.server.channels:
        if channel.name == 'server-welcome':
            embed = discord.Embed(title=f'Welcome {member.name} to {member.server.name}', description='Do not forget to check rules and never try to break any one of them', color = 0x36393E)
            embed.add_field(name='__Thanks for joining__', value='**Hope you will be active here.**', inline=True)
            embed.set_thumbnail(url='https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif')
            embed.add_field(name='__Join position__', value='{}'.format(str(member.server.member_count)), inline=True)
            embed.add_field(name='Time of joining', value=member.joined_at)
            await asyncio.sleep(0.4)
            await client.send_message(channel, embed=embed)


@client.command(pass_context = True)
@commands.check(is_owner)
async def servers(ctx):
  servers = list(client.servers)
  await client.say(f"Connected on {str(len(servers))} servers:")
  await client.say('\n'.join(server.name for server in servers))


@client.command(pass_context = True)
async def lock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    if not channelname:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
        await client.say("Channel locked by: {}".format(ctx.message.author))
    else:
        if ctx.message.author.server_permissions.kick_members == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("Channel locked by: {}".format(ctx.message.author))
@client.command(pass_context = True)
async def unlock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=None, read_messages=True)
    if not channelname:
        if ctx.message.author.server_permissions.kick_members == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
            await client.say("Channel unlocked by: {}".format(ctx.message.author))
    else:
        if ctx.message.author.server_permissions.kick_members == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("Channel unlocked by: {}".format(ctx.message.author))

@client.command(pass_context = True)
async def dm(ctx, user: discord.Member, *, msg: str):
   if user is None or msg is None:
       await client.say('Invalid args. Use this command like: ``*dm @user message``')
   if ctx.message.author.server_permissions.kick_members == False:
       await client.say('**You do not have permission to use this command**')
       return
   else:
       await client.send_message(user, msg)
       await client.delete_message(ctx.message)
       await client.say("Success! Your DM has made it! :white_check_mark: ")

@client.command(pass_context = True)
async def setw(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, 'server-welcome',everyone)

@client.command(pass_context = True)
async def setuplog(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      author = ctx.message.author
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, 'server-log',everyone)

@client.command(pass_context=True)
async def getuser(ctx, role: discord.Role = None):
    if role is None:
        await client.say('Please tag a role to get users having it. Example- ``*getuser @role``')
        return
    if ctx.message.author.server_permissions.kick_members == False:
       await client.say('**You do not have permission to use this command**')
       return
    empty = True
    for member in ctx.message.server.members:
        if role in member.roles:
            await client.say("{0.name}: {0.id}".format(member))
            empty = False
    if empty:
        await client.say("Nobody has the role {}".format(role.mention))

@client.command(pass_context = True)
async def userinfo(ctx, user: discord.Member=None):
    if user is None:
      await client.say('Please tag a user to get user information. Example- ``*userinfo @user``')
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.kick_members == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.")
      embed.add_field(name="Name", value=user.mention, inline=True)
      embed.add_field(name="ID", value=user.id, inline=True)
      embed.add_field(name="Status", value=user.status, inline=True)
      embed.add_field(name="Highest role", value=user.top_role)
      embed.add_field(name="Color", value=user.color)
      embed.add_field(name="Playing", value=user.game)
      embed.add_field(name="Nickname", value=user.nick)
      embed.add_field(name="Joined", value=user.joined_at.strftime("%d %b %Y %H:%M"))
      embed.add_field(name="Created", value=user.created_at.strftime("%d %b %Y %H:%M"))
      embed.set_thumbnail(url=user.avatar_url)
      await client.say(embed=embed)

@client.command(pass_context = True)
async def roleinfo(ctx,*, role:discord.Role=None):
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await client.say("No such role found")
        return
    if ctx.message.author.server_permissions.manage_roles == False:
        await client.say('**You do not have permission to use this command**')
        return
    else:
        embed = discord.Embed(title="{}'s info".format(role.name), description="Here's what I could find.")
        embed.set_thumbnail(url = ctx.message.server.icon_url)
        embed.add_field(name="Name", value=role.name, inline=True)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Color", value=role.color)
        embed.add_field(name="Created", value=role.created_at.strftime("%d %b %Y %H:%M"))
        await client.say(embed=embed)

@client.command(pass_context = True)
async def rolecolor(ctx, role:discord.Role=None, value:str=None):
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await client.say("Use this command like ``*rolecolor (ROLENAME) (ROLECOLOUR IN HEXCODE)``")
        return
    if value is None:
        await client.say("Use this command like ``*rolecolor (ROLENAME) (ROLECOLOUR IN HEXCODE)``")
        return
    if ctx.message.author.server_permissions.manage_roles == False:
        await client.say('**You do not have permission to use this command**')
        return
    else:
        new_val = value.replace("#", "")
        colour = '0x' + new_val
        user = ctx.message.author
        await client.edit_role(ctx.message.server, role, color = discord.Color(int(colour, base=16)))
        await client.say("{} role colour has been edited.".format(role))

@client.command(pass_context = True)
@commands.has_permissions(manage_roles=True)
async def role(ctx, user: discord.Member=None, *, role: discord.Role = None):
        if user is None:
            await client.say("You haven't specified a member! ")
        if role is None:
            await client.say("You haven't specified a role! ")
        if role not in user.roles:
            await client.add_roles(user, role)
            await client.say("{} role has been added to {}.".format(role, user))
            return
        if role in user.roles:
            await client.remove_roles(user, role)
            await client.say("{} role has been removed from {}.".format(role, user))

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, userName: discord.User=None,*, message:str=None):
    if userName is None:
      await client.say('Please tag a person to warn user. Example- ``*warn @user <reason>``')
      return
    else:
      await client.send_message(userName, "You have been warned for: **{}**".format(message))
      await client.say(":warning: __**{0} Has Been Warned!**__ :warning: ** Reason:{1}** ".format(userName,message))
      for channel in userName.server.channels:
        if channel.name == 'server-log':
            embed=discord.Embed(title="User Warned!", description="{0} warned by {1} for {2}".format(userName, ctx.message.author, message), color=0x0521F6)
            await client.send_message(channel, embed=embed)



@client.command(pass_context=True)
async def virus(ctx,user: discord.Member=None,*,hack=None):
    nome = ctx.message.author
    if not hack:
        hack = 'discord'
    else:
        hack = hack.replace(' ','_')
    channel = ctx.message.channel
    x = await client.send_message(channel, '``[▓▓▓                    ] / {}-virus.exe Packing files.``'.format(hack))
    await asyncio.sleep(1.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓                ] - {}-virus.exe Packing files..``'.format(hack))
    await asyncio.sleep(0.3)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {}-virus.exe Packing files...``'.format(hack))
    await asyncio.sleep(1.2)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {}-virus.exe Initializing code.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {}-virus.exe Initializing code..``'.format(hack))
    await asyncio.sleep(1.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {}-virus.exe Finishing.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {}-virus.exe Finishing..``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Successfully downloaded {}-virus.exe``'.format(hack))
    await asyncio.sleep(2)
    x = await client.edit_message(x,'``Injecting virus.   |``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus..  /``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus... -``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus....\``')
    await client.delete_message(x)
    await client.delete_message(ctx.message)

    if user:
        await client.say('`{}-virus.exe` successfully injected into **{}**\'s system.'.format(hack,user.name))
        await client.send_message(user,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
    else:
        await client.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
        await client.send_message(name,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))

@client.command(pass_context=True)
async def invites(ctx, user:discord.Member=None):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    if user is None:
        total_uses=0
        embed=discord.Embed(title='__Invites from {}__'.format(ctx.message.author.name), color = discord.Color((r << 16) + (g << 8) + b))
        invites = await client.invites_from(ctx.message.server)
        for invite in invites:
          if invite.inviter == ctx.message.author:
              total_uses += invite.uses
              embed.add_field(name='Invite',value=invite.id)
              embed.add_field(name='Uses',value=invite.uses)
              embed.add_field(name='Channel',value=invite.channel)
              embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
              embed.add_field(name='__Total Uses__',value=total_uses)
              await client.say(embed=embed)
    else:
        total_uses=0
        embed=discord.Embed(title='__Invites from {}__'.format(user.name), color = discord.Color((r << 16) + (g << 8) + b))
        invites = await client.invites_from(ctx.message.server)
        for invite in invites:
          if invite.inviter == user:
              total_uses += invite.uses
              embed.add_field(name='Invite',value=invite.id)
              embed.add_field(name='Uses',value=invite.uses)
              embed.add_field(name='Channel',value=invite.channel)
              embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
              embed.add_field(name='__Total Uses__',value=total_uses)
              await client.say(embed=embed)
@client.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_image(url=res['message'])
            embed.title = "{} twitted: {}".format(usernamename, txt)
            await client.say(embed=embed)

@client.command(pass_context = True)
async def announce(ctx, channel: discord.Channel=None, *, msg: str=None):
    member = ctx.message.author
    if channel is None or msg is None:
        await client.say('Invalid args. Use this command like ``*announce #channel text here``')
        return
    else:
        if member.server_permissions.administrator == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed=discord.Embed(title="Announcement", description="{}".format(msg), color = discord.Color((r << 16) + (g << 8) + b))
            await client.send_message(channel, embed=embed)
            await client.delete_message(ctx.message)
@client.command(pass_context = True)
async def delchannel(ctx, channel: discord.Channel=None):
    if channel is None:
        await client.delete_channel(ctx.message.channel)
        await client.send_message(ctx.message.author, "{} channel has been deleted in {}".format(ctx.message.channel.name, ctx.message.server.name))
    else:
        if ctx.message.author.server_permissions.administrator == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            await client.delete_channel(channel)
            await client.say("{} channel has been deleted.".format(channel.name))


@client.command(pass_context = True)
async def addchannel(ctx, channel: str=None):
    server = ctx.message.server
    if channel is None:
        await client.say("Please specify a channel name")
    else:
        if ctx.message.author.server_permissions.administrator == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            everyone_perms = discord.PermissionOverwrite(send_messages=None, read_messages=None)
            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
            await client.create_channel(server, channel, everyone)
            await client.say("{} channel has been created.".format(channel))

@client.command(pass_context = True)
async def mute(ctx, member: discord.Member=None, mutetime=None):
    msgauthor = ctx.message.author
    if member is None:
        await client.say('Please specify member i.e. Mention a member to mute. Example-``*mute @user <time in minutes>``')
        return
    if mutetime is None:
        await client.say('Please specify time i.e. Mention a member to mute with time. Example-``*mute @user <time in minutes>``')
        return
    if member.server_permissions.kick_members:
        await client.say('**You cannot mute admin/moderator!**')
        return
    if msgauthor.server_permissions.kick_members == False:
        await client.say('**You do not have permission. So you are unable to use this command**')
        return
    if discord.utils.get(member.server.roles, name='Muted') is None:
        await client.say('No muted role found. Please add it')
        return
    if ctx.message.author.bot:
      return
    else:
      mutetime =int(mutetime)
      mutetime = mutetime * 60
      output = mutetime/60
      role = discord.utils.get(member.server.roles, name='Muted')
      await client.add_roles(member, role)
      await client.say("Muted **{}**".format(member.name))
      await client.send_message(member, "You are muted by {0} for {1} Minutes".format(ctx.message.author, output))
      for channel in member.server.channels:
        if channel.name == 'server-log':
            embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}** for {2} minutes!".format(member, ctx.message.author, output), color=0x37F60A)
            await client.send_message(channel, embed=embed)
            await asyncio.sleep(mutetime)
            if discord.utils.get(member.server.roles, name='Muted') in member.roles:
                await client.remove_roles(member, role)
                await client.say("Unmuted **{}**".format(member.name))
                embed=discord.Embed(title="User unmuted!", description="**{0}** was unmuted!".format(member, ctx.message.author), color=0xFD1600)
                await client.send_message(channel, embed=embed)
            else:
                return

@client.command(pass_context = True)
async def meme(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title='Random Meme', description='from reddit', color = discord.Color((r << 16) + (g << 8) + b))
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.reddit.com/r/me_irl/random") as r:
            data = await r.json()
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            await client.say(embed=embed)

@client.command(pass_context = True)
async def avatar(ctx, user: discord.Member=None):
    if user is None:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=f'Avatar', description='Avatar is profile picture of a user in discord', color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name='User: {}'.format(ctx.message.author.name), value='Avatar:', inline=True)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/534408805048516611/546270988925665280/images5.jpg')
        embed.set_image(url = ctx.message.author.avatar_url)
        await client.say(embed=embed)
    else:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=f'Avatar', description='Avatar is profile picture of a user in discord', color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name='User: {}'.format(user.name), value='Avatar:', inline=True)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/534408805048516611/546270988925665280/images5.jpg')
        embed.set_image(url = user.avatar_url)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def flipcoin(ctx):
    choices = ['Heads', 'Tails', 'Coin self-destructed']
    color = discord.Color(value=0x00ff00)
    em=discord.Embed(color=color, title='Flipped a coin!')
    em.description = random.choice(choices)
    await client.send_typing(ctx.message.channel)
    await client.say(embed=em)

@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member=None):
    if member is None:
      await client.say('Please specify member i.e. Mention a member to unmute. Example- ``*unmute @user``')
    if ctx.message.author.bot:
      return
    else:
      if ctx.message.author.server_permissions.kick_members == False:
        await client.say('**You do not have permission to use this command**')
        return
      else:
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.remove_roles(member, role)
        await client.say("Unmuted **{}**".format(member))
        for channel in member.server.channels:
          if channel.name == 'server-log':
              embed=discord.Embed(title="User unmuted!", description="**{0}** was unmuted by **{1}**!".format(member, ctx.message.author), color=0xFD1600)
              await client.send_message(channel, embed=embed)

@client.command(pass_context = True)
@commands.cooldown(rate=5,per=86400,type=BucketType.user)
async def access(ctx, member: discord.Member=None):
    if member is None:
      await client.say("Please specify a member to give access to him. Example- ``*access @user``")
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.kick_members == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      role = discord.utils.get(member.server.roles, name='Access')
      await client.add_roles(member, role)
      await client.say("Gave access to {}".format(member))
      for channel in member.server.channels:
        if channel.name == 'server-log':
            embed=discord.Embed(title="User Got Access!", description="**{0}** got access from **{1}**!".format(member, ctx.message.author), color=0x020202)
            await client.send_message(channel, embed=embed)
            await asyncio.sleep(45*60)
            await client.remove_roles(member, role)



client.run('NTQ1OTc5MzE4ODc1MDYyMjkw.D0hj0g.Y55eynhXXNwkFkvmTJLqkW_fPoA')
