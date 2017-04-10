import discord, asyncio, json
import schema
from commands import Commands

with open('config.json') as conf:
    CONFIG = json.load(conf)

ADMINS = [
    '144668502928654336'
]

cnx = mysql.connector.connect(**CONFIG['db'], host='127.0.0.1')

schema.setup(cnx)

cmds = Commands(cnx)

client = discord.Client()

@client.event
async def on_ready():
    print("Configuring bot named {} - {}".format(client.user.name, client.user.id))
    print("======")

@client.event
async def on_message(message):
    tagged = client.user.id in message.raw_mentions
    if (tagged or message.server.id in CONFIG['servers']) and not message.author.bot:
        cmds.handle(message.content, tagged)


client.run(CONFIG['client_id'])
