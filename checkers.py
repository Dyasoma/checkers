# TODO
# the pieces "belong" to the board
import pygame, sys
from pygame.locals import *
# Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
SQUARECOUNT = 8
WINDOWTOBOARDRATIO = 0.85
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
SQUARESIZE = WINDOWWIDTH / SQUARECOUNT
BOARDSIZE = WINDOWWIDTH * WINDOWTOBOARDRATIO
BOARDPOSX = (WINDOWWIDTH - BOARDSIZE) / 2
BOARDPOSY = (WINDOWHEIGHT- BOARDSIZE) / 2
EMPTY = None

class Board:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def create_board_surface(self):
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object. 
        """
        self.surface = pygame.Surface((self.length, self.width))
        square_size = self.length / 8
        square_rect = pygame.Rect(0, 0, square_size, square_size)

        for i in range(SQUARECOUNT):  # ith row
            for j in range(SQUARECOUNT):  # jth column
                if (i + j) % 2 == 0:
                    square_rect = pygame.draw.rect(self.surface, BLACK, square_rect)
                else:
                    square_rect = pygame.draw.rect(self.surface, WHITE, square_rect)
                square_rect = square_rect.move(square_size, 0)
            square_rect.x = 0
            square_rect = square_rect.move(0, square_size)

    def create_board_rect(self):
        """
        create_board_rect(self)
        Creates an instance attribute of object Board, using the instance attribute surface. 
        Acts as a wrapper to the get_rect() function for objects of class Surface from pygame module
        Must be called after create_board_surface(self), and any changes made surface attribute
        requires another call to create_board_rect(self)
        """
        self.rect = self.surface.get_rect()
        self.rect.left = BOARDPOSX
        self.rect.top = BOARDPOSY

    def create_board_struct(self):
        """
        create_board_struct(self):
        Creates the instance attribute struct of the class Board.
        Data structure is a list of lists whoses entries are initialized to None
        Once object of class Piece are initialized entries will either contain None (no piece there)
        Or will contain a piece at entry board.struct[i][j] where i is the "row" and j is the "col"
        of the board.
        Parameters : No parameters
        Returns: None
        Side effects: Assigns stuct instance attribute of class Board, Builds list of lists. 
        """
        self.struct = []
        for i in range(SQUARECOUNT):
            row = []
            for j in range(SQUARECOUNT):
                row.append(EMPTY) # all peices are initially Empty

class Piece:
    def __init__(self, position: tuple, team_color: str):
        self.position = position # graphical
        self.row = 0 # row index on board
        self.col = 0 # col index on board
        self.team_color = team_color
        if self.team_color == "Red":
            self.color = RED
        else:
            self.color = BLUE
        self.size = BOARDSIZE/ SQUARECOUNT

    def create_piece_surface(self,  board : Board):
        square_size = board.length / SQUARECOUNT
        self.surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

    def create_piece_rect(self):
        self.rect = pygame.draw.ellipse(
            self.surface, self.color, self.surface.get_rect(), 0
        )


def init_board(board_width : int, board_length : int) -> Board:
    """
    init_board(board_width, board_height) -> Board:
    Initalizes board, taking in as parameters the board width and board length as ints
    creates object of class Board, initializing board objects surface and struct attributes
    creates rect instance attribute.
    Returns an instance of the Board Class
    """
    board = Board(board_width, board_length)
    board.create_board_surface()
    board.create_board_struct()
    board.create_board_rect()
    return board
 
def create_pieces(number, team: str, board : Board) -> list[Piece]:
    """
    create_pieces(number, team : str) -> list[Piece]:
    creates a list whoses elements are Piece objects.
    parameters: number is the int representing the number of pieces to make.
    team is the str representing the team the pieces belong to.
    Board is the current board the pieces will be placed upon
    returns a list of Piece Objects
    """
    pieces = []
    for i in range(number):
        piece = Piece((0, 0), team)  # all pieces will begin at the same "position"
        piece.create_piece_surface(board)
        piece.create_piece_rect()
        pieces.append(piece)
    return pieces

def set_pieces_position(pieces: list[Piece], team_color : str, board : Board):
    """
    set_pieces_position(pieces: list[Piece], team_color : str)
    sets pieces position relative to the board surface, that is if the board moves, when we draw
    the pieces they will be drawn relative to the boards top right corner
    updates the instance attribute "position" of the object of class
    Piece. Takes in as parameters a list of Piece objects and the team color stored as a string.
    Side effect: mutates instance attribute "position"
    returns : None
    """

    # set pieces position 




def init_pieces(board : Board) -> list[list[Piece]]:
    """
    initializes pieces, creating a list of lists whose elements are objects of class Piece.

    """
    game_pieces = []
    player_1_pieces = create_pieces(12, "Red", board)
    set_pieces_position(player_1_pieces, "Red", board)
    player_2_pieces = create_pieces(12, "Blue", board)
    set_pieces_position(player_2_pieces, "Blue", board)
    game_pieces.append(player_1_pieces)
    game_pieces.append(player_2_pieces)
    return game_pieces


def draw_pieces(board: Board, pieces: list[Piece]):
    """
    Draws pieces onto the board surface, mutating it
    """
    for piece in pieces:
        board.surface.blit(piece.surface, piece.position, piece.rect)


def draw_elements(board : Board, pieces_1: list[Piece], pieces_2: list[Piece]):
    DISPLAY_SURF.fill("grey")
    draw_pieces(board, pieces_1)
    draw_pieces(board, pieces_2)
    DISPLAY_SURF.blit(board.surface, (BOARDPOSX, BOARDPOSY))


def main():
    pygame.display.set_caption("Checkers")
    pygame.init()
    checkerboard = init_board(BOARDSIZE, BOARDSIZE)
    game_pieces = init_pieces(checkerboard)
    player_1_pieces, player_2_pieces = game_pieces[:]

    # draw objects
    draw_elements(checkerboard, player_1_pieces, player_2_pieces)  
    GAME_IS_RUNNING = True
    while GAME_IS_RUNNING:  # main game loop
        # collect inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # handle events

        # update
        pygame.display.update()
    pygame.quit()


main()
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