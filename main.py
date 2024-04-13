#wcg9ev && mam9cfe
"""
welcome to Tron

bugs:
    hardware limitations on the keyboard can lead to buttons not registering a press, if you experience unexpected
    movement during gameplay it's probably because of this.
features:
    boosting has a 50% chance to "jump" you over another players wall, can be reliably done only by skilled players
    if you boost a pixel before you touch their wall

    crashing into a wall at the same will give both players a point. this is because it takes an equal amount of skill
    from both players to accomplish this, so they both earn a point.

interesting notes about the rending and collision: they are done at the same time to save on operations, this led to
the previously mentioned feature. it would be possible to remove this feature, but it would require a complete rewrite
or doubling the collision operations per frame (which would increase lag noticeably).

REQUIREMENTS:
User Input:
    players can control their bike using (WASD + LSHIFT) and (PL;' + RSHIFT) respectively
Game Over:
    crashing into a wall ends the round
    a player reaching 5 points ends the game
Small Enough Window:
    window is 540x600
Graphics/Images:
    game uses locally imported images for the background and the explosion animation

OPTIONAL REQUIREMENTS:
Sprite Animation:
    an explosion animation plays over the losing player upon their death
    (i was told by a TA that this was sufficient)
Restart From Game Over:
    game can be restarted after every round and every game by pressing space
Two Players Simultaneously:
    this is a two player game
Something More:
    options on start up for cosmetic customization (choosing bike color and background)
    (i was told by a TA that this was sufficient)
"""
import gamebox
camera=gamebox.Camera(540,600)

#every asset/variable associated with p1
p1Colors=[['blue','cyan'],['forestgreen','green'],['gray','white']]
p1Color=0
p1=gamebox.from_color(60,340,p1Colors[p1Color][0], 4, 4)
p1trail=[]
p1Dir='d'
p1DirLast='d'
p1Bst=False
p1BstTimer=120
p1Select=gamebox.from_color(100,290,"white",55,55)

#every asset/variable associated with p2
p2Colors=[['red','orange'],['gold3','yellow'],['darkorchid','magenta']]
p2Color=0
p2=gamebox.from_color(480,340,p2Colors[p2Color][0], 4, 4)
p2trail=[]
p2Dir='l'
p2DirLast='l'
p2Bst=False
p2BstTimer=120
p2Select=gamebox.from_color(440,290,"white",55,55)

#shared/general assets/variables
walls=[gamebox.from_color(400, 70, "white", 800, 20),
       gamebox.from_color(400, 590, "white", 800, 20),
       gamebox.from_color(10, 250, "white", 20, 700),
       gamebox.from_color(530, 250, "white", 20, 700)]
art=['grid.png','chess.png','ice.png','sand.png','rust.png','nebula.png','galaxy.png','jim.png']
background= 0
colorSelect=True
mapSelect=False
difSelect=False
gameOn=False
gameWon=False
scoreOpen=True
scoreClosingSequence=False
score=[0,0]

#menu key checks
wPress=False
sPress=False
aPress=False
dPress=False
pPress=False
semiPress=False
lPress=False
apoPress=False
spacePress=False

#explosion animation
explosion_sprite=gamebox.load_sprite_sheet('explosion.png',1,7)
explosion=gamebox.from_image(0,0,explosion_sprite[0])
frame=0
def explode(x,y):
    global frame
    explosion.center=(x,y)
    camera.draw(explosion)
    frame+=1
    if frame >= 35:
        frame = 0
    explosion.image=explosion_sprite[int(frame/5)]

def tick(keys):
    global colorSelect
    global mapSelect
    global p1Color
    global p2Color
    global background
    global wPress
    global sPress
    global aPress
    global dPress
    global pPress
    global semiPress
    global lPress
    global apoPress
    global spacePress
    camera.clear("black")#frame reset

    #color select menu
    if colorSelect==True:
        global p1Select
        global p2Select

        # p1selection interface
        if 119 in keys and wPress!=True and p1Select.y!=290:
            p1Select.move(0, -70)
            wPress=True
        if not 119 in keys:
            wPress=False
        if 115 in keys and sPress!=True and p1Select.y!=430:
            p1Select.move(0, 70)
            sPress = True
        if not 115 in keys:
            sPress = False

        # p2selection interface
        if 112 in keys and pPress!=True and p2Select.y!=290:
            p2Select.move(0, -70)
            pPress = True
        if not 112 in keys:
            pPress = False
        if 59 in keys and semiPress!=True and p2Select.y!=430:
            p2Select.move(0, 70)
            semiPress = True
        if not 59 in keys:
            semiPress = False

        # select color and move onto map select
        if 32 in keys and spacePress==False:
            colorSelect=False
            mapSelect=True
            if p1Select.y==290:
                p1Color = 0
            elif p1Select.y==360:
                p1Color = 1
            elif p1Select.y==430:
                p1Color = 2
            if p2Select.y==290:
                p2Color = 0
            elif p2Select.y==360:
                p2Color = 1
            elif p2Select.y==430:
                p2Color = 2
            p1Select.center = (67, 260)
            p2Select.center = (67, 260)
            p1Select.scale_by(2)
            p2Select.scale_by(2)
            spacePress=True
        if not 32 in keys:
            spacePress=False

        #Drawing
        camera.draw(p1Select)
        camera.draw(p2Select)
        camera.draw(gamebox.from_text(270, 50, "T  R  O  N",80, 'white', True, True))
        camera.draw(gamebox.from_text(270, 540,"Press Space When Ready",40,'white'))
        camera.draw(gamebox.from_text(270, 130, "Choose Your Color!", 30, 'white'))
        camera.draw(gamebox.from_text(100, 200,"Player 1", 30,'white'))
        camera.draw(gamebox.from_text(100, 230, "(wasd & LShift)", 30, 'white'))
        camera.draw(gamebox.from_text(440, 200, "Player 2", 30, 'white'))
        camera.draw(gamebox.from_text(440, 230, "(pl;' & RShift)", 30, 'white'))
        camera.draw(gamebox.from_color(100, 290, p1Colors[0][0], 50, 50))
        camera.draw(gamebox.from_color(100, 360, p1Colors[1][0], 50, 50))
        camera.draw(gamebox.from_color(100, 430, p1Colors[2][0], 50, 50))
        camera.draw(gamebox.from_color(440, 290, p2Colors[0][0], 50, 50))
        camera.draw(gamebox.from_color(440, 360, p2Colors[1][0], 50, 50))
        camera.draw(gamebox.from_color(440, 430, p2Colors[2][0], 50, 50))

    #map select menu
    elif mapSelect==True:
        #p1selection interface
        if 119 in keys and wPress!=True and p1Select.y!=260:
            p1Select.move(0, -135)
            wPress=True
        if not 119 in keys:
            wPress=False
        if 115 in keys and sPress!=True and p1Select.y!=395:
            p1Select.move(0, 135)
            sPress = True
        if not 115 in keys:
            sPress = False
        if 97 in keys and aPress!=True and p1Select.x!=67:
            p1Select.move(-135,0)
            aPress = True
        if not 97 in keys:
            aPress = False
        if 100 in keys and dPress!=True and p1Select.x!=472:
            p1Select.move(135,0)
            dPress = True
        if not 100 in keys:
            dPress = False

        # p2selection interface
        if 112 in keys and pPress!=True and p2Select.y!=260:
            p2Select.move(0, -135)
            pPress = True
        if not 112 in keys:
            pPress = False
        if 59 in keys and semiPress!=True and p2Select.y!=395:
            p2Select.move(0, 135)
            semiPress = True
        if not 59 in keys:
            semiPress = False
        if 108 in keys and lPress!=True and p2Select.x!=67:
            p2Select.move(-135,0)
            lPress = True
        if not 108 in keys:
            lPress = False
        if 39 in keys and apoPress!=True and p2Select.x!=472:
            p2Select.move(135,0)
            apoPress = True
        if not 39 in keys:
            apoPress = False

        #drawing
        camera.draw(p1Select)
        camera.draw(p2Select)
        temp=[gamebox.from_image(67,260,art[0]),
              gamebox.from_image(202,260,art[1]),
              gamebox.from_image(337,260,art[2]),
              gamebox.from_image(472,260,art[3]),
              gamebox.from_image(67,395,art[4]),
              gamebox.from_image(202,395,art[5]),
              gamebox.from_image(337,395,art[6]),
              gamebox.from_image(472,395,art[7])]
        for each in temp:
            each.scale_by(.2)
            camera.draw(each)
        camera.draw(gamebox.from_text(270, 50, "T  R  O  N",80, 'white', True, True))
        camera.draw(gamebox.from_text(270, 130, "Agree on a Map!", 30, 'white'))
        camera.draw(gamebox.from_text(270,540,"Press Space When Ready",40,'white'))

        #select map and move onto game
        if 32 in keys and spacePress==False and p1Select.center==p2Select.center:
            for x in range(len(temp)):
                if p1Select.touches(temp[x]):
                    background=x
            p1Select.scale_by(.5)
            p2Select.scale_by(.5)
            mapSelect=False
            spacePress=True
        if not 32 in keys:
            spacePress=False

    #main game
    else:
        global scoreOpen
        global scoreClosingSequence
        global gameOn
        global gameWon

        #active gameplay loop
        if gameOn:
            global p1
            global p1Bst
            global p1BstTimer
            global p1trail
            global p1Dir
            global p1DirLast

            #p1 boost
            if 1073742049 in keys and p1BstTimer>0:
                p1Bst=True
                p1BstTimer-=2
            else:
                p1Bst=False
                if p1BstTimer<120:
                    p1BstTimer+=1
            #p1 movement input
            if 119 in keys and p1DirLast!='s':
                p1Dir='w'
            if 115 in keys and p1DirLast!='w':
                p1Dir='s'
            if 97 in keys and p1DirLast!='d':
                p1Dir='a'
            if 100 in keys and p1DirLast!='a':
                p1Dir='d'
            #p1 movement evaluation
            if p1Dir=='w':
                if p1Bst==True:
                    p1.move(0,-5)
                p1.move(0,-5)
                p1DirLast = 'w'
            if p1Dir=='s':
                if p1Bst==True:
                    p1.move(0,5)
                p1.move(0,5)
                p1DirLast = 's'
            if p1Dir=='a':
                if p1Bst==True:
                    p1.move(-5,0)
                p1.move(-5,0)
                p1DirLast = 'a'
            if p1Dir=='d':
                if p1Bst==True:
                    p1.move(5,0)
                p1.move(5,0)
                p1DirLast = 'd'
            if p1Bst==False:#p1 trail
                p1trail.append(gamebox.from_color(p1.x,p1.y,p1Colors[p1Color][1],5,5))

            global p2
            global p2Bst
            global p2BstTimer
            global p2trail
            global p2Dir
            global p2DirLast

            #p2 boost
            if 1073742053 in keys and p2BstTimer > 0:
                p2Bst = True
                p2BstTimer -= 2
            else:
                p2Bst = False
                if p2BstTimer < 120:
                    p2BstTimer += 1
            #p2 movement input
            if 112 in keys and p2DirLast != ';':
                p2Dir = 'p'
            if 59 in keys and p2DirLast != 'p':
                p2Dir = ';'
            if 108 in keys and p2DirLast != '\'':
                p2Dir = 'l'
            if 39 in keys and p2DirLast != 'l':
                p2Dir = '\''
            #p2 movement evaluation
            if p2Dir == 'p':
                if p2Bst == True:
                    p2.move(0, -5)
                p2.move(0, -5)
                p2DirLast = 'p'
            if p2Dir == ';':
                if p2Bst == True:
                    p2.move(0, 5)
                p2.move(0, 5)
                p2DirLast = ';'
            if p2Dir == 'l':
                if p2Bst == True:
                    p2.move(-5, 0)
                p2.move(-5, 0)
                p2DirLast = 'l'
            if p2Dir == '\'':
                if p2Bst == True:
                    p2.move(5, 0)
                p2.move(5, 0)
                p2DirLast = '\''
            if p2Bst == False:  # p2 trail
                p2trail.append(gamebox.from_color(p2.x, p2.y,p2Colors[p2Color][1], 5, 5))

        #game start/reset loop
        if 32 in keys and gameOn==False and spacePress==False:
            #handling for either round won or game won
            if gameWon==True:
                score[0]=0
                score[1]=0
                gameWon=False
                colorSelect=True
                p1Select.center=(100,290)
                p2Select.center=(440,290)
            else:
                gameOn = True
            p1.center=(60,340)
            p1trail = []
            p1Dir = 'd'
            p1DirLast='d'
            p1BstTimer = 120
            p2.center=(480,340)
            p2trail = []
            p2Dir = 'l'
            p2DirLast='l'
            p2BstTimer = 120
            scoreOpen=True
            scoreClosingSequence=False
            spacePress=True
        if not 32 in keys:
            spacePress=False

        #draw background
        camera.draw(gamebox.from_image(270, 330,art[background]))
        #head on collision exception
        if p1.touches(p2):
            gameOn=False
            camera.draw(gamebox.from_text(130, 30, "HEAD - ON", 24, "white"))
            camera.draw(gamebox.from_text(400, 30, "COLLISION", 24, "white"))
            explode(p1.x, p1.y)
            explode(p2.x, p2.y)
        #drawing and collision for p1 trail
        for each in p1trail:
            if each != p1trail[-1]:
                camera.draw(each)
                if p1.touches(each):
                    gameOn = False
                    explode(p1.x, p1.y)
                    camera.draw(gamebox.from_text(400, 30, "P2 WINS", 24, p2Colors[p2Color][1]))
                    if scoreOpen:
                        score[1]+=1
                if p2.touches(each):
                    gameOn = False
                    explode(p2.x, p2.y)
                    camera.draw(gamebox.from_text(130, 30, "P1 WINS", 24, p1Colors[p1Color][1]))
                    if scoreOpen:
                        score[0]+=1
                if p1.touches(each) or p2.touches(each):
                    scoreClosingSequence= True
            elif p1Bst==True:
                camera.draw(each)
        #drawing and collision for p2 trail
        for each in p2trail:
            if each != p2trail[-1]:
                camera.draw(each)
                if p1.touches(each):
                    gameOn = False
                    explode(p1.x, p1.y)
                    camera.draw(gamebox.from_text(400, 30, "P2 WINS", 24, p2Colors[p2Color][1]))
                    if scoreOpen:
                        score[1]+=1
                if p2.touches(each):
                    gameOn = False
                    explode(p2.x, p2.y)
                    camera.draw(gamebox.from_text(130, 30, "P1 WINS", 24, p1Colors[p1Color][1]))
                    if scoreOpen:
                        score[0]+=1
                if p1.touches(each) or p2.touches(each):
                    scoreClosingSequence = True
            elif p2Bst == True:
                camera.draw(each)

        #draw p1 & p2 representations and turning
        if p1Dir=='w' or p1Dir=='s':
            camera.draw(gamebox.from_color(p1.x, p1.y, p1Colors[p1Color][0], 5, 15))
        elif p1Dir=='a' or p1Dir=='d':
            camera.draw(gamebox.from_color(p1.x, p1.y,p1Colors[p1Color][0], 15, 5))
        if p2Dir=='p' or p2Dir==';':
            camera.draw(gamebox.from_color(p2.x, p2.y, p2Colors[p2Color][0], 5, 15))
        elif p2Dir=='l' or p2Dir=='\'':
            camera.draw(gamebox.from_color(p2.x, p2.y, p2Colors[p2Color][0], 15, 5))

        #drawing and collision for walls
        for each in walls:
            camera.draw(each)
            if p1.touches(each):
                gameOn = False
                explode(p1.x, p1.y)
                camera.draw(gamebox.from_text(400, 30, "P2 WINS", 24, p2Colors[p2Color][1]))
                if scoreOpen :
                    score[1] += 1
            if p2.touches(each):
                gameOn = False
                explode(p2.x, p2.y)
                camera.draw(gamebox.from_text(130, 30, "P1 WINS", 24, p1Colors[p1Color][1]))
                if scoreOpen:
                    score[0] += 1
            if p1.touches(each) or p2.touches(each):
                scoreClosingSequence= True
        camera.draw(gamebox.from_text(270, 30, str(score[0])+'-'+str(score[1]), 30, "white", True))
        #shuts score board after point(s) have been scored
        if scoreClosingSequence==True:
            scoreOpen=False

        #handling for gameWon state
        if score[0]==5 and score[1]==5:
            camera.draw(gamebox.from_text(270, 200, "Nobody is the  T R O N  Champion", 35, 'white', True, True))
            gameWon=True
        elif score[0]==5:
            camera.draw(gamebox.from_text(270, 200, "P1 is the  T R O N  Champion!", 40, p1Colors[p1Color][0], True, True))
            gameWon=True
        elif score[1]==5:
            camera.draw(gamebox.from_text(270, 200, "P2 is the  T R O N  Champion!", 40, p2Colors[p2Color][0], True, True))
            gameWon=True
        if gameWon==True:
            camera.draw(gamebox.from_text(270, 500, "Press Space to play again", 30, 'white', True, True))

    camera.display()#end def tick

gamebox.timer_loop(45, tick)
