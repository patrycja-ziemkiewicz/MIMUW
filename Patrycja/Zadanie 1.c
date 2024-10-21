#include <stdio.h>
#include <stdbool.h>

#define KOLUMNY 8
#define WIERSZE 8

//kolor_1 i kolor_2 to zmienne globalne opisujące jakim kolorem obecnie posługuje się gracz wykonujący ruch
char kolor_1 = 'B', kolor_2 = 'C';

bool sprawdz(int i, int j, int kolumna, int wiersz, char tab[][KOLUMNY]) {
    wiersz += i;
    kolumna += j;
    bool czy = false;
    while (kolumna < KOLUMNY && kolumna >= 0 && wiersz < WIERSZE && wiersz >= 0) {
        if (tab[wiersz][kolumna] == '-')
            return false;
        else if (tab[wiersz][kolumna] == kolor_1)
            czy = true;
        else
            return czy;
        wiersz += i;
        kolumna += j;
    }
    return false;
}

void wypisz(char tab[][KOLUMNY]) {
     putchar(kolor_2);
     bool czy = false;
     for (int i = 0; i < KOLUMNY; i++) {
        for (int j = 0; j < WIERSZE; j++) {
            czy = false;
            if (tab[i][j] == '-') {
                for (int k = -1; k <= 1; k++) {
                    for (int p = -1; p <= 1; p++) {
                         if (p != 0 || k != 0) {
                             if (sprawdz(k, p, j, i, tab)) {
                                czy = true;
                                break;
                             }
                         }
                    }
                    if (czy){
                        char a = (char) i + 'a', b = (char) j + '1';
                        putchar(' ');
                        putchar(a);
                        putchar(b);
                        break;
                    }
                }
            }
        }
     }
     putchar('\n');
}

void zamien_kolory(int i, int j, int kolumna, int wiersz, char tab[][KOLUMNY]) {
    wiersz += i;
    kolumna += j;
    int ile = 0;
    while (kolumna < KOLUMNY && kolumna >= 0 && wiersz < WIERSZE && wiersz >= 0) {
        if (tab[wiersz][kolumna] == kolor_1) {
            ile++;
        }
        else if (tab[wiersz][kolumna] == kolor_2) {
            while (ile > 0) {
                tab[wiersz - ile * i][kolumna - ile * j] = kolor_2;
                ile--;
            }
            break;
       }
       else {
            break;
       }
       wiersz += i;
       kolumna += j;
    }

}

bool wykonaj_ruch(char tab[][KOLUMNY]) {
    int wiersz = getchar();
    if (wiersz == '=') {
        getchar();
        return false;
    }
    else if (wiersz == '-') {
        getchar();
        return true;
    }
    else {
        int kolumna = getchar() - '1';
        wiersz -= 'a';
        tab[wiersz][kolumna] = kolor_2;
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                if (j != 0 || i != 0)
                    zamien_kolory(i, j, kolumna, wiersz, tab);
            }
        }
        getchar();
        return true;
    }
}

int main(void) {
    char tab[WIERSZE][KOLUMNY], temp;
    for (int i = 0; i < WIERSZE; i++) {
        for (int j = 0; j < KOLUMNY; j++)
            tab[i][j] = '-';
    }
    tab[3][3] = 'B';
    tab[4][4] = 'B';
    tab[3][4] = 'C';
    tab[4][3] = 'C';
    bool start = true;
    while (start) {
        wypisz(tab);
        start = wykonaj_ruch(tab);
        temp = kolor_1;
        kolor_1 = kolor_2;
        kolor_2 = temp;
    }
    return 0;
}
