# TwitterBot

twitter bot written in python with basic retweet and like functions

## functionalities

- retweet
- like
- find user page

## usage

import `TwitterBot` to your Python3 project:

	from TwitterBotClass import TwitterBot
	
create a `TwitterBot` object and authenticate:

	bot = TwitterBot(path)
	bot.login(username, password)
	bot.main_page()
	
go to some user's page and like 10 tweets

	bot.find_user('elonmusk')
	bot.interact(10, retweet=False, like=True)
