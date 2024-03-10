
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
    EnemyExist = True

    Map, MapText, PlayerX, PlayerY, MapName, HP, MaxHP, Attack, Speed, Level, Typing = SaveFileProcess(save)
    
    MainMainCharacter = Character("Characters/Character.png", HP, MaxHP, Attack, Speed, Level, PlayerX, PlayerY, Typing)
    
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    EnemyExist = TurnBasedRpg(MainMainCharacter, Cat, screen)

        
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
                   
        if EnemyExist == True:

            EnemyWalkTime = time.time() - MoveEnemyStart

            if EnemyWalkTime >= 3:
                Cat.Walk(screen, Decision, Walls)
                if EnemyWalkTime >= 3.2:
                    Decision = random.randint(0,4)
                    MoveEnemyStart = time.time()

           
            Cat.Spawn(screen)
        
            if CharacterRect.colliderect(Cat.Get_Rect()):
                EnemyExist = TurnBasedRpg(MainMainCharacter, Cat, screen)

            
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
    Typing = str(SaveFileLines[8].strip())
        
    return LoadMap, TextMap, PlayerX, PlayerY, Map, HP, MaxHP, Attack, Speed, Level, Typing

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
    def __init__(self, Image, HP, MaxHP, Attack, Speed, Typing, X, Y):
        replaced = Image.replace("Characters/", "")
        self.Name = replaced.replace(".png", "")
        self.Image = pygame.image.load(Image)
        self.HP = HP
        self.MaxHP = MaxHP
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
    
    def GetName(self):
        return self.Name
    
    def GetMaxHP(self):
        return self.MaxHP
    
    def GetImage(self):
        return self.Image
    
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
                    
    def GetHP(self):
        return self.HP
    
    def GetSpeed(self):
        return self.Speed
    
    def UpdateHP(self, NewHP):
        self.HP = NewHP
        
    def GetAttack(self):
        return self.Attack
        
                
class Character():
    def __init__(self, Image, HP, MaxHP, Attack, Speed, Level, X, Y, Typing):
        replaced = Image.replace("Characters/", "")
        self.Name = replaced.replace(".png", "")
        self.Image = pygame.image.load(Image)
        self.HP = HP
        self.MaxHP = MaxHP
        self.Attack = Attack
        self.Speed = Speed
        self.X = X
        self.Y = Y
        self.Typing = Typing
        
    def GetHP(self):
        return self.HP
    
    def GetMaxHP(self):
        return self.MaxHP
    
    def GetSpeed(self):
        return self.Speed
    
    def GetAttack(self):
        return self.Attack
    
    def GetName(self):
        return self.Name
    
    def UpdateHP(self, NewHP):
        self.HP = NewHP
        
        
        

Cat = Enemy("Characters/Cat.png", 10, 10, 2, 3, "Normal", 880, 280)
        
def TurnBasedRpg(MainCharacter, Enemyy, screen):
    running = True
    background = pygame.image.load("BattleScreen.png")
    EnemyImage = Enemyy.GetImage()
    backbackground = pygame.image.load("Woods.png")
    
    if MainCharacter.GetSpeed() > Enemyy.GetSpeed():
        SpeedQueue = [MainCharacter, Enemyy]
    else:
        SpeedQueue = [Enemyy, MainCharacter]
    PlayerMove = 1
    EnemyMove = 0 
    Button = 1
    while running:
        TextBubble = False
        for event in pygame.event.get():
            if PlayerMove == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        running = False
                    if event.key == pygame.K_w:
                        if Button != 1:
                            Button -= 1
                    if event.key == pygame.K_s:
                        if Button != 5:
                            Button += 1
                    if event.key == pygame.K_RETURN:
                        if Button == 1:
                            Enemyy.UpdateHP(PlayerAttack(MainCharacter.GetAttack(), Enemyy.GetHP()))
                            Text = "You dealt " + str(MainCharacter.GetAttack()) + " damage!"
                            BattleTextBubble(screen, Text)
                            running = BattleStatus(Enemyy.GetHP())
                            if running == False:
                                EnemyExist = False

                        
            if EnemyMove == 1:
                MainCharacter.UpdateHP(EnemyTurn(Enemyy.GetAttack(), MainCharacter.GetHP()))
                PlayerMove = 1
                EnemyMove = 1
                     
                            

                    
        screen.blit(background, (0,0))
        screen.blit(backbackground, (15, 16))
        draw_text(str(Enemyy.GetName()) + "    " + str(Enemyy.GetHP()) + "/" + str(Enemyy.GetMaxHP()), TextFont, (255,255,255), 16, 498, screen)
        draw_text("Main Character" + "    " + str(MainCharacter.GetHP()) + "/" + str(MainCharacter.GetMaxHP()), TextFont, (255,255,255), 656, 498, screen)
        if Button == 1:
            draw_text("Attack", TextFontUnderline, (255,255,255), 320, 480, screen)
        else:
            draw_text("Attack", TextFont, (255,255,255), 320, 480, screen)
        if Button == 2:
            draw_text("Skills", TextFontUnderline, (255,255,255), 320, 520, screen)
        else:
            draw_text("Skills", TextFont, (255,255,255), 320, 520, screen)
        if Button == 3:
            draw_text("Defend", TextFontUnderline, (255,255,255), 320, 560, screen)
        else:
            draw_text("Defend", TextFont, (255,255,255), 320, 560, screen)
        if Button == 4:
            draw_text("Items", TextFontUnderline, (255,255,255), 320, 600, screen)
        else:
            draw_text("Items", TextFont, (255,255,255), 320, 600, screen)
        if Button == 5:
            draw_text("Run", TextFontUnderline, (255,255,255), 320, 640, screen)
        else:
            draw_text("Run", TextFont, (255,255,255), 320, 640, screen)
            
        screen.blit(EnemyImage , (500, 500))
        
        pygame.display.flip()
        
    return EnemyExist

def PlayerAttack(PlayerAttack, EnemyHealth):
    NewHP = EnemyHealth - PlayerAttack
    return NewHP

def EnemyTurn(EnemyAttack, PlayerHealth):
    NewHP = PlayerHealth - EnemyAttack
    return NewHP
    
    
def BattleStatus(EnemyHP):
    running = True
    if EnemyHP <= 0:
        running = False
    else: 
        running = True
    return running

def BattleTextBubble(screen, text):
    BattleTextBubbl = pygame.image.load("BattleTextBubble.png")
    TextBubble = True
    while TextBubble == True:
        screen.blit(BattleTextBubbl, (0, 477))
        draw_text(text, TextFont, (0,0,0), 20, 485, screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    TextBubble = False
        pygame.display.flip()


    

TextFont = pygame.font.SysFont("Comic Sans", 30)
TextFontUnderline = pygame.font.SysFont("Comic Sans", 30)
TextFontUnderline.set_underline(True)


def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# List of skills

def FireBall():
    Damage = 5
    Typing = "Fire"

def WaterGun():
    Damage = 5
    Typing = "Water"
    
def VineWhip():
    Damage = 5
    Typing = "Grass"
menu()