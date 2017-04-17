import discord_bot
from debugger import Logger

async def analysis(executor, message, args, logger):
    if len(args) > 0:
        if int(args[0]) < 5:
            await discord_bot.discord_bot.send_message(message.channel, "\n".join(Logger.recall(args[0])))
        else:
            await discord_bot.discord_bot.send_message(message.channel, "Dist out of range")
    else:
        await discord_bot.discord_bot.send_message(message.channel, "\n".join(Logger.recall(1)))
    logger.close()

exports = {
    "executor": analysis,
    "rank": 2,
    "man": "print analysis for last executed command"
}
