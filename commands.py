import discord_bot, json, os, sys, re, asyncio, random, os.path
from user import User
from util import get_user
from subprocess import call, check_output, Popen
from sql_connector import connection
from config import config
import threading, user
from ideone_connector import Ideone
from debugger import Logger

async def stats(executor, message, args, logger):
    if len(args) == 0:
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(executor.hash()))
    else:
        user = get_user(message, 0, logger)
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(user.hash()))
    logger.close()

async def promote(executor, message, args, logger):
    target = get_user(message, 0, logger)
    if target is not None:
        logger.log("Target identified as {}".format(json.dumps(target.hash())))
        if target._from_cache:
            logger.log("Target loaded from cache")
        else:
            logger.log("Target selected from database {}".format("(new)" if target._new else ""))
        if target.rank == 2:
            await discord_bot.discord_bot.send_message(message.channel, "Already an admin")
        else:
            target.promote()
            await discord_bot.discord_bot.send_message(message.channel, "Promoted to {}".format(target.rank_name()))
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based promotion, please tag instead")
    logger.close()

async def demote(executor, message, args, logger):
    target = get_user(message, 0, logger)
    if target is not None:
        logger.log("Target identified as {}".format(json.dumps(target.hash())))
        if target._from_cache:
            logger.log("Target loaded from cache")
        else:
            logger.log("Target selected from database {}".format("(new)" if target._new else ""))
        if target.rank == 0:
            await discord_bot.discord_bot.send_message(message.channel, "Cannot demote below regular")
        else:
            target.demote()
            await discord_bot.discord_bot.send_message(message.channel, "Demoted to {}".format(target.rank_name()))
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based demotion, please tag instead")
    logger.close()


async def update(executor, message, args, logger):
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

async def reboot(executor, message, args, logger):
    await discord_bot.discord_bot.send_message(message.channel, "Shutting down for reboot!")
    print("Shutting down for reboot!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    os.execl(sys.executable, *([sys.executable]+sys.argv))

async def manual(executor, message, args, logger):
    await discord_bot.discord_bot.send_message(message.channel, commands[args[0]]["man"])
    logger.close()

async def purge(executor, message, args, logger):
    if args[0] == "users":
        cursor = connection.cursor()
        logger.log("Executing ```TRUNCATE TABLE `users`;```")
        cursor.query("TRUNCATE TABLE `users`;")
        connection.commit()
        cursor.close()
        await discord_bot.discord_bot.send_message(message.channel, "Clearing all users from database!")
    elif args[0] == "user":
        if args[1] == "cache":
            logger.log("User cache before purge {}".format(str(user.cache)))
            User.purge_cache()
            logger.log("User cache after purge {}".format(str(user.cache)))
            await discord_bot.discord_bot.send_message(message.channel, "Clearing all users from user model cache!")
        else:
            target = re.findall(r'<@(.+)>', args[1])
            if len(target) > 0:
                target = User.find(target[0])
                logger.log("Target identified as {}".format(json.dumps(target.hash())))
                if target._from_cache:
                    logger.log("Target loaded from cache")
                else:
                    logger.log("Target selected from database {}".format("(new)" if target._new else ""))
                target.purge()
                await discord_bot.discord_bot.send_message(message.channel, "Removed {} from the database!".format(target.name))
            else:
                await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based puring, please tag instead")
    logger.close()

async def code_exec(executor, message, args, logger):
    code = re.findall(r'`{3}((.|[\n])+)`{3}', message.content)
    if len(code) == 0:
        code = re.findall(r'`((.|[\n])+)`', message.content)
    code = code[0][0]
    msg = await discord_bot.discord_bot.send_message(message.channel, "Compiling...")
    ideone = Ideone(code, args[0], logger)
    thr = threading.Thread(target=ideone.execute)
    thr.daemon = True
    thr.start()
    dots = 0
    while thr.is_alive():
        dots = dots + 1
        await discord_bot.discord_bot.edit_message(msg, "Compiling{}".format('.'*dots))
        if dots == 3:
            dots = 0
        await asyncio.sleep(1)
    dots = 0
    while ideone.std_out is None and ideone.error is None:
        dots = dots + 1
        ideone.fetch_results()
        await discord_bot.discord_bot.edit_message(msg, "Compiled to {}\n Fetching results{}".format(ideone.id, '.'*dots))
        if dots == 3:
            dots = 0
        await asyncio.sleep(1)
    print(ideone.std_out)
    if ideone.std_out:
        await discord_bot.discord_bot.edit_message(msg, "Result:\n```\n\n{}```".format(ideone.std_out))
    else:
        await discord_bot.discord_bot.edit_message(msg, "Error: ".format(ideone.error))
    logger.close()

async def analysis(executor, message, args, logger):
    await discord_bot.discord_bot.send_message(message.channel, "\n".join(Logger.recall_last()))
    logger.close()

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
    "reboot": {
        "executor": reboot,
        "rank": 1,
        "man": "Restarts Thompson"
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
    },
    "analysis": {
        "executor": analysis,
        "rank": 2,
        "man": "print analysis for last executed command"
    }
}
