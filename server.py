#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from game_server import GameServer
import json

class MyHandler(BaseHTTPRequestHandler):
	def __init__(self, gs, *args):
		self.gs = gs
		BaseHTTPRequestHandler.__init__(self, *args)
	
	def do_GET(self):

		# Запросы на Favicon
		if (self.path == "/favicon.ico"):
			Type = "image/x-icon"
			f = open('./images/favicon.ico')
			data = f.read()
			f.close()

		# Запросы на HTML
		elif (self.path == "/"):
			Type = "text/html"
			f = open('./html/index.html')
			data = f.read()
			f.close()

		elif (self.path == "/start_game"):
			Type = "application/json"
			num_game = self.gs.NewGame()
			data = json.dumps(num_game)

		elif (self.path.split("/")[1] == "step"):
			result = self.gs.Serve(int(self.path.split("/")[2]), int(self.path.split("/")[3]))
			Type = "application/json"
			data = json.dumps(result)

		# Запросы на JS
		elif (self.path.split("/")[1] == "game.js"):
			Type = "script/js"
			f = open('./js/game.js', 'rb')
			data = f.read()
			f.close()
		
		# Запросы CSS
		elif (self.path.split("/")[1] == "styles.css"):
			Type = "text/css"
			f = open('./css/styles.css', 'rb')
			data = f.read()
			f.close()

		else:
			return

		self.send_response(200)
		self.send_header("Content-type", Type)
		self.end_headers() 
		self.wfile.write(data)

class http_server:
	def __init__(self, gs):
		def handler(*args):
			MyHandler(gs, *args)
		server = HTTPServer(('',80), handler)
		server.serve_forever()

print "Server started"
gs = GameServer()
server = http_server(gs)

