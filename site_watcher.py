from threading import Thread
from splinter import Browser
import discord_bot

class SiteWatch(Thread):

    def __init__(self, url, xpath, timeout, total_time, logger, channel):
        self.url = url
        self.xpath = xpath
        self.timeout = timeout
        self.total_time = total_time
        self.logger = logger.log
        self.message = await discord_bot.discord_bot.send_message(channel, "Fetching...")
        self.fetch()

    def fetch(self):
        with Browser() as browser:
            self.logger("Screen ready")
            browser.visit(self.url)
            val = browser.find_by_xpath(self.xpath).first["text"]
            await discord_bot.discord_bot.edit_message(self.message, val)
