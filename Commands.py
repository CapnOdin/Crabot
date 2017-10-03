# -*- coding: utf-8 -*-

def hello(data):
	return "Hello " + data["name"]

def goodbye(data):
	return "Goodbye " + data["name"]

def highlight(data):
	return "```" + data["lan"] + "\n" + data["msg"] + "\n```"


