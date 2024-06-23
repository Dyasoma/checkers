from checkers import *
piece_count = 6
square_count = 6
RED = (255, 0, 0)
my_color = RED
row = 0
col = 0
radius = 100
size = radius * 2
my_piece = Piece(radius, RED)
my_pieces = Pieces(piece_count, RED) 
my_square = Square(200, RED, row, col)
my_board = Board(BOARDSIZE, BOARDSIZE, square_count)


def test_piece_attributes():
        assert my_piece.radius == radius
        assert my_piece.color == my_color
        assert my_piece.row == 0  # row index on board
        assert my_piece.col == 0  # col index on board
        assert my_piece.size == my_piece.radius * 2 # size of rect enclosing piece
        assert my_piece.surface.get_size() == (size, size)
        assert my_piece.rect.size == (size, size) # draws onto surface and provides rect
        assert my_piece.rel_pos == (col * size, row * size)
        assert my_piece.abs_pos == (col * size + BOARDPOSX, row * size + BOARDPOSY)
        

def test_pieces():
        assert my_pieces.team_color == RED
        assert my_pieces.number_of_pieces == piece_count
        assert my_pieces.team_color == my_color
        assert len(my_pieces.struct) == piece_count
        for i in range(piece_count):
                assert my_pieces.struct[i].size == SQUARESIZE
                assert my_pieces.struct[i].color == my_color



def test_squares():
        assert my_square.size == size
        assert my_square.color == my_color
        assert my_square.row == row
        assert my_square.col == col
        #rel_pos is relative to the board
        #abs_pos is relative to the entire window
        assert my_square.rel_pos == ( col * size, row * size)
        assert my_square.abs_pos == (col*size + BOARDPOSX, row*size + BOARDPOSY)
        assert my_square.surface.get_size() == (size,size)
        assert my_square.rect.size == (size,size)
        assert my_square.contents == EMPTY

def test_squares_fill():
        test_square = Square(200, RED, row, col)
        test_square.fill_square(my_piece)
        assert test_square.contents == my_piece


def test_board():
        assert my_board.width  == BOARDSIZE
        assert my_board.height == BOARDSIZE
        assert my_board.square_count  == square_count
        assert len(my_board.struct) == square_count
        for i in  range(square_count):
                for j in range(square_count):
                    if (i + j) % 2 == 0:
                        assert my_board.struct[i][j].color == WHITE
                        print(i,j)
                    else:
                        assert my_board.struct[i][j].color == BLACK
                        print(i,j)

        assert my_board.surface.get_size() == (BOARDSIZE, BOARDSIZE)
        assert my_board.rect.size == (BOARDSIZE, BOARDSIZE)
        assert my_board.square_size == my_board.struct[0][0].size

def test_set_pieces():
    test_board = Board(BOARDSIZE, BOARDSIZE, square_count)
    test_pieces_1 = Pieces(piece_count, RED)
    test_pieces_2 = Pieces(piece_count, BLUE)
    game_pieces = (test_pieces_1, test_pieces_2)
    test_board.set_pieces(game_pieces)

    for test_pieces in game_pieces:
        k = 0
        if test_pieces.team_color == RED:
            my_range = range(test_board.square_count)
        else:
            my_range = reversed(range(test_board.square_count))
        for i in my_range:
            for j in range(test_board.square_count):
                if test_board.struct[i][j].color == BLACK:
                    test_board.move_piece(test_pieces.struct[k], i,j)
                    assert test_pieces.struct[k].row == i
                    assert test_pieces.struct[k].col == j
                    assert test_board.struct[i][j].contents == test_pieces.struct[k]
                    k += 1
                if k == test_pieces.number_of_pieces:
                    break
            if k == test_pieces.number_of_pieces:
                break