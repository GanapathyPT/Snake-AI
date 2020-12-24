import pygame, random
from constants import *

def generate_grid(screen, rows, cols):
	grid = []
	for row in range(rows):
		grid.append([])
		for col in range(cols):
			grid[row].append(Item(screen, row, col))

	return grid

def get_food_pos(grid, snake):
	row = random.randint(0, ROWS - 1)
	col = random.randint(0, ROWS - 1)

	food = grid[row][col]
	for item in snake:
		if item == food:
			return get_food_pos(grid, snake)
	return food

class Item():
	ITEM_WIDTH = WIDTH // ROWS

	def __init__(self, screen, row, col):
		self.screen = screen
		self.row = row
		self.col = col
		self.color = WHITE

		self.x = self.row * self.ITEM_WIDTH
		self.y = self.col * self.ITEM_WIDTH

	def draw(self):
		pygame.draw.rect(
			self.screen, 
			self.color,
			(self.x, self.y, self.ITEM_WIDTH, self.ITEM_WIDTH)	 
		)

	def make_defaut(self):
		self.color = WHITE

	def make_snake(self):
		self.color = BLACK

	def make_food(self):
		self.color = RED

	def get_pos(self):
		return self.row, self.col

	def get_neighbours(self, grid):
		neighbours = []

		if self.row > 0:
			neighbours.append(grid[self.row - 1][self.col])

		if self.row < ROWS - 1:
			neighbours.append(grid[self.row + 1][self.col])

		if self.col > 0:
			neighbours.append(grid[self.row][self.col - 1])

		if self.col < ROWS - 1:
			neighbours.append(grid[self.row][self.col + 1])

		return neighbours

	def __str__(self):
		return f"{self.row}, {self.col}"

	def __hash__(self):
		return hash((self.row, self.col))

	def __lt__(self, other):
		self_row, self_col = self.get_pos()
		other_row, other_col = other
		return self_row < other_row and self_col < other_col

	def __gt__(self, other):
		self_row, self_col = self.get_pos()
		other_row, other_col = other
		return self_row > other_row and self_col > other_col

	def __eq__(self, other):
		self_row, self_col = self.get_pos()
		other_row, other_col = other.get_pos()
		return self_row == other_row and self_col == other_col

class Game():
	def __init__(self, screen):
		self.screen = screen
		self.score = 0
		self.grid = generate_grid(screen, ROWS, ROWS)
		self.snake = [
			self.grid[0][0],
			self.grid[1][0]
		]
		self.direction = RIGHT
		self.food = get_food_pos(self.grid, self.snake)

	def _draw_snake(self):
		for item in self.snake:
			item.make_snake()
			item.draw()

	def _draw_food(self):
		self.food.make_food()
		self.food.draw()

	def draw(self):
		for row in self.grid:
			for col in row:
				col.make_defaut()
				col.draw()
		
		self._draw_snake()
		self._draw_food()
		pygame.display.update()

	def refresh_food_pos(self):
		self.food = get_food_pos(self.grid, self.snake)

	def increment_score(self):
		self.refresh_food_pos()
		self.score += 1

	def change_direction(self, direction):
		if (self.direction == UP and direction != DOWN) or \
		(self.direction == DOWN and direction != UP) or \
		(self.direction == LEFT and direction != RIGHT) or \
		(self.direction == RIGHT and direction != LEFT):
			self.direction = direction

	# this function is not working
	# donno why
	def check_errors(self, head):
		if head < (0, 0) and head > (ROWS - 1, ROWS - 1):
			pygame.quit()
		for item in self.snake[1:]:
			if item == head:
				pygame.quit()

	def move_snake(self):
		row, col = self.snake[-1].get_pos()
		head = None

		if self.direction == UP:
			head = self.grid[row][col - 1]

		elif self.direction == DOWN:
			head = self.grid[row][col + 1]

		elif self.direction == LEFT:
			head = self.grid[row - 1][col]

		elif self.direction == RIGHT:
			head = self.grid[row + 1][col]

		# self.check_errors(head)

		self.snake.append(head)
		if head == self.food:
			self.increment_score()
		else:
			self.snake.pop(0)