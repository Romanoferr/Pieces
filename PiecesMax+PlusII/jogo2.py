from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from random import randint


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


table = [['V' for i in range(10)] for j in range(24)]
shapes = [S, Z, I, O, J, L, T]

ilegais = [[0, 0], [1, 0], [2, 0], [3, 0],[4, 0], [5, 0], [6, 0],[7, 0], [8, 0], [9, 0]]

pontos = 0

strike = 1

fase = 1

tempototal = 0


def reset():
	global pontos, strike, fase, tempototal, table, descendo, nova, locked, posx, posy, rotation, gameover

	table = [['V' for i in range(10)] for j in range(24)]

	pontos = 0

	strike = 1

	fase = 1

	tempototal = 0

	descendo = 1
	nova = True
	locked = []
	posx, posy = 0, 0
	rotation = 0

	gameover = 0



def geraPos(shape, rotation, posx, posy, pos):
	global shapes, locked
	newpos = []
	format = shapes[shape][rotation % len(shapes[shape])]
	for i in range(len(format)):
		linha = list(format[i])
		for j in range(len(linha)):
			if linha[j] == '0':
				if posx+j-2 < 0 or posx+j-2 > 9 or posy+i-2 > 19 or [posx+j-2, posy+i-2] in locked:
					return pos
				newpos.append([posx+j-2, posy+i-2])
	return newpos


def colocaDentro(pos, shape):
	global table

	for x, y in pos:
		if table[y][x] == 'V':
			table[y][x] = shape


def tiraFora(pos):
	global table
	for x, y in pos:
		table[y][x] = 'V'


def movePeca(direcao, pos, shape):
	global nova, table, posx, posy, rotation, gameover, ilegais
	newpos = []
	if direcao == 'direita':
		for i in range(len(pos)):
			newx = pos[i][0]+1
			if 0 <= newx <= 9 and [pos[i][0]+1, pos[i][1]] not in locked:
				newpos.append([pos[i][0]+1, pos[i][1]])
			else:
				return pos
		posx += 1

	elif direcao == 'esquerda':
		for i in range(len(pos)):
			newx = pos[i][0]-1
			if newx >= 0 and newx <= 9 and [pos[i][0]-1, pos[i][1]] not in locked:
				newpos.append([pos[i][0]-1, pos[i][1]])
			else:
				return pos
		posx -= 1

	elif direcao == 'baixo':
		for i in range(len(pos)):
			newy = pos[i][1]+1
			if newy <= 19 and [pos[i][0], pos[i][1]+1] not in locked:
				newpos.append([pos[i][0], pos[i][1]+1])
			else:
				locked.extend(pos)
				locked.sort(key=segundo)
				destroiLinha()
				for ilegal in ilegais:
					if ilegal in locked:
						gameover = 1
				nova = True
				return pos
		posy += 1

	elif direcao == 'cima':
		newpos1 = geraPos(shape, rotation, posx, posy, pos)
		if newpos1 not in locked:
			newpos = geraPos(shape, rotation, posx, posy, pos)
		else:
			return pos

	tiraFora(pos)
	colocaDentro(newpos, shape)
	return newpos


def movimentoAtual(delaydesc, pos, shape):
	global descendo, table
	delaypeca = 0.40 - 0.025 * fase
	if delaypeca <= 0.15:
		delaypeca = 0.15
	if delaydesc > delaypeca:    # Velocidade da peca em descida automatica
		if descendo == 1:
			pos = movePeca('baixo', pos, shape)
		return 0, pos
	else:
		return delaydesc, pos


def desenha(matriz):
	for i in range(len(matriz)):
		matriz[i].draw()


def coloreMatriz(tabuleiro):
	global table
	pecas = []
	for i in range(len(table)):
		for j in range(len(table[i])):
			if table[i][j] != 'V':
				pecinha = Sprite("img/colors/"+str(table[i][j]+1)+".png")
				pecinha.x = tabuleiro.x+j*30
				pecinha.y = tabuleiro.y+i*30
				pecas.append(pecinha)
	return pecas


def segundo(elem):
	return elem[1]


def contador(segundos):
	minutos = 0
	if segundos > 60:
		minutos += segundos//60
		segundos -= minutos*60
	return minutos, segundos


def destroiLinha():
	global locked, table, pontos, strike, fase
	i = 19
	while i >= 0:
		if 'V' not in table[i]:
			for row in range(10):
				try:
					locked.remove([row, i])
				except:
					print(locked)
					print("locked.remove([{},{}])".format(row,i))
					continue

			table[i] = ['V' for i in range(10)]
			for k in range(i, 0, -1):
				table[k] = table[k-1].copy()

			for k in range(len(locked)):
				if locked[k][1] <= i:
					locked[k][1] += 1
				elif locked[k][1] > i:
					break

			pontos += int(100*(1+fase/10))
			strike -= 1
			if strike == 0:
				strike += int(fase*1.37)*2
				fase += 1

		else:
			i -= 1


descendo = 1
nova = True
locked = []
posx, posy = 0, 0
rotation = 0

gameover = 0


def jogo(janela):
	global nova, descendo, posx, posy, rotation, pontos, fase, tempototal, strike, gameover
	mouse = Window.get_mouse()
	teclado = Window.get_keyboard()

	cenario = Sprite("img/scenary/jogo3.png")
	cenario.set_position(0, 0)

	tabuleiro = Sprite("img/scenary/tabuleiro.png")
	tabuleiro.set_position(397, 40)

	gameo = Sprite("img/scenary/gameo.png")
	gameo.set_position(janela.width/2-gameo.width/2, janela.height/2-gameo.height/2)

	proxpecas = []
	for i in range(7):
		peca = Sprite("img/scenary/"+str(i)+".png")
		if i == 2:
			peca.set_position(780, 130)
		else:
			peca.set_position(800, 100)
		proxpecas.append(peca)

	delay = 0.3
	delaydesc = 0
	pos = []
	proxshape = randint(0, 6)
	pause = False
	while True:
		delay += janela.delta_time()
		tempototal += janela.delta_time()
		cenario.draw()
		tabuleiro.draw()

		if gameover == 0:
			minutos, segundos = contador(int(tempototal))

			if not pause:

				if nova:
					descendo = 1
					posx = 4 #posição de inicio da peça nova
					posy = 0
					shapeatual = proxshape
					pos = geraPos(shapeatual, 0, posx, posy, pos)
					colocaDentro(pos, shapeatual)
					rotation = 0
					proxshape=randint(0, 6)
					nova = False
				if (teclado.key_pressed("UP") or teclado.key_pressed("z")) and delay > 0.14:
					rotation += 1
					pos = movePeca('cima', pos, shapeatual)
					delay = 0
				if teclado.key_pressed("RIGHT") and delay > 0.14:
					pos = movePeca('direita', pos, shapeatual)
					delay = 0
				if teclado.key_pressed("LEFT") and delay > 0.14:
					pos = movePeca('esquerda', pos, shapeatual)
					delay = 0
				if teclado.key_pressed("DOWN") and delay > 0.14:
					pos = movePeca('baixo', pos, shapeatual)
					delay = 0
				if teclado.key_pressed("ESCAPE") and delay > 0.14:
					pause=not(pause)
					delay = 0


				delaydesc += janela.delta_time()
				delaydesc, pos = movimentoAtual(delaydesc, pos, shapeatual)
				pecas = coloreMatriz(tabuleiro)
				desenha(pecas)
				proxpecas[proxshape].draw()
				janela.draw_text(str(minutos)+"min"+str(segundos)+"s", 800, 600, size=30, bold=True, color=(172, 231, 237))
				janela.draw_text(str(pontos), 190, 100, size=30, bold=True, color=(222, 230, 12))
				janela.draw_text(str(strike), 260, 280, size=28, bold=True, color=(207, 78, 78))
				janela.draw_text(str(fase), 320, 460, size=40, bold=True, color=(95, 183, 219))

			else:

				certeza = Sprite("img/scenary/certeza.png")
				certeza.set_position(0, 0)

				simTrue = Sprite("img/scenary/simTrue.png")
				sim = Sprite("img/scenary/sim.png")

				simTrue.set_position(385,385)
				sim.set_position(385,385)

				naoTrue = Sprite("img/scenary/naoTrue.png")
				nao = Sprite("img/scenary/nao.png")

				naoTrue.set_position(530,385)
				nao.set_position(530,385)

				certeza.draw()

				if mouse.is_over_object(sim):
					simTrue.draw()
					if mouse.is_button_pressed(1):
						reset()
						return 0,pontos
				else:
					sim.draw()

				if mouse.is_over_object(nao):
					naoTrue.draw()
					if mouse.is_button_pressed(1):
						pause = not(pause)
				else:
					nao.draw()

		elif gameover == 1:
			pecas=coloreMatriz(tabuleiro)
			desenha(pecas)
			proxpecas[proxshape].draw()
			janela.draw_text(str(minutos)+"min"+str(segundos)+"s", 800, 600, size=30, bold=True, color=(172, 231, 237))
			janela.draw_text(str(pontos), 190, 100, size=30, bold=True, color=(222, 230, 12))
			janela.draw_text(str(strike), 260, 280, size=28, bold=True, color=(207, 78, 78))
			janela.draw_text(str(fase), 320, 460, size=40, bold=True, color=(95, 183, 219))
			if teclado.key_pressed("ESCAPE") or teclado.key_pressed("ENTER"):
				return 2,pontos
			gameo.draw()
		janela.update()
