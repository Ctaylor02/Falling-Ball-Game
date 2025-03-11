
import pygame
import random

pygame.init() #initialize pygame

#Create window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#set the window title
pygame.display.set_caption('Falling Objects Game!')

#load images on to the screen
paddle_image = pygame.image.load('paddle.jpeg').convert()
basketball_image = pygame.image.load('basketball.jpg').convert()
soccer_image = pygame.image.load('soccer.jpg').convert()
tennis_image = pygame.image.load('tennis.jpg').convert()
football_image = pygame.image.load('football.jpg').convert()
baseball_image = pygame.image.load('baseball.jpg').convert()

#clear white space around the image
for img in [paddle_image, basketball_image, tennis_image, football_image,
            baseball_image, soccer_image]:
    img.set_colorkey((255, 255, 255))



#change size of image
def scale_img(img, factor):
    return pygame.transform.scale(img, (int(img.get_width() / factor), int(img.get_height() / factor)))
paddle_image = scale_img(paddle_image, 3)
basketball_image = scale_img(basketball_image, 8)
soccer_image = scale_img(soccer_image, 8)
football_image = scale_img(football_image, 20)
baseball_image = scale_img(baseball_image, 18)
tennis_image = scale_img(tennis_image, 7)


#getting paddle position
paddle_x, paddle_y  = 345, 490

#speed that paddle and balls move at
image_speed = 7
ball_speed = 1
move_left, move_right = False, False


#List of available balls
ball_types = [("basketball", basketball_image),
              ("soccer", soccer_image),
              ("tennis", tennis_image),
              ("football", football_image),
              ("baseball", baseball_image)]

#active balls list
falling_balls = []

#timing for spawning the balls
last_spawn_time = pygame.time.get_ticks()
spawn_interval = 1000 #1 second in milliseconds

#initializing a font
font = pygame.font.Font(None, size=30)

#keep track of score and lives
score, lives = 0, 3

#creating a sound
drum = pygame.mixer.Sound('drum.wav')
gameMusic = pygame.mixer.Sound('gameMusic.mp3')


clock = pygame.time.Clock()
running = True

#main loop to keep the window open
while running:
    screen.fill((255, 255, 255))

    # gameMusic.play()


    score1 = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score1, (0,0))

    lives1 = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(lives1, (0,20))

    #paddle hitbox
    hitbox = pygame.Rect(paddle_x, paddle_y, paddle_image.get_width(), paddle_image.get_height())

    #handle for ball spawning every 1 second
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_interval:
        ball_name, ball_img = random.choice(ball_types)
        ball_x = random.randint(0, WIDTH - ball_img.get_width())
        ballHeight = ball_img.get_height()
        ballWidth = ball_img.get_width()
        falling_balls.append({"Image": ball_img,
                              "x": ball_x,
                              "y": 0,
                              "width": ballWidth,
                              "height": ballHeight}) #add a falling ball
        last_spawn_time = current_time


    #make the objects fall
    for ball in falling_balls:
        ball["y"] += ball_speed
        screen.blit(ball["Image"], (ball["x"], ball["y"]))
        # handle if ball collides with paddle
        target = pygame.Rect(ball["x"], ball["y"], ball["width"], 15)
        collide = hitbox.colliderect(target)
        if collide:
            score += 1
            score1 = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score1, (0, 0))
        #handle for if ball is missed by paddle
        if 495 < ball["y"] < HEIGHT and not collide:
            lives -= 1
            lives1 = font.render(f"Lives: {lives}", True, (0, 0, 0))
            screen.blit(lives1, (0, 20))




    #remove balls that reach the bottom of screen
    falling_balls = [ball for ball in falling_balls if ball["y"] < HEIGHT]



    #put paddle on screen
    screen.blit(paddle_image, (paddle_x, paddle_y))

    #keeping track of events in game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if a key is pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = True
        #if a key is let go of
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = False

    #move paddle based on keys
    if move_left:
        paddle_x -= image_speed
    if move_right:
        paddle_x += image_speed

    # Keep paddle inside screen bounds
    paddle_x = max(0, min(800 - paddle_image.get_width(), paddle_x))

    pygame.display.flip()

    clock.tick(60)

pygame.quit() #quits game
