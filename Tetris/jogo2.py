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


table = [['V' for i in range(10)] for j in range(20)]
shapes = [S, Z, I, O, J, L, T]


def geraPos(shape,rotation,posx,posy,pos):
	global shapes,locked
	newpos = []
	format=shapes[shape][rotation%len(shapes[shape])]
	for i in range(len(format)):
		linha=list(format[i])
		for j in range(len(linha)):
			if linha[j]=='0':
				#if posx+j-2<0 or posx+j-2>9 or posy+i-2>19 or [posx+j-2,posy+i-2] in locked:
					#return pos
				newpos.append([posx+j-2,posy+i-2])
	return newpos

def colocaDentro(pos, shape):
	global table

	for x, y in pos:
		if table[y][x] == 'V':
			table[y][x] = shape


def tiraFora(pos):
	global table
	for x,y in pos:
		table[y][x]='V'


def movePeca(direcao,pos,shape):
	global nova,table,posx,posy,rotation
	newpos=[]
	if direcao=='direita':
		for i in range(len(pos)):
			newx=pos[i][0]+1
			if newx>=0 and newx<=9 and [pos[i][0]+1,pos[i][1]] not in locked:
				newpos.append([pos[i][0]+1,pos[i][1]])
			else:
				return pos
		posx+=1
	elif direcao=='esquerda':
		for i in range(len(pos)):
			newx=pos[i][0]-1
			if newx>=0 and newx<=9 and [pos[i][0]-1,pos[i][1]] not in locked:
				newpos.append([pos[i][0]-1,pos[i][1]])
			else:
				return pos
		posx-=1
	elif direcao=='baixo':
		for i in range(len(pos)):
			newy=pos[i][1]+1
			if newy<=19 and [pos[i][0],pos[i][1]+1] not in locked:
				newpos.append([pos[i][0],pos[i][1]+1])
			else:
				locked.extend(pos)
				destroiLinha()
				nova=True
				locked.sort(key=segundo)
				return pos
		posy+=1
	elif direcao=='cima':
		newpos1=geraPos(shape,rotation,posx,posy,pos)
		if newpos1 not in locked:
			newpos=geraPos(shape,rotation,posx,posy,pos)
		else:
			return pos

	tiraFora(pos)
	colocaDentro(newpos,shape)
	return newpos


def movimentoAtual(delaydesc,pos,shape):
	global descendo,table
	if delaydesc>0.42:
		if descendo==1:
			pos=movePeca('baixo',pos,shape)
		return 0,pos
	else:
		return delaydesc,pos


def desenha(matriz):
	for i in range(len(matriz)):
		matriz[i].draw()


def coloreMatriz(tabuleiro):
	global table
	pecas=[]
	for i in range(len(table)):
		for j in range(len(table[i])):
			if table[i][j]!='V':
				pecinha=Sprite("img/colors/"+str(table[i][j]+1)+".png")
				pecinha.x=tabuleiro.x+j*30
				pecinha.y=tabuleiro.y+i*30
				pecas.append(pecinha)
	return pecas


def segundo(elem):
	return elem[1]

def destroiLinha():
	global locked, table
	i=19
	while i>=0:
		if 'V' not in table[i]:
			print(table[i])
			for row in range(10):
				print(i)
				print(row)
				locked.remove([row, i])
			table[i] = ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']
			for k in range(i, 0, -1):
				table[k] = table[k-1]
				if k == 0:
					table[k] = ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']
				#if table[k-1] == ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'] and table[k-2] == ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']:
				#	break


			for k in range(len(locked)):
				if locked[k][1]<i:
					locked[k][1]+=1
				elif locked[k][1]>i:
					break

		else:
			i-=1




descendo = 1
nova=True
locked=[]
posx,posy=0,0
rotation=0


def jogo(janela):
	global nova,descendo,posx,posy,rotation
	mouse = Window.get_mouse()
	teclado = Window.get_keyboard()

	cenario = Sprite("img/scenary/jogo.png")
	cenario.set_position(0,0)

	tabuleiro = Sprite("img/scenary/tabuleiro.png")
	tabuleiro.set_position(397,40)

	delay=0.3
	delaydesc=0
	pos=[]
	while True:
		delay+=janela.delta_time()
		cenario.draw()
		tabuleiro.draw()
		if nova == True:
			descendo = 1
			shapeatual=randint(0,6)
			posx=4
			posy=2
			pos = geraPos(shapeatual,0,posx,posy,pos)
			colocaDentro(pos,shapeatual)
			rotation=0
			nova = False
		if (teclado.key_pressed("UP") or teclado.key_pressed("UP")) and delay>0.17:
			rotation+=1
			pos=movePeca('cima',pos,shapeatual)
			delay=0
		if teclado.key_pressed("RIGHT") and delay>0.17:
			pos=movePeca('direita',pos,shapeatual)
			delay=0
		if teclado.key_pressed("LEFT") and delay>0.17:
			pos=movePeca('esquerda',pos,shapeatual)
			delay=0
		if teclado.key_pressed("DOWN") and delay>0.25:
			pos=movePeca('baixo',pos,shapeatual)
			delay=0
		delaydesc+=janela.delta_time()
		delaydesc,pos=movimentoAtual(delaydesc,pos,shapeatual)
		pecas=coloreMatriz(tabuleiro)
		desenha(pecas)
		janela.update()
