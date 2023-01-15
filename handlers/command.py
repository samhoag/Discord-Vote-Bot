import handlers.ballot as ballot
#from discord.ext import commands
import interactions
import re

class Command(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client


    ''' === ELECTION COMMANDS === '''
    @interactions.extension_command(
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
    async def createelection(self, ctx: interactions.CommandContext, election_name: str, candidates: str):
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


        election = ballot.Election(election_name, validated_candidates_list, "TEST GUILD")
        
        await ctx.send("Election created with name: `" + election_name + "`, ID: `" + election.id + "` and candidates: " + candidate_tags + "\n" +
                        "The following candidates were unable to be added: " + not_added_candidates + "\n" +
                        "*please verify that they are not bots, roles, or plain text and that they are in this discord*")

    @interactions.extension_command(
        name="vote",
        description="Request a ballot",
        default_scope=False
    )
    async def vote(self, ctx):
        # SelectMenu : which election?

        # SelectMenu(s) : 1 per each candidate

        



        await ctx.author.send("BALLOT")
        await ctx.send("Please check your DM's for a ballot!", ephemeral=True)



    @interactions.extension_command(
        name="close-polls",
        description="Ends the current election",
        default_scope=False
    )
    async def closepolls(self, ctx, arg):
        await ctx.send(ballot.end_election())    

    ''' === MISC COMMANDS === '''

    @interactions.extension_command(
        name="ping",
        description="You'll never guess what this one does!",
        default_scope=False
    )
    async def my_first_command(self, ctx: interactions.CommandContext):
        await ctx.send("Pong!")

    @interactions.extension_command(
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
    async def parrot(self, ctx: interactions.CommandContext, text: str):
        await ctx.send(f"'{text}'!")

    ''' === MENU TESTING === '''

    @interactions.extension_command(
        name="button_test",
        description="This is the first command I made!",
        default_scope=False,
    )
    async def button_test(self, ctx):
        select_menu = interactions.SelectMenu(
        options=[interactions.SelectOption(
            label="I'm a cool option. :)",
            value="internal_option_value",
            description="some extra info about me! :D",
        )],
        placeholder="Check out my options. :)",
        custom_id="menu_component",
    )

        await ctx.send("testing", components=select_menu)

    @interactions.extension_component("hello")
    async def button_response(self, ctx):
        await ctx.send("You clicked the Button :O", ephemeral=False) #ephemeral makes the message visible only to the command sender?



def setup(client):
    Command(client)





