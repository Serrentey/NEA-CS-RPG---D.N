
import pygame
import random
import time

pygame.init()


Title = pygame.image.load("MainMenu/Title.png")
NewGameButton = pygame.image.load("MainMenu/NewGame.png")
NewGameButtonSelect = pygame.image.load("MainMenu/NewGameSelect.png")
LoadButton = pygame.image.load("MainMenu/Load.png")
SettingsButton = pygame.image.load("MainMenu/Settings.png")
QuitButton = pygame.image.load("MainMenu/Quit.png")
Background = pygame.image.load("MainMenu/Sky.png")


def menu():
    
    running = True
    ButtonPress = 1
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    dt = 0
    NewGame = 0
    
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if ButtonPress != 1:
                        ButtonPress -= 1
                    else:
                        ButtonPress = 1
                if event.key == pygame.K_s:
                    if ButtonPress != 4:
                        ButtonPress += 1
                    else:
                        button_pressm= 4
                if event.key == pygame.K_RETURN:
                    if ButtonPress == 1:
                        running = False
                        NewGame = 1
                        save = "NewGame.txt"
                    elif ButtonPress == 4:
                        running = False
                        
                    

        screen.blit(Background, (0,0))
        screen.blit(Title, (390, 100))

        if ButtonPress == 1:
            screen.blit(NewGameButtonSelect, (554, 400))
        else:
            screen.blit(NewGameButton, (554,400) )
        if ButtonPress == 2:
            pass
        else:
            screen.blit(LoadButton, (554,435) )
        if ButtonPress == 3:
            pass
        else:
            screen.blit(SettingsButton, (554,470) )
        if ButtonPress == 4:
            pass
        else:
            screen.blit(QuitButton, (554,505) )


        pygame.display.flip()

        dt = clock.tick(60) / 1000

    if NewGame == 1:
        game(save)
    else:
        pygame.quit()
    pygame.quit()


def game(save):
    
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    MoveAmount = 8

    Map, MapText, PlayerX, PlayerY, MapName, HP, MaxHP, Attack, Speed, Level = SaveFileProcess(save)
    
    MainCharacter = Character("Characters/Character.png", HP, MaxHP, Attack, Speed, Level, PlayerX, PlayerY)
    print(MainCharacter.GetHP())
    
    TempPlayerX = PlayerX
    TempPlayerY = PlayerY
    MoveEnemyStart = time.time()
    Decision = 2

    Walls = MapTextProcess(MapText, screen)

    MainCharacter = pygame.image.load("Characters/Character.png")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        screen.blit(Map, (0,0))

        CharacterRect = MainCharacter.get_rect(topleft = (PlayerX, PlayerY))
        TempCharacterRect = MainCharacter.get_rect(topleft = (TempPlayerX, TempPlayerY))

        WallTouchNum = 0
        WallTouchNum = WallTouch(CharacterRect, Walls)
        
        TempPlayerX = PlayerX
        TempPlayerY = PlayerY

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            TempPlayerY -= MoveAmount
            WallTouchNum = WallTouch(TempCharacterRect, Walls)
            if WallTouchNum == 1:
                pass
            elif WallTouchNum == 0:
                PlayerY -= MoveAmount    
            if PlayerY == 0:
                try:
                    MapName2 = MapName
                    MapName, NewMapText = ChangeMap(MapName, "UP")
                    Map = pygame.image.load(MapName)
                    Walls = MapTextProcess(NewMapText, screen)
                    PlayerY = 712
                except:
                    MapName = MapName2
                    PlayerY = 8
        if keys[pygame.K_s]:
            TempPlayerY += MoveAmount
            WallTouchNum = WallTouch(TempCharacterRect, Walls)
            if WallTouchNum == 1:
                pass
            elif WallTouchNum == 0:
                PlayerY += MoveAmount
            if PlayerY >= 720:
                try:
                    MapName2 = MapName
                    MapName, NewMapText = ChangeMap(MapName, "DOWN")
                    Map = pygame.image.load(MapName)
                    Walls = MapTextProcess(NewMapText, screen)
                    PlayerY = 8
                except:
                    MapName = MapName2
                    PlayerY = 712
        if keys[pygame.K_a]:
           TempPlayerX -= MoveAmount
           WallTouchNum = WallTouch(TempCharacterRect, Walls)
           if WallTouchNum == 1:
              pass
           elif WallTouchNum == 0:
              PlayerX -= MoveAmount
           if PlayerX == 0:
                try:
                    MapName2 = MapName
                    MapName, NewMapText = ChangeMap(MapName, "LEFT")
                    Map = pygame.image.load(MapName)
                    Walls = MapTextProcess(NewMapText, screen)
                    PlayerX = 1272
                except:
                    MapName = MapName2
                    PlayerX = 8
        if keys[pygame.K_d]:
           TempPlayerX += MoveAmount
           WallTouchNum = WallTouch(TempCharacterRect, Walls)
           if WallTouchNum == 1:
               pass
           elif WallTouchNum == 0:
               PlayerX += MoveAmount
           if PlayerX == 1280:
               try: 
                   MapName2 = MapName
                   MapName, NewMapText = ChangeMap(MapName, "RIGHT")
                   Map = pygame.image.load(MapName)
                   Walls = MapTextProcess(NewMapText, screen)
                   PlayerX = 8
               except:
                   MapName = MapName2
                   PlayerX = 1272
                   
        EnemyWalkTime = time.time() - MoveEnemyStart

        if EnemyWalkTime >= 3:
            Cat.Walk(screen, Decision, Walls)
            if EnemyWalkTime >= 3.2:
                Decision = random.randint(0,4)
                MoveEnemyStart = time.time()

           
        Cat.Spawn(screen)
        
        if CharacterRect.colliderect(Cat.Get_Rect()):
            print("yes")
            
        screen.blit(MainCharacter, (PlayerX, PlayerY))
        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()
    

def ChangeMap(NewMap, direction):
    if direction == "UP":
        NameReplace = NewMap.replace(".png", "")
        NameSplit = NameReplace.split("_")
        Number = int(NameSplit[1]) + 1
        NewMap = NameSplit[0].strip() + "_" + str(Number) + ".png"
        NewMapText = NameSplit[0].strip() + "_" + str(Number) + ".txt"
        return NewMap, NewMapText
    elif direction == "DOWN":
        NameReplace = NewMap.replace(".png", "")
        NameSplit = NameReplace.split("_")
        Number = int(NameSplit[1]) - 1
        NewMap = NameSplit[0].strip() + "_" + str(Number) + ".png"
        NewMapText = NameSplit[0].strip() + "_" + str(Number) + ".txt"
        print(NewMap, NewMapText)
        return NewMap, NewMapText
    elif direction == "LEFT":
        NameReplace = NewMap.replace(".png", "")
        NameSplit = NameReplace.split("_")
        Number = int(NameSplit[0]) - 1
        NewMap = str(Number) + "_" + NameSplit[1].strip() + ".png"
        NewMapText = str(Number) + "_" + NameSplit[1].strip() + ".txt"
        return NewMap, NewMapText
    else:
        NameReplace = NewMap.replace(".png", "")
        NameSplit = NameReplace.split("_")
        Number = int(NameSplit[0]) + 1
        NewMap = str(Number) + "_" + NameSplit[1].strip() + ".png"
        NewMapText = str(Number) + "_" + NameSplit[1].strip() + ".txt"
        return NewMap, NewMapText
    
def SaveFileProcess(save):
    SaveFile = open(save, "r")
    SaveFileLines = SaveFile.readlines()
    Map = SaveFileLines[0]
    MapStrip = Map.strip()
    TextMap = MapStrip.replace(".png", ".txt")

    LoadMap = pygame.image.load(MapStrip)
    
    PlayerX = int(SaveFileLines[1].strip())
    PlayerY = int(SaveFileLines[2].strip())
    HP = int(SaveFileLines[3].strip())
    MaxHP = int(SaveFileLines[4].strip())
    Attack = int(SaveFileLines[5].strip())
    Speed = int(SaveFileLines[6].strip())
    Level = int(SaveFileLines[7].strip())
        
    return LoadMap, TextMap, PlayerX, PlayerY, Map, HP, MaxHP, Attack, Speed, Level

def MapTextProcess(TextFile, screen):
    YNumber = 0
    WallList = []
    EnemyList = []
    
    Text = open(TextFile, "r")
    TextLines = Text.readlines()


    for x in TextLines:
        XStrip = x.strip()
        XSplit = XStrip.split(",")
        XNumber = 0
        for y in XSplit:
            if y == "0":
                XNumber += 1
            elif y == "1":
                x = XNumber * 80
                yy = YNumber * 80
                Wall = pygame.draw.rect(screen, (255,255,255), pygame.Rect(x, yy, 80, 80))
                WallList.append(Wall)
                XNumber += 1
            elif y == "2":
                enemy = "yes"
                EnemyList.append(enemy)
                XNumber += 1
            else:
                pass
                
        YNumber += 1
    return WallList
  
def WallTouch(CharacterRect, walls):
    WallTouchNum = 0
    for x in walls:
        if CharacterRect.colliderect(x):
            WallTouchNum = 1
    return WallTouchNum
        
class Enemy():
    def __init__(self, Image, HP, Attack, Speed, Typing, X, Y):
        self.Image = pygame.image.load(Image)
        self.HP = HP
        self.Attack = Attack
        self.Speed = Speed
        self.Typing = Typing
        self.X = X
        self.Y = Y
        self.EnemyRect = self.Image.get_rect(topleft = (self.X, self.Y))
        
    def Spawn(self, screen):
        screen.blit(self.Image, (self.X, self.Y))
        
    def Change_Location(self, x, y):
        self.X = x
        self.Y = y
        
    def Get_Rect(self):
        return self.EnemyRect
    
    def UpdateRect(self):
        self.EnemyRect = self.Image.get_rect(topleft = (self.X, self.Y))
        
    def Walk(self, screen, decision, walls):
        
        WallTouchNum = 0

        if decision == 0:
            if self.Y >= 720:
                self.Y = 712
                Cat.UpdateRect()
            else:
                self.Y += 8
                Cat.UpdateRect()
                WallTouchNum = WallTouch(Cat.Get_Rect(), walls)
                if WallTouchNum == 1:
                    self.Y -= 8
        elif decision == 1:
            if self.Y <= 0:
                self.Y = 8
                Cat.UpdateRect()
            else:
                self.Y -= 8
                Cat.UpdateRect()
                WallTouchNum = WallTouch(Cat.Get_Rect(), walls)
                if WallTouchNum == 1:
                    self.Y += 8
        elif decision == 2:
            if self.X >= 1280:
                self.X = 1272
                Cat.UpdateRect()
            else:
                self.X += 8
                Cat.UpdateRect()
                WallTouchNum = WallTouch(Cat.Get_Rect(), walls)
                if WallTouchNum == 1:
                    self.X -= 8
        elif decision == 3:
            if self.X <= 0:
                self.X = 8
                Cat.UpdateRect()
            else:
                self.X -= 8
                Cat.UpdateRect()
                WallTouchNum = WallTouch(Cat.Get_Rect(), walls)
                if WallTouchNum == 1:
                    self.X += 8
        
                
class Character():
    def __init__(self, Image, HP, MaxHP, Attack, Speed, Level, X, Y):
        self.Image = pygame.image.load(Image)
        self.HP = HP
        self.MaxHP = MaxHP
        self.Attack = Attack
        self.Speed = Speed
        self.X = X
        self.Y = Y
        
    def GetHP(self):
        return self.HP
        

Cat = Enemy("Characters/Cat.png", 10, 2, 3, "Normal", 880, 280)
        



menu()