import pygame
from pygame.locals import *
import sys
from gameobjects.vector2 import Vector2
from math import cos, sin, radians
from copy import deepcopy

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
fps = pygame.time.Clock()
wallWidth = 20
font = pygame.font.Font('fonts/UbuntuMono-B.ttf', 26)

pygame.display.set_caption('A funny mouse game')
background = (255, 255, 255)

class Game:
	def __init__(self):
		self.blocks = []
		self.starting = []
		self.speed = 0
		self.target = []
		self.death = 0
		self.totalDeath = 0
		self.round = 0

	def loadMap(self, fileName):
		try:
			mapFile = open(fileName, 'rU')
			exec(mapFile.read())
			mapFile.close()
			return True
		except:
			print 'Load Map Error!!'
			return False

	def isWin(self):
		d2 = (self.starting[0][0] - self.target[0][0]) ** 2 + (self.starting[0][1] - self.target[0][1]) ** 2
		if (self.starting[1] + self.target[1]) ** 2 >= d2: return True
		return False

	def isLose(self):
		sx, sy= self.starting[0]
		rad = self.starting[1]
		for block in self.blocks:
			if block[0] & 1:
				x, y = block[1]
				r= block[2]
				if (sx - x) ** 2 + (sy - y) ** 2 <= (rad + r) ** 2: return True
			else:
				x, y, w, h = block[1]
				if x <= sx <= x + w:
					dis = min(abs(sy - y), abs(sy - (y + h)))
					if dis <= self.starting[1]: return True
				elif y <= sy <= y + h:
					dis = min(abs(sx - x), abs(sx - (x + w)))
					if dis <= self.starting[1]: return True
				else:
					if sx > x + w: x += w
					if sy > y + h: y += h
					if (sx - x) ** 2 + (sy - y) ** 2 <= rad ** 2:
						return True
		return False

	def movePlayer(self):
		mx, my = pygame.mouse.get_pos()
		destination = Vector2(mx, my) - Vector2(self.starting[0])
		magnitude = destination.get_magnitude()
		if magnitude < self.speed:
			self.starting[0] = mx, my
		else:
			self.starting[0] = Vector2(game.starting[0]) + destination.normalize() * self.speed

	def draw(self):
		#draw starting and target point
		pygame.draw.circle(screen, self.starting[2], (int(self.starting[0][0]), int(self.starting[0][1])), self.starting[1])
		pygame.draw.circle(screen, self.target[2], self.target[0], self.target[1])

		#draw blocks
		for block in self.blocks:
			if block[0] & 1:
				pygame.draw.circle(screen, block[3], block[1], block[2])
			else:
				pygame.draw.rect(screen, block[2], block[1])
	
		#print info
		screen.blit(font.render('Round: ' + str(self.round), True, (0, 0, 0)), (50, height - 35))
		screen.blit(font.render('Death: ' + str(self.death), True, (255, 255, 0)), (330, height - 35))
		screen.blit(font.render('Total Death: ' + str(self.totalDeath), True, (255, 0, 0)), (580, height - 35))

	def move(self):
		for block in self.blocks:
			if block[0] == 2:
				block[1][0] += block[3][0]
				block[1][1] += block[3][1]
				if [block[1][0], block[1][1]] == block[4]:
					block[4], block[5] = block[5], block[4]
					block[3][0], block[3][1] = -block[3][0], -block[3][1]

			if block[0] == 3:
				x, y = block[1]
				block[6] += block[5]
				if block[6] % 360:
					block[1][0] = int((x - block[4][0]) * cos(radians(block[5])) - (y - block[4][1]) * sin(radians(block[5])) + block[4][0])
					block[1][1] = int((x - block[4][0]) * sin(radians(block[5])) + (y - block[4][1]) * cos(radians(block[5])) + block[4][1])
				else:
					block[1] = deepcopy(block[7])
				print block[1], block[7]

#---------------------------------------------------------------------#
game = Game()

level = 1

while level:

	isNext = False
	mb = 0

	if not game.loadMap('maps/map' + str(level) + '.txt'): break

	#add wall
	game.blocks.append([0, (0, 0, 800, wallWidth), (0, 0, 255)])
	game.blocks.append([0, (0, 0, wallWidth, 600), (0, 0, 255)])
	game.blocks.append([0, (width - wallWidth, 0, wallWidth, 600), (0, 0, 255)])
	game.blocks.append([0, (0, height - wallWidth - 30, 800, wallWidth + 30), (0, 0, 255)])

	while 1:
		fps.tick(100)

		screen.fill(background)
		game.draw()
		pygame.display.update()

		for evnt in pygame.event.get():
			if evnt.type == QUIT or (evnt.type == KEYDOWN and evnt.key == K_ESCAPE):
				pygame.quit()
				exit()
			elif evnt.type == KEYDOWN:
				if evnt.key == K_SPACE:
					isNext = True
			elif evnt.type == MOUSEBUTTONDOWN:
				if evnt.button == 1: mb = 1
			elif evnt.type == MOUSEBUTTONUP:
				if evnt.button == 1: mb = 0
		
		game.move()
		if mb == 1: game.movePlayer()
		if game.isWin() or isNext:
			level += 1
			game.death = 0
			break
		if game.isLose():
			game.death += 1
			game.totalDeath += 1
			break

pygame.quit()
exit()
