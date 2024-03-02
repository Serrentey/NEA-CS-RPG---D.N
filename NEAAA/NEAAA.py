import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

title = pygame.image.load("titlee.png")
new_game_button = pygame.image.load("NewGame.png")
new_game_button_select = pygame.image.load("NewGameSelect.png")
load_button = pygame.image.load("Load.png")
settings_button = pygame.image.load("Settings.png")
quit_button = pygame.image.load("Quit.png")

def menu():
    running = True
    button_press = 1
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if button_press != 1:
                        button_press -= 1
                    else:
                        button_press = 1
                if event.key == pygame.K_s:
                    if button_press != 4:
                        button_press += 1
                    else:
                        button_pressm= 4
                if event.key == pygame.K_KP_ENTER:
                    

        screen.fill("white")
        screen.blit(title, (390, 100))

        if button_press == 1:
            screen.blit(new_game_button_select, (554, 400))
        else:
            screen.blit(new_game_button, (554,400) )
        if button_press == 2:
            pass
        else:
            screen.blit(load_button, (554,435) )
        if button_press == 3:
            pass
        else:
            screen.blit(settings_button, (554,470) )
        if button_press == 4:
            pass
        else:
            screen.blit(quit_button, (554,505) )


        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()

menu()