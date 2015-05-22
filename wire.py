from time import sleep
import RPi.GPIO as GPIO
import pygame


pygame.init()
pygame.mixer.init()


GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(21, GPIO.IN, GPIO.PUD_UP)

def life_counter(i):
    if i == 3:
        GPIO.output(14,1)
        GPIO.output(15,1)
        GPIO.output(18,1)
    elif i == 2:
        GPIO.output(14,1)
        GPIO.output(15,1)
        GPIO.output(18,0)
    elif i == 1:
        GPIO.output(14,1)
        GPIO.output(15,0)
        GPIO.output(18,0)
    elif i == 0:
        GPIO.output(14,0)
        GPIO.output(15,0)
        GPIO.output(18,0)

def picture(img,w,h):
    pic = pygame.image.load(img)
    background = (255, 64, 64)
    screen = pygame.display.set_mode((w,h))
    screen.fill((background))
    screen.blit(pic,(0,0))
    pygame.display.flip()
    sleep(2)
    pygame.display.quit()

try:
    toggle = False 
    picture('./pi.jpg',640,771)
    while True:
        if GPIO.input(21) == False:
            lives = 3
            pygame.mixer.music.load('./fanfare.mp3')
            pygame.mixer.music.play(1)
            toggle = True
            while True:
                if toggle == True:
                    print("You have "+str(lives)+" lives left")
                    life_counter(lives)
                    if GPIO.input(2) == False:
                        GPIO.output(24,1)
                        sleep(0.2)
                        GPIO.output(24,0)
                        pygame.mixer.music.load('./wrong.mp3')
                        pygame.mixer.music.play(1)
                        picture('shockdanger.jpg',724,634)
                        lives = lives - 1
                        life_counter(lives)
                        print("You have "+str(lives)+" lives left")
                        sleep(3)
                    elif lives == 0:
                        pygame.mixer.music.load('./wrong.mp3')
                        pygame.mixer.music.play(2)
                        print("GAME OVER")
                        sleep(3)
                        break
        else:
            print("Press Button to play")
except KeyboardInterrupt:
    GPIO.cleanup()
    print("EXIT")
