# -*- coding: utf-8 -*-
"""
@author: Kamaleshwar M

Email : mkamaleshwar80@gmail.com

"""

import pygame as p
import MovesandRules, AI
from multiprocessing import Process, Queue

width = height = 700
dim = 7
sqsize = height // dim
max_fps = 15
images = {}
global difficulty
TWOPLAYER = False
PLAYERVAI = False
DIFFICULTY = None

def loadimg():
    pieces = ['bO', 'bM', 'bS', 'bL', 'bW', 'bB', 'bH', 'bp', 'bD', 'cO', 'cM', 'cS', 'cL', 'cW', 'cB', 'cH', 'cp', 'cD']
    for i in pieces:
        images[i] = p.transform.scale(p.image.load("images/" + i + ".png"), (sqsize, sqsize))

def main():
    global TWOPLAYER, PLAYERVAI, DIFFICULTY
    p.init()
    screen = p.display.set_mode((width, height))
    p.display.set_caption('SupesBoard')
    clock = p.time.Clock()
    screen.fill(p.Color('black'))

    # Create buttons
    twoplayer_button = p.Rect(100, 400, 200, 50)
    playervai_button = p.Rect(390, 400, 200, 50)
    beginner_button = p.Rect(50, 480, 140, 50)
    easy_button = p.Rect(230, 480, 100, 50)
    medium_button = p.Rect(390, 480, 120, 50)
    hard_button = p.Rect(550, 480, 100, 50)

    show_buttons = True
    while show_buttons:
        for e in p.event.get():
            if e.type == p.QUIT:
                show_buttons = False
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                if twoplayer_button.collidepoint(mouse_pos):
                    test=True
                    playerone = True
                    playertwo = True
                    TWOPLAYER = True
                    PLAYERVAI = False
                    DIFFICULTY = None
                    show_buttons = False
                elif playervai_button.collidepoint(mouse_pos):
                    test=True
                    playerone = True
                    playertwo = False
                    TWOPLAYER = False
                    PLAYERVAI = True
                    DIFFICULTY = None
                elif beginner_button.collidepoint(mouse_pos) and PLAYERVAI:
                    DIFFICULTY = 'beginner'
                    difficulty = 1
                    print("Difficulty is :", difficulty)
                    show_buttons = False
                elif easy_button.collidepoint(mouse_pos) and PLAYERVAI:
                    DIFFICULTY = 'easy'
                    difficulty=2
                    print("Difficulty is :",difficulty)
                    show_buttons = False
                elif medium_button.collidepoint(mouse_pos) and PLAYERVAI:
                    DIFFICULTY = 'medium'
                    difficulty=3
                    print("Difficulty is :",difficulty)
                    show_buttons = False
                elif hard_button.collidepoint(mouse_pos) and PLAYERVAI:
                    difficulty=4
                    DIFFICULTY = 'hard'
                    print("Difficulty is :",difficulty)
                    show_buttons = False

        draw_buttons(screen, twoplayer_button, playervai_button,beginner_button, easy_button, medium_button, hard_button)
        p.display.flip()

    # Start the game
    gb = MovesandRules.gameboard()
    loadimg()
    running = True
    sqselected = ()
    playerclicks = []
    validmoves = gb.getvalidmoves()
    movemade = False
    animate = False
    gameover = False
    aithinking = False
    moveundone = False
    movefinderprocess = None

    while running:
        humanturn = (gb.colortomove and playerone) or (not gb.colortomove and playertwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    if not show_buttons: 
                        show_buttons = True
                        break
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameover:
                    location = p.mouse.get_pos()
                    col = location[0] // sqsize
                    row = location[1] // sqsize
                    if sqselected == (row, col):
                        sqselected = ()
                        playerclicks = []
                    else:
                        sqselected = (row, col)
                        playerclicks.append(sqselected)
                    if len(playerclicks) == 2 and humanturn:
                        move = MovesandRules.move(playerclicks[0], playerclicks[1], gb.board)
                        for i in range(len(validmoves)):
                            if move == validmoves[i]:
                                gb.makemove(validmoves[i])
                                movemade = True
                                animate = True
                                sqselected = ()
                                playerclicks = []
                        if not movemade:
                            playerclicks = [sqselected]
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gb.undomove()
                    movemade = True
                    animate = False
                    gameover = False
                    if aithinking:
                        movefinderprocess.terminate()
                        aithinking = False
                    moveundone = True
                if e.key == p.K_r:
                    gb = MovesandRules.gameboard()
                    validmoves = gb.getvalidmoves()
                    sqselected = ()
                    playerclicks = []
                    movemade = False
                    animate = False
                    gameover = False
                    if aithinking:
                        movefinderprocess.terminate()
                        aithinking = False
                    moveundone = True


        if show_buttons:
            gb = MovesandRules.gameboard()
            validmoves = gb.getvalidmoves()
            sqselected = ()
            playerclicks = []
            movemade = False
            animate = False
            gameover = False
            aithinking = False
            moveundone = False
            playerone=None
            playertwo=None
            difficulty=None
            DIFFICULTY=None
            PLAYERVAI=False
            TWOPLAYER=False
            movefinderprocess = None

            while show_buttons:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        show_buttons = False
                        running=False
                    elif e.type == p.MOUSEBUTTONDOWN:
                        mouse_pos = p.mouse.get_pos()
                    if twoplayer_button.collidepoint(mouse_pos):
                        playerone = True
                        playertwo = True
                        TWOPLAYER = True
                        PLAYERVAI = False
                        DIFFICULTY = None
                        show_buttons = False
                    elif playervai_button.collidepoint(mouse_pos):
                        playerone = True
                        playertwo = False
                        TWOPLAYER = False
                        PLAYERVAI = True
                        DIFFICULTY = None
                    elif beginner_button.collidepoint(mouse_pos) and PLAYERVAI:
                        DIFFICULTY = 'beginner'
                        difficulty = 1
                        print("Difficulty is :", difficulty)
                        show_buttons = False
                    elif easy_button.collidepoint(mouse_pos) and PLAYERVAI:
                        DIFFICULTY = 'easy'
                        difficulty=2
                        print("Difficulty is :",difficulty)
                        show_buttons = False
                    elif medium_button.collidepoint(mouse_pos) and PLAYERVAI:
                        DIFFICULTY = 'medium'
                        difficulty=3
                        print("Difficulty is :",difficulty)
                        show_buttons = False
                    elif hard_button.collidepoint(mouse_pos) and PLAYERVAI:
                        difficulty=4
                        DIFFICULTY = 'hard'
                        print("Difficulty is :",difficulty)
                        show_buttons = False

                draw_buttons(screen, twoplayer_button, playervai_button,beginner_button, easy_button, medium_button, hard_button)
                p.display.flip()
                if not show_buttons:
                    break
                            


        if not gameover and not humanturn and not moveundone:
            if not aithinking:
                aithinking = True
                print("Finding best move")
                returnqueue = Queue()
                if difficulty==1:
                    print("Beginner mode")
                    movefinderprocess = Process(target=AI.findbestmovebeginner, args=(gb, validmoves, returnqueue))
                if difficulty==2:
                    print("Easy mode")
                    movefinderprocess = Process(target=AI.bfs, args=(gb, validmoves, returnqueue))
                if difficulty==3:
                    print("Medium mode")
                    movefinderprocess = Process(target=AI.findbestmovemedium, args=(gb, validmoves, returnqueue))
                if difficulty==4:
                    print("Hard mode")
                    movefinderprocess = Process(target=AI.findbestmovehard, args=(gb, validmoves, returnqueue))
                movefinderprocess.start()
            if not movefinderprocess.is_alive():
                print("Got it")
                aimove = returnqueue.get()
                if aimove is None:
                    print("from random move")
                    aimove = AI.findrandommove(validmoves)
                gb.makemove(aimove)
                movemade = True
                animate = True
                aithinking = False

        if movemade:
            if animate:
                animation(gb.movelog[-1], screen, gb.board, clock)
            validmoves = gb.getvalidmoves()
            movemade = False
            animate = False
            moveundone = False

        drawgameboard(screen, gb, validmoves, sqselected)
        if gb.checkmate:
            gameover = True
            if gb.colortomove:
                drawText(screen, "Black & White wins")
            else:
                drawText(screen, "Color wins")
        elif gb.stalemate:
            gameover = True
            drawText(screen, "Draw")
        clock.tick(max_fps)
        p.display.flip()

def highlight(screen, gb, validmoves, sqselected):
    if sqselected != ():
        r, c = sqselected
        if gb.board[r][c][0] == ('c' if gb.colortomove else 'b'):
            s = p.Surface((sqsize, sqsize))
            s.set_alpha(100)
            s.fill(p.Color('red'))
            screen.blit(s, (c * sqsize, r * sqsize))
            s.fill(p.Color('green'))
            for move in validmoves:
                if move.startrow == r and move.startcol == c:
                    screen.blit(s, (move.endcol * sqsize, move.endrow * sqsize))

def drawgameboard(screen, gb, validmoves,sqselected):
    drawboard(screen)
    highlight(screen, gb, validmoves, sqselected)
    drawpiece(screen, gb.board)

def drawboard(screen):
   global colors
   colors = [p.Color('#DBAFA0'), p.Color('#49243E')]
   for x in range(dim):
       for y in range(dim):
           color = colors[(x + y) % 2]
           p.draw.rect(screen, color, (y * sqsize, x * sqsize, sqsize, sqsize))

def drawpiece(screen, board):
   for x in range(dim):
       for y in range(dim):
           piece = board[x][y]
           if piece != '--':
               screen.blit(images[piece], p.Rect(y * sqsize, x * sqsize, sqsize, sqsize))

def animation(move, screen, board, clock):
   global colors
   dr = move.endrow - move.startrow
   dc = move.endcol - move.startcol
   framespersquare = 10
   framecount = (abs(dr) + abs(dc)) + framespersquare
   for frame in range(framecount + 1):
       r, c = (move.startrow + dr * frame / framecount, move.startcol + dc * frame / framecount)
       drawboard(screen)
       drawpiece(screen, board)
       color = colors[(move.endrow + move.endcol) % 2]
       endsquare = p.Rect(move.endcol * sqsize, move.endrow * sqsize, sqsize, sqsize)
       p.draw.rect(screen, color, endsquare)
       if move.piececaptured != '--':
           screen.blit(images[move.piececaptured], endsquare)
       screen.blit(images[move.piecemoved], p.Rect(c * sqsize, r * sqsize, sqsize, sqsize))
       p.display.flip()
       clock.tick(60)

def drawText(screen, text):

   font = p.font.SysFont("Asul", 100, True, False)
   textobj = font.render(text, 0, p.Color('#B4B4B8'))
   textloc = p.Rect(0, 130, width, height).move(width / 2 - textobj.get_width() / 2, height / 2 - textobj.get_width() / 2)
   screen.blit(textobj, textloc)
   textobj = font.render(text, 0, p.Color('#0C0C0C'))
   screen.blit(textobj, textloc.move(2, 2))

background_image = p.image.load("images/backgroundimg.png")
background_image = p.transform.scale(background_image, (width, height))

def draw_buttons(screen, twoplayer_button, playervai_button, beginner_button,easy_button, medium_button, hard_button):
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the buttons
    twoplayer_button_color = p.Color('#DFD7BF')
    playervai_button_color = p.Color('Black')
    if TWOPLAYER:
        twoplayer_button_color = p.Color('#066309')
    elif PLAYERVAI:
        playervai_button_color = p.Color('#323232')

    p.draw.rect(screen, twoplayer_button_color, twoplayer_button)
    p.draw.rect(screen, playervai_button_color, playervai_button)

    font = p.font.SysFont("Asul", 40, True, False)
    text_twoplayer = font.render("Multi Player", True, p.Color('black'))
    text_playervai = font.render("Player vs AI", True, p.Color('white'))
    screen.blit(text_twoplayer, (twoplayer_button.x + 10, twoplayer_button.y + 10))
    screen.blit(text_playervai, (playervai_button.x + 10, playervai_button.y + 10))

    if PLAYERVAI:

        beginner_button_color = p.Color('#DFD7BF')
        easy_button_color = p.Color('#DFD7BF')
        medium_button_color = p.Color('Black')
        hard_button_color = p.Color('Black')
        if DIFFICULTY == 'beginner':
            beginner_button_color = p.Color('#066309')
        if DIFFICULTY == 'easy':
            easy_button_color = p.Color('#066309')
        elif DIFFICULTY == 'medium':
            medium_button_color = p.Color('#323232')
        elif DIFFICULTY == 'hard':
            hard_button_color = p.Color('#323232')

        p.draw.rect(screen, beginner_button_color, beginner_button)
        p.draw.rect(screen, easy_button_color, easy_button)
        p.draw.rect(screen, medium_button_color, medium_button)
        p.draw.rect(screen, hard_button_color, hard_button)
        text_beginner = font.render("Beginner", True, p.Color('black'))
        text_easy = font.render("Easy", True, p.Color('black'))
        text_medium = font.render("Medium", True, p.Color('white'))
        text_hard = font.render("Hard", True, p.Color('white'))
        screen.blit(text_beginner, (beginner_button.x + 10, beginner_button.y + 10))
        screen.blit(text_easy, (easy_button.x + 10, easy_button.y + 10))
        screen.blit(text_medium, (medium_button.x + 10, medium_button.y + 10))
        screen.blit(text_hard, (hard_button.x + 10, hard_button.y + 10))


if __name__ == "__main__":
   main() 