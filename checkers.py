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
BOARDSIZE = WINDOWWIDTH * WINDOWTOBOARDRATIO
SQUARESIZE = BOARDSIZE / SQUARECOUNT
BOARDPOSX = (WINDOWWIDTH - BOARDSIZE) / 2
BOARDPOSY = (WINDOWHEIGHT - BOARDSIZE) / 2
EMPTY = None
PIECESCOUNT = 12

 # Classes
class Board:
    """
    Represents the Board where a "Board" is a nxn checkered board. Whoses squares are themselves
    objects. 
    """
    def __init__(self, width : int, length : int, square_count : int):
        """
        Board is initalized by providing its width and length, and the square_count
        Note that square_count refers to the count of squares along either the x axis or y axis.
        ex: if square count is 5, it will be assumed that a 5x5 board is desired. 
        """
        self.width: int = width
        self.length: int = length
        self.square_count: int = square_count
        self.struct = self.create_board_struct()
        self.surface = self.create_board_surface()
        self.rect = self.create_board_rect()

    def create_board_struct(self):
        """
        Creates the instance attribute "struct" for the board object of class Board. instance 
        attribute refers to the boards Data structure, implemented as a list of lists 
        whose entries are objects of class Square. Mutates the list as the list is built. 
        board.struct[i][j] refers to the ith row, and the jth column of the board.
        Returns : a list of lists
        Side effect : creates instance attribute "struct" and mutates it 
        Calls to create_board_struct will overide previous instance attribute. 
        creates empty list,
        """
        struct: list = []
        square_size = self.length / self.square_count
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                # checks if square is even or odd, setting even to white and odd to black
                if (row_index + col_index) % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK
                square = Square(square_size, color, row_index, col_index)
                row.append(square)  # creates a square and adds it to the struct
            struct.append(row)
        return struct

    def create_board_surface(self):
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        Serves as the "image" of the board
        """
        surf = pygame.Surface((self.length, self.width))
        for row_index in range(self.square_count):
            for col_index in range(self.square_count):
                current_square: Square = self.struct[row_index][col_index]
                surf.blit(current_square.surface, current_square.pos)
        return surf

    def create_board_rect(self):
        """
        create_board_rect(self)
        Creates an instance attribute of object Board, using the instance attribute surface.
        Acts as a wrapper to the get_rect() function for objects of class Surface from pygame module
        """
        rec = self.surface.get_rect() # provides size but not position
        # sets the position of the board
        rec.left = BOARDPOSX 
        rec.top = BOARDPOSY
        return rec

class Square:
    def __init__(self, size : int, color : pygame.Color, row : int, col :int):# row/col are indices
        """
        Square objects represent a single square tile on the board.
        Note that the square in the ith row and jth column will have a position
        (j * size, i * size) where i and j are the indices of the squares on the board struct.
        ex: for square in board.struct[3][4] with size 100 it will have a position = (400, 300)
        where the position refers to the top left corner of the square. 
        """
        self.size = size
        self.color = color
        self.contents = EMPTY  # squares hold nothing in the beginning
        self.row = row
        self.col = col
        self.pos = ( col * size, row * size)  # columns go left to right, rows go up and down
        self.surface = self.create_square_surface()
        self.rect = self.create_square_rect()

    def create_square_surface(self):
        """
        creates a surface object for the current square, which should be square.
        Fills the square with the given color
        """ 
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        return surf

    def create_square_rect(self):
        """
        creates the rectangular area of the square, If the board does not fill the entire window
        Then rec.x and rec.y are positions relative to the window, not the baord. 
        """
        rec = self.surface.get_rect()
        rec.x = BOARDPOSX + self.pos[0] 
        rec.y = BOARDPOSY + self.pos[1]
        return rec

class Pieces:
    """
    Object Pieces represents all the pieces that belong to a single team. Team is defined by team 
    color parameter, number_of_pieces refers to the number of pieces on a single team, board
    is passed as a parameter to allow for setting the pieces
    """
    def __init__(self, number_of_pieces: int, team_color: str, board):
        self.team_color = team_color
        self.number_of_pieces = number_of_pieces
        self.struct = self.create_pieces()
        self.set(board)

    def create_pieces(self) -> list:
        """
        create_pieces(self) -> list:
        creates a list whoses elements are Piece objects.
        uses the number_of_pieces instance attribute to decide on the number of pieces to make
        uses the team_color instance attribute  to decide which teamm all the pieces belong to,
        and how to color the pieces. Uses the Board object to place pieces onto the boards squares
        parameters: number is the int representing the number of pieces to make.
        returns a list of Piece Objects
        """
        struct = []
        for i in range(self.number_of_pieces):
            piece = Piece(
                SQUARESIZE, self.team_color
            )  # all pieces will begin at the same "position"
            struct.append(piece)
        return struct

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
    def __init__(self, size : float,  team_color: str):
        self.row = 0  # row index on board
        self.col = 0  # col index on board
        self.team_color = team_color
        self.size = size
        if self.team_color == "Red":
            self.color = RED
        else:
            self.color = BLUE
        self.surface = self.create_piece_surface()
        self.rect = self.create_piece_rect()

    def create_piece_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        surf = surf.convert_alpha()
        return surf

    def create_piece_rect(self):
        rec = pygame.draw.ellipse(
            self.surface, self.color, self.surface.get_rect(), 0
        )
        return rec

    def set_pos(self):
        self.pos = (self.col * self.size, self.row * self.size)

    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.set_pos()


# Functions
def init_board(board_width: int, board_length: int, square_count : int) -> Board:
    """
    init_board(board_width: int, board_length: int, square_count : int) -> Board
    Initalizes board, taking in as parameters the board width and board length as ints. Instantiates 
    an object of class Board, creates board data structure, creates the board's surface to represent
    the image of the board and creates the board's rect attribute to store and manipuate its 
    rectangular area and position.
    returns: Instance of Board Object
    side effects : None
    """
    board = Board(board_width, board_length, square_count)
    return board


def init_pieces(board: Board):
    """
    initializes pieces, creating a list of lists whose elements are objects of class Piece.
    Then makes a call to the method set
    """
    player_1_pieces = Pieces(PIECESCOUNT, "Red", board)
    player_2_pieces = Pieces(PIECESCOUNT, "Blue", board)

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


def init():
    pygame.display.set_caption("Checkers")
    pygame.init()
    checkerboard = init_board(BOARDSIZE, BOARDSIZE, SQUARECOUNT)
    player_1_pieces, player_2_pieces = init_pieces(checkerboard)
    return checkerboard, player_1_pieces, player_2_pieces


def main():
    checkerboard : Board  
    player_1_pieces : Pieces 
    player_2_pieces : Pieces
    checkerboard, player_1_pieces, player_2_pieces = init()

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

if __name__ == "__main__":
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
