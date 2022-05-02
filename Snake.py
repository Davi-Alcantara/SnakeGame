# Importando bilbiotecas
import pygame as pg
from pygame.locals import *
from sys import exit
from random import randint
from time import sleep

# Definindo bases
pg.init()
init_comp = 10
controleMusica = 0
contagem = 4
contagemDpsMorte = True
xControle = 20
yControle = 0
dead = False
controleDeTela = True
vel = 10
lostLife = pg.mixer.Sound('sons/smw_lost_a_life.wav')
menu = pg.display.set_mode((640, 480))
pg.mixer.music.set_volume(0.60)
MusicaDeFundo = pg.mixer.music.load('sons/MusicFundo.mp3')
pg.mixer.music.play(-1)
lista_cobra = []
x = 320
y = 240
relogio = pg.time.Clock()
fruta_x = randint(40, 600)
fruta_y = randint(50, 430)
tela = pg.display.set_mode((640, 480))
pg.display.set_caption('Snake')
fonte = pg.font.SysFont('arial', 40, True, True)
fonte4 = pg.font.SysFont('arial', 20, True, True)
pontos = 0
fonte5 = pg.font.SysFont('arial', 40, True, True)
fonte6 = pg.font.SysFont('arial', 20, True, True)



#Definindo funções
def mudarCorFruta(varPontos):
    if varPontos <= 10:
        cor = (255, 0, 0)
    elif varPontos <= 30:
        cor = (0, 255, 0)
    elif varPontos <= 50:
        cor = (0, 0, 255)
    else:
        cor = (128, 0, 128)
    return cor


def arquivo_existente(arq):
    try:
        a = open(arq, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True



def criar_arquivo(arq):
    try:
        a = open(arq, 'wt+')
        a.close()
    except:
        print('Erro ao criar o arquivo.')
        sleep(3)
    else:
        pass


def salvarPontuacao(arq, varPontos):
    try:
        a = open(arq, 'at')
    except:
        print('Erro ao ler arquivo.')
        sleep(3)
    else:
        varPontosFormatado = f'{varPontos}\n'
        a.write(varPontosFormatado)
        a.close()


def verPontuacao(arq):
    global pontuacao
    pontuacao = []
    pontuacaoNum = []
    try:
        a = open(arq, 'rt')
    except:
        print('Erro ao ler arquivo.')
    else:
        for l in a:
            pontuacao.append(l.replace('\n', ''))
        pontos =len(pontuacao)
        for p in range(0, pontos):
            pontuacaoNum.append(int(pontuacao[p]))
        maiorValor = max(pontuacaoNum)
        a.close()
        return maiorValor


def corpoCobra(lista):
    for xy in lista:
        pg.draw.rect(tela, (255, 255, 255), (xy[0], xy[1], 20, 20))


def reiniciarJogo():
    global pontos, init_comp, x, y, lista_cobra, lista_cabeca, fruta_x, fruta_y, vel, dead
    pontos = 0
    init_comp = 10
    x = 320
    y = 240
    lista_cobra = []
    lista_cabeca = []
    fruta_x = randint(40, 600)
    fruta_y = randint(50, 430)
    vel = 10
    dead = False


# Verifica se o arquivo existe
arquivo = 'Pontuações.txt'
if not arquivo_existente(arquivo): # Se o arquivo não existir, crie
    criar_arquivo(arquivo)


while True:
    # Tela de boas vindas
    while controleDeTela:
        tela.fill((0, 0, 0))
        boasVindas = 'Bem vindo. Pressione SPACE para jogar.'
        boasVindasFormat = fonte4.render(boasVindas, True, (255, 255, 255))
        boasVindasRet = boasVindasFormat.get_rect()
        boasVindasRet.center = (320, 240)
        tela.blit(boasVindasFormat, boasVindasRet)
        pg.display.update()

        for evento in pg.event.get():
            if evento.type == QUIT:
                pg.quit()
                exit()

            if evento.type == KEYDOWN:
                if evento.key == K_SPACE:
                    controleDeTela = False
    # Contagem regressiva para o jogo começar
    while contagem != 0:
        contagem -= 1
        tela.fill((0, 0, 0))
        contagemstr = str(f'{contagem}')
        sleep(1)
        contagemFormatada = fonte5.render(contagemstr, True, (255, 255, 255))
        tela.blit(contagemFormatada, (320, 240))
        pg.display.update()
        for evento in pg.event.get():
            if evento.type == QUIT:
                pg.quit()
                exit()
    # Tela de Jogo
    relogio.tick(vel)
    tela.fill((0, 0, 0))
    msg = f'Pontos {pontos}'
    msgFormat = fonte.render(msg, True, (255, 255, 255))
    for evento in pg.event.get():
        if evento.type == QUIT:
            pg.quit()
            exit()

        if evento.type == KEYDOWN:
            if evento.key == K_a or evento.key == K_LEFT:
                if xControle == 20:
                    pass
                else:
                    xControle = -20
                    yControle = 0
            if evento.key == K_d or evento.key == K_RIGHT:
                if xControle == -20:
                        pass
                else:
                    xControle = +20
                    yControle = 0
            if evento.key == K_s or evento.key == K_DOWN:
                if yControle == -20:
                    pass
                else:
                    yControle = +20
                    xControle = 0
            if evento.key == K_w or evento.key == K_UP:
                if yControle == 20:
                    pass
                else:
                    yControle = -20
                    xControle = 0
    x += xControle
    y += yControle

    cobra = pg.draw.rect(tela, (255, 255, 255), (x, y, 20, 20))
    fruta = pg.draw.rect(tela, mudarCorFruta(pontos), (fruta_x, fruta_y, 20, 20))
    if cobra.colliderect(fruta):
        if pontos < 30:
            pontos += 1
        elif pontos < 50:
            pontos += 2
        else:
            pontos += 3
        vel += 1
        init_comp += 1
        contato = pg.mixer.Sound('sons/smw_coin.wav')
        contato.play()
        fruta_x = randint(40, 600)
        fruta_y = randint(50, 430)

    tela.blit(msgFormat, (450, 40))
    lista_cabeca = []
    lista_cabeca.append(x)
    lista_cabeca.append(y)
    lista_cobra.append(lista_cabeca)
    # Tela de Game Over
    if lista_cobra.count(lista_cabeca) != 1:
        salvarPontuacao(arquivo, pontos)
        recorde = verPontuacao(arquivo)
        fonte3 = pg.font.SysFont('arial', 20, True, True)
        gameOver = 'Game Over. Pressione R para reiniciar.'
        recordestr = f'Maior pontuação: {recorde}'
        gameOverFormatado = fonte3.render(gameOver, True, (255, 255, 255))
        recordeFormatado = fonte6.render(recordestr, True, (255, 255, 255))
        retText = gameOverFormatado.get_rect()
        controleMusica = 0
        dead = True
        while dead:
            controleMusica += 1
            pg.mixer.music.rewind()
            if controleMusica == 1:
                lostLife.play()
            tela.fill((0, 0, 0))
            for evento in pg.event.get():
                if evento.type == QUIT:
                    pg.quit()
                    exit()
                if evento.type == KEYDOWN:
                    if evento.key == K_r:
                        # Contegem regressiva após a morte
                        contagem = 4
                        while contagem != 0:
                            contagem -= 1
                            tela.fill((0, 0, 0))
                            contagemstr = str(f'{contagem}')
                            sleep(1)
                            contagemFormatada = fonte5.render(contagemstr, True, (255, 255, 255))
                            tela.blit(contagemFormatada, (320, 240))
                            pg.display.update()
                            for evento in pg.event.get():
                                if evento.type == QUIT:
                                    pg.quit()
                                    exit()
                        reiniciarJogo()



            retText.center = (320, 240)
            tela.blit(gameOverFormatado, (retText))
            tela.blit(recordeFormatado, (450, 450))
            pg.display.update()
    if len(lista_cobra) > init_comp:
        del lista_cobra[0]

    corpoCobra(lista_cobra)
    if x > 640:
        x = 0
    if x < 0:
        x = 640
    if y > 480:
        y = 0
    if y < 0:
        y = 480
    pg.display.update()
