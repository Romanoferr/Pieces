
T = ['..0..',
     '..0..',
     '..0..',
     '..0..',
     '.....']
shapes = [S, Z, I, O, J, L, T]


pecaXY=[3,2]

def geraPos(shape,rotation,tabuleiro,posx,posy):
	global shapes
	pos = []
	format=shapes[shape][rotation%len(shapes[shape])]
	for i in range(len(format)):
		linha=list(format[i])
		for j in range(len(linha)):
			if linha[j]=='0':
				pos.append([posx+j-2,posy+i-2])
	return pos

def colocaDentro(pos,shape):
	global table
	for x,y in pos:
		tabuleiro[x][y]=shape

def tiraFora(pos):
	for x,y in pos:
		tabuleiro[x][y]='V'


def movePeca(direcao,pos):
	newpos=[]
	if direcao=='direita':
		for i in range(len(pos)):
			newpos.append([pos[i][0]+1,pos[i][1]])
	elif direcao=='esquerda':
		for i in range(len(pos)):
			newpos.append([pos[i][0]-1,pos[i][1]])
	elif direcao=='baixo':
		for i in range(len(pos)):
			newpos.append([pos[i][0],pos[i][1]+1])
	tiraFora(pos)
	colocaDentro(newpos)
	return newpos



table = [['V' for i in range(10)] for j in range(20)]

modelo='1'
peca = [[4,1],[4,2],[4,3],[5,2]]



for i in range(4):
	peca[i][1]+=1
