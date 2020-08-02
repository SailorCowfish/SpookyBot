#!/usr/bin/env python3

import Polls
import movies
import os
import storage
import logging

from discord.ext import commands

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

TOKEN = ''
GUILD = ''
pollFile = 'currentpoll.yaml'
movieFile = 'movielist.yaml'

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
@bot.command(name='suggest')
async def bot_suggest(ctx, *title):
	titleStr = " ".join(title)

	if movieList.add(titleStr):
		storage.write(movieFile, movieList.movies)
		response = f'"{titleStr}" has been added to the movie list.'
	else:
		response = f'"{titleStr}" has already been suggested.'

	await ctx.send(response)

#To Do:
#Remove movie list entry.

@bot.command(name='list')
async def bot_movieList(ctx):
	response = ""
	for index,movie in enumerate(movieList.movies):
		response = f'{response}\n{index} - {movie["title"]}'
	await ctx.send(response)

#Show the list of movies and their votes
@bot.command(name='status')
async def bot_status(ctx):
	response = currentPoll.status()
	logging.debug('response=%s', response)

	await ctx.send(response)

#Vote for a movie. User uses the index to indicate title chosen.
#This is broken. You need to figure out how to properly attribute a user's vote to them.
#Once this is fixed, make sure a user can change their vote. Be sure it's not just adding a new vote to the list (so they would get 2 votes instead of 1).
#Use ctx.message.author to find the name of the user who cast the vote.
@bot.command(name='vote')
async def bot_vote(ctx, num):
	voter = ctx.message.author.name

	result = currentPoll.vote(voter, num)
	storage.write(pollFile, currentPoll.suggestion)
	if result is None:
		response = (f'Thanks for your vote {voter}!')
	else:
		response = result
	await ctx.send(response)


@bot.command(name='create')
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

@bot.command(name='close')
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

@bot.command(name='remove')
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
