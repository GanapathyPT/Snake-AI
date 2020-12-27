from constants import *
from queue import PriorityQueue

# get the direction when two positions are given
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

# extract the path from the output of the algorithm
def get_path(from_list, start, end):
	path = []
	while end != start:
		path.append(end)
		end = from_list[end]
	path.reverse()
	return path

# visualizing path for testing
def visualize_path(path, start):
	for item in path:
		direction = get_direction(start, item)
		item.draw_path(direction)
		start = item

# handling the output of the algorithm
def move_snake(game, from_list, start, end):
	path = get_path(from_list, start, end)
	# for testing
	# visualize_path(path, start)
	for item in path:
		direction = get_direction(start, item)
		game.change_direction(direction)
		game.move_snake()
		game.draw()
		start = item

# estimate the distance from current pos to the end pos
def heuristic(pos_x, pos_y):
	x1, y1 = pos_x
	x2, y2 = pos_y
	# Manhattan Distance
	return abs(x1 - x2) + abs(y1 - y2)

def get_shortest_path(game):
	snake = game.snake

	grid = game.grid
	start = snake[-1]
	end = game.food

	# count is used to resolv the tie break of two node with same f_score
	# based on which is added first nodeis choosen on tie condition
	count = 0
	# PriorityQueue to store the node that are calculated and considered
	open_set = PriorityQueue()
	open_set.put((0, count, start))

	# list to store the items in open-set
	closed_set = [start]
	from_list = {}

	# intialize the g_score to infinity for all nodes
	g_score = {col: float("inf") for row in grid for col in row}
	g_score[start] = 0

	# sam for f_score
	f_score = {col: float("inf") for row in grid for col in row}
	f_score[start] = heuristic(start.get_pos(), end.get_pos())

	# do the algorithm untill the open_set becomes empty
	while not open_set.empty():
		# current node is chosen which has the lowest f_score in the open_set
		current = open_set.get()[2]
		closed_set.remove(current)

		if current == end:
			# path is found if the current is the end
			move_snake(game, from_list, start, end)
			return True

		# get all the neighbours for the current node
		for neighbour in current.get_neighbours(grid):
			# calculating the g_score for the current and adding 1 to it
			# the distance between two nodes is considered as 1
			temp_g_score = g_score[current] + 1

			# at start the G_score of all the nodes is infinity
			# so adding the lowest g_score of the neighbour
			if temp_g_score < g_score[neighbour]:
				# when lowest g_score is found add the neighbour to the result
				from_list[neighbour] = current

				# finding the h_score and f_score for the neighbor
				g_score[neighbour] = temp_g_score
				h_score = heuristic(neighbour.get_pos(), end.get_pos())
				f_score[neighbour] = temp_g_score + h_score

				# adding the neighbour to the open_set if it is not there
				if neighbour not in closed_set:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					closed_set.append(neighbour)
