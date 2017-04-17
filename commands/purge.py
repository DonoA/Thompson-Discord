import discord_bot, json, re, user
from user import User
from sql_connector import connection

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
            user.purge_cache()
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

exports = {
    "executor": purge,
    "rank": 2,
    "man": "Purge data from the database or a cache"
}
