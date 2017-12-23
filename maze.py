import pygame
from pygame.locals import *
import random
import os, sys
from parameter import *

class Cell(object):
	"""individual cell for maze"""
	def __init__(self, x, y):
		self.x, self.y = x, y
		self.checked = 0	# initially unchecked
		self.size = CELL_SIZE
		self.boundary = [True, True, True, True]
		self.rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)

	def draw(self, surface):
		if self.boundary[0]:
			pygame.draw.line(surface, BLACK, (self.x * self.size, self.y * self.size), ((self.x + 1) * self.size, self.y * self.size), 1)
		if self.boundary[1]:
			pygame.draw.line(surface, BLACK, ((self.x + 1) * self.size, self.y * self.size), ((self.x + 1) * self.size, (self.y + 1) * self.size), 1)
		if self.boundary[2]:
			pygame.draw.line(surface, BLACK, ((self.x + 1) * self.size, (self.y + 1) * self.size), (self.x * self.size, (self.y + 1) * self.size), 1)
		if self.boundary[3]:
			pygame.draw.line(surface, BLACK, (self.x * self.size, (self.y + 1) * self.size), (self.x * self.size, self.y * self.size), 1)
			
	def fill_in(self, surface):
		pygame.draw.rect

class Grid(object):
	def __init__(self, screen_size):
		self.w, self.h = screen_size[0] / CELL_SIZE, screen_size[1] / CELL_SIZE
		self.cells = [[] for _ in range(self.w)]
		for i in range(self.w):
			for j in range(self.h):
				self.cells[i].append(Cell(i, j))

		# generator
		self.current = self.cells[0][0]
		self.current.checked = 1
		self.stack = [self.current]

	def find_next_neighbor(self, cell):
		i, j = cell.x, cell.y
		for order in random.sample(range(4), 4):
			if order == 0 and j and not self.cells[i][j-1].checked:
				cell.boundary[0] = False
				self.cells[i][j-1].boundary[2] = False
				return self.cells[i][j-1]
			elif order == 1 and i < self.w-1 and not self.cells[i+1][j].checked:
				cell.boundary[1] = False
				self.cells[i+1][j].boundary[3] = False
				return self.cells[i+1][j]
			elif order == 2 and j < self.h-1 and not self.cells[i][j+1].checked:
				cell.boundary[2] = False
				self.cells[i][j+1].boundary[0] = False
				return self.cells[i][j+1]
			elif order == 3 and i and not self.cells[i-1][j].checked:
				cell.boundary[3] = False
				self.cells[i-1][j].boundary[1] = False
				return self.cells[i-1][j]
		 
		return None


	def generator(self, skip):
		if not skip:
			if self.stack:
				next_cell = self.find_next_neighbor(self.current)
				if not next_cell:
					self.current = self.stack.pop()
				else:
					self.current = next_cell
					self.stack.append(next_cell)
					self.current.checked = 1
		else:
			while self.stack:
				next_cell = self.find_next_neighbor(self.current)
				if not next_cell:
					self.current = self.stack.pop()
				else:
					self.current = next_cell
					self.stack.append(next_cell)
					self.current.checked = 1


class Game(object):
	"""docstring for Game"""
	def __init__(self):
		
		screen_size = SCREEN_WIDTH, SCREEN_HEIGHT

		pygame.init()
		self.screen = pygame.display.set_mode(screen_size)
		pygame.display.set_caption("Maze Generator")
		self.playing = False

		myfont = pygame.font.SysFont('Comic Sans MS', 30)

		self.gameover = myfont.render(GAMEOVER, False, BLACK)
		self.skipmessage = myfont.render(SKIP, False, BLACK)
		exitfont = pygame.font.SysFont('Comic Sans MS', EXITSIZE)
		self.exitmessage = exitfont.render(EXIT, False, BLACK)

		self.grid = Grid(screen_size)
		self.run()

	def render(self):
		self.screen.fill(WHITE)
		
		pygame.draw.rect(self.screen, RED, self.grid.current.rect)

		for i in range(self.grid.w):
			for each in self.grid.cells[i]:
				each.draw(self.screen)
		if not self.playing:
			self.screen.blit(self.skipmessage, ((SCREEN_WIDTH - self.skipmessage.get_size()[0])//2,(SCREEN_HEIGHT - self.skipmessage.get_size()[1])//6*5))
		else:
			if self.grid.current.x == self.grid.w-1 and self.grid.current.y == self.grid.h-1:
				self.screen.blit(self.gameover,((SCREEN_WIDTH - self.gameover.get_size()[0])//2,(SCREEN_HEIGHT - self.gameover.get_size()[1])//2))
			
			self.screen.blit(self.exitmessage, ((SCREEN_WIDTH - self.exitmessage.get_size()[0]),(SCREEN_HEIGHT - self.exitmessage.get_size()[1]) ))
		
		pygame.display.flip()


	def run(self):
		while not self.playing:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:	sys.exit()
				if event.type == pygame.KEYUP:
					self.playing = True
			self.grid.generator(self.playing)
			if not self.grid.stack:
				self.playing = True



			self.render()

			


		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:	sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:		sys.exit()
					elif event.key == K_UP:
						if self.grid.current.y and not self.grid.current.boundary[0]:				self.grid.current = self.grid.cells[self.grid.current.x][self.grid.current.y-1]
					elif event.key == K_DOWN:
						if self.grid.current.y < self.grid.h-1 and not self.grid.current.boundary[2]:	self.grid.current = self.grid.cells[self.grid.current.x][self.grid.current.y+1]
					elif event.key == K_LEFT:
						if self.grid.current.x and not self.grid.current.boundary[3]:				self.grid.current = self.grid.cells[self.grid.current.x-1][self.grid.current.y]
					elif event.key == K_RIGHT:
						if self.grid.current.x < self.grid.w-1 and not self.grid.current.boundary[1]:	self.grid.current = self.grid.cells[self.grid.current.x+1][self.grid.current.y]
	

			self.render()


if __name__ == "__main__":
	Sicheng = Game()
