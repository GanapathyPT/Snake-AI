import pygame
from constants import WIDTH
from component import Game
from algorithm import get_shortest_path

pygame.init()
pygame.display.set_caption("Snake AI")
screen = pygame.display.set_mode([ WIDTH, WIDTH ])
timer = pygame.time.Clock()

def main():
	running = True
	game = Game(screen)

	while running:
		get_shortest_path(game)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			# uncomment for user as a player
			'''
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					game.change_direction(UP)

				elif event.key == pygame.K_DOWN:
					game.change_direction(DOWN)

				elif event.key == pygame.K_LEFT:
					game.change_direction(LEFT)

				elif event.key == pygame.K_RIGHT:
					game.change_direction(RIGHT)
			'''

		timer.tick(5)

	pygame.quit()

if __name__ == '__main__':
	main()