import pygame

global screen
global a
a = 0

def main():
	global a
	screen = pygame.display.set_mode((640, 400))
	running = 1
	#Main game loop
	while running:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			running = 0
		print a
		screen.fill((int(a),int(a),int(a)))
		if a < 255:
			a+=1
		else:
			a = 0
	
if __name__ == "__main__":
	main()