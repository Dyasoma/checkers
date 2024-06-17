# TODO
# Clean description of EVERYTHING
# Consider the overall flow of the program
# Consider how to setup objects.
import pygame, sys
from pygame.locals import *
import pygame.surface

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
BOARDPOSY = (WINDOWHEIGHT - BOARDSIZE) / 2
EMPTY = None
PIECESCOUNT = 12


class Board:
    def __init__(self, width, length, square_count):
        self.width: int = width
        self.length: int = length
        self.square_count: int = square_count

    def create_board_struct(self):
        """ """
        self.struct: list = []
        square_size = self.length / self.square_count
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                # handles swapping colors to create checkered pattern
                if (row_index + col_index) % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK
                square = Square(square_size, color, row_index, col_index)
                row.append(square)  # all peices are initially Empty
            self.struct.append(row)

    def create_board_surface(self):
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        """
        self.surface = pygame.Surface((self.length, self.width))
        for row_index in range(self.square_count):
            for col_index in range(self.square_count):
                current_square: Square = self.struct[row_index][col_index]
                self.surface.blit(current_square.surface, current_square.pos)

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


# Board squares object


class Square:
    def __init__(self, size, color, row, col):  # rows/col are indices starting from 0
        self.size = size
        self.color = color
        self.contents = EMPTY  # squares hold nothing in the beginning
        self.row = row
        self.col = col
        self.pos = (
            col * size,
            row * size,
        )  # columns go left to right, rows go up and down
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x = BOARDPOSX + self.pos[0]
        self.rect.y = BOARDPOSY + self.pos[1]


# Pieces Object


class Pieces:
    def __init__(self, number_of_pieces: int, team_color: str):
        self.team_color = team_color
        self.number_of_pieces = number_of_pieces
        self.struct = []

    def create_pieces(self):
        """
        create_pieces(number, team : str) -> list[Piece]:
        creates a list whoses elements are Piece objects.
        parameters: number is the int representing the number of pieces to make.
        team is the str representing the team the pieces belong to.
        Board is the current board the pieces will be placed upon
        returns a list of Piece Objects
        """
        for i in range(self.number_of_pieces):
            piece = Piece(
                (0, 0), self.team_color
            )  # all pieces will begin at the same "position"
            piece.create_piece_surface()
            piece.create_piece_rect()
            self.struct.append(piece)

    def set(self, board: Board):
        """
        set_pieces_position(pieces: list[Piece], team_color : str)
        sets pieces position relative to the board surface, that is if the board moves, when we draw
        the pieces they will be drawn relative to the boards top right corner
        updates the instance attribute "position" of the object of class
        Piece. Takes in as parameters a list of Piece objects and the team color stored as a string.
        Side effect: mutates instance attribute "position"
        returns : None
        """

        k = 0
        if self.team_color == "Red":

            for i in range(board.square_count):
                for j in range(board.square_count):
                    if board.struct[i][j].color == BLACK:
                        self.struct[k].move_piece(i, j)
                        board.struct[i][j].contents = self.struct[k]
                        k += 1
                    if k == self.number_of_pieces:
                        break
                if k == self.number_of_pieces:
                    break
        else:
            for i in list(range(board.square_count - 1, -1, -1)):
                for j in range(board.square_count):
                    if board.struct[i][j].color == BLACK:
                        self.struct[k].move_piece(i, j)
                        board.struct[i][j].contents = self.struct[k]
                        k += 1

                    if k == self.number_of_pieces:
                        break
                if k == self.number_of_pieces:
                    break

        # set pieces position


class Piece:
    def __init__(self, pos: tuple, team_color: str):
        self.pos = pos  # graphical
        self.row = 0  # row index on board
        self.col = 0  # col index on board
        self.team_color = team_color
        if self.team_color == "Red":
            self.color = RED
        else:
            self.color = BLUE
        self.size = BOARDSIZE / SQUARECOUNT

    def create_piece_surface(self):
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

    def create_piece_rect(self):
        self.rect = pygame.draw.ellipse(
            self.surface, self.color, self.surface.get_rect(), 0
        )

    def set_pos(self):
        self.pos = (self.col * self.size, self.row * self.size)

    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.set_pos()


def init_board(board_width: int, board_length: int, square_count) -> Board:
    """
    init_board(board_width, board_height) -> Board:
    Initalizes board, taking in as parameters the board width and board length as ints
    creates object of class Board, initializing board objects surface and struct attributes
    creates rect instance attribute.
    Returns an instance of the Board Class
    """
    board = Board(board_width, board_length, square_count)
    board.create_board_struct()
    board.create_board_surface()
    board.create_board_rect()
    return board


def init_pieces(board: Board):
    """
    initializes pieces, creating a list of lists whose elements are objects of class Piece.

    """
    player_1_pieces = Pieces(PIECESCOUNT, "Red")
    player_1_pieces.create_pieces()
    player_1_pieces.set(board)

    player_2_pieces = Pieces(PIECESCOUNT, "Blue")
    player_2_pieces.create_pieces()
    player_2_pieces.set(board)

    return player_1_pieces, player_2_pieces


def draw_pieces(board: Board, pieces: Pieces):
    """
    Draws pieces onto the board surface, mutating it
    """
    for piece_index in range(len(pieces.struct)):
        piece = pieces.struct[piece_index]
        board.surface.blit(piece.surface, piece.pos, piece.rect)


def draw_elements(board: Board, pieces_1: Piece, pieces_2: Pieces):
    DISPLAY_SURF.fill("grey")
    draw_pieces(board, pieces_1)
    draw_pieces(board, pieces_2)
    DISPLAY_SURF.blit(board.surface, (BOARDPOSX, BOARDPOSY))


def main():
    pygame.display.set_caption("Checkers")
    pygame.init()
    checkerboard = init_board(BOARDSIZE, BOARDSIZE, SQUARECOUNT)
    player_1_pieces, player_2_pieces = init_pieces(checkerboard)

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
