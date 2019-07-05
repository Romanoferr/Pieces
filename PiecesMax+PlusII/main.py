from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from menu import *
from jogo2 import *
from fim import *

GAME_STATE=0


janela = Window(1000, 700)
janela.set_title("Pieces")
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

janela.set_background_color((255, 255, 255))


while True:

	if GAME_STATE == 0:
		GAME_STATE = menu(janela, mouse)
	if GAME_STATE == 1:
		GAME_STATE,pontos = jogo(janela)
	if GAME_STATE == 2:
		GAME_STATE = fim(pontos)
	janela.update()
