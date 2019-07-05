from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *


def ranking():
	arq = open('ranking.txt', 'r')  # abre o arquivo
	conteudo = arq.readlines()  # transforma o arquivo em array
	nomes = []    # fiz essas 2 pra separar nome do que é ponto
	pontos = []
	for i in range(len(conteudo)):
		linha=conteudo[i].split()   # a informação vem assim "(nome) (dific) (pontos)"
		nomes.append(linha[0])  # aqui eu coloquei todos os nomes numa lista
		pontos.append(int(linha[1].rstrip('\n')))   # aqui coloquei todos os pontos
	arq.close()
	for j in range(5):  # aqui é pra ordenar do maior pro menor
		for i in range(len(pontos)-1):
			if pontos[i] < pontos[i+1]:   # se a pontuaçao for menor, troca os pontos e o nome nas listas
				pontos[i+1], pontos[i] = pontos[i], pontos[i+1]
				nomes[i+1], nomes[i] = nomes[i], nomes[i+1]

	return nomes, pontos




def menu(janela, mouse):
	cenario = Sprite("img/scenary/menu.png")

	playTrue = Sprite("img/scenary/jogar.png")
	play = Sprite("img/scenary/jogarFalse.png")

	playTrue.set_position(490,300)
	play.set_position(490,300)


	sairTrue = Sprite("img/scenary/sair.png")
	sair = Sprite("img/scenary/sairFalse.png")

	sairTrue.set_position(490,380)
	sair.set_position(490,380)

	nomes,pontos = ranking()


	cenario.set_position(0,0)
	while True:
		cenario.draw()

		for i in range(len(nomes)):
			if i > 7:
				break
			janela.draw_text("{}".format(nomes[i]), 120, 110+i*40, size=20, color=(255, 255, 255))
			janela.draw_text("{}".format(pontos[i]), 250, 110+i*40, size=20, color=(255, 255, 255))

		if mouse.is_over_object(play):
			playTrue.draw()
			if mouse.is_button_pressed(1):
				return 1
		else:
			play.draw()

		if mouse.is_over_object(sair):
			sairTrue.draw()
			if mouse.is_button_pressed(1):
				janela.close()
		else:
			sair.draw()

		janela.update()
