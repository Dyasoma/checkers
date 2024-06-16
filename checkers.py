import random
import pygame, sys
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 640
DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BOARDSIZE = 8
SQUARESIZE = WINDOWWIDTH / BOARDSIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Board:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def create_board_surface(self):
        self.surface = pygame.Surface((self.length, self.width))
        square_rect = pygame.Rect(0, 0, SQUARESIZE, SQUARESIZE)
        for i in range(BOARDSIZE):  # ith row
            for j in range(BOARDSIZE):  # jth column
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


class Piece:
    def __init__(self, position: tuple, team_color: str):
        self.position = position
        self.team_color = team_color
        if self.team_color == "Red":
            self.color = RED
        else:
            self.color = BLUE
        self.size = WINDOWWIDTH / BOARDSIZE

    def create_piece_surface(self):
        self.surface = pygame.Surface((SQUARESIZE, SQUARESIZE), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

    def create_piece_rect(self):
        self.rect = pygame.draw.ellipse(
            self.surface, self.color, self.surface.get_rect(), 0
        )

        ### get possible moves?

        ### get position

        ### captured???


def create_pieces(number, team: str) -> list[Piece]:
    """
    create_pieces(number, team : str) -> list[Piece]:
    create a list whoses elements are Piece objects.
    parameters: number is the int representing the number of pieces in the list of pieces
                team is the str representing the team the pieces belong to.
    returns a list of those pieces
    """
    pieces = []
    for i in range(number):
        piece = Piece((0, 0), team)  # all pieces will exist at the same "position"
        piece.create_piece_surface()
        piece.create_piece_rect()
        pieces.append(piece)
    return pieces


def place_pieces(Board, pieces: list[Piece], team_color: str):
    """
    Places pieces onto the board surface
    """
    size = pieces[0].size
    i = 0
    j = 0
    if team_color == "Blue":
        j = BOARDSIZE - 1
    for piece in pieces:
        piece.position = (i * size, j * size)
        i += 1


def draw_pieces(board: Board, pieces: list[Piece]):
    """
    Draws pieces onto the board surface, mutating it
    """
    for piece in pieces:
        board.surface.blit(piece.surface, piece.position, piece.rect)


def main():

    pygame.display.set_caption("Checkers")
    pygame.init()
    checkerboard = Board(WINDOWWIDTH, WINDOWHEIGHT)
    checkerboard.create_board_surface()
    checkerboard.create_board_object()

    ## create pieces

    player_1_pieces = create_pieces(8, "Red")
    place_pieces(checkerboard, player_1_pieces, "Red")

    player_2_pieces = create_pieces(8, "Blue")
    place_pieces(checkerboard, player_2_pieces, "Blue")

    # draw backwords
    draw_pieces(checkerboard, player_1_pieces)
    draw_pieces(checkerboard, player_2_pieces)
    DISPLAY_SURF.blit(checkerboard.surface, (0, 0))
    GAME_IS_RUNNING = True

    """
    Turn system :
    Player 1 begins by selecting a piece 

    Handle Piece selection()

    Player 1 moves pieces

    Handle Piece movement()

    Player 1 takes piece

    Handle Take Piece Movement()
        Piece can move to spot on checkerboard
        Piece cannot move to a spot where their teams piece is
        Piece can move to spot where other players piece is, and in doing so
        Is allowed to move again if next movement also allows taking a piece
        Handle double-jump, triple-jump, and N-jump


    Handle Removing taken piece()
        Removed Pieces have their removed Attribute set to true.
        And they are disappeared from the checkerboard
        Handle Cleaning board of removed pieces()

    Once player 1 has made their move

    Handle End Turn()

    Player 2 starts Turn

    If piece reaches the end of the board, Set queen Attribute to true. 
    Handle Queen Creation()
        > Maybe remove old piece and have a queen object?
        > Maybe have an attribute that affects all pieces?

    



    
    
    """

    while GAME_IS_RUNNING:  # main game loop

        # collect inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # handle events

        # if Move valid, piece moves

        # If piece takes another piece, remove second piece, restart player 1's turn.

        # update

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


# TODO
# Determine how sequence of surface, draw and displaying work
# Determine how to create a checker piece
# As a checker piece is an object, determine a way to create a checker piece class.
# the board is an object.
# the pieces are objects
# the pieces "belong" to the board
