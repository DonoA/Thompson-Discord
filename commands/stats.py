import discord_bot, json
from util import get_user

async def stats(executor, message, args, logger):
    if len(args) == 0:
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(executor.hash()))
    else:
        user = get_user(message, 0, logger)
        await discord_bot.discord_bot.send_message(message.channel, json.dumps(user.hash()))
    logger.close()

exports = {
    "executor": stats,
    "man": "Prints stats on the current user or supplied user"
}
