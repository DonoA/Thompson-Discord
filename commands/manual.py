import discord_bot

async def manual(executor, message, args, logger):
    await discord_bot.discord_bot.send_message(message.channel, commands[args[0]]["man"])
    logger.close()

exports = {
    "executor": manual,
    "man": "Print manual info for a given command"
}
