import discord_bot, json, os, sys, re, asyncio, random, os.path
from user import User
from util import get_user
from subprocess import call, check_output, Popen
from config import config
import threading
from ideone_connector import ideone

async def stats(executor, message, args):
    if len(args) == 0:
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(executor.hash()))
    else:
        user = get_user(message, 0)
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(user.hash()))

async def promote(executor, message, args):
    target = get_user(message, 0 if message[0]=="$" else 1)
    if target is None:
        if target.rank == 2:
            await discord_bot.discord_bot.send_message(message.channel, "Already an admin")
        else:
            target.promote()
            await discord_bot.discord_bot.send_message(message.channel, "Promoted to {}".format(target.rank_name()))
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based promotion, please tag instead")

async def demote(executor, message, args):
    target = get_user(message, 0 if message[0]=="$" else 1)
    if target is None:
        if target.rank == 0:
            await discord_bot.discord_bot.send_message(message.channel, "Cannot demote below regular")
        else:
            target.demote()
            await discord_bot.discord_bot.send_message(message.channel, "Demoted to {}".format(target.rank_name()))
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based demotion, please tag instead")

async def update(executor, message, args):
    diff = check_output(["git", "rev-list", "--left-right", "--count", "origin/master...master"])
    diff = re.findall(r'([0-9]+)[ \t]', diff.decode("utf-8"))[0]
    if int(diff) > 0:
        await discord_bot.discord_bot.send_message(message.channel,
                    "Found {} new updates to install, will now update".format(diff))
        print("Gitting latest master version")
        call(["git", "pull", "origin", "master"])
        await discord_bot.discord_bot.send_message(message.channel, "Updated, shutting down for reboot!")
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Shutting down for reboot!")
    print("Shutting down for reboot!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    os.execl(sys.executable, *([sys.executable]+sys.argv))

async def manual(executor, message, args):
    await discord_bot.discord_bot.send_message(message.channel, commands[args[0]]["man"])

async def purge(executor, message, args):
    if args[0] == "users":
        await discord_bot.discord_bot.send_message(message.channel, "Clearing all users from database!")
    elif args[0] == "user":
        if args[1] == "cache":
            User.purge_cache
            await discord_bot.discord_bot.send_message(message.channel, "Clearing all users from user model cache!")
        else:
            target = re.findall(r'<@(.+)>', args[1])
            if len(target) > 0:
                target = User.find(target[0])
                target.purge()
                await discord_bot.discord_bot.send_message(message.channel, "Removing {} from the database!".format(target.name))
            else:
                await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based puring, please tag instead")

async def code_exec(executor, message, args):
    code = re.findall(r'`{3}((.|[\n])+)`{3}', message.content)
    if len(code) == 0:
        code = re.findall(r'`((.|[\n])+)`', message.content)
    code = code[0][0]
    msg = await discord_bot.discord_bot.send_message(message.channel, "Compiling...WIP, not working just yet!")

    # while not os.path.isfile("ide_swap/{}.out".format(token)):
    #     if not thr.poll():
    #         await discord_bot.discord_bot.edit_message(msg, "An error was thrown, unable to execute")
    #         return
    #     print("sleeping")
    #     print(thr.poll())
    #     await asyncio.sleep(1)
    #
    # with open("ide_swap/{}.out".format(token)) as swap:
    #     result = json.load(swap)
    #     await discord_bot.discord_bot.edit_message(msg, 'Result:```{}```'.format(result['output']))

commands = {
    "stats": {
        "executor": stats,
        "man": "Prints stats on the current user or supplied user"
    },
    "promote": {
        "executor": promote,
        "rank": 2,
        "man": "Promotes the user to admin"
    },
    "demote": {
        "executor": demote,
        "rank": 2,
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
        "rank": 2,
        "man": "Purge data from the database or a cache"
    },
    "exec": {
        "executor": code_exec,
        "rank": 1,
        "man": "Execute a `code` sample or ```code\nblock``` in the given language"
    }
}
