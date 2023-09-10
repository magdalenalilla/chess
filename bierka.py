import pygame
from graphics import rozmiar_kwadratu


class Bierka:

    #  konstruktor bierki
    def __init__(self, x, y, colour, isSelected):
        self._x = x  # pozycja x
        self._y = y  # pozycja y
        self._colour = colour  # kolor
        self._isSelected = isSelected  # czy jest wybrana
        self.image = None

    #  funkcja aktualizuje atrybuty bierki po wykonanym ruchu (np. że już się kiedyś ruszyła)
    def update_bierka(self):
        pass

    def move(self, x, y):
        pass

    # właściowości
    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value):
        self._colour = value

    @property
    def isSelected(self):
        return self._isSelected

    @isSelected.setter
    def isSelected(self, value):
        self._isSelected = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class King(Bierka):
    def __init__(self, x, y, colour, isSelected):
        # konstruktor ogólny, analogicznie w innych bierkach
        super().__init__(x, y, colour, isSelected)
        # czy kiedykolwiek była ruszona
        self._isFirstMove = True
        # czy był zroszowany
        self._castling = False
        # czy jest szachowany
        self._isChecked = False

        # dobranie odpowiedniego pliku zdjęciowego
        if colour == "white":
            self.image = pygame.image.load('bierki/white_king.png')
        else:
            self.image = pygame.image.load('bierki/black_king.png')
        self.image = pygame.transform.scale(self.image, (rozmiar_kwadratu, rozmiar_kwadratu))

    #funkcja do wykonania roszady
    def castling(self, board, rook_x, rook_y):
        if self._isFirstMove:
            rook = board.get_piece(rook_x, rook_y)
            if isinstance(rook, Rook) and rook.isFirstMove and rook.colour == self._colour:  # asekuracyjne sprawadzanie
                step = 1 if rook_x > self._x else -1  # w ktorą stonę jest wykonywana

                # Wykonywanie roszady
                new_king_x = self._x + 2 * step
                new_rook_x = rook_x - step
                self._x = new_king_x
                rook._x = new_rook_x
                self._isFirstMove = False
                rook._isFirstMove = False
                return True

    # zmiana atrybutu na "ruszony"
    def update_bierka(self):
        self._isFirstMove = False

    @property
    def castling(self):
        return self._castling

    @castling.setter
    def castling(self, value):
        self._castling = value

    @property
    def isChecked(self):
        return self._isChecked

    @isChecked.setter
    def isChecked(self, value):
        self._isChecked = value

    def move(self, board):
        moves = []  # tablica ruchów możliwych do wykonania
        directions = []  # tablica wszystkich potencjalnych kierunków
        for i in range(-1, 2): # wszystkie kierunki i zwroty
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    directions.append((i, j))

        # sprawdzanie roszady w lewo dokładniej opisane, w prawo analogicznie
        if self._isFirstMove:  # król nie może być ruszony podczas roszady
            # dla białego króla
            if self._colour == "white" and board.get_piece(0, self._y) is not None:  # jeśli jest to biały kolor i jest to wieża na lewo
                left_rook = board.get_piece(0, self._y)  # wybierana jest wieża na lewo
                if isinstance(left_rook, Rook) and left_rook.isFirstMove and left_rook.colour == self._colour and self._isFirstMove == True:  #jeśli jest to wieża i jest to pirwszy ruch wieży
                    can_castle_left = True
                    for x in range(self._x - 1, self._x - 3, -1): # sprwadzanie czy jest wolna przestrzń między królem a wieża
                        if board.get_piece(x, self._y) is not None:
                            can_castle_left = False
                            break

                    # sprwadzanie czy miejsce, przez które przechodzi król jest szachowane
                    if can_castle_left and not board.is_king_in_check(self._x, self._y, self._colour) and not board.is_king_in_check(self._x - 1, self._y, self._colour) and not board.is_king_in_check(self._x - 2, self._y, self._colour):
                        moves.append((self._x - 2, self._y))
            # dla czarnego króla
            if self._colour == "black" and board.get_piece(0, self._y) is not None:
                left_rook = board.get_piece(0, self._y)
                if isinstance(left_rook, Rook) and left_rook.isFirstMove and left_rook.colour == self._colour and self._isFirstMove == True:
                    can_castle_left = True
                    for x in range(self._x - 1, self._x - 3, -1):
                        if board.get_piece(x, self._y) is not None:
                            can_castle_left = False
                            break
                    if can_castle_left and not board.is_king_in_check(self._x, self._y, self._colour) and not board.is_king_in_check(self._x - 1, self._y, self._colour) and not board.is_king_in_check(self._x - 2, self._y, self._colour):
                        moves.append((self._x - 2, self._y))

        # Sprawdzanie roszady w prawo
        if self._isFirstMove:
            if self._colour == "white" and board.get_piece(7, self._y) is not None:
                right_rook = board.get_piece(7, self._y)
                if isinstance(right_rook, Rook) and right_rook.isFirstMove and right_rook.colour == self._colour and self._isFirstMove == True:
                    can_castle_right = True
                    for x in range(self._x + 1, self._x + 2):
                        if board.get_piece(x, self._y) is not None:
                            can_castle_right = False
                            break
                    if can_castle_right and not board.is_king_in_check(self._x, self._y, self._colour) and not board.is_king_in_check(self._x + 1, self._y, self._colour) and not board.is_king_in_check(self._x + 2, self._y, self._colour):
                        moves.append((self._x + 2, self._y))

            if self._colour == "black" and board.get_piece(7, self._y) is not None:
                right_rook = board.get_piece(7, self._y)
                if isinstance(right_rook, Rook) and right_rook.isFirstMove and right_rook.colour == self._colour and self._isFirstMove == True:
                    can_castle_right = True
                    for x in range(self._x + 1, self._x + 2):
                        if board.get_piece(x, self._y) is not None:
                            can_castle_right = False
                            break
                    if can_castle_right and not board.is_king_in_check(self._x, self._y, self._colour) and not board.is_king_in_check(self._x + 1, self._y, self._colour) and not board.is_king_in_check(self._x + 2, self._y, self._colour):
                        moves.append((self._x + 2, self._y))

        # pozostałych ruchy króla
        for dx, dy in directions:
            new_x, new_y = self._x + dx, self._y + dy
            if board.is_valid(new_x, new_y, self._colour):
                moves.append((new_x, new_y))

        return moves


class Queen(Bierka):

    def __init__(self, x, y, colour, isSelected):
        super().__init__(x, y, colour, isSelected)
        if colour == "white":
            self.image = pygame.image.load('bierki/white_queen.png')
        else:
            self.image = pygame.image.load('bierki/black_queen.png')
        self.image = pygame.transform.scale(self.image, (rozmiar_kwadratu, rozmiar_kwadratu))

    def move(self, board):
        moves = []
        directions = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    directions.append((i, j))
        # ruchy damy
        for dx, dy in directions:
            for dist in range(1, 8):
                new_x, new_y = self._x + dist * dx, self._y + dist * dy
                if not board.is_valid(new_x, new_y, self._colour):  # czy pole jest dozwolone (funkcja is valid w klasie Board)
                    break
                if board.is_occupied_by_opponent(new_x, new_y, self._colour):  # jeśli jest oponent to dalej nie da się poruszać bo nie przeskakujemy przez figury
                    moves.append((new_x, new_y))
                    break
                moves.append((new_x, new_y))
        return moves

class Bishop(Bierka):

    def __init__(self, x, y, colour, isSelected):
        super().__init__(x, y, colour, isSelected)
        if colour == "white":
            self.image = pygame.image.load('bierki/white_bishop.png')
        else:
            self.image = pygame.image.load('bierki/black_bishop.png')
        self.image = pygame.transform.scale(self.image, (rozmiar_kwadratu, rozmiar_kwadratu))

    def move(self, board):
        moves = []

        directions = [(i, j) for i in [-1, 1] for j in [-1, 1]]
        for dx, dy in directions:
            for dist in range(1, 8):
                new_x, new_y = self._x + dist * dx, self._y + dist * dy
                if not board.is_valid(new_x, new_y, self._colour):
                    break
                if board.is_occupied_by_opponent(new_x, new_y, self._colour):
                    moves.append((new_x, new_y))
                    break
                moves.append((new_x, new_y))
        return moves


class Knight(Bierka):

    def __init__(self, x, y, colour, isSelected):
        super().__init__(x, y, colour, isSelected)
        if colour == "white":
            self.image = pygame.image.load('bierki/white_knight.png')
        else:
            self.image = pygame.image.load('bierki/black_knight.png')
        self.image = pygame.transform.scale(self.image, (rozmiar_kwadratu, rozmiar_kwadratu))

    def move(self, board):
        moves = []
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for dx, dy in directions:
            new_x, new_y = self._x + dx, self._y + dy
            if board.is_valid(new_x, new_y, self._colour):
                moves.append((new_x, new_y))
        return moves

class Rook(Bierka):

    def __init__(self, x, y, colour, isSelected):
        super().__init__(x, y, colour, isSelected)
        self._isFirstMove = True
        self._isMoved = False
        if colour == "white":
            self.image = pygame.image.load('bierki/white_rook.png')
        else:
            self.image = pygame.image.load('bierki/black_rook.png')
        self.image = pygame.transform.scale(self.image, (rozmiar_kwadratu, rozmiar_kwadratu))

    def move(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            for dist in range(1, 8):
                new_x, new_y = self._x + dist * dx, self._y + dist * dy
                if not board.is_valid(new_x, new_y, self._colour):
                    break
                if board.is_occupied_by_opponent(new_x, new_y, self._colour):
                    moves.append((new_x, new_y))
                    break
                moves.append((new_x, new_y))
        return moves

    # ten fragment jest potrzebny do prawidłowego działania roszady
    def update_bierka(self):
        self._isFirstMove = False

    @property
    def isMoved(self):
        return self._isMoved

    @isMoved.setter
    def isMoved(self, value):
        self._isMoved = value

    @property
    def isFirstMove(self):
        return self._isFirstMove

class Pawn(Bierka):
    def __init__(self, x, y, colour, isSelected):
        super().__init__(x, y, colour, isSelected)
        self._isFirstMove = True
        if colour == "white":
            self.image = pygame.image.load('bierki/white_pown.png')
        else:
            self.image = pygame.image.load('bierki/black_pown.png')
        self.image = pygame.transform.scale(self.image, (rozmiar_kwadratu, rozmiar_kwadratu))

    def move(self, board):
        moves = []
        direction = 1 if self._colour == "white" else -1
        new_x, new_y = self._x, self._y + direction

        # sprawdzanie, czy pole przed pionkiem jest puste
        if board.is_valid(new_x, new_y, self._colour) and not board.is_occupied_by_opponent(new_x, new_y, self.colour):
            moves.append((new_x, new_y))

        # sprawdzanie, czy pionek może przesunąć się o dwa pola na początku
        if self._isFirstMove and not board.is_occupied_by_opponent(new_x, new_y, self.colour):
            new_x, new_y = self._x, self._y + 2 * direction
            if board.is_valid(new_x, new_y, self._colour) and not board.is_occupied_by_opponent(new_x, new_y,
                                                                                                self.colour):
                moves.append((new_x, new_y))

        # sprawdzanie, czy pionek może wykonać bicie w prawo
        new_x, new_y = self._x + 1, self._y + direction
        if board.is_valid(new_x, new_y, self._colour) and board.is_occupied_by_opponent(new_x, new_y, self._colour):
            moves.append((new_x, new_y))

        # Sprawdzenie, czy pionek może wykonać bicie w lewo
        new_x, new_y = self._x - 1, self._y + direction
        if board.is_valid(new_x, new_y, self._colour) and board.is_occupied_by_opponent(new_x, new_y, self._colour):
            moves.append((new_x, new_y))
        return moves

    def update_bierka(self):
        self._isFirstMove = False

    @property
    def isFirstMove(self):
        return self._isFirstMove

    @isFirstMove.setter
    def isFirstMove(self, value):
        self._isFirstMove = value
