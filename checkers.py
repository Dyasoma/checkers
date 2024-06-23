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
WINDOWTOBOARDRATIO = 0.9
BOARDSIZE = WINDOWWIDTH * WINDOWTOBOARDRATIO
SQUARESIZE = BOARDSIZE / SQUARECOUNT
BOARDPOSX = (WINDOWWIDTH - BOARDSIZE) / 2
BOARDPOSY = (WINDOWHEIGHT - BOARDSIZE) / 2
EMPTY = None
PIECESCOUNT = 12

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
YELLOW = (255, 255, 0)


pygame.init()
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Checkers")


 # Classes


class Piece:
    def __init__(self, radius : float,  color: pygame.Color):
        self.radius = radius
        self.color = color
        self.row = 0  # row index on board
        self.col = 0  # col index on board
        self.size = self.radius * 2 # size of rect enclosing piece
        self.surface = self.__create_piece_surface()
        self.rect = self.__create_piece_rect()
        self.__set_pos()

    def __create_piece_surface(self) -> pygame.Surface:
        """
        __create_piece_surface(self) -> pygame.Surface: creates the surface of a game piece. 
        Where the surface is an image with area that encloses it. Creates a surface that can become
        transparent, and fills it with a transparent color
        return : pygame surface object. 
        """
        # creates the transparent surface to draw on
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surf.fill((0,0,0,0)) #fills surface with "transparency"
        return surf

    def __create_piece_rect(self) -> pygame.Rect:
        """
        Creates the rectangular area enclosing the piece. Used for moving the piece
        returns : a pygame rect object. 
        """
        # The center we use to draw is relative to the the surface we drawn onto. 
        rect = pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
        return rect

    def __set_pos(self):
        """
        __set_pos(self):
        Sets the position of the piece, creating two instance attributes rel_pos and abs_pos
        which represent the relative position and absolute position of the piece respectively
        the relative position is relative to the board. The absolute position is relative to the 
        screen window. 
        """
        self.rel_pos = (self.col * self.size, self.row * self.size)
        self.abs_pos = (self.col * self.size + BOARDPOSX, self.row * self.size + BOARDPOSY)

    def move_piece(self, new_row, new_col):
        """
        move_piece(self, new_row, new_col):
        takes in as parameters the new row and col a piece will be set to. updates the row and col
        instance attributes, and then makes a call to __set_pos().

        """
        self.row = new_row
        self.col = new_col
        self.__set_pos()


class Pieces:
    """
    Object Pieces represents all the pieces that belong to a single team. Team is defined by team 
    color parameter, number_of_pieces refers to the number of pieces on a single team.
    """
    def __init__(self, number_of_pieces: int, team_color: pygame.Color):
        self.team_color = team_color
        self.number_of_pieces = number_of_pieces
        self.struct = self.__create_pieces()

    def __create_pieces(self) -> list:
        """
        create_pieces(self) -> list:
        creates a list whoses elements are Piece objects.
        uses the number_of_pieces instance attribute to decide on the number of pieces to make
        uses the team_color instance attribute  to decide which team all the pieces belong to,
        and how to color the pieces.
        returns a list of Piece Objects
        """
        struct = []
        for i in range(self.number_of_pieces):
            piece = Piece(
                SQUARESIZE/2, self.team_color
            )  # all pieces will begin at the same "position"
            struct.append(piece)
        return struct


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
        self.row = row
        self.col = col
        #rel_pos is relative to the board
        #abs_pos is relative to the entire window
        self.rel_pos = ( col * size, row * size)  # columns go left to right, rows go up and down
        self.abs_pos = (col*size + BOARDPOSX, row*size + BOARDPOSY)
        self.surface = self.__create_square_surface()
        self.rect = self.__create_square_rect()
        self.contents = EMPTY  # squares hold nothing in the beginning

    def __create_square_surface(self) -> pygame.Surface:
        """
        __create_square_surface(self) -> pygame.Surface:
        creates a surface object for the current square, which should be square.
        Fills the square with the given color
        """ 
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        return surf

    def __create_square_rect(self) -> pygame.Rect:
        """
        __create_square_rect(self) -> pygame.Rect:
        creates the rectangular area of the square, If the board does not fill the entire window
        Then rec.x and rec.y are positions relative to the window, not the board. 
        """
        rec = self.surface.get_rect(topleft = self.abs_pos)
        return rec
    
    def fill_square(self, piece):
        """
        fill_square(self, piece):
        sets the instance attribute "contents" to be filled with a certain piece. 
        """
        self.contents = piece

class Board:
    """
    Represents an nxn checkered board.
    """
    def __init__(self, width: int, height : int, square_count : int):
        """
        Board is initalized by providing its width and length, and the square_count
        Note that square_count refers to the count of squares along either the x axis or y axis.
        ex: if square count is 5, it will be assumed that a 5x5 board is desired. 
        """
        self.width : int = width
        self.height: int = height
        self.square_count: int = square_count
        self.struct = self.__create_board_struct()
        self.surface = self.__create_board_surface()
        self.rect = self.__create_board_rect()
        self.square_size = self.struct[0][0].size

    def __create_board_struct(self) -> list[list[Square]]:
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
        square_size = self.height / self.square_count
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

    def __create_board_surface(self) -> pygame.Surface:
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        Serves as the "image" of the board
        """
        # Surf is first the entire size of the board
        surf = pygame.Surface((self.width, self.height))
        # we go through the board and for each square, we "blit" onto the board the current square.
        for row_index in range(self.square_count):
            for col_index in range(self.square_count):
                current_square: Square = self.struct[row_index][col_index]
                surf.blit(current_square.surface, current_square.rel_pos)
        return surf

    def __create_board_rect(self) -> pygame.Rect:
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


    def update_board_elements(self, piece : Piece, row : int, col : int):
        piece.move_piece(row, col)
        self.struct[row][col].fill_square(piece)


    def set_pieces(self, game_pieces : tuple[Pieces]):
            """
            set_pieces(self, game_pieces : tuple[Pieces])
            sets pieces position relative to the board surface, that is if the board moves,
            when we draw the pieces they will be drawn relative to the boards top right corner
            updates the instance attribute "position" of the object of class Piece. 
            Takes in as parameters a list of Piece objects and the team color stored as a string.
            Side effect: mutates instance attribute "position"
            returns : None
            """

            for pieces in game_pieces:
                k = 0
                if pieces.team_color == RED:
                    my_range = range(self.square_count)
                else:
                    my_range = reversed(range(self.square_count))
                for i in my_range:
                    for j in range(self.square_count):
                        if self.struct[i][j].color == BLACK:
                            self.update_board_elements(pieces.struct[k], i, j)
                            k += 1
                        if k == pieces.number_of_pieces:
                            break
                    if k == pieces.number_of_pieces:
                        break


    def draw_pieces(self, pieces : Pieces):
        """
        Goes through the pieces data structure finds the piece and then Blits the piece onto the
        board surface, mutating it
        """
        for piece_index in range(len(pieces.struct)):
            piece = pieces.struct[piece_index]
            self.surface.blit(piece.surface, piece.rel_pos, piece.rect)

    def draw_elements(self, pieces_1, pieces_2):
        SCREEN.fill("grey")
        self.draw_pieces(pieces_1)
        self.draw_pieces(pieces_2)
        SCREEN.blit(self.surface, (BOARDPOSX, BOARDPOSY))

# Functions
def main():

    player_1_pieces : Pieces = Pieces(PIECESCOUNT, RED)
    player_2_pieces : Pieces = Pieces(PIECESCOUNT, BLUE)
    checkerboard : Board = Board(BOARDSIZE, BOARDSIZE, SQUARECOUNT)
    checkerboard.set_pieces((player_1_pieces, player_2_pieces))

    GAME_IS_RUNNING = True
    while GAME_IS_RUNNING:  # main game loop
        # collect inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                GAME_IS_RUNNING = False
                
        # handle events

        # update
        checkerboard.draw_elements(player_1_pieces, player_2_pieces)
        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()