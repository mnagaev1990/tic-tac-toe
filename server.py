#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from json import dumps

from game_server import GameServer

class MyHandler(BaseHTTPRequestHandler):
	def __init__(self, gs, *args):
		self.gs = gs
		BaseHTTPRequestHandler.__init__(self, *args)
	
	def do_GET(self):

		# Запросы на Favicon
		if (self.path == "/favicon.ico"):
			Type = "image/x-icon"
			f = open('./images/favicon.ico')
			Data = f.read()
			f.close()

		# Запросы на HTML
		elif (self.path == "/"):
			Type = "text/html"
			f = open('./html/index.html')
			Data = f.read()
			f.close()

		elif (self.path == "/start_game"):
			Type = "application/json"
			num_game = self.gs.NewGame()
			Data = dumps(num_game)

		elif (self.path.split("/")[1] == "step"):
			result = self.gs.Serve(int(self.path.split("/")[2]), int(self.path.split("/")[3]))
			Type = "application/json"
			Data = dumps(result)

		elif (self.path.split("/")[1] == "first_step_ai"):
			result = self.gs.Serve(int(self.path.split("/")[2]), None)
			Type = "application/json"
			Data = dumps(result) 

		# Запросы на JS
		elif (self.path.split("/")[1] == "game.js"):
			Type = "script/js"
			f = open('./js/game.js', 'rb')
			Data = f.read()
			f.close()
		
		# Запросы CSS
		elif (self.path.split("/")[1] == "styles.css"):
			Type = "text/css"
			f = open('./css/styles.css', 'rb')
			Data = f.read()
			f.close()

		else:
			return

		self.send_response(200)
		self.send_header("Content-type", Type)
		self.end_headers() 
		self.wfile.write(Data)

class http_server:
	def __init__(self, gs):
		def handler(*args):
			MyHandler(gs, *args)
		server = HTTPServer(('',80), handler)
		server.serve_forever()


if __name__ == "__main__":
	gs = GameServer()
	# Create threads
	thread_gs = Thread(target = gs.Clean)
	thread_http = Thread(target = http_server, args = (gs, ))
	# Start threads
	thread_gs.start()
	thread_http.start()
	# Join threads
	thread_gs.join()
	thread_http.join()
