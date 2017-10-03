# -*- coding: utf-8 -*-

import threading, queue, time

import Commands

class Crabot:
	
	cmds = {}
	responses = queue.Queue(10)
	
	def __init__(self, lst):
		for key in lst:
			obj = self.addChar(self.cmds, key[0])
			for c in key[1:]:
				obj = self.addChar(obj, c)
			obj["fun"] = getattr(Commands, lst[key])
		self.Respond(self.responses).start()
	
	def addChar(self, obj, char):
		if(not char in obj):
			obj[char] = {}
		return obj[char]
	
	def evalCmd(self, msg):
		if(not self.responses.full()):
			self.Cmd(msg, self.cmds, self.responses).start()
	
	class Respond(threading.Thread):
		
		def __init__(self, responses):
			super().__init__()
			self.responses = responses
		
		def run(self):
			while True:
				msg = self.responses.get()
				if(msg):
					print(msg)
				time.sleep(1)
	
	class Cmd(threading.Thread):
		
		def __init__(self, msg, cmds, responses):
			super().__init__()
			self.msg = msg
			self.cmds = cmds
			self.responses = responses
		
		def run(self):
			self.parser(self.msg)
		
		def parser(self, cmd):
			obj = self.cmds
			i = 0
			for c in cmd:
				if(c in obj):
					obj = obj[c]
				else:
					break
				i += 1
			
			if(callable(obj["fun"])):
				res = obj["fun"](cmd[i:])
				if(res):
					self.responses.put(res)


bot = Crabot({"!h" : "hello"})
for i in range(100):
	bot.evalCmd("!h Cap'n Odin")





