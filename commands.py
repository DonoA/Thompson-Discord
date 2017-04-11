import discord_bot, json
from user import User
from util import get_user

async def stats(executor, message, args):
    if len(args) < 1:
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(executor.hash()))
    else:
        user = get_user(message, 0)
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(user.hash()))

async def promote(executor, message, args):
    target = get_user(message, 0 if message[0]=="$" else 1)
    if target is None:
        if target.rank == 1:
            await discord_bot.discord_bot.send_message(message.channel, "Already an admin")
        else:
            target.set_rank(1)
            target.commit()
            await discord_bot.discord_bot.send_message(message.channel, "Promoted")
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based promotion, please tag instead")

async def demote(executor, message, args):
    target = get_user(message, 0 if message[0]=="$" else 1)
    if target is None:
        if target.rank == 0:
            await discord_bot.discord_bot.send_message(message.channel, "Cannot demote below regular")
        else:
            target.set_rank(0)
            target.commit()
            await discord_bot.discord_bot.send_message(message.channel, "Demoted")
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based demotion, please tag instead")

async def update(executor, message, args):
    discord_bot.discord_bot.send_message(message.channel, "WIP")

async def manual(executor, message, args):
    await discord_bot.discord_bot.send_message(message.channel, commands[args[(1 if args[0] == "man" else 0)]]["man"])

async def purge(executor, message, args):
    if args[1] == "users":
        await discord_bot.discord_bot.send_message(message.channel, "Clearing all users from database!")
    elif args[1] == "user":
        if args[2] == "cache":
            User.purge_cache
            await discord_bot.discord_bot.send_message(message.channel, "Clearing all users from user model cache!")
        else:
            target = re.findall(r'<@(.+)>', args[2])
            if len(target) > 0:
                target = User.find(target[0])
                target.purge()
                await discord_bot.discord_bot.send_message(message.channel, "Removing {} from the database!".format(args[2]))
            else:
                await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based puring, please tag instead")


commands = {
    "stats": {
        "executor": stats,
        "man": "Prints stats on the current user or supplied user"
    },
    "promote": {
        "executor": promote,
        "rank": 1,
        "man": "Promotes the user to admin"
    },
    "demote": {
        "executor": demote,
        "rank": 1,
        "man": "Demotes the user from admin"
    },
    "update": {
        "executor": update,
        "rank": 1,
        "man": "Restarts Thompson and updates his software"
    },
    "man": {
        "executor": manual,
        "man": "Print manual info for a given command"
    },
    "purge": {
        "executor": purge,
        "rank": 1,
        "man": "purge data from the database or a cache"
    }
}
