from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from jogo2 import reset

def fim(pontos):
    nome = str(input('Digite o nome: '))
    arq = open('ranking.txt', 'r')
    conteudo = arq.readlines()
    linha = nome + ' ' + str(pontos) + '\n'
    conteudo.append(linha)
    arq.close()
    arq = open('ranking.txt', 'w')
    arq.writelines(conteudo)
    arq.close()
    reset()

    print('Pontuacao armazenada com sucesso')

    return 0
