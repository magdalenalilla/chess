import bierka
import graphics
from bierka import King, Queen, Bishop, Knight, Rook, Pawn


class Board:

    def __init__(self):
        self.board = self.create_board()

    # sprawdzanie czy król jest w szachu
    def is_king_in_check(self, king_x, king_y, king_color):
        opponent_color = "black" if king_color == "white" else "white"

        # sprawdzanie czy jakaś figura przeciwnika atakuje

        # sprawdzanie ataków w pionie i poziomie
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = king_x + dx, king_y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.get_piece(new_x, new_y)
                if piece is not None:
                    if piece.colour == opponent_color:
                        if isinstance(piece, Queen) or isinstance(piece, Rook):
                            return True
                    break
                new_x += dx
                new_y += dy

        # sprawdzanie ataków na skos
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_x, new_y = king_x + dx, king_y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.get_piece(new_x, new_y)
                if piece is not None:
                    if piece.colour == opponent_color:
                        if isinstance(piece, Queen) or isinstance(piece, Bishop):
                            return True
                    break
                new_x += dx
                new_y += dy

        # sprawdzanie ataków ze strony skoczków
        knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for dx, dy in knight_moves:
            new_x, new_y = king_x + dx, king_y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.get_piece(new_x, new_y)
                if piece is not None and isinstance(piece, Knight) and piece.colour == opponent_color:
                    return True
        # sprawdzanie ataków ze strony pionków
        pawn_moves = [(1, 1), (-1, 1)]
        if king_color == "black":
            pawn_moves = [(1, -1), (-1, -1)]

        for dx, dy in pawn_moves:
            new_x, new_y = king_x + dx, king_y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.get_piece(new_x, new_y)
                if piece is not None and isinstance(piece, Pawn) and piece.colour == opponent_color:
                    return True

        return False

    def get_piece(self, x, y):
        return self.board[x][y]

    def is_valid(self, x, y, colour):
        # sprawdzanie czy pozycja jest na planszy
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        if self.board[x][y] is None or self.board[x][y].colour != colour:
            return True
        return False

    # wykonanie ruchu
    def make_move(self, start_x, start_y, end_x, end_y, dozwolony_kolor, okno_chess, rozmiar):
        piece = self.board[start_x][start_y]
        if piece is not None and piece.colour == dozwolony_kolor:
            possible_moves = piece.move(self)
            if (end_x, end_y) in possible_moves:

                if isinstance(piece, King) and (start_x - end_x == 2 or start_x - end_x == -2) and start_y - end_y == 0:
                    if piece._castling == False and piece._isFirstMove == True:
                        king = piece
                        rook_x = 0 if end_x == 2 else 7
                        rook_y = king._y
                        self.do_castling(king, rook_x, rook_y, okno_chess, rozmiar)
                        return True

                zbita_figura_poczatkowa = self.board[start_x][start_y]
                zbita_figura_poczatkowa_x = piece._x
                zbita_figura_poczatkowa_y = piece._y

                self.board[start_x][start_y] = None
                zbita_figura = self.board[end_x][end_y]
                self.board[end_x][end_y] = piece  # ustawienie figury na nowej pozycji

                piece._x = end_x
                piece._y = end_y

                king_x, king_y = self.find_king(dozwolony_kolor)

                if not self.is_king_in_check(king_x, king_y, dozwolony_kolor):
                    piece.update_bierka()
                    if isinstance(piece, Pawn):
                        if (piece.colour == 'black' and end_y == 0) or (piece.colour == 'white' and end_y == 7):
                            self.board[end_x][end_y] = Queen(end_x, end_y, dozwolony_kolor, False)
                            piece = self.board[end_x][end_y]

                    return True
                else:
                    self.board[start_x][start_y] = zbita_figura_poczatkowa
                    self.board[end_x][end_y] = zbita_figura
                    piece._x = zbita_figura_poczatkowa_x
                    piece._y = zbita_figura_poczatkowa_y
                    return False

        return False
    # wykonanie roszady
    def do_castling(self, king, rook_x, rook_y, okno_chess, rozmiar):
        # przesuń króla
        if king._x - rook_x > 0:
            new_king_x = king._x - 2
            new_rook_x = king._x - 1
        else:
            new_king_x = king._x + 2
            new_rook_x = king._x + 1

        king.update_bierka()

        rook = self.board[rook_x][rook_y]
        king._castling = True

        graphics.move(okno_chess, rook_x, 7 - rook_y, rook, new_rook_x, 7 - rook._y, rozmiar)

        self.board[new_king_x][king._y] = king
        self.board[king._x][king._y] = None
        king._x = new_king_x

        # przesuń wieżę
        self.board[new_rook_x][rook._y] = rook
        self.board[rook._x][rook._y] = None
        rook._x = new_rook_x

    def is_checkmate(self, king_color, okno_chess, rozmiar):
        king_x, king_y = self.find_king(king_color)

        # sprawdzanie, czy król jest w szachu
        if self.is_king_in_check(king_x, king_y, king_color):
            # sprawdzanie, czy król ma możliwość wykonania jakiegokolwiek ruchu
            for x in range(8):
                for y in range(8):
                    piece = self.board[x][y]
                    if piece is not None and piece.colour == king_color:
                        possible_moves = piece.move(self)
                        for move_x, move_y in possible_moves:
                            if not self.is_king_check_after_move(x, y, move_x, move_y, king_color):
                                return False
            # jeśli król jest w szachu i nie ma możliwości ruchu, to jest szach-mat
            return True
        return False
    # sprawdzanie, czy król będzie szachowany po wykonaniu ruchu
    def is_king_check_after_move(self, start_x, start_y, end_x, end_y, player_color):
        piece = self.board[start_x][start_y]

        if piece is not None and piece.colour == player_color:
            zbita_figura_poczatkowa = self.board[start_x][start_y]
            zbita_figura_poczatkowa_x = piece._x
            zbita_figura_poczatkowa_y = piece._y

            self.board[start_x][start_y] = None

            zbita_figura = self.board[end_x][end_y] if self.board[end_x][end_y] is not None else None
            self.board[end_x][end_y] = piece

            piece._x = end_x
            piece._y = end_y

            king_x, king_y = self.find_king(player_color)
            is_check = self.is_king_in_check(king_x, king_y, player_color)

            self.board[start_x][start_y] = zbita_figura_poczatkowa
            if zbita_figura is not None:
                self.board[end_x][end_y] = zbita_figura
            else:
                self.board[end_x][end_y] = None
            piece._x = zbita_figura_poczatkowa_x
            piece._y = zbita_figura_poczatkowa_y

            return is_check
        return False

    def is_occupied_by_opponent(self, x, y, colour):
        if self.board[x][y] is not None and self.board[x][y].colour != colour:
            return True
        return False

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Ustawianie pionków
        for i in range(8):
            board[i][6] = Pawn(i, 6, "black", False)
            board[i][1] = Pawn(i, 1, "white", False)

        # Ustawianie wież
        board[0][7] = Rook(0, 7, "black", False)
        board[7][7] = Rook(7, 7, "black", False)
        board[0][0] = Rook(0, 0, "white", False)
        board[7][0] = Rook(7, 0, "white", False)

        # Ustawianie skoczków
        board[1][7] = Knight(1, 7, "black", False)
        board[6][7] = Knight(6, 7, "black", False)
        board[1][0] = Knight(1, 0, "white", False)
        board[6][0] = Knight(6, 0, "white", False)

        # Ustawianie gońców
        board[2][7] = Bishop(2, 7, "black", False)
        board[5][7] = Bishop(5, 7, "black", False)
        board[2][0] = Bishop(2, 0, "white", False)
        board[5][0] = Bishop(5, 0, "white", False)

        # Ustawianie hetmanów
        board[3][7] = Queen(3, 7, "black", False)
        board[3][0] = Queen(3, 0, "white", False)

        # Ustawianie królów
        board[4][7] = King(4, 7, "black", False)
        board[4][0] = King(4, 0, "white", False)

        return board

    def find_king(self, dozwolony_kolor):
        for y in range(8):
            for x in range(8):
                piece = self.get_piece(x, y)
                if isinstance(piece, King) and piece.colour == dozwolony_kolor:
                    return x, y
        return None, None
