import sql_connector
import discord_bot
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

def main():
    sql_connector.setup()
    discord_bot.start()

if __name__ == "__main__":
    main()
