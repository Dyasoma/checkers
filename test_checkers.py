from checkers import *
board_size = 500
piece_count = 12
square_count = 8
row = 2
col = 2
size = 100
my_board = Board(board_size, board_size, square_count)
my_square = Square(200, RED, row, col)
my_piece = Piece(size, "Red")
my_pieces = Pieces(piece_count, "Red", my_board) 


def test_board_struct_creation():

    assert len(my_board.struct) == 8

def test_board_surf_creation():
    assert my_board.surface.get_size() == (500,500) 


def test_board_rect_creation():
    assert my_board.rect.size == (500, 500)


def test_piece_constructor():
    init_piece = Piece(0, "Red")
    assert type(init_piece) == Piece

def test_piece_surf_creation():
    assert my_piece.surface.get_size() == (100,100)


def test_piece_rect_creation():
    assert my_piece.rect.size == (100,100)



def test_square_surf_creation():
    assert my_square.surface.get_size() == (200, 200)

def test_square_rect_creation():
    assert my_square.rect.size == (200, 200)


def test_pieces_creation():
    my_board = Board(500, 500, 8)
    my_pieces = Pieces(12, "Red", my_board)
    for i in range(12):
        assert type(my_pieces.struct[i]) == Piece

def test_pieces_creation_1():

    assert len(my_pieces.struct) == 12


def test_overall_shape_board():
    assert len(my_board.struct) * len(my_board.struct[0]) == square_count**2

def test_checking_rows():
    for k in range(piece_count):
        pos_row = my_pieces.struct[k].row
        pos_col = my_pieces.struct[k].col
        assert my_board.struct[pos_row][pos_col].color == BLACK
    


def test_setting_up_pieces_empty():
    for i in range(square_count): 
        assert type(my_pieces.struct[i]) == Piece
        for j in range(square_count):
            my_square = my_board.struct[i][j]
            if (i + j) % 2 == 0:
                assert my_board.struct[i][j].color == WHITE
            else:
                print(f"i is : {i} j is : {j}")
                assert my_board.struct[i][j].color == BLACK

###########
def test_square_construction():
    board_size = 800
    square_count = 16
    siz = board_size / square_count
    my_board = Board(board_size, board_size, 16)
    sqr = my_board.struct[3][4]
    assert sqr.pos == (4 * siz, 3 * siz)
    assert sqr.size == siz
    assert sqr.color == BLACK
    assert sqr.contents == EMPTY
    assert sqr.row == 3
    assert sqr.col == 4
    assert sqr.rect.x == 4 * siz + BOARDPOSX
    assert sqr.rect.y == 3 * siz + BOARDPOSY


def test_pieces_creation2():
    for i in range(4):
        assert my_pieces.struct[i].color == RED

def test_piece_setting():
    my_piece = my_pieces.struct[2]
    print(my_piece.pos)
    assert my_piece.move_piece(2,2)
    print(my_piece.pos)