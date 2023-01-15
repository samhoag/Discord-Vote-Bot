# This example requires the 'message_content' intent.
# https://discord.com/oauth2/authorize?client_id=1063106733528076318&permissions=8&scope=bot
import bot_secrets
import discord
import ballot_handler
#from discord.ext import commands
import interactions
import re

intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
bot = interactions.Client(bot_secrets.TOKEN)

prefix = '!'

@bot.event
async def on_ready():
    print(f'We have logged in!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        await bot.process_commands(message)
    if message.content.startswith(prefix):
        if message.content.startswith(prefix + 'hello'):
            
            await message.channel.send('Hello!')

        elif message.content.startswith(prefix + 'vote'):
            # Send DM to user who issused the command
            # Check if user has already voted
            # If yes
            #   "Sorry, you can only vote once!"
            # Else 
            #   Ballot

            await message.author.send('👋')

            #if message.author == client.user:
        elif message.content.startswith(prefix + 'closepollsold'):
            await message.channel.send(ballot_handler.end_election())
        elif message.content.startswith(prefix + "create-election"):
            
            election = ballot_handler.Election("test election", message.mentions)
            candidate_tags = ""
            for m in message.mentions:
                candidate_tags += '<@' + str(m.id) + '>, '
            await message.channel.send("Election created with ID: `" + election.id + "` and candidates: " + candidate_tags)


    # Checks if the message was recieved in a DM channel
    elif isinstance(message.channel, discord.DMChannel):
        votes = ballot_handler.parse_raw_ballot(message.content)
        ballot_handler.cast_ballot(votes)

        await message.channel.send("Ballot recieved!")

''' === ELECTION COMMANDS === '''
@bot.command(
    name="create-election",
    description="Creates a new election",
    default_scope=False,
    options = [
        interactions.Option(
            name="election_name",
            description="What do you want to call the election?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="candidates",
            description="Who will be running in the election?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def createelection(ctx: interactions.CommandContext, election_name: str, candidates: str):
    # Candidate here will be a list [nickname, id, discord tag]

    raw_candidates_list = candidates.split(' ')
    validated_candidates_list = []

    not_added_candidates = ""
    candidate_tags = ""
    guild = await ctx.get_guild()
    for c in raw_candidates_list:
        id = re.sub('[^0-9]','', c)
        try:
            member = await guild.get_member(id)
        except:
            not_added_candidates += c + " "
            continue

        if not member.user.bot:
            validated_candidates_list.append([member.name, member.id, member.user.username + "#" + member.user.discriminator])
            candidate_tags += c + " "
        else:
            not_added_candidates += c + " "


    election = ballot_handler.Election(election_name, validated_candidates_list, "TEST GUILD")
    
    await ctx.send("Election created with name: `" + election_name + "`, ID: `" + election.id + "` and candidates: " + candidate_tags + "\n" +
                    "The following candidates were unable to be added: " + not_added_candidates + "\n" +
                    "*please verify that they are not bots, roles, or plain text and that they are in this discord*")

@bot.command(
    name="vote",
    description="Request a ballot",
    default_scope=False
)
async def vote(ctx):
    # SelectMenu : which election?

    # SelectMenu(s) : 1 per each candidate

     



    await ctx.author.send("BALLOT")
    await ctx.send("Please check your DM's for a ballot!", ephemeral=True)



@bot.command(
    name="close-polls",
    description="Ends the current election",
    default_scope=False
)
async def closepolls(ctx, arg):
    await ctx.send(ballot_handler.end_election())    

''' === MISC COMMANDS === '''
@bot.command(
    name="ping",
    description="You'll never guess what this one does!",
    default_scope=False
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Pong!")

@bot.command(
    name="parrot",
    description="Polly want a cracker!",
    default_scope=False,
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def parrot(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"'{text}'!")

''' === MENU TESTING === '''
select_menu = interactions.SelectMenu(
    options=[interactions.SelectOption(
        label="I'm a cool option. :)",
        value="internal_option_value",
        description="some extra info about me! :D",
    )],
    placeholder="Check out my options. :)",
    custom_id="menu_component",
)

@bot.command(
    name="button_test",
    description="This is the first command I made!",
    default_scope=False,
)
async def button_test(ctx):
    await ctx.send("testing", components=select_menu)

@bot.component("hello")
async def button_response(ctx):
    await ctx.send("You clicked the Button :O", ephemeral=False) #ephemeral makes the message visible only to the command sender?



bot.start()
