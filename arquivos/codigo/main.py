import pygame, sys
from settings import *
from player import Player
from laser import Laser
from meteor_generator import MeteorGenerator
from game_manager import GameManager
from ui import UI

# setup básico
pygame.init()
janela = pygame.display.set_mode((LARGURA_DA_JANELA, ALTURA_DA_JANELA))
titulo_do_jogo = 'Jogo Espacial em Python'
pygame.display.set_caption(titulo_do_jogo)
clock = pygame.time.Clock()

# grupos
jogador_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteoro_group = pygame.sprite.Group()

# BG
background = pygame.image.load(CAMINHOS['Bg'])
background = pygame.transform.scale(background, (1280, 1280))

# músicas
musica_de_fundo = pygame.mixer.Sound('../sons/musica_de_fundo.wav')
musica_de_fundo.set_volume(0.5)
musica_de_fundo.play(loops = -1)

musica_de_game_over = pygame.mixer.Sound('../sons/musica_de_game_over.wav')
tocou_musica_de_game_over = False

game_manager = GameManager()
ui = UI((LARGURA_DA_JANELA * 0.5, 50), pygame.display.get_surface(), game_manager)

# cria o jogador
player = Player(
	posicao_inicial = (LARGURA_DA_JANELA * 0.5, ALTURA_DA_JANELA * 0.5),
	caminho = CAMINHOS['Jogador'],
	game_manager = game_manager,
	group_do_laser = laser_group,
	group_do_meteoro = meteoro_group,
	groups = jogador_group
	)

# criar o gerador de meteoros
meteor_generator = MeteorGenerator(caminho_do_meteoro = CAMINHOS['Meteoro'], group_do_meteoro = meteoro_group)

# loop do jogo
while True:

	# loop de eventos
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# delta time
	delta_time = clock.tick() / 1000

	if not player.game_over:
		
		# update
		jogador_group.update(delta_time)
		laser_group.update(delta_time)
		meteor_generator.update(delta_time)
		meteoro_group.update(delta_time)

		# desenha os graficos
		janela.fill('black')
		janela.blit(background, (0, 0))
		jogador_group.draw(janela)
		laser_group.draw(janela)
		meteoro_group.draw(janela)
		ui.mostrar_pontuacao()

	else:
		if not tocou_musica_de_game_over:
			musica_de_fundo.stop()
			musica_de_game_over.play()
			tocou_musica_de_game_over = True

		janela.fill((235, 64, 52))
		ui.mostrar_texto_de_game_over()

	# desenha o frame final
	pygame.display.update()
