import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((139, 193, 220))

while True:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
			
	pygame.display.update()