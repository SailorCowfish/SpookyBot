#!/usr/bin/env python3

import sys
import Polls
import movies
import os
import storage
import logging

from discord.ext import commands

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

pollFile = 'currentpoll.yaml'
movieFile = 'movielist.yaml'
configFile = 'botconfig.yaml'

required_configs = [ "bot_discord_token", "guild" ]
if os.path.exists(configFile):
    botConfig = storage.load(configFile)["config"]
    logging.debug("This is what botConfit holds %s", botConfig)
else:
    logging.critical("Unable to find config file, please create %s as described in the README", configFile)
    sys.exit(1)

for entry in required_configs:
    if entry not in botConfig:
        logging.crit("Required config entry %s not found in configuration.", entry)
        sys.exit(1)

TOKEN = botConfig['bot_discord_token']
GUILD = botConfig['guild']

if os.path.exists(pollFile):
    #Code to read file and save it as "pollData"
    logging.debug("Found file '%s'", pollFile)
    pollData = storage.load(pollFile)
    #Instantiate poll, passing it data and updating the isActive flag because we know a poll was already started. Poor bot probably died.
    logging.info("Restarting saved poll.")
    logging.debug("Using data %s", pollData)
    currentPoll = Polls.Poll(suggestion = pollData, isActive = True)
else:
    #Instantiate poll, without passing it data
    logging.info("Creating fresh poll")
    currentPoll = Polls.Poll()

if os.path.exists(movieFile):
    #Code to read file and save it as "movieList"
    logging.debug("Found file '%s'", movieFile)
    movieData = storage.load(movieFile)
    #Instantiate poll, passing it data and updating the isActive flag because we know a poll was already started. Poor bot probably died.
    logging.info("Loading saved movie list.")
    logging.debug("Using data %s", movieData)
    movieList = movies.MovieList(movieData)
else:
    movieList = movies.MovieList()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    logging.info("Connected to discord guild %s.", guild.name)
    logging.debug(f'{bot.user.name} is connected to the following guild: \n\n'
               f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    logging.debug(f'Guild Members:\n - {members}')

#Suggest a movie for movie night. User gives a title that is added to the MovieList.
@bot.command(name='suggest', help='This command saves a new movie title to the master movie list.', brief='Adds a new title to the movie list.', usage='MovieTitle')
async def bot_suggest(ctx, *title):

    titleStr = " ".join(title)

    if movieList.add(titleStr):
        storage.write(movieFile, movieList.movies)
        response = f'"{titleStr}" has been added to the movie list.'
    else:
        response = f'"{titleStr}" has already been suggested.'

    await ctx.send(response)


@bot.command(name='list', help='This command displays master movie list.', brief='Displays the movie list.')
async def bot_movieList(ctx):
    response = ""
    for index,movie in enumerate(movieList.movies):
        response = f'{response}\nMovieID: {index} - Title: {movie["title"]}'
    await ctx.send(response)

#Show the list of movies and their votes
@bot.command(name='status', help='If a poll is currently running a list of the movies being voted on as well as their current vote totals will be displayed. Otherwise it will ask you to start a poll.', brief='Displays the current polls movies and votes.')
async def bot_status(ctx):
    response = currentPoll.status()
    logging.debug('response=%s', response)

    await ctx.send(response)

#Vote for a movie. User uses the index to indicate title chosen.
@bot.command(name='vote', help='Use this command with a movie ID number to cast your vote.', brief='Records your movie choice.', usage='MovieID')
async def bot_vote(ctx, num):
    voter = ctx.message.author.name

    result = currentPoll.vote(voter, num)
    storage.write(pollFile, currentPoll.suggestion)
    if result is None:
        response = (f'Thanks for your vote {voter}!')
    else:
        response = result
    await ctx.send(response)


@bot.command(name='create', help='Creates a poll using the movie ID numbers from the mast movie list. There is no limit on the amount of movies a poll can contain.', brief='Starts a poll using MovieIDs.', usage='MovieID')
async def bot_start(ctx, *choices):
    choiceList = []
    response = f'{ctx.message.author.name} has started a poll! Please vote for one of the following:\n'

    for choice in choices:
        try:
            choice = int(choice)
        except ValueError:
            response = f'{choice} is not a number. Please give me a number.'
            await ctx.send(response)
            return

        choiceList.append(movieList.movies[choice]["title"])

    if currentPoll.start(choiceList):
        response = f'{response}{currentPoll.status()}'
        if not storage.write(pollFile, currentPoll.suggestion):
            response = (f"{response}\nCouldn't save the poll to a file"
                        f"after starting. Poll will not be saved (this is ok)")
    else:
        response = "Error starting the poll."

    await ctx.send(response)

@bot.command(name='close', help='This command closes the poll, tallies up all of the votes, announces the winner and removes the winning title from the master movie list.', brief='Ends the poll and announces the winner.')
async def bot_close(ctx):
    if not currentPoll.isActive:
        response = "There is no active poll to close."
        await ctx.send(response)

    currentPoll.close()
    response = f'The winner is {currentPoll.winner}! "{currentPoll.winner}" will be removed from the movie list.'
    await ctx.send(response)

    winnerIndex = movieList.getMovieID(currentPoll.winner)
    if winnerIndex is None:
        response = f"Hey boss, I couldn't find the ID of the winning movie. Halp."
        await ctx.send(response)

    else:
        movieList.remove([winnerIndex])
        os.remove(pollFile)
        storage.write(movieFile, movieList.movies)

@bot.command(name='remove', help='Removes any number of titles from the master movie list using MovieIDs', brief='Removes a movie(s) from the list.', usage='MovieID')
async def bot_remove(ctx, *num):
    titles = []
    for number in num:
        try:
            choice = int(number)
        except ValueError:
            response = f'{number} is not a number. Please give me a number.'
            await ctx.send(response)
            return
        titles.append(movieList.movies[choice]['title'])

    #For every "entry" in the list "num" from above, call int() to cast the string value to an integer and save it to a list contained within the remove function
    movieList.remove([int(entry) for entry in num])
    storage.write(movieFile, movieList.movies)
    response = f'{titles} has been removed from the movie list.'
    await ctx.send(response)


bot.run(TOKEN)

#--Future Features
#IMDB synopsis
