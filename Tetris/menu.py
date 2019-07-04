from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *


def menu(janela,mouse):
	cenario = Sprite("img/scenary/menu.png")
	cenario.set_position(0,0)
	while True:
		cenario.draw()

		janela.update()
