import discord_bot, json, user
from util import get_user

async def demote(executor, message, args, logger):
    target = get_user(message, 0, logger)
    if target is not None:
        new_rank = target.rank - 1
        if len(args) > 1:
            new_rank = user.ranks.index(args[1].lower().title())
        new_rank_name = user.ranks[new_rank]
        logger.log("Target identified as {}".format(json.dumps(target.hash())))
        if target._from_cache:
            logger.log("Target loaded from cache")
        else:
            logger.log("Target selected from database {}".format("(new)" if target._new else ""))
        if target.rank <= new_rank:
            await discord_bot.discord_bot.send_message(message.channel, "{} not a demotion".format(new_rank_name.title()))
        else:
            if target.demote(new_rank):
                await discord_bot.discord_bot.send_message(message.channel, "Demoted to {}".format(target.rank_name()))
            else:
                await discord_bot.discord_bot.send_message(message.channel, "No such rank avalible")
    else:
        await discord_bot.discord_bot.send_message(message.channel, "Thompson does not currently support username based demotion, please tag instead")
    logger.close()

exports = {
    "executor": demote,
    "rank": 2,
    "man": "Demotes the user from admin or the given rank"
}
