from slackclient import SlackClient
import json
import requests
from threading import Thread
from utils import*

slack_token = 'YOUR-SLACK-TOKEN-HERE'

slack_client = SlackClient(slack_token)

#just for example
allowedChannels = ['G7N3MRCCS','G7P2M4CCS']

#slack common utils
def isIntenedMessage(event):
	try:
		j = event['subtype']
		return False
	except:
		try:
			j = event['channel']
			return True
		except:
			return False

def isAllowedChannel(event,allowedChannels):
	try:
		return event['channel'] in allowedChannels
	except:
		return False

def isDM(channel):
	try:
		return channel.startswith("D")
	except:
		return False

def handle(event,triggerWord,callbacks,restrictions=None):
	'''
	Handles all the incomming command messages.
	:param event: slack event (json/dict format)
	:param triggerWord: The word that triggers the command. (EX: !echo)
	:param restrictions: A list of booleans that give the command special rules.
			EX: has to be in a certain channel, said by a certain person, etc.
	:param callbacks: List of functions to call when the parameters are satisfied.
	:return: None
	'''
	if restrictions == None:
		restrictions = []
	if event['text'].startswith(f"!{triggerWord}") and False not in restrictions:
		try:
			context = event['text'].split(f"!{triggerWord} ")[1]
		except:
			context = ""

		for callback in callbacks:
			Thread(target=callback(context,event), daemon=True).start()

def parseInput(events):
	for event in events:
		if event['type'] == 'message' and isIntenedMessage(event):
			try:
				handle(event,'echo',[echo],restrictions=[isAllowedChannel(event,allowedChannels)])
				handle(event,'user',[findUserByID],restrictions=[isDM(event['channel'])])
			except Exception as e:
				log(str(e),prefix="HANDLER ERROR",color='red')


#Example slackbot functions
def echo(context,event):
	Thread(
		target=slack_client.api_call,
		args=("chat.postMessage",),
	    kwargs=dict(
			channel=event['channel'],
			text=context
	    ),
		daemon=True
	).start()

def findUserByID(context,event):
	Thread(
		target=slack_client.api_call,
		args=("chat.postMessage",),
	    kwargs=dict(
			channel=event['channel'],
			text=f"User: <@{context}>"
	    ),
		daemon=True
	).start()




if __name__ == "__main__":
	if slack_client.rtm_connect(with_team_state=False):
		log("Bot connected and running!",prefix='SYSTEM',color='blue')
		# Read bot's user ID by calling Web API method `auth.test`
		id = slack_client.api_call("auth.test")["user_id"]
		while True:
			parseInput(slack_client.rtm_read())
	else:
		log("Connection failed.",prefix='SYSTEM',color='red')

