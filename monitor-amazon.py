import config
import feedparser
import logging
from twitter import *
from twilio.rest import TwilioRestClient

logging.basicConfig(filename='/Users/mireynol/logs/amazon-search.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Your Account Sid and Auth Token from twilio.com/user/account
client = TwilioRestClient(config.twilio["account_sid"], config.twilio["auth_token"]) 

amazon_gold_deals_rss = "http://rssfeeds.s3.amazonaws.com/goldbox"
feed = feedparser.parse(amazon_gold_deals_rss)

rss_count = 0
twitter_count = 0

for item in feed["items"]:
	rss_count = rss_count + 1
	if "Toshiba" in item["title"] and "TV" in item["title"]:
		logging.debug('We found it: ' + item["title"] + " - " + item["link"])
		
		message = client.messages.create(body=item["title"] + " - " + item["link"],
		    to="+18067861300",    # Replace with your phone number
		    from_=config.twilio["phone_number"]) # Replace with your Twilio number
		message = client.messages.create(body=item["title"] + " - " + item["link"],
		    to="+18064382579",    # Replace with your phone number
		    from_=config.twilio["phone_number"]) # Replace with your Twilio number


logging.debug("Checked Gold Deals RSS: " + str(rss_count))

# Twitter checking as well
t = Twitter(auth=OAuth(config.twitter["token"], config.twitter["token_secret"], config.twitter["api_key"], config.twitter["api_secret"]))

statuses = t.statuses.user_timeline(screen_name="amazondeals")

for status in statuses:
	twitter_count = twitter_count + 1
	if "Toshiba" in status['text'] and "TV" in status['text']:
		logging.debug("We found it on Twitter: " + status['text'])
		message = client.messages.create(body=status['text'],
		    to="+18067861300",    # Replace with your phone number
		    from_="+18064170145") # Replace with your Twilio number
		message = client.messages.create(body=status['text'],
		    to="+18064382579",    # Replace with your phone number
		    from_="+18064170145") # Replace with your Twilio number


logging.debug("Checked Twitter: " + str(twitter_count))
