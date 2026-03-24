import sys
import pygame
import random

pygame.init() #boots all of them up at once (all the subsystems that is in pygame)

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

#define some colors
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (0,   200, 100)
PURPLE = (120, 80,  220)
OFFWHITE = (220, 220, 220)


left_y  = 250
right_y = 250
ball_x = 295
ball_y = 295
ball_vx = -4   # velocity: moves 4 pixels right every frame
ball_vy = -3   # velocity: moves 3 pixels down every frame
left_score = 0
right_score = 0
prev_ball_x = ball_x   # removes the problem of tunneling (ball passing through the paddle at high pixel speeds)

font = pygame.font.SysFont("monospace", 64, bold=True)
win_font = pygame.font.SysFont("arial", 80, bold=True)
small_font = pygame.font.SysFont("arial", 32)

while True:

    menu = None
    while menu is None:

        screen.fill(BLACK)

        title_text = win_font.render("Pong", True, OFFWHITE)
        single_text = font.render("Singleplayer", True, OFFWHITE)
        multi_text = font.render("multiplayer", True, OFFWHITE)

        screen.blit(title_text, (400 -title_text.get_width()//2, 100))
        screen.blit(single_text, (400 - single_text.get_width()//2, 300))
        screen.blit(multi_text, (400 -multi_text.get_width()//2, 380))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (400 - single_text.get_width()//2 < mouse_x < 400 - single_text.get_width()//2 + single_text.get_width()) and (300 < mouse_y < 300 + single_text.get_height()):

                    menu = "single"

                elif (400 - multi_text.get_width()//2 < mouse_x < 400 - multi_text.get_width()//2 + multi_text.get_width()) and (400 < mouse_y < 400 + multi_text.get_height()):

                    menu = "multi"



    #game loop
    running = True
    while running:

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        #left-paddle (W and S)
        if keys[pygame.K_w] and left_y > 0:
            left_y -= 10
        if keys[pygame.K_s] and left_y < 520:
            left_y += 10
        
        if menu == "multi":
        
            #Right paddle — arrow keys
            if keys[pygame.K_UP] and right_y >0:
                right_y -= 10
            if keys[pygame.K_DOWN] and right_y < 520:
                right_y += 10
        elif menu == "single":

            x = random.randint(1,10)

            if ball_y < right_y and right_y >0:
                if x < 10:
                    right_y -= random.choice([4,3,1,2])
                
            elif ball_y > right_y  and right_y < 520:
                if x < 10:
                    right_y += random.choice([4,3,1,2])
            
        # Move the ball
        prev_ball_x = ball_x # Bug correction, we need to save the current position of ball before changing it...
        ball_x += ball_vx
        ball_y += ball_vy

        # Bounce off top and bottom walls
        if ball_y <= 0 or ball_y >= 590:
            ball_vy *= -1

        # Ball goes off left or right — reset to center
        if ball_x < 0:
            right_score += 1
            ball_x = 395
            ball_y = 295
            ball_vy = random.choice([-3, -2, -1, 1, 2, 3])
            ball_vx = -4
        if ball_x > 800:    
            left_score += 1
            ball_x = 395
            ball_y = 295
            ball_vy = random.choice([-3, -2, -1, 1, 2, 3])
            ball_vx = 4
        
        # ball hits paddle
        # if (((ball_x >= 36) and (ball_x <= 46)) and ((ball_y > (left_y)) and (ball_y < (left_y + 80)))) or (((ball_x >= 754) and (ball_x <= 762)) and ((ball_y > (right_y)) and (ball_y < (right_y + 80)))):
        #     ball_vx *= -1

        # Left paddle — did ball cross x=42 from right to left?
        if prev_ball_x >= 42 and ball_x <= 42 and (left_y - 10 < ball_y < left_y + 90):  #increased 10 in both sides to manage the miss bug
            ball_x = 42
            ball_vx *= -1.2
            if abs(ball_vx) > 20:
                ball_vx = 20

        # Right paddle — did ball cross x=758 from left to right?
        if prev_ball_x <= 758 and ball_x >= 758 and (right_y - 10 < ball_y < right_y + 90):
            ball_x = 758
            ball_vx *= -1.2
            if abs(ball_vx) > 20:
                ball_vx = -20

        #draw the background of game screen
        screen.fill(BLACK)

        # Left paddle
        pygame.draw.rect(screen, GREEN, (30, left_y, 12, 80))

        # Right paddle
        pygame.draw.rect(screen, PURPLE, (758, right_y, 12, 80))

        # Ball
        pygame.draw.rect(screen, WHITE, (ball_x, ball_y, 10, 10))

        #dashed line
        for y in range(0, 600, 20):
            pygame.draw.rect(screen, WHITE, (395, y, 10, 10))
            
        #prints the score
        left_text  = font.render(str(left_score),  True, GREEN)
        right_text = font.render(str(right_score), True, PURPLE)
        screen.blit(left_text,  (200, 20))
        screen.blit(right_text, (560, 20))

        if left_score == 10 or right_score == 10:       # to get that screen at the end (winner, play again and quit)
                screen.fill(BLACK)

                if left_score == 10:
                    win_text = win_font.render("LEFT WINS", True, OFFWHITE)
                else:
                    win_text = win_font.render("RIGHT WINS", True, OFFWHITE)
                
                screen.blit(win_text, (400 - win_text.get_width()//2, 180))
                again_text = small_font.render("Press Q to play again", True, OFFWHITE)
                quit_text = small_font.render("Press E to quit", True, OFFWHITE)

                screen.blit(again_text, (400 - again_text.get_width()//2, 320))
                screen.blit(quit_text,  (400 - quit_text.get_width()//2,  390))

                pygame.display.flip()

                #input
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            waiting = False
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                            # Reset everything
                                left_y  = 250
                                right_y = 250
                                ball_x  = 395
                                ball_y  = 295
                                ball_vx = -4
                                ball_vy = -3
                                left_score  = 0
                                right_score = 0
                                waiting = False
                                menu = None
                                running = False
                            if event.key == pygame.K_e:
                                waiting = False
                                running = False
                                
            

        # pygame.draw.rect(surface, color, (x, y, width, height))
        pygame.display.flip()

        #tick       
        clock.tick(60)

    pygame.quit()
    sys.exit()