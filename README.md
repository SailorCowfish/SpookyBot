# SpookyBot
SpookyBot is a discord bot that keeps a running list of suggestions and allows users to facilitate polls and vote. It is currently designed with movies in mind.

A user !suggest(s) a movie which is added to the running list of movies. A poll is !create(d), users will !vote, and a winner will be chosen when the poll is !close(d). The winning title will then be removed from the movie list.

## Installation
SpookyBot requires yaml and discord to function. Those can be installed with:

`pip -r requirements.text`

You will need to use the botconfig.yaml file to store the bot token that was issued from discord as well as your guild ID. A template file "botconfig.yaml.dist" has been provided as a template for this purpose. Be sure to remove ".dist" before implementing this bot.

## Bot Scope
As stated in the top description this bot is currently designed to be a movie polling service. A user should be able to:

* Add and remove a movie to the master list of movies

  * The master list of movies should be perpetual

* Create a poll from the movies in the master list

* Close a poll, triggering a winner announcement

  * Polls should be maintained until they are closed

  * Winners should be removed from the master list of movies

#### Guiding ideas:

1. Polls should be easy for users to understand and should not contain too many options or options users don't care about.

2. Polls should be time agnostic to allow for user flexibility.

3. Users shouldn't be able to interfere with or rig a poll.

4. Data should be saved regularly in case of bot misbehavior.

5. Users shouldn't be spammed with information from the bot.

## Development Requirements
References to "ID" should be in all caps.

Use camel casing.

Be sure to include help information for any new commands with "help", "brief", and "usage" if applicable.

The Bot handles interactions with the file system.

"Polls" and "movies" handle polling and movie list functions.

## Development Contributions

Contributors should submit a pull request for review. Pull requests that do not fit within the scope or adhere to requirements will be rejected. Pull requests are expected to be tested and fully functional before submission.

## Future Feature Plans by SailorCowfish
IMDb synopsis listing

"Volunteer" command to signify the user has or is willing to purchase a copy of a specific movie

Bug fixes for movie list

Catches to prevent users from interferring in polls
