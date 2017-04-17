import discord_bot, re, sys
from subprocess import call, check_output, Popen

async def update(executor, message, args, logger):
    call(["git", "fetch", "origin"])
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

exports = {
    "executor": update,
    "rank": 1,
    "man": "Restarts Thompson and updates his software"
}
