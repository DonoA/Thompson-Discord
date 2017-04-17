import discord_bot, os, sys

async def reboot(executor, message, args, logger):
    await discord_bot.discord_bot.send_message(message.channel, "Shutting down for reboot!")
    print("Shutting down for reboot!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    os.execl(sys.executable, *([sys.executable]+sys.argv))

exports = {
    "executor": reboot,
    "rank": 1,
    "man": "Restarts Thompson"
}
