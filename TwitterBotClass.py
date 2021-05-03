from selenium import webdriver
from time import sleep

class TwitterBot():
	def __init__(self, path):
		self.driver = webdriver.Chrome(executable_path=path)
		self.is_logged = False
		self.current_user = ''
		self.path = path

	def login(self, username : str, password : str):
		"""
		Login using provided username and password

		Parameters
		----------
		username : str
			the username to login into
		password : str
			the password
		"""

		self.driver.get('https://twitter.com/login')
		sleep(2)

		username_in = self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
		username_in.clear()
		username_in.send_keys(username)

		password_in = self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
		password_in.clear()
		password_in.send_keys(password)
		sleep(2)

		login_btn = self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
		login_btn.click()

		self.is_logged = True

	def find_user(self, user, replies=True):
		"""
		Find user Twitter's homepage

		Parameters
		----------
		user : str
			user to be found
		replies : bool
			if True, redirects to user 'Tweets & Replies' page, otherwise redirects to 'Tweets' page
		"""

		path = 'https://twitter.com/' + user
		if replies:
			path += '/with_replies'
		self.driver.get(path)
		self.current_user = user
		sleep(1)

	def main_page(self):
		"""
		Redirects to Twitter's main page
		"""

		self.driver.get('https://twitter.com')
		sleep(1)

	def interact(self, iterations : int, retweet=True, like=True, delete=True):
		"""
		interact with tweets that has the current_user string (tweets by the user and tweets that mention the user).

		Parameters
		----------
		iterations : int
			number of tweets to interact with, include non-tweets (suggestion or tweet that was replied)
		retweet : bool
			if interaction includes retweeting
		like : bool
			if interaction includes liking
		delete : bool
			if tweet will be deleted after interaction (helps cleaning the page for further interaction)
		"""

		if not self.is_logged:
			raise Exception("You must log in first.")

		for i in range(iterations):
			try:
				tweets = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div")
				tweet = tweets.find_element_by_xpath(".//div")
				stats = tweet.find_element_by_xpath("//div[@role='group']").get_attribute('aria-label')
			except:
				stats = ''
				sleep(0.3)
				continue

			if self.current_user in tweet.text:
				retweet = tweet.find_element_by_xpath("//div[@data-testid='retweet']")
				like =  tweet.find_element_by_xpath("//div[@data-testid='like']")

				try:
					if "Retweeted" not in stats and retweet:
						retweet.click()
						sleep(0.5)
						self.driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']").click()

					if "Liked" not in stats and like:
						like.click()
						sleep(0.5)
						
					if delete:
						self.driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", tweet)
						sleep(0.5)
				except:
					if delete:
						self.driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", tweet)

			elif delete:
				self.driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", tweet)
				sleep(0.3)
				continue