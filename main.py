import bot_secrets
import interactions

def main():

        print("Starting bot...")
        bot = interactions.Client(bot_secrets.TOKEN)
        bot.load("handlers.command")
        

        bot.start()

if __name__ == "__main__":
    main()