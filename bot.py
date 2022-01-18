import discord
from discord.ext import commands
from game import Game
from colors import *

TOKEN = "YOUR TOKEN HERE"

client = commands.Bot(command_prefix="!")
# dict of username, Game
current_games = {}
# dict of message id, username
current_messages = {}

@client.event
async def on_ready():
    print("Bot is on")

@client.command(pass_context=True)
async def newgame(ctx, args="25 white brown black"):
    arg_list = args.split()
    game = Game(int(arg_list[0]), arg_list[1:])
    embed = discord.Embed(
        title = game.title(),
        description = game.content(),
    )
    embed.set_author(name=str(ctx.message.author))
    msg = await ctx.send(embed=embed)

    # update the current game/msg for the user
    current_games[str(ctx.message.author)] = game
    current_messages[msg.id] = str(ctx.message.author)

    # add a reaction for each square
    reactions = [EMOJIS[color] for color in game.colors]
    for rxn in reactions:
        await msg.add_reaction(rxn)

@client.event
async def on_reaction_add(reaction, user):
    # whose game does the reacted message belongs to
    msg = reaction.message
    player = current_messages[msg.id]

    # make a move if the correct player made the reaction
    if str(player) == str(user):
        game = current_games[str(player)]
        reactions = game.get_reaction_emojis()
        rxn_val = reactions.index(reaction.emoji)
        game.make_move(rxn_val)

        # update the embed for the message
        embed = discord.Embed(
            title = game.title(),
            description = game.content(),
        )
        embed.set_author(name=str(player))
        await msg.edit(embed=embed)

    # remove the reaction if not from the bot
    if user != client.user:
        await reaction.remove(user)

@client.command(pass_context=True)
async def colors(ctx):
    msg_text = "The available colours are:\n"
    for i in range(len(COLORS)):
        msg_text += f"{EMOJIS[COLORS[i]]} {COLORS[i]}\n"
    await ctx.send(msg_text)

@client.command(pass_context=True)
async def howto(ctx):
    msg_text = ('Use !newgame to start your own new game.\n\n' 
    'To enter parameters, use double quotes and the format "num_turns  unused_colours"' 
    ', e.g. !newgame "40 red blue white".\n\n' 
    'If no parameters are entered, the default values of "25 white brown black" are used.')
    
    await ctx.send(msg_text)

@client.command(pass_context = True)
async def clean(ctx, n):
    msgs = [] 
    chnl = ctx.message.channel
    async for x in chnl.history(limit = int(n)):
        if x.author == client.user:
            msgs.append(x)
    for msg in msgs:
        await msg.delete()

client.run(TOKEN)

