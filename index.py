import pygame
from constants import *
from component import *
from algorithm import get_shortest_path

pygame.init()
screen = pygame.display.set_mode([ WIDTH, WIDTH ])
timer = pygame.time.Clock()

def main():
	running = True
	game = Game(screen)

	while running:
		game.draw()
		game.move_snake()
		get_shortest_path(game)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					game.change_direction(UP)

				elif event.key == pygame.K_DOWN:
					game.change_direction(DOWN)

				elif event.key == pygame.K_LEFT:
					game.change_direction(LEFT)

				elif event.key == pygame.K_RIGHT:
					game.change_direction(RIGHT)

		timer.tick(10)

	pygame.quit()

if __name__ == '__main__':
	main()