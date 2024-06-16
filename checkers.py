import pygame, sys
from pygame.locals import *
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BOARDSIZE = 8
SQUARESIZE = WINDOWWIDTH / BOARDSIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)


pygame.display.set_caption("Checkers")
pygame.init()


class Board():
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def create_board_surface(self):
        self.surface = pygame.Surface((self.length, self.width))
        square_rect = pygame.Rect(0,0,SQUARESIZE, SQUARESIZE)
        for i in range(BOARDSIZE): #ith row
            for j in range(BOARDSIZE): #jth column
                if (i + j) % 2 == 0:
                    square_rect = pygame.draw.rect(self.surface, BLACK, square_rect)
                else:
                    square_rect = pygame.draw.rect(self.surface, WHITE, square_rect)
                square_rect = square_rect.move(SQUARESIZE, 0)
        square_rect.x = 0
        square_rect = square_rect.move(0, SQUARESIZE)


    def create_board_object(self):
        self.board = []
        board_row = list(range(BOARDSIZE))
        for i in range(BOARDSIZE):
            self.board.append(board_row)


def main():
    GAME_IS_RUNNING = True
    checkerboard = Board(WINDOWWIDTH, WINDOWHEIGHT)
    checkerboard.create_board_surface()
    checkerboard.create_board_object()
    DISPLAY_SURF.blit(checkerboard.surface, (0,0))
    # display the iniital state.

    while GAME_IS_RUNNING: # main game loop
    # collect inputace
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #handle events

        #update
        pygame.display.update()
    pygame.quit()

main()



"""
class Piece:
    def __init__ (self, team, position):
        self.team = team
        self.position = position
        self.captured = False
        self.queen = False

    #def move(self, position):
        #return new_position

    def take(self, Piece):
        # I don't know lol. 


    # a piece should be able to move
    # a piece has a position current position on the board
    # a piece has team
"""

"""
    A game of checkers.

    We begin, two players I and me. The Board, The Pieces. Turns.

    I place the board on the ground, I place the pieces on the board
    Once all the pieces are on the board we can start.

    I start, I choose a checker piece, it knows where it is, I know where it is.
    I find the piece. I touch it, it shows me where it can go, what pieces it can take
    The piece tells me that it is my piece. I move the piece, the piece speaks to the board
    The board answers, the move is accepted. The piece moves. My turn ends

    Me does the same thing now, he selects a piece on the board, he selects a piece
    The piece tells him that he is not his piece. He selects another piece and tries to move it
    The piece moves but the board says that move is not possible. Me tries again. He succeeds in moving
    his piece. 

    I move my piece, and take Me's piece, hopping over it In turn I get to repeat my turn.

    some time passes, several turns pass. A piece reaches the end of the board, it tells me it is a queen
    IT can move backwards and forwards.

    we continue, I take Me's Pieces Me takes my pieces.
    Eventually I take all of Me's pieces. The game is over
"""


#TODO
# Determine how sequence of surface, draw and displaying work
# Determine how to create a checker piece
# As a checker piece is an object, determine a way to create a checker piece class. 
# the board is an object.
# the pieces are objects
# the pieces "belong" to the board