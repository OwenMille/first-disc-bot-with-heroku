import discord
from discord.utils import find
import json
import random 
import os
import pandas
from secret import BOT_TOKEN

client = discord.Client()

"""
Heroku Hosting
Since we are using "local" images to heroku, replace 'C:/.../.../pictures' 
path with the '/app' path, where heroku stores project files
Also using heroku's  Config vars  which is why bot is run with 
' client.run(os.environ['BOT_TOKEN']) '
"""
path = '/app'
sdc_posts = os.listdir(path)

sdc_story_files = ['']
for x in os.listdir(path):
    if x.startswith('tory'):
        sdc_story_files.append(x)

def write_json(data, filename='data.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["idea_submissions"].append(data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}! Type !c to see a list of commands.'.format(guild.name))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!commands'):
        await message.channel.send('AquaBot current commands: !stilldontcae or !sdc to get a random post from @stilldontcae on Instagram (!ssdcs gives a random story post)')
        await message.channel.send('Use  !idea to submit an idea for more stuff for AquaBot to do.')

    if message.content.startswith('!c'):
        await message.channel.send('AquaBot current commands: !stilldontcae or !sdc to get a random post from @stilldontcae on Instagram (!ssdc gives a random story post)')
        await message.channel.send('Use  !idea to submit an idea for more stuff for AquaBot to do.')

    if message.content.startswith('!stilldontcae'):
        with open(sdc_posts[random.randrange(0,len(sdc_posts)-1)], 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

    if message.content.startswith('!sdc'):
        with open(sdc_posts[random.randrange(0,len(sdc_posts)-1)], 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

    if message.content.startswith('!story stilldontcae'):
        with open(sdc_story_files[random.randrange(0,len(sdc_story_files)-1)], 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

    if message.content.startswith('!ssdc'):
        with open(sdc_story_files[random.randrange(0,len(sdc_story_files)-1)], 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)


    if message.content.startswith('!idea'):
        data = pandas.DataFrame(columns=['content', 'time', 'author'])

        def is_command (msg): # Checking if the message is a command call
            if len(msg.content) == 0:
                return False
            elif msg.content.split()[0] == '_scan':
                return True
            else:
                return False
        
        limit=1
        async for msg in message.channel.history(limit=1): 
            if msg.author != client.user:                            
                if not is_command(msg):                                 
                    data = {'content': msg.content,
                            'time': str(msg.created_at),
                            'author': msg.author.name}
                    write_json(data)
                if len(data) == limit:
                    break
            
print(len(sdc_posts)-1)
print(len(sdc_story_files)-1)

client.run(BOT_TOKEN)
client.run(os.environ['BOT_TOKEN'])