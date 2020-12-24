from constants import *
from queue import PriorityQueue

def get_direction(from_item, to_item):
	from_row, from_col = from_item.get_pos()
	to_row, to_col = to_item.get_pos()

	if from_row - 1 == to_row:
		return LEFT
	elif from_row + 1 == to_row:
		return RIGHT
	elif from_col - 1 == to_col:
		return UP
	elif from_col + 1 == to_col:
		return DOWN

def get_path(from_list, start, end):
	path = []
	while end != start:
		path.append(end)
		end = from_list[end]
	path.reverse()
	return path

def move_snake(game, from_list, start, end):
	path = get_path(from_list, start, end)
	for item in path:
		direction = get_direction(start, item)
		game.change_direction(direction)
		start = item

def heuristic(pos_x, pos_y):
	x1, y1 = pos_x
	x2, y2 = pos_y
	# Manhattan Distance
	return abs(x1 - x2) + abs(y1 - y2)

def get_shortest_path(game):
	game.clear_search_path()
	snake = game.snake

	grid = game.grid
	start = snake[-1]
	end = game.food

	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))

	closed_set = [start]
	from_list = {}

	g_score = {col: float("inf") for row in grid for col in row}
	g_score[start] = 0

	f_score = {col: float("inf") for row in grid for col in row}
	f_score[start] = heuristic(start.get_pos(), end.get_pos())

	while not open_set.empty():
		current = open_set.get()[2]
		closed_set.remove(current)

		if current == end:
			move_snake(game, from_list, start, end)
			return True

		for neighbour in current.get_neighbours(grid):
			if neighbour.is_snake() and neighbour not in snake:
				continue

			neighbour.make_searching()

			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbour]:
				from_list[neighbour] = current
				
				g_score[neighbour] = temp_g_score
				h_score = heuristic(neighbour.get_pos(), end.get_pos())
				f_score[neighbour] = temp_g_score + h_score

				if neighbour not in closed_set:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					closed_set.append(neighbour)
