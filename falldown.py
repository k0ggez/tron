#wcg9ev
"""
welcome to Fall-Down by Will Goodrum
use the left and right arrow keys to control your player character, the lime square
the lime square has acceleration, friction, and wall sliding abilities
the gaps in the floors are randomly generated and stored in a list structure
the score reflects how many floors you have passed
the game saves the highest score of the session but it doesn't persist between instances

this game is contains several movement bugs, i have tried to make them less noticeable
in particular, i have decided that sliding down walls is more of a feature
a very small bug that persists is the inability to reach a horizontal velocity of zero after moving
this is caused by the friction algorithm being linear and flipping back and forth across zero
there is a debug mode that you can activate by pressing d that will print out each frame's relevant values


for more advanced graphics and animated art, please contact me to purchase the Fall-Down DLC game pass
"""
import pygame
import gamebox
import random
camera=gamebox.Camera(700, 700)

#define boxes (player, walls, floor variables)
gameOver=True
p1=gamebox.from_color(350,500,"lime",20,20)
floors=[]
walls=[
gamebox.from_color(350,-10,"black",700,20),
gamebox.from_color(350, 710,"black",700,20),
gamebox.from_color(5,350,"white", 10, 700),
gamebox.from_color(695,350,"white",10,700)]
score=0
highscore=0
tickCounter=0
debug=False

def tick(keys):
    global floors
    global score
    global highscore
    global gameOver
    if gameOver==False:
        if pygame.K_RIGHT in keys: #player movement
            if p1.xspeed < 10:
                p1.xspeed += 1.2
        if pygame.K_LEFT in keys:
            if p1.xspeed > -10:
                p1.xspeed -= 1.2

        if p1.xspeed > 0 and not pygame.K_RIGHT in keys: #player friction
            p1.xspeed -= .3
            if p1.xspeed>.5:
                p1.xspeed-=.3
        elif p1.xspeed < 0 and not pygame.K_LEFT in keys:
            p1.xspeed += .3
            if p1.xspeed<-.5:
                p1.xspeed+=.3

        for floor in floors: #player gravity/floor collision
            if p1.touches(floor):
                p1.yspeed = -3
                p1.move_to_stop_overlapping(floor)
        p1.yspeed += 2
        if p1.top_touches(walls[1]):#catches player if you clip through bottom
            p1.yspeed=0
            p1.move(0, -10)

        for wall in walls: #wall collision
            if p1.touches(wall):
                p1.move_to_stop_overlapping(wall)

        p1.move_speed()

        global tickCounter #floor randomization
        if tickCounter%30==0 or tickCounter==0:
            floorLeftTemp=random.randrange(30, 630)
            floorRightTemp=700-floorLeftTemp-40
            floors.append(gamebox.from_color(floorLeftTemp/2, 700,"gray", floorLeftTemp, 30))
            floors[-1].yspeed=-5
            floors.append(gamebox.from_color((700-floorRightTemp/2), 700, "gray", floorRightTemp, 30))
            floors[-1].yspeed=-5
        for floor in floors:
            floor.move_speed()
        tickCounter+=1

        if (tickCounter-20) % 3 == 0 and tickCounter>130:  # count floors that pass ceiling for score
            score += 1
        #end game0ver while check

    if p1.touches(walls[0]):#gameOver sequence
        camera.draw(gamebox.from_text(350, 300, "GAME 0VER", 40, "red", True))
        gameOver=True
        for floor in floors:
            floor.yspeed=0
            floor.move_speed

    if pygame.K_SPACE in keys and gameOver==True:#replay sequence
        floors=[]
        p1.center=[350, 500]
        p1.yspeed = 0
        p1.xspeed = 0
        tickCounter=0
        if score > highscore:
            highscore = score
        score=0
        gameOver=False

    camera.clear("black") #draw boxes
    camera.draw(p1)
    for floor in floors:
        camera.draw(floor)
    for wall in walls:
        camera.draw(wall)
    if gameOver==True:
        camera.draw(gamebox.from_text(350, 260, "GAME OVER", 60, "red", True))
        camera.draw(gamebox.from_text(350, 380, "PRESS SPACE TO PLAY", 25, "red", True))
        if score > highscore:
            camera.draw(gamebox.from_text(350, 415, "!!!NEW HIGH SCORE!!!", 30, "lime", True))
    camera.draw(gamebox.from_text(40, 20, str(score), 25, "red", True))

    global debug#press d to enter debug mode and print out relevant values
    if pygame.K_d in keys:
        debug=True
    if debug==True:
        print('x&yLOC: (',round(p1.center[0],1),' ',round(p1.center[1],1),'), x&ySPD: (',p1.xspeed,', ',p1.yspeed,')',sep='')
        print('high&score: (',highscore,', ',score,') , TICK: ',tickCounter,sep='')
    camera.display()

gamebox.timer_loop(30, tick)

