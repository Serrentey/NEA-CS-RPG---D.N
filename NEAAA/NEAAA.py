
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

    Map, MapText, PlayerX, PlayerY, MapName, HP, MaxHP, Attack, Speed, Level, Typing, Skills = SaveFileProcess(save)
    
    MainCharacter = Character("Characters/Character.png", HP, MaxHP, Attack, Speed, Level, PlayerX, PlayerY, Typing, Skills)
    
    TempPlayerX = MainCharacter.GetX()
    TempPlayerY = MainCharacter.GetY()
    MoveEnemyStart = time.time()
    Decision = 2

    Walls, EnemyList = MapTextProcess(MapText, screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(Map, (0,0))

        CharacterRect = MainCharacter.GetImage().get_rect(topleft = (MainCharacter.GetX(), MainCharacter.GetY()))
        TempCharacterRect = MainCharacter.GetImage().get_rect(topleft = (TempPlayerX, TempPlayerY))

        WallTouchNum = 0
        WallTouchNum = WallTouch(CharacterRect, Walls)
        
        TempPlayerX = MainCharacter.GetX()
        TempPlayerY = MainCharacter.GetY()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            TempPlayerY -= MoveAmount
            WallTouchNum = WallTouch(TempCharacterRect, Walls)
            if WallTouchNum == 1:
                pass
            elif WallTouchNum == 0:
                MainCharacter.UpdateY(TempPlayerY)    
            if MainCharacter.GetY() == 0:
                try:
                    MapName2 = MapName
                    MapName, NewMapText = ChangeMap(MapName, "UP")
                    Map = pygame.image.load(MapName)
                    Walls, EnemyList = MapTextProcess(NewMapText, screen)
                    MainCharacter.UpdateY(712)
                except:
                    MapName = MapName2
                    MainCharacter.UpdateY(8)
        if keys[pygame.K_s]:
            TempPlayerY += MoveAmount
            WallTouchNum = WallTouch(TempCharacterRect, Walls)
            if WallTouchNum == 1:
                pass
            elif WallTouchNum == 0:
                MainCharacter.UpdateY(TempPlayerY)
            if MainCharacter.GetY() >= 720:
                try:
                    MapName2 = MapName
                    MapName, NewMapText = ChangeMap(MapName, "DOWN")
                    Map = pygame.image.load(MapName)
                    Walls, EnemyList = MapTextProcess(NewMapText, screen)
                    MainCharacter.UpdateY(8)
                except:
                    MapName = MapName2
                    MainCharacter.UpdateY(712)
        if keys[pygame.K_a]:
           TempPlayerX -= MoveAmount
           WallTouchNum = WallTouch(TempCharacterRect, Walls)
           if WallTouchNum == 1:
              pass
           elif WallTouchNum == 0:
              MainCharacter.UpdateX(TempPlayerX)
           if MainCharacter.GetX() == 0:
                try:
                    MapName2 = MapName
                    MapName, NewMapText = ChangeMap(MapName, "LEFT")
                    Map = pygame.image.load(MapName)
                    Walls, EnemyList = MapTextProcess(NewMapText, screen)
                    MainCharacter.UpdateX(1272)
                except:
                    MapName = MapName2
                    MainCharacter.UpdateX(8)
        if keys[pygame.K_d]:
           TempPlayerX += MoveAmount
           WallTouchNum = WallTouch(TempCharacterRect, Walls)
           if WallTouchNum == 1:
               pass
           elif WallTouchNum == 0:
               MainCharacter.UpdateX(TempPlayerX)
           if MainCharacter.GetX() == 1280:
               try: 
                   MapName2 = MapName
                   MapName, NewMapText = ChangeMap(MapName, "RIGHT")
                   Map = pygame.image.load(MapName)
                   Walls, EnemyList = MapTextProcess(NewMapText, screen)
                   MainCharacter.UpdateX(8)
               except:
                   MapName = MapName2
                   MainCharacter.UpdateX(1272)
                   
        EnemyWalkTime = time.time() - MoveEnemyStart

        for Enemies in EnemyList:
            if Enemies.GetExist() == True:
                if EnemyWalkTime >= 3:
                    Enemies.Walk(screen, Decision, Walls, MainCharacter.GetLocation(), EnemyWalkTime)
                    if EnemyWalkTime >= 3.2:
                        Decision = random.randint(0,4)
                        MoveEnemyStart = time.time()  
                if CharacterRect.colliderect(Enemies.Get_Rect()):
                    if CharacterRect.colliderect(Enemies.Get_Rect()):
                        Enemies.UpdateExist(TurnBasedRpg(MainCharacter, Enemies, screen))
                Enemies.Spawn(screen)

        screen.blit(MainCharacter.GetImage(), (MainCharacter.GetX(), MainCharacter.GetY()))
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
    Skill = SaveFileLines[9].strip()
    Skills = Skill.split(", ")
        
    return LoadMap, TextMap, PlayerX, PlayerY, Map, HP, MaxHP, Attack, Speed, Level, Typing, Skills

def MapTextProcess(TextFile, screen):
    YNumber = 0
    WallList = []
    EnemyList = []
    
    Text = open(TextFile, "r")
    TextLines = Text.readlines()
    
    EnemyKind = TextLines[9].strip()
    EnemyHP = TextLines[10].strip()
    EnemyMaxHP = TextLines[11].strip()
    EnemyAttack = TextLines[12].strip()
    EnemySpeed = TextLines[13].strip()
    EnemyType = TextLines[14].strip()
                              
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
                x = XNumber * 80
                yy = YNumber * 80
                print(EnemyKind)
                if EnemyKind == "Koshka":
                    NewEnemy = Koshka(EnemyHP, EnemyMaxHP, EnemyAttack, EnemySpeed, EnemyType, x, yy, True)
                if EnemyKind == "Snake":
                    NewEnemy = Snake(EnemyHP, EnemyMaxHP, EnemyAttack, EnemySpeed, EnemyType, x, yy, True)
                EnemyList.append(NewEnemy)
                XNumber += 1
            else:
                pass
                
        YNumber += 1
    return WallList, EnemyList
  
def WallTouch(CharacterRect, walls):
    WallTouchNum = 0
    for x in walls:
        if CharacterRect.colliderect(x):
            WallTouchNum = 1
    return WallTouchNum
        
class Enemy():
    def __init__(self, HP, MaxHP, Attack, Speed, Typing, X, Y, Exist):
        self.HP = HP
        self.MaxHP = MaxHP
        self.Attack = Attack
        self.Speed = Speed
        self.Typing = Typing
        self.X = X
        self.Y = Y
        self.Exist = Exist
        
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
        
    def Walk(self, screen, decision, walls, CharacterLocation, Time):
        
        WallTouchNum = 0

        if decision == 0:
            if self.Y >= 720:
                self.Y = 712
            else:
                self.Y += 8
                WallTouchNum = WallTouch(self.EnemyRect, walls)
                if WallTouchNum == 1:
                    self.Y -= 8
        elif decision == 1:
            if self.Y <= 0:
                self.Y = 8
            else:
                self.Y -= 8
                WallTouchNum = WallTouch(self.EnemyRect, walls)
                if WallTouchNum == 1:
                    self.Y += 8
        elif decision == 2:
            if self.X >= 1280:
                self.X = 1272
            else:
                self.X += 8
                WallTouchNum = WallTouch(self.EnemyRect, walls)
                if WallTouchNum == 1:
                    self.X -= 8
        elif decision == 3:
            if self.X <= 0:
                self.X = 8
            else:
                self.X -= 8
                WallTouchNum = WallTouch(self.EnemyRect, walls)
                if WallTouchNum == 1:
                    self.X += 8
        self.EnemyRect = self.Image.get_rect(topleft = (self.X, self.Y))
                    
    def GetHP(self):
        return self.HP
    
    def GetSpeed(self):
        return self.Speed
    
    def UpdateHP(self, NewHP):
        self.HP = NewHP
        
    def GetAttack(self):
        return self.Attack
    
    def GetTyping(self):
        return self.Typing
    
    def GetExist(self):
        return self.Exist
    
    def UpdateExist(self, New):
        self.Exist = New
        
class Koshka(Enemy):
    def __init__ (self, HP, MaxHP, Attack, Speed, Typing, X, Y, Exist):
        Enemy.__init__(self, HP, MaxHP, Attack, Speed, Typing, X, Y, Exist)
        
        self.Image = pygame.image.load("Characters/Cat.png")
        self.Name = ("Cat")
        self.EnemyRect = self.Image.get_rect(topleft = (self.X, self.Y))

        
class Snake(Enemy):
    def __init__ (self, HP, MaxHP, Attack, Speed, Typing, X, Y, Exist):
        Enemy.__init__(self, HP, MaxHP, Attack, Speed, Typing, X, Y, Exist)
        
        self.Image = pygame.image.load("Characters/Snake.png")
        self.Name = ("Snake")
        self.EnemyRect = self.Image.get_rect(topleft = (self.X, self.Y))


    def Walk(self, screen, decision, walls, CharacterLocation, Time):
        WallTouchNum = 0
        if self.X >= CharacterLocation[0]:
            self.X -= 8
            WallTouchNum = WallTouch(self.EnemyRect, walls)
            if WallTouchNum == 1:
                self.X += 8
        if self.X <= CharacterLocation[0]:
            self.X += 8
            WallTouchNum = WallTouch(self.EnemyRect, walls)
            if WallTouchNum == 1:
                self.X -= 8
        if self.Y >= CharacterLocation[1]:
            self.Y -= 8
            WallTouchNum = WallTouch(self.EnemyRect, walls)
            if WallTouchNum == 1:
                self.Y += 8
        if self.Y <= CharacterLocation[1]:
            self.Y += 8
            WallTouchNum = WallTouch(self.EnemyRect, walls)
            if WallTouchNum == 1:
                self.Y -= 8
        self.EnemyRect = self.Image.get_rect(topleft = (self.X, self.Y))
        
                  
class Character():
    def __init__(self, Image, HP, MaxHP, Attack, Speed, Level, X, Y, Typing, Skills):
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
        self.Skills = Skills
        
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
        
    def GetSkills(self):
        return self.Skills
    
    def GetImage(self):
        return self.Image
    
    def GetLocation(self):
        return (self.X, self.Y)
    
    def GetX(self):
        return self.X
    
    def UpdateX(self, NewX):
        self.X = NewX
    
    def GetY(self):
        return self.Y
    
    def UpdateY(self, NewY):
        self.Y = NewY
        

Cat = Koshka(10, 10, 2, 3, "Grass", 880, 280, True)
Dog = Snake(10, 10, 2, 3, "Grass", 400, 480, True)
        

def TurnBasedRpg(MainCharacter, Enemyy, screen):
    running = True
    background = pygame.image.load("BattleScene/BattleScreen.png")
    EnemyImage = Enemyy.GetImage()
    MainCharacterImage = MainCharacter.GetImage()
    backbackground = pygame.image.load("BattleScene/Woods.png")
    
    if MainCharacter.GetSpeed() > int(Enemyy.GetSpeed()):
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
                            EnemyMove = 1
                            PlayerMove = 0
                        if Button == 2:
                            SkillChoice(screen, MainCharacter.GetSkills(), Enemyy)
                            running = BattleStatus(Enemyy.GetHP())
                            if running == False:
                                EnemyExist = False
                            EnemyMove = 1
                            PlayerMove = 0
                            

            if EnemyMove == 1:
                MainCharacter.UpdateHP(EnemyTurn(Enemyy.GetAttack(), MainCharacter.GetHP()))
                Text = "You took " + str(Enemyy.GetAttack()) + " damage!"
                BattleTextBubble(screen, Text)
                PlayerMove = 1
                EnemyMove = 0
                     
                           
                    
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
            
        screen.blit(MainCharacterImage, (440, 360))
        screen.blit(EnemyImage , (840, 360))
        
        pygame.display.flip()
        
    return EnemyExist

def PlayerAttack(PlayerAttack, EnemyHealth):
    NewHP = EnemyHealth - PlayerAttack
    return NewHP

def EnemyTurn(EnemyAttack, PlayerHealth):
    NewHP = PlayerHealth - int(EnemyAttack)
    return NewHP
    
    
def BattleStatus(EnemyHP):
    running = True
    if EnemyHP <= 0:
        running = False
    else: 
        running = True
    return running

def BattleTextBubble(screen, text):
    BattleTextBubbl = pygame.image.load("BattleScene/BattleTextBubble.png")
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

def SkillChoice(screen, Skills, Enemyy):
    running = True
    SkillMenu = pygame.image.load("BattleScene/SkillSelect.png")
    Length = len(Skills)
    SkillsListLength = Length - 1
    Button = 0
    X = 320
    Y = 480
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    running = False
                if event.key == pygame.K_w:
                    if Button != 0:
                        Button -= 1
                if event.key == pygame.K_s:
                    if Button != SkillsListLength:
                        Button += 1
                if event.key == pygame.K_RETURN:
                    SkillUse = Skills[Button]
                    if str(SkillUse) == "FireBall":
                        NewHP = (FireBall(Enemyy.GetHP(), Enemyy.GetTyping()))
                        text = "You dealt " + str(int(Enemyy.GetHP()) - NewHP) + " damage!"
                        BattleTextBubble(screen, text)
                        Enemyy.UpdateHP(NewHP)
                    if str(SkillUse) == "WaterGun":
                        NewHP = (WaterGun(Enemyy.GetHP(), Enemyy.GetTyping()))
                        text = "You dealt " + str(int(Enemyy.GetHP()) - NewHP) + " damage!"
                        BattleTextBubble(screen, text)
                        Enemyy.UpdateHP(NewHP)
                    if str(SkillUse) == "VineWhip":
                        NewHP = (VineWhip(Enemyy.GetHP(), Enemyy.GetTyping()))
                        text = "You dealt " + str(int(Enemyy.GetHP()) - NewHP) + " damage!"
                        BattleTextBubble(screen, text)
                        Enemyy.UpdateHP(NewHP)
                    if str(SkillUse) == "MultiHit":
                        NewHP = (MultiHit(Enemyy.GetHP()))
                        text = "You dealt " + str(int(Enemyy.GetHP()) - NewHP) + " damage!"
                        BattleTextBubble(screen, text)
                        Enemyy.UpdateHP(NewHP)
                    running = False
                    
        screen.blit(SkillMenu, (293, 478))
        Y = 480
        index = 0
        for x in Skills:
            if index == Button:
                draw_text(str(x), TextFontUnderline, (0,0,0), X, Y, screen)
            else:
                draw_text(str(x), TextFont, (0,0,0), X, Y, screen)
            index += 1
            Y += 40
        pygame.display.flip()


def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# List of skills

ElementBonus = 1.5
ElementReduction = 0.5
ElementNull = 0

def FireBall(EnemyHP, EnemyTyping):
    EnemyHP = float(EnemyHP)
    EnemyTyping = str(EnemyTyping)
    Damage = 4
    Typing = "Fire"
    if EnemyTyping == "Water":
        NewHP = EnemyHP - (Damage * ElementReduction)
    elif EnemyTyping == "Grass":
        NewHP = EnemyHP - (Damage * ElementBonus)
    elif EnemyTyping == "Fire":
        NewHP = EnemyHP - (Damage * ElementNull)
    else:
        NewHP = EnemyHP - Damage     
    return int(NewHP)
        
def WaterGun(EnemyHP, EnemyTyping):
    Damage = 4
    Typing = "Water"
    if EnemyTyping == "Grass":
        NewHP = EnemyHP - (Damage * ElementReduction)
    elif EnemyTyping == "Fire":
        NewHP = EnemyHP - (Damage * ElementBonus)
    elif EnemyTyping == "Water":
        NewHP = EnemyHP - (Damage * ElementNull)
    else:
        NewHP = EnemyHP - Damage     
    return int(NewHP)
    
def VineWhip(EnemyHP, EnemyTyping):
    Damage = 4
    Typing = "Grass"
    if EnemyTyping == "Fire":
        NewHP = EnemyHP - (Damage * ElementReduction)
    elif EnemyTyping == "Water":
        NewHP = EnemyHP - (Damage * ElementBonus)
    elif EnemyTyping == "Grass":
        NewHP = EnemyHP - (Damage * ElementNull)
    else:
        NewHP = EnemyHP - Damage     
    return int(NewHP)
    
def MultiHit(EnemyHP):
    Damage = 3
    Luck = 0
    NewHP = EnemyHP - Damage
    Luck = random.randint(0,1)
    if Luck == 1:
        NewHP = NewHP - Damage
    return int(NewHP)
    
menu()