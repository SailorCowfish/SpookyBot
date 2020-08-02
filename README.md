#SpookyBot#
SpookyBot is a discord bot that keeps a running list of suggestions and allows users to facilitate polls and vote. It is currently designed with movies in mind.

A user !suggest(s) a movie which is added to the running list of movies. A poll is !create(d), users will !vote, and a winner will be chosen when the poll is !close(d). The winning title will then be removed from the movie list.

##Installation##
SpookyBot requires yaml and discord to function. Those can be installed with:
`pip -r requirements.text`

##Development Notes##
References to "ID" should be in all caps.
The Bot handles interactions with the file system.
"Polls" and "movies" handle polling and movie list functions.

##Future Projects##
IMDb synopsis listing
