"""
This code was developed by the owner of the
"Tech with Tim" Youtube channel. I just wanted to share
the same information for the spanish community. You can
watch the original tutorial in the YouTube Channel 
"Tech with Tim".
"""

import pygame
import os

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500   
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255 , 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Grenade.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Shot.wav')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#Fotogramas por segundo
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 90, 70   

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('spaceship_yellow.png'))
#YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    #YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('spaceship_red.png'))
#RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    #RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('space.png')), (WIDTH, HEIGHT))


#Esta función sirve para dibujar lo que necesitemos en la pantalla
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #El orden en el que dibujamos las cosas importa
    #Si dibujas la spaceship antes que el fondo, la spaceship 
    #no se verá
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    #WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    #WIN.blit(RED_SPACESHIP, (red.x, red.y))
    #YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
    #(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),x)
    #WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    #Actualiza la pantalla
    #pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow,x):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        x=270
        yellow.x -= VEL    
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
        x=90
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        x=180
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
        x=0
        yellow.y += VEL
    YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
    (YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),x)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    pygame.display.update()
    return x

def red_handle_movement(keys_pressed, red, y):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        y=270
        red.x -= VEL    
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
        y=90
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        y=180
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #DOWN
        y=0
        red.y += VEL
    RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
    (RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),y)
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    pygame.display.update()
    return y

#Esta función se encarga del movimiento de las balas, de la colisión de éstas
#y de eliminarlas cuando se salen de la pantalla
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 
                        2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Función principal
def main():
    #Estos rectángulos representan las spaceship
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        #Se encarga de que este bucle se repita 60 veces por segundo
        clock.tick(FPS)

        #pygame.event.get() es una lista con todos los eventos
        #de pygame. Con el bucle for la recorremos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 5, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                #Se utilizan dos // en la división para que el resultado sea un número entero
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 + 5, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
  
        #Devuelve una lista con las teclas presionadas
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, 90)
        red_handle_movement(keys_pressed, red, 270)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


    main()

#Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()