
import pygame


pygame.init()


title = pygame.image.load("titlee.png")
new_game_button = pygame.image.load("NewGame.png")
new_game_button_select = pygame.image.load("NewGameSelect.png")
load_button = pygame.image.load("Load.png")
settings_button = pygame.image.load("Settings.png")
quit_button = pygame.image.load("Quit.png")
background = pygame.image.load("sky.png")
new_game = 0

def menu():
    
    running = True
    button_press = 1
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    dt = 0
    
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
                if event.key == pygame.K_RETURN:
                    if button_press == 1:
                        running = False
                        new_game = 1
                        save = "NewGame.txt"
                    else:
                        pass
                    

        screen.blit(background, (0,0))
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

    if new_game == 1:
        game(save)
    else:
        pass
    pygame.quit()


def game(save):
    
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    mov_amount = 8
    wall_move_amount = 1

    Map, MapText, Player_X, Player_Y = SaveFileProcess(save)
    
    walls = MapTextProcess(MapText, screen)

    character = pygame.image.load("Character.png")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        screen.blit(Map, (0,0))
        screen.blit(character, (Player_X, Player_Y))
        CharacterRect = character.get_rect(topleft = (Player_X, Player_Y))
        
        wall_touch = 0
        for x in walls:
            if CharacterRect.colliderect(x):
                wall_touch = 1


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if wall_touch == 1:
                Player_Y += mov_amount
            else:
                Player_Y -= mov_amount
        if keys[pygame.K_s]:
            if wall_touch == 1:
                Player_Y -= mov_amount
            else:
                Player_Y += mov_amount
        if keys[pygame.K_a]:
            if wall_touch == 1:
                Player_X += mov_amount
            else:
                Player_X -= mov_amount
        if keys[pygame.K_d]:
            if wall_touch == 1:
                Player_X -= mov_amount
            else:
                Player_X += mov_amount
                

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()
    

def ChangeMap(current, direction):
    if direction == "UP":
        name_rep = current.replace(".png", "")
        name_split = name_rep.split("_")
        num = int(name_split[1]) + 1
        current = name_split[0] + "_" + str(num) + ".png"
        return current   
    elif direction == "DOWN":
        name_rep = current.replace(".png", "")
        name_split = name_rep.split("_")
        num = int(name_split[1]) - 1
        current = name_split[0] + "_" + str(num) + ".png"
        return current
    elif direction == "LEFT":
        name_rep = current.replace(".png", "")
        name_split = name_rep.split("_")
        num = int(name_split[0]) - 1
        current = str(num) + "_" + name_split[1] + ".png"
        return current
    else:
        name_rep = current.replace(".png", "")
        name_split = name_rep.split("_")
        num = int(name_split[0]) + 1
        current = str(num) + "_" + name_split[1] + ".png"
        return current
    
def SaveFileProcess(save):
    SaveFile = open(save, "r")
    SaveFileLines = SaveFile.readlines()
    mapp = SaveFileLines[0]
    mapppp = mapp.strip()
    TextMap = mapppp.replace(".png", ".txt")

    mappp = pygame.image.load(mapppp)
    
    Player_X = int(SaveFileLines[1].strip())
    Player_Y = int(SaveFileLines[2].strip())
        
    return mappp, TextMap, Player_X, Player_Y

def MapTextProcess(TextFile, screen):
    flag = 0
    amount = 0
    listt = []
    
    Text = open(TextFile, "r")
    TextLines = Text.readlines()

        
    for x in TextLines:
        xxx = x.strip()
        xx = xxx.split(",")
        number = 0
        for y in xx:
            if y == "0":
                number += 1
            elif y == "1":
                x = number * 80
                yy = amount * 80
                Wall = pygame.draw.rect(screen, (255,255,255), pygame.Rect(x, yy, 80, 80))
                number += 1
                listt.append(Wall)
                number += 1
            else:
                pass
        amount += 1
                
    print(listt)
    return listt
        
        
        
            
    
menu()