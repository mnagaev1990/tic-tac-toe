#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
from copy import deepcopy
from time import sleep, time


class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

class Game:
	def __init__(self):
		self.all_points = [(i,j) for i in range(3) for j in range(3)]
		self.d1 = [(0,0),(1,1),(2,2)]
		self.d2 = [(0,2),(1,1),(2,0)]
		self.num_points = 0
		self.human_points = []
		self.ai_points = []
		self.end = False
		
	def check_win(self, points):
		rows_fill = [0,0,0]
		cols_fill = [0,0,0]
		d1_fill = 0
		d2_fill = 0
		
		for p in points:
			if p in self.d1:
				d1_fill += 1
				if d1_fill == 3:
					print "Win! Diagonal is fill!"
					return True, "d", 1
			
			if p in self.d2:
				d2_fill += 1
				if d2_fill == 3:
					print "Win! Diagonal is fill!"
					return True, "d", 2
			
			rows_fill[p[0]] += 1
			if rows_fill[p[0]] == 3:
				print "Win! Row ", p[0], " is fill!"
				return True, "r", p[0]
			
			cols_fill[p[1]] += 1
			if cols_fill[p[1]] == 3:
				print "Win! Column ", p[1], " is fill!"
				return True, "c", p[1]
		
		return False, None, None

	def find_end_step(self):
		human_rows = []
		human_cols = []
		human_d1 = False    
		human_d2 = False

		for hm_pnt in self.human_points:
			if not hm_pnt[0] in human_rows:
				human_rows.append(hm_pnt[0])
			if not hm_pnt[1] in human_cols:
				human_cols.append(hm_pnt[1])
			if hm_pnt in self.d1:
				human_d1 = True
			if hm_pnt in self.d2:
				human_d2 = True          

		rows_fill = [0,0,0]
		cols_fill = [0,0,0]
		d1_fill = 0
		d2_fill = 0

		for ai_pnt in self.ai_points:
			if ai_pnt in self.d1:
				d1_fill += 1
				if (d1_fill == 2 and not human_d1):
					for d1_pnt in self.d1:
						if not d1_pnt in self.ai_points:
							return d1_pnt, "d", 1
			if ai_pnt in self.d2:
				d2_fill += 1
				if (d2_fill == 2 and not human_d2):
					for d2_pnt in self.d2:
						if not d2_pnt in  self.ai_points:
							return d2_pnt, "d", 2
			rows_fill[ai_pnt[0]] += 1
			if (rows_fill[ai_pnt[0]] == 2 and not ai_pnt[0] in human_rows):
				for row_pnt in [(ai_pnt[0], 0), (ai_pnt[0], 1), (ai_pnt[0], 2)]:
					if not row_pnt in  self.ai_points:
						return row_pnt, "r", ai_pnt[0]
			cols_fill[ai_pnt[1]] += 1
			if (cols_fill[ai_pnt[1]] == 2 and not ai_pnt[1] in human_cols):
				for col_pnt in [(0, ai_pnt[1]), (1, ai_pnt[1]), (2, ai_pnt[1])]:
					if not col_pnt in  self.ai_points:
						return col_pnt, "c", ai_pnt[1]
		return None, None, None

	def find_human_attack(self):
		for i in range(len(self.human_points)-1):
			for j in range(i+1, len(self.human_points)):
				p1 = self.human_points[i]
				p2 = self.human_points[j]
				if p1[0] == p2[0]: 
					x = [0,1,2]
					x.remove(p1[1])
					x.remove(p2[1])
					defend_step = (p1[0],x[0])
					if not defend_step in self.ai_points:
						return defend_step                
			
				elif p1[1] == p2[1]:
					y = [0,1,2]
					y.remove(p1[0])
					y.remove(p2[0])
					defend_step = (y[0],p1[1])
					if not defend_step in self.ai_points:
						return defend_step   
				
				elif p1 in self.d1 and p2 in self.d1:
					d1_ = deepcopy(self.d1)
					d1_.remove(p1)
					d1_.remove(p2)
					defend_step = d1_[0]
					if not defend_step in self.ai_points:
						return defend_step   
				
				elif p1 in self.d2 and p2 in self.d2:
					d2_ = deepcopy(self.d2)
					d2_.remove(p1)
					d2_.remove(p2)
					defend_step = d2_[0]
					if not defend_step in self.ai_points:
						return defend_step   
		return None

	def find_power_point(self):
		rows_free = [0,1,2]
		cols_free = [0,1,2]
		d1_free = True
		d2_free = True
		for point in self.human_points:
			if point[0] in rows_free:
				rows_free.remove(point[0])
			if point[1] in cols_free:
				cols_free.remove(point[1])
			if point in self.d1:
				d1_free = False
			if point in self.d2:
				d2_free = False
		
		rows_forced = []
		cols_forced = []
		d1_forced = False
		d2_forced = False
		
		for point in self.ai_points:
			if not (point[0] in rows_forced):
				rows_forced.append(point[0])
			if not (point[1] in cols_forced):
				cols_forced.append(point[1])
			if point in self.d1:
				d1_forced = True
			if point in self.d2:
				d2_forced = True
			
		power_points = {}
		for point in self.all_points:
			if (point in self.human_points) or (point in self.ai_points):
				continue
			power = 0
			if point[0] in rows_free:
				power += 1
				if (point[0] in rows_forced):
					power += 1
			
			if point[1] in cols_free:
				power += 1
				if (point[1] in cols_forced):
					power += 1 
				
			if (d1_free and (point in self.d1)):
				power += 1
				if d1_forced:
					power += 1
				
			if (d2_free and (point in self.d2)):
				power += 1
				if d2_forced:
					power += 1
					
			if not power_points.has_key(power):
				power_points[power] = []
			power_points[power].append(point)
			
		#print "power_points: ", power_points
		max_power = max(power_points.keys())
		r = randint(0, len(power_points[max_power])-1)    
		return power_points[max_power][r]

	def display(self):
		for i in range(3):
			str_row = ""
			for j in range(3):
				flag = False
				for p in self.all_points:
					if (p in self.human_points and p == (i,j)): 
						str_row += color.RED + "X" + color.END
						flag = True
					elif (p in self.ai_points and p == (i,j)):
						str_row += color.BLUE + "O" + color.END
						flag = True
				if not flag:
					str_row += " "
				if j != 2:
					str_row += "|" 
			print str_row

	def step(self, human_step):
		if type(human_step) is tuple and len(human_step) == 2 and \
			human_step[0] in range(0,3) and human_step[1] in range(0,3) and \
				not human_step in self.human_points and not human_step in self.ai_points:
					
			# Input Human
			print "Human step: ", human_step
			self.human_points.append(human_step)
			self.num_points += 1
			self.display()
			chck_win = self.check_win(self.human_points)
			if chck_win[0]:
				print "Human win!!"
				self.end = True
				return "Human Win!", self.human_points, self.ai_points, chck_win[1], chck_win[2]
			if self.num_points == 9:
				self.end = True
				return "Draw", self.human_points, self.ai_points
			
			# Find end step
			end_pnt = self.find_end_step()
			if (end_pnt[0] != None):
				print "AI step: ", end_pnt[0]
				self.ai_points.append(end_pnt[0])
				self.num_points += 1
				self.display()
				print "AI win!!"
				self.end = True
				return "AI Win!", self.human_points, self.ai_points, end_pnt[1], end_pnt[2]
			
			# Defend
			defend_step = self.find_human_attack()
			if defend_step != None:
				print "AI step: ", defend_step
				self.ai_points.append(defend_step)
				self.num_points += 1
				self.display()
				chck_win = self.check_win(self.ai_points)
				if chck_win[0]:
					print "AI win!!"
					self.end = True
					return "AI Win!", self.human_points, self.ai_points, chck_win[1], chck_win[2]
				if self.num_points == 9:
					self.end = True
					return "Draw", self.human_points, self.ai_points
				return "AI Step", self.human_points, self.ai_points
			
			# Attack
			attack_step = self.find_power_point()
			print "AI step: ", attack_step
			self.ai_points.append(attack_step)
			self.num_points += 1
			self.display()
			chck_win = self.check_win(self.ai_points)
			if chck_win[0]:
				print "AI win!!"
				self.end = True
				return "AI Win!", self.human_points, self.ai_points, chck_win[1], chck_win[2]
			if self.num_points == 9:
				self.end = True
				return "Draw", self.human_points, self.ai_points
			return "AI Step", self.human_points, self.ai_points
		else:
			return "Invalid Step!"
			

class GameServer:
	def __init__(self):
		self.TIME_PERIOD = 30	# Time for game
		self.num_game = 0
		self.games  = {}

	def NewGame(self):
		self.num_game += 1
		self.games[self.num_game] = (Game(), time() + self.TIME_PERIOD)
		return self.num_game

	def Serve(self, cur_game, human_step):
		if self.games.has_key(cur_game) and not self.games[cur_game][0].end:
			pnt = (human_step/10, human_step%10)
			result = self.games[cur_game][0].step(pnt)
			return result
		else:
			return "Game not founded!"

	def Clean(self):
		# Delete old game
		while 1:	
			game_nums = self.games.keys()
			for gm in game_nums:
				if self.games[gm][0].end:
					self.games.pop(gm)
					print "Delete ended game №", gm
				elif time() > self.games[gm][1]:
					self.games.pop(gm)
					print "Time is over! Delete game №", gm
			sleep(1)
