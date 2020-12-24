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

	def is_snake(self):
		return self.color == BLACK

	def is_searching(self):
		return self.color == GREY

	def make_defaut(self):
		self.color = WHITE

	def make_snake(self):
		self.color = BLACK

	def make_food(self):
		self.color = RED

	def make_searching(self):
		self.color = GREY

	def get_pos(self):
		return self.row, self.col

	def get_neighbours(self, grid):
		neighbours = []

		if self.row > 0 and not grid[self.row - 1][self.col].is_snake():
			neighbours.append(grid[self.row - 1][self.col])

		if (self.row < ROWS - 1) and not grid[self.row + 1][self.col].is_snake():
			neighbours.append(grid[self.row + 1][self.col])

		if self.col > 0 and not grid[self.row][self.col - 1].is_snake():
			neighbours.append(grid[self.row][self.col - 1])

		if (self.col < ROWS - 1) and not grid[self.row][self.col + 1].is_snake():
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

	def _draw_score(self):
		text = pygame.font.SysFont("Comic Sans MS", 25)
		surface = text.render(f"Score : {self.score}", False, BLACK)
		self.screen.blit(surface, (10, 10))
 
	def draw(self):
		for row in self.grid:
			for col in row:
				if not col.is_searching():
					col.make_defaut()
				col.draw()
		
		self._draw_snake()
		self._draw_food()
		self._draw_score()
		pygame.display.update()

	def clear_search_path(self):
		for row in self.grid:
			for col in row:
				if col.is_searching():
					col.make_defaut()
				col.draw()
		
		self._draw_snake()
		self._draw_food()
		self._draw_score()
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

	def move_snake(self):
		row, col = self.snake[-1].get_pos()
		head = None

		if self.direction == UP:
			col -= 1

		elif self.direction == DOWN:
			col += 1

		elif self.direction == LEFT:
			row -= 1

		elif self.direction == RIGHT:
			row += 1

		if row < 0 or row > ROWS - 1 or \
		col < 0 or col > ROWS - 1:
			print("snake hits on wall")
			return False

		head = self.grid[row][col]

		# for item in self.snake:
		# 	item_row, item_col = item.get_pos()
		# 	if item_row == row and item_col == col:
		# 		print(head)
		# 		print(*self.snake, sep="\n")
		# 		print("snake collapsed")
		# 		return False

		self.snake.append(head)
		if head == self.food:
			self.increment_score()
		else:
			self.snake.pop(0)

		return True