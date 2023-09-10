# grafika pobrana ze strony https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

import pygame

# stałe kolorów
kolor = (75, 185, 225) # kolor tła planszy
kolor_kwadratu1 = (233, 236, 239)
kolor_kwadratu2 = (125, 135, 150)
kolor_swiecenia = (255, 132, 165)  # różowy

# stałe rozmiarów
szerokosc = 800
rozmiar_kwadratu = szerokosc // 8  # rozmiar pojedynczego kwadratu
rozmiar_pionka = rozmiar_kwadratu // 2  # rozmiar pionka


# inicjalizacja figur
def load_pieces(size):
    global white_pown, black_pown, white_rook, black_rook, white_knight, black_knight, white_bishop, black_bishop, white_queen, black_queen, white_king, black_king

    white_pown = pygame.image.load('bierki/white_pown.png')  # załaduj obraz
    white_pown = pygame.transform.scale(white_pown,
                                        (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    black_pown = pygame.image.load('bierki/black_pown.png')  # załaduj obraz
    black_pown = pygame.transform.scale(black_pown,
                                        (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    white_rook = pygame.image.load('bierki/white_rook.png')  # załaduj obraz
    white_rook = pygame.transform.scale(white_rook,
                                        (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    black_rook = pygame.image.load('bierki/black_rook.png')  # załaduj obraz
    black_rook = pygame.transform.scale(black_rook,
                                        (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    white_knight = pygame.image.load('bierki/white_knight.png')  # załaduj obraz
    white_knight = pygame.transform.scale(white_knight,
                                          (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    black_knight = pygame.image.load('bierki/black_knight.png')  # załaduj obraz
    black_knight = pygame.transform.scale(black_knight,
                                          (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    white_bishop = pygame.image.load('bierki/white_bishop.png')  # załaduj obraz
    white_bishop = pygame.transform.scale(white_bishop,
                                          (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    black_bishop = pygame.image.load('bierki/black_bishop.png')  # załaduj obraz
    black_bishop = pygame.transform.scale(black_bishop,
                                          (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    white_queen = pygame.image.load('bierki/white_queen.png')  # załaduj obraz
    white_queen = pygame.transform.scale(white_queen,
                                         (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    black_queen = pygame.image.load('bierki/black_queen.png')  # załaduj obraz
    black_queen = pygame.transform.scale(black_queen,
                                         (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    white_king = pygame.image.load('bierki/white_king.png')  # załaduj obraz
    white_king = pygame.transform.scale(white_king,
                                        (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu

    black_king = pygame.image.load('bierki/black_king.png')  # załaduj obraz
    black_king = pygame.transform.scale(black_king,
                                        (rozmiar_kwadratu, rozmiar_kwadratu))  # skaluj obraz do rozmiaru kwadratu


# funkcja rysująca planszę
def draw_board(okno_chess, aktywny_x, aktywny_y):
    # rysowanie obiektów
    okno_chess.fill(kolor)  # kolor okna gry

    for row in range(7, -1, -1):
        for col in range(8):
            # Rysowanie na przemian kolorami kwadratów planszy
            if (row + col) % 2 == 0:
                kolor_kwadratu = kolor_kwadratu1
            else:
                kolor_kwadratu = kolor_kwadratu2

            if aktywny_x == col and aktywny_y == row:
                kolor_kwadratu = kolor_swiecenia

            pygame.draw.rect(okno_chess, kolor_kwadratu, # rysowanie prostokątów na planszy
                             pygame.Rect(col * rozmiar_kwadratu, row * rozmiar_kwadratu, rozmiar_kwadratu,
                                         rozmiar_kwadratu))

            if row == 6:
                # umieszczenie białego pionka na planszy
                okno_chess.blit(white_pown, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 1:
                # umieszczenie czarnego pionka na planszy
                okno_chess.blit(black_pown, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 0 and (col == 0 or col == 7):
                # umieszczanie czarnych wież
                okno_chess.blit(black_rook, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 7 and (col == 0 or col == 7):
                # umieszczanie białych wież
                okno_chess.blit(white_rook, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 0 and (col == 1 or col == 6):
                # umieszczanie czarnych skoczków
                okno_chess.blit(black_knight, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 7 and (col == 1 or col == 6):
                # umieszczanie białych skoczków
                okno_chess.blit(white_knight, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 0 and (col == 2 or col == 5):
                # umieszczanie czarnych gońców
                okno_chess.blit(black_bishop, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 7 and (col == 2 or col == 5):
                # umieszczanie białych gońców
                okno_chess.blit(white_bishop, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 0 and (col == 3):
                # umieszczanie czarnego hetmana
                okno_chess.blit(black_queen, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 7 and (col == 3):
                # umieszczanie białego hetmana
                okno_chess.blit(white_queen, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 0 and (col == 4):
                # umieszczanie czarnego króla
                okno_chess.blit(black_king, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))
            elif row == 7 and (col == 4):
                # umieszczanie białego króla
                okno_chess.blit(white_king, (col * rozmiar_kwadratu, row * rozmiar_kwadratu))

# okno_chess.blit(): rysowanie obrazu pionka na planszy na podstawie podanych współrzędnych

def move_zbij(okno_chess, przeciagana_figura, docelowe_x, doceleowe_y, rozmiar):
    # Najpierw rysujemy kwadrat na poprzedniej figurze biały lub czarny
    if (docelowe_x + doceleowe_y) % 2 == 0:
        kolor_tla = kolor_kwadratu1
    else:
        kolor_tla = kolor_kwadratu2

    # pygame.draw.rect rysowanie prostokątnego obszaru na ekranie
    pygame.draw.rect(okno_chess, kolor_tla,
                     pygame.Rect(docelowe_x * rozmiar_kwadratu, doceleowe_y * rozmiar_kwadratu, rozmiar_kwadratu,
                                 rozmiar_kwadratu))

    # renderowanie obiektów gry na ekranie
    okno_chess.blit(przeciagana_figura.image, (docelowe_x * rozmiar, doceleowe_y * rozmiar))


def draw_castling(okno_chess, plansza, roszada, rozmiar):
    # Znajdowanie pozycji początkowej i końcowej dla króla i wieży w roszadzie
    krol_poczatkowy_x, krol_poczatkowy_y, krol_koncowy_x, krol_koncowy_y, wieza_poczatkowa_x, wieza_poczatkowa_y, wieza_koncowa_x, wieza_koncowa_y = roszada

    # Przemieszczanie króla
    plansza.move_piece(krol_poczatkowy_x, krol_poczatkowy_y, krol_koncowy_x, krol_koncowy_y)
    move(okno_chess, krol_poczatkowy_x, krol_poczatkowy_y, plansza.get_piece(krol_koncowy_x, krol_koncowy_y),
         krol_koncowy_x, krol_koncowy_y, rozmiar)

    # Przemieszczanie wieży
    plansza.move_piece(wieza_poczatkowa_x, wieza_poczatkowa_y, wieza_koncowa_x, wieza_koncowa_y)
    move(okno_chess, wieza_poczatkowa_x, wieza_poczatkowa_y, plansza.get_piece(wieza_koncowa_x, wieza_koncowa_y),
         wieza_koncowa_x, wieza_koncowa_y, rozmiar)


def move(okno_chess, aktywny_x, aktywny_y, przeciagana_figura, docelowe_x, doceleowe_y, rozmiar):
    # Zapisywanie koloru tła aktualnego pola
    if (aktywny_x + aktywny_y) % 2 == 0:
        kolor_tla = kolor_kwadratu1
    else:
        kolor_tla = kolor_kwadratu2

    # Rysowanie tła na polu startowym
    pygame.draw.rect(okno_chess, kolor_tla,
                     pygame.Rect(aktywny_x * rozmiar, aktywny_y * rozmiar, rozmiar, rozmiar))

    # Rysowanie przeciągniętej figury na docelowym polu
    okno_chess.blit(przeciagana_figura.image, (docelowe_x * rozmiar, doceleowe_y * rozmiar))


def podswietlanie(okno_chess, aktywny_x, aktywny_y, rozmiar, figura):
    kolor_kwadratu = kolor_swiecenia  # Kolor podświetlenia

    # Rysowanie kwadratu podświetlenia
    pygame.draw.rect(okno_chess, kolor_kwadratu,
                     pygame.Rect(aktywny_x * rozmiar, aktywny_y * rozmiar, rozmiar, rozmiar))

    # Rysowanie obrazu figury na kwadracie, jeśli jest to możliwe
    if figura is not None:
        figura_rect = figura.image.get_rect()
        figura_rect.center = (aktywny_x * rozmiar + rozmiar // 2, aktywny_y * rozmiar + rozmiar // 2)
        okno_chess.blit(figura.image, figura_rect)


def delete_podswitlanie(okno_chess, aktywny_x, aktywny_y, rozmiar, figura):
    # Określenie koloru kwadratu
    if (aktywny_x + aktywny_y) % 2 == 0:
        kolor_kwadratu = kolor_kwadratu1  # Przypisanie pierwszego koloru kwadratu
    else:
        kolor_kwadratu = kolor_kwadratu2  # Przypisanie drugiego koloru kwadratu

    # Rysowanie kwadratu o zdefiniowanym kolorze
    pygame.draw.rect(okno_chess, kolor_kwadratu,
                     pygame.Rect(aktywny_x * rozmiar, aktywny_y * rozmiar, rozmiar, rozmiar))

    if figura is not None:
        # Przygotowanie obiektu Rect dla figury, aby wyśrodkować ją na kwadracie
        figura_rect = figura.image.get_rect()
        figura_rect.center = (aktywny_x * rozmiar + rozmiar // 2, aktywny_y * rozmiar + rozmiar // 2)
        # Wyświetlenie obrazu figury w wyznaczonym miejscu na planszy
        okno_chess.blit(figura.image, figura_rect)