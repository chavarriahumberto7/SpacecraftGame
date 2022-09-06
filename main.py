
import pygame
import random
import math
from pygame import mixer


#inicializamos pygame
pygame.init()



#declaramos variables iniciales de la pantalla
ancho=800
alto=600

#inicializamos el contador de puntaje
fuente=pygame.font.Font("freesansbold.ttf",32)
contador=0
texto_x=10
texto_y=10
muertes=0



#inicializamos la pantalla
pantalla= pygame.display.set_mode((ancho,alto))

#Titulo , icono y fondo

pygame.display.set_caption("Invacion Espacial")
icono=pygame.image.load("alien.png")
pygame.display.set_icon(icono)
fondo=pygame.image.load("fondo.jpg")


#cargando sonido 
mixer.music.load("musicafondo.mp3")
mixer.music.play(-1)



#inicializamos pantalla de marcador 

def monstrar_puntaje(x,y):
    texto=fuente.render(f"Puntaje:  {contador}",True,(255,255,225))
    pantalla.blit(texto,(x,y))   

#jugador determinamos las dimenciones 

img_jugador=pygame.image.load("astronave.png")
imagen_alto=64
imagen_ancho=64
jugador_x=(ancho/2)-(imagen_ancho/2)
jugador_y=alto-imagen_alto

#determinando dimenciones del enemigo

img_enemigo=pygame.image.load("enemigo.png")
enemigo_alto=64
enemigo_ancho=64
enemigo_x=random.randint(0,ancho)
enemigo_y=random.randint(0,(alto/2)+enemigo_alto)
cambio_x_enemigo=0.2
cambio_y_enemigo=enemigo_alto/2

#funcion generar enemigo
def generar_enemigo():
   global enemigo_x
   global enemigo_y
   enemigo_x=random.randint(0,ancho-enemigo_ancho)
   enemigo_y=random.randint(0,(alto/2)+enemigo_alto)


#valores de la bala
bala_img=pygame.image.load("bala.png")
bala_x=0
bala_y=0
bala_cambio=-1
bala_activa=False

#inicializamos la variable que va ajecutar el cambio 
valor_cambio=0.3
cambio_posicion_x=0
cambio_posicion_y=0

#se pinta al jugador en pantalla
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))


#se pinta al enemigo en pantalla
def enemigo(x,y):
    pantalla.blit(img_enemigo,(x,y))

#pintamos la bala
def bala(x,y):
    global bala_activa
    bala_activa=True
    if bala_activa:
        pantalla.blit(bala_img,(x,y))

#Detectar colisiones

def hay_colision(x1,y1,x2,y2):
    valor_colision=30
    distancia=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
    
    if distancia<valor_colision:
        return True
    else:
        return False


#se ejecuta la pantalla
se_ejecuta=True
while se_ejecuta:
    #cambio de color de fondo 
    pantalla.blit(fondo,(0,0))


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta=False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                cambio_posicion_x=-valor_cambio

            elif evento.key == pygame.K_RIGHT:
                cambio_posicion_x=valor_cambio          
            elif evento.key == pygame.K_DOWN:
               cambio_posicion_y=valor_cambio       
          
            elif evento.key == pygame.K_UP:
                 cambio_posicion_y=-valor_cambio 

            elif evento.key == pygame.K_SPACE:
                if  not bala_activa:
                    bala_y=jugador_y
                    bala_x=jugador_x
                    bala_activa=True
                    sonido_bala=mixer.Sound("disparo.mp3")
                    sonido_bala.play()

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                cambio_posicion_x=0
            elif evento.key == pygame.K_RIGHT:
                cambio_posicion_x=0           
            elif evento.key == pygame.K_DOWN:
               cambio_posicion_y=0           
          
            elif evento.key == pygame.K_UP:
                 cambio_posicion_y=0 
    
  
   
    
    #restablecemos bordes de pantalla para el jugador
    jugador_y+=cambio_posicion_y
    jugador_x+=cambio_posicion_x
    if jugador_x<0:
        jugador_x=0
    elif jugador_x>ancho-imagen_ancho:
        jugador_x=ancho-imagen_ancho

    if jugador_y < 0:
        jugador_y=alto
    elif jugador_y>alto-imagen_alto+10:
        jugador_y=alto-imagen_alto

    #restablecemos bordes de pantalla para elenemigo

    #redeficion de posicion para enemigo
    enemigo_x+=cambio_x_enemigo
    
    if enemigo_x<0:
        cambio_x_enemigo*=-1
        enemigo_y+=cambio_y_enemigo
    elif enemigo_x>ancho-enemigo_ancho:
        cambio_x_enemigo*=-1
        enemigo_y+=cambio_y_enemigo

    if enemigo_y>alto:
        enemigo_y=0    



 #evaluando las colisiones bala/enemigo
    if hay_colision(bala_x,bala_y,enemigo_x,enemigo_y):
        bala_activa=False
        generar_enemigo()
        contador+=1
        sonido_muerte=mixer.Sound("Golpe.mp3")
        sonido_muerte.play()
#evaluando colisiones  enemigo/jugador
    if hay_colision(jugador_x,jugador_y,enemigo_x,enemigo_y):
        contador+=1
        print(f"chocaste contra el enemigo {contador}")

  #llamada a pintar jugador en pantalla
    jugador(jugador_x,jugador_y)
    #llamada a pintar a enemigo en pantalla
    enemigo(enemigo_x,enemigo_y)
    #pintalmos marcador en pantalla
    monstrar_puntaje(texto_x,texto_y)
 #llamada a pintar la bala en pantalla
    if bala_y <0:
      bala_activa=False

    if bala_activa:
        bala_y+=bala_cambio
        bala(bala_x,bala_y)



    pygame.display.update()
    