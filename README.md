# tron
this is my final project for intro to computer science. to run it, you must install pygame. i do not claim to own gamebox.py, but have received permission to redistribute it. a note about the rending and collision: they are done at the same time to save on operations, this led to the previously mentioned feature. it would be possible to remove this feature, but it would require a complete rewrite or doubling the collision operations per frame (which would increase lag noticeably).

bugs:  
- hardware limitations on the keyboard can lead to buttons not registering a press, if you experience unexpected movement during gameplay it's probably because of this.
- each segment of the tron bike paths is an individual element in a list, which leads to considerable lag past 30 seconds into a round.

features:  
- boosting has a 50% chance to "jump" you over another players wall, can be reliably done only by skilled players if you boost a pixel before you touch their wall
- crashing into a wall at the same will give both players a point. this is because it takes an equal amount of skill from both players to accomplish this, so they both earn a point.

No collaborators other than myself in this project.

REQUIREMENTS:  
User Input:
- players can control their bike using (WASD + LSHIFT) and (PL;' + RSHIFT) respectively

Game Over:
- crashing into a wall ends the round
- a player reaching 5 points ends the game

Small Enough Window:
- window is 540x600

Graphics/Images:
- game uses locally imported images for the background and the explosion animation  

OPTIONAL REQUIREMENTS:  
Sprite Animation:
- an explosion animation plays over the losing player upon their death

Restart From Game Over:
- game can be restarted after every round and every game by pressing space

Two Players Simultaneously:
- this is a two player game

Something More:
- options on start up for cosmetic customization (choosing bike color and background)
