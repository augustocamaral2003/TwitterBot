from secrets import username, password, path

from TwitterBotClass import TwitterBot

#creates a bot using webdriver at indicated path
bot = TwitterBot(path)
#login with username and password
bot.login(username, password)
#goes to twitter main page (may be done after login to avoid bugs)
bot.main_page()
#goes to elon musk's page
bot.find_user('elonmusk')
#interact with 20 tweets (retweet and like)
bot.interact(20)