import discord_bot, re, threading
from ideone_connector import Ideone

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

exports = {
    "executor": code_exec,
    "rank": 1,
    "man": "Execute a `code` sample or ```code\nblock``` in the given language"
}
