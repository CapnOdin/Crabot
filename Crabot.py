# -*- coding: utf-8 -*-

import threading, queue, time
import Commands

class Crabot:
	
	cmds = {}
	responses = queue.Queue(10)
	
	def __init__(self, lst, callback):
		for key in lst:
			obj = self.addChar(self.cmds, key[0])
			for c in key[1:]:
				obj = self.addChar(obj, c)
			obj["fun"] = getattr(Commands, lst[key])
		self.Respond(self.responses, callback).start()
	
	def addChar(self, obj, char):
		if(not char in obj):
			obj[char] = {}
		return obj[char]
	
	def evalCmd(self, msg):
		if(not self.responses.full()):
			self.Cmd(msg, self.cmds, self.responses).start()
	
	
	class Respond(threading.Thread):
		
		def __init__(self, responses, callback):
			super().__init__()
			self.responses = responses
			self.callback = callback
		
		def run(self):
			while True:
				msg = self.responses.get()
				if(msg):
					self.callback(msg)
				time.sleep(1)
	
	
	class Cmd(threading.Thread):
		
		def __init__(self, data, cmds, responses):
			super().__init__()
			self.data = data
			self.cmds = cmds
			self.responses = responses
		
		def run(self):
			self.parser(self.data)
		
		def parser(self, data):
			obj = self.cmds
			i = 0
			for c in data["msg"]:
				if(c in obj):
					obj = obj[c]
				else:
					break
				i += 1
			
			if("fun" in obj and callable(obj["fun"])):
				data["cmd"] = data["msg"][0:i]
				data["msg"] = data["msg"][i:] if data["msg"][i] != " " else data["msg"][i + 1:]
				data["response"] = obj["fun"](data)
				if(data["response"]):
					self.responses.put(data)


bot = Crabot({"!h" : "highlight", "Hello" : "hello", "Goodbye" : "goodbye"}, lambda data: print(data["response"]))

bot.evalCmd({"msg" : "!h if(True) {\n\tMsgBox, % \"Hello World\"\n}", "lan" : "Autohotkey"})

input()

#for i in range(100):
#	bot.evalCmd({"msg" : "Hello", "name" : "Cap'n Odin"})
#	bot.evalCmd({"msg" : "Goodbye", "name" : "Cap'n Odin"})
	

