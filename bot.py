#Author Mike Terranova

import time
import os
import sys
import re
import urllib
import json
import requests

#might be using a class? Dunno, maybe just a main function that'll use all our functions

class Bot:
	def _init_():
		self.groupID = 	
		self.botID = 	
def message(request):
	text = body['text']
	text = text.lower()
	if 'meseeks' in text:
		args = text.split('')
		groupID = 
		botID = 
		msgOut = {'bot_id':botID, 'text' : " Look at me! I'm Mr.Meseeks"}
		print("sending message")
		r = requests.post("", data = msgOut)

def start():
	Bot._init_()
	while 1:
		message()

