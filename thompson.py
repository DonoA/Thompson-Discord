import sql_connector
import discord_bot

def main():
    sql_connector.setup()
    discord_bot.start()

if __name__ == "__main__":
    main()
