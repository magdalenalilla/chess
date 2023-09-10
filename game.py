import pygame
from pygame import font
from pygame.locals import *
import sys
import graphics
from board import Board



pygame.init()

# zmienne przetrzymujące wielkość okna gry
wysokosc = 800
szerokosc = 800

okno_chess = pygame.display.set_mode((szerokosc, wysokosc)) # tworzenie okna gry o określonych wymiarach

# ustawianie nazwy okna gry
pygame.display.set_caption('Chess')

# wczytywanie grafik reprezentujących figury szachowe do gry
graphics.load_pieces(szerokosc // 8)

dozwolony_kolor = 'white'  # zmienna informująca, który kolor pionka wykonuje ruch
zaznaczony_kwadracik_x = None  # pole, które zaznaczamy (podświetlamy), współrzędne zaznaczonego pola na planszy
zaznaczony_kwadracik_y = None  # pole, które zaznaczamy (podświetlamy), współrzędne zaznaczonego pola na planszy
zanaczone_pole = False # brak zaznaczonego pola na planszy
board = Board()  # tworzenie obiektu-konkretnej planszy, na której będziemy grać
przeciagana_figura = None  # zmienna przetrzymująca referencje na figurę
czy_zaznaczona_figura = None # sprawdzanie, czy na planszy jest zaznaczona figura
docelowe_x = None # zmienne używane do przechowywania docelowej współrzędnej(x)
docelowe_y = None # zmienne używane do przechowywania docelowej współrzędnej(y)
czy_zbity = False # sprawdzanie, czy w bieżącym ruchu doszło do zbicia figury na planszy

font.init()  # Inicjalizacja modułu czcionki
czcionka = font.SysFont(None, 36)  # Utworzenie obiektu czcionki

# rysowanie początkowego położenia pionków i całej planszy
graphics.draw_board(okno_chess, zaznaczony_kwadracik_x, zaznaczony_kwadracik_y)

while True:
    for event in pygame.event.get():  # pętla, która odpowiada za iterowanie zdarzeń
        if event.type == QUIT:  # zamykanie okna gry
            pygame.quit()  # kończenie pracy z biblioteką pygame
            sys.exit()  # kończenie działanie aplikacji od strony systemu

        elif event.type == MOUSEBUTTONDOWN: # ponowne kliknięcie przycisku myszy po wcześniejszym zaznaczeniu figury na planszy

            mouse_x, mouse_y = pygame.mouse.get_pos()  # pobieranie pozycji z kliknięcia myszy
            klikniety_x = (mouse_x // (szerokosc // 8))  # obliczanie pozycji (współrzędnej x) na planszy
            klikniety_y = (mouse_y // (wysokosc // 8))  # obliczanie pozycji (współrzędnej y) na planszy

            if not zanaczone_pole:  # jeśli pole nie jest zaznaczone to podświetlamy i wybieramy figurę, którą chcemy wykonać ruch
                zaznaczony_kwadracik_x = klikniety_x  # pozycje (x) figury

                zaznaczony_kwadracik_y = klikniety_y # pozycja (y) figury
                zanaczone_pole = True
                przeciagana_figura = board.get_piece(zaznaczony_kwadracik_x,
                                                     7 - zaznaczony_kwadracik_y)  # bierzemy do zmiennej obiekt figury
                graphics.podswietlanie(okno_chess, zaznaczony_kwadracik_x, zaznaczony_kwadracik_y, szerokosc // 8,
                                       przeciagana_figura)  # graficznie podświetlenie pola na planszy

            else:  # jeśli pole jest już podświetlone
                docelowe_x = klikniety_x  # docelowa pozycja (x) przeciąganej figury
                docelowe_y = klikniety_y  # docelowa pozycja (y) przeciąganej figury

                #  anulowanie podświetlenia
                if (klikniety_x, klikniety_y) == (zaznaczony_kwadracik_x, zaznaczony_kwadracik_y):
                    graphics.delete_podswitlanie(okno_chess, zaznaczony_kwadracik_x, zaznaczony_kwadracik_y,
                                                 szerokosc // 8,
                                                 przeciagana_figura)  # graficzne usunięcie podświetlenia kwadraciku
                    zaznaczony_kwadracik_x = None
                    zaznaczony_kwadracik_y = None #resetowanie zmiennych związanych z zaznaczonym polem na planszy i przeciąganą figurą
                    zanaczone_pole = False
                    przeciagana_figura = None

                else:



                    #  jeśli figura została przeciągnięta
                    if przeciagana_figura is not None and board.make_move(zaznaczony_kwadracik_x,
                                                                          7 - zaznaczony_kwadracik_y,
                                                                          docelowe_x, 7 - docelowe_y, dozwolony_kolor,
                                                                          okno_chess, szerokosc // 8):

                        #  zaktualizowanie figury (promocja figury)
                        przeciagana_figura = board.get_piece(docelowe_x,7-docelowe_y)

                        graphics.move(okno_chess, zaznaczony_kwadracik_x, zaznaczony_kwadracik_y, przeciagana_figura,
                                      docelowe_x, docelowe_y, szerokosc // 8)

                        if board.board[docelowe_x][7 - docelowe_y] is not None: # sprawdzanie zawartości planszy ,,board" na konkretnej pozycji
                            graphics.move_zbij(okno_chess, przeciagana_figura, docelowe_x, docelowe_y, szerokosc // 8)

                        zaznaczony_kwadracik_x = None
                        zaznaczony_kwadracik_y = None
                        zanaczone_pole = False

                        #  ustalenie koloru figury, która może się teraz ruszać
                        if dozwolony_kolor == 'white':
                            dozwolony_kolor = 'black'
                        else:
                            dozwolony_kolor = 'white'

                        #  sprawdzanie matu
                        if board.is_checkmate(dozwolony_kolor, okno_chess, szerokosc // 8):
                            wygrany = "black" if dozwolony_kolor == "white" else "white"
                            okno_chess.fill(wygrany)
                            win_text = czcionka.render(wygrany+"win !", True, dozwolony_kolor)
                            okno_chess.blit(win_text,
                                        ((szerokosc - win_text.get_width()) // 2, (szerokosc - win_text.get_height()) // 2))

                        pygame.display.flip()


                    else:  # kliknięcie w inne miejsce na plaszy
                        graphics.delete_podswitlanie(okno_chess, zaznaczony_kwadracik_x, zaznaczony_kwadracik_y,
                                                     szerokosc // 8, przeciagana_figura)
                        zanaczone_pole = False
                        zaznaczony_kwadracik_x = None
                        zaznaczony_kwadracik_y = None
                        przeciagana_figura = None

        pygame.display.update()