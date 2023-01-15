import bot_secrets
import discord
import handlers.ballot as ballot
#from discord.ext import commands
import interactions
import re

class Command(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client


    @interactions.extension_command(
        name="ping",
        description="You'll never guess what this one does!",
        default_scope=False
    )
    async def my_first_command(ctx: interactions.CommandContext):
        await ctx.send("Pong!")


def setup(client):
    Command(client)





