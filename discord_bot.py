import discord
from config import config
from user import User
import commands

discord_bot = discord.Client()

@discord_bot.event
async def on_ready():
    print("Configuring bot named {} - {}".format(discord_bot.user.name, discord_bot.user.id))
    print("======")

@discord_bot.event
async def on_message(message):
    if message.author.id == discord_bot.user.id:
        return
    called = "thompson" in message.content.lower() or discord_bot.user.id in message.raw_mentions
    commanded = message.content[0] == "$"
    args = message.content.split(" ")
    sender = User.find(message.author.id, name=message.author.name)
    if commanded or called:
        if commanded:
            args[0] = args[0][1:]
        if args[0] not in commands.commands and commanded:
            await discord_bot.send_message(message.channel, "Unknown command executed")
        else:
            cmd = commands.commands[args[0]]
            if sender.has_perm(cmd):
                if ('args' in cmd and cmd['args'] <= len(args)-1) or 'args' not in cmd:
                    await cmd['executor'](sender, message, args[1:])
                else:
                    await commands.commands['man']['executor'](sender, message, args)
            else:
                await discord_bot.send_message(message.channel, "You have insufficient permissions to preform this action")

def start():
    discord_bot.run(config['client_id'])
